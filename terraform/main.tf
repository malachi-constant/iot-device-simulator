# create a dynamodb table for locking the state file
resource "aws_dynamodb_table" "sim-table" {
  name = "simulation-table"
  hash_key = "simulation-id"
  read_capacity = 10
  write_capacity = 100

  attribute {
    name = "simulation-id"
    type = "S"
  }

  tags {
    Name = "Mojio Simulation State Table"
  }
}

### Autoscaling Group
resource "aws_autoscaling_group" "simulation_fleet" {
    name = "sim-fleet"
    desired_capacity = 0
    launch_configuration = "${aws_launch_configuration.simulation_fleet.id}"
    max_size = 0
    min_size = 0
    vpc_zone_identifier = ["subnet-2cdb9e02"]
    tag {
        key   = "Name"
        value = "sim-fleet"
        propagate_at_launch = true
    }
}

### Amazon Linux 2 Latest AMI
data "aws_ami" "amazon-linux-2" {
 most_recent = true
 owners = ["amazon"]
 filter {
   name   = "name"
   values = ["amzn2-ami-hvm*"]
 }
}

### Launch Configuration
resource "aws_launch_configuration" "simulation_fleet" {
    name_prefix = "sim-fleet"
    image_id = "ami-0cc96feef8c6bbff3"
    instance_type = "m5.4xlarge"
    key_name = "mojio-sim"
    iam_instance_profile = "${aws_iam_instance_profile.simulation_fleet.id}"
    security_groups = [
      "${aws_security_group.simulation_fleet.id}"
    ]
    associate_public_ip_address = true
    user_data = "${data.template_file.simulation_fleet.rendered}"
    ebs_optimized = true
    root_block_device {
        volume_type = "gp2"
        volume_size = 50
        delete_on_termination = true
    }
    lifecycle {
        create_before_destroy = true
    }
}

### User Data DotNet Linux
data "template_file" "simulation_fleet" {
  template = "${file("./scripts/sim-userdata.sh")}"
}

### IAM Resources for Dotnet-Linux Nodes

resource "aws_iam_role" "simulation_fleet" {
    name = "sim-fleet"
    path = "/"
    assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": "sts:AssumeRole",
            "Principal": {
               "Service": "ec2.amazonaws.com"
            },
            "Effect": "Allow",
            "Sid": ""
        }
    ]
}
EOF
}

resource "aws_iam_instance_profile" "simulation_fleet" {
    name = "sim-fleet"
    role = "${aws_iam_role.simulation_fleet.name}"
}

resource "aws_iam_role_policy_attachment" "simulation_fleet" {
    role       = "${aws_iam_role.simulation_fleet.name}"
    policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_security_group" "simulation_fleet" {
  name = "simulation_fleet_ssh"
  description = "Allow ssh to sim_fleet"
  vpc_id = "${var.vpc_id}"

  ingress {
    protocol = "tcp"
    from_port = 22
    to_port = 22
    cidr_blocks = ["172.249.71.28/32", "38.32.68.178/32", "73.221.37.117/32"]
  }
  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
