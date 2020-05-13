### Mojio Simulator Usage
IoT Device Simulator Built for Mojio Sample Data

### Prerequisites
##### Python3
`brew install python3`
##### Boto3
`pip install boto3`

### Usage
```
usage: mojio-sim.py [-h] [--region REGION] [--iot-endpoint IOT_ENDPOINT]
                    [--simulation-table SIMULATION_TABLE]
                    [--iot-topic IOT_TOPIC] [--trip TRIP] [--profile PROFILE]

IoT Device Simulator Built for Mojio Sample Data

optional arguments:
  -h, --help            show this help message and exit
  --region REGION       Specify the AWS Region
  --iot-endpoint IOT_ENDPOINT
                        Specify the AWS IoT Core Endpoint to publish to.
  --simulation-table SIMULATION_TABLE
                        Specify a DynamoDB Table for storing simulation state.
  --iot-topic IOT_TOPIC
                        Specify a IoT Topic to Publish to.
  --trip TRIP           Use specific sample trip. e.g. xaa.csv. This must
                        exist in your "files/" directory
  --profile PROFILE     AWS Profile to use.
```
#### Example Execution
```
python3 mojio-sim.py --region us-east-1 --iot-endpoint a28t31er3mx77a-ats.iot.us-east-1.amazonaws.com --simulation-table simulation-table-name --iot-topic connectedcar/telemetry/test
```
