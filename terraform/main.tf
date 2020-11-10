
# dynamodb table for storing simulation state
resource "aws_dynamodb_table" "simulation_table-table" {
  name           = join("-", [var.prefix, "simulations"])
  hash_key       = "simulation_id"
  read_capacity  = 10
  write_capacity = 100

  attribute {
    name = "simulation_id"
    type = "S"
  }

  tags {
    Name = join("-", [var.prefix, "simulations"])
  }
}

# autoscaling group for simulation workers
resource "aws_autoscaling_group" "simulation_fleet" {
  name                 = join("-", [var.prefix, "simulation-fleet"])
  desired_capacity     = 0
  launch_configuration = aws_launch_configuration.simulation_fleet.id
  max_size             = 0
  min_size             = 0

  tag {
    key                 = "Name"
    value               = join("-", [var.prefix, "simulation-fleet"])
    propagate_at_launch = true
  }
}

# amazon linux 2 latest ami
data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm*"]
  }
}

# launch configuration for simulation fleet
resource "aws_launch_configuration" "simulation_fleet" {
  name_prefix          = join("-", [var.prefix, "simulation-fleet"])
  image_id             = data.aws_ami.amazon_linux_2.id
  instance_type        = var.instance_type
  key_name             = "a-sim"
  iam_instance_profile = "${aws_iam_instance_profile.simulation_fleet.id}"
  user_data            = "${data.template_file.simulation_fleet.rendered}"
  security_groups = [
    aws_security_group.simulation_fleet.id
  ]

  root_block_device {
    volume_type           = "gp2"
    volume_size           = 25
    delete_on_termination = true
  }

  lifecycle {
    create_before_destroy = true
  }
}

# userdata
data "template_file" "simulation_fleet" {
  template = "${file("./scripts/sim-userdata.sh")}"

  vars = {
    s3_bucket = aws
  }
}


# iam
resource "aws_iam_role" "simulation_fleet" {
  name               = join("-", [var.prefix, "simulation-fleet"])
  path               = "/"
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
  name = join("-", [var.prefix, "simulation-fleet"])
  role = aws_iam_role.simulation_fleet.name
}

resource "aws_iam_role_policy_attachment" "simulation_fleet" {
  role       = aws_iam_role.simulation_fleet.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_security_group" "simulation_fleet" {
  name        = join("-", [var.prefix, "simulation-fleet"])
  description = "Allow access to simulation fleet"
  vpc_id      = var.vpc_id

  dynamic "ingress" {
    for_each = var.whitelist_ips

    content {
      from_port   = ingress.value["port"]
      to_port     = ingress.value["port"]
      protocol    = "tcp"
      cidr_blocks = [ingress.value["cidr"]]
    }
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
