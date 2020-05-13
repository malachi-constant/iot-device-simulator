### clevertime Simulator Usage
IoT Device Simulator Built for clevertime Sample Data

### Prerequisites
##### Python3
`brew install python3`
##### Boto3
`pip install boto3`

### Usage
```
usage: __main__.py [-h] [--region REGION] [--iot-endpoint IOT_ENDPOINT]
                   [--simulation-table SIMULATION_TABLE]
                   [--iot-topic IOT_TOPIC] [--data DATA]
                   [--interval MESSAGE_INTERVAL] [--profile PROFILE]

IoT Device Simulator

optional arguments:
  -h, --help            show this help message and exit
  --region REGION, -r REGION
                        Specify the AWS Region
  --iot-endpoint IOT_ENDPOINT, -e IOT_ENDPOINT
                        Specify the AWS IoT Core Endpoint to publish to.
  --simulation-table SIMULATION_TABLE, -T SIMULATION_TABLE
                        Specify a DynamoDB Table for storing simulation state.
  --iot-topic IOT_TOPIC, -t IOT_TOPIC
                        Specify a IoT Topic to Publish to.
  --data DATA, -d DATA  Data schema file to use.
  --interval MESSAGE_INTERVAL, -i MESSAGE_INTERVAL
                        Message Interval in seconds.
  --profile PROFILE     AWS Profile to use.
```
#### Example Execution
```
python3 clevertime-sim.py --region us-east-1 --iot-endpoint a28t31er3mx77a-ats.iot.us-east-1.amazonaws.com --simulation-table simulation-table-name --iot-topic connectedcar/telemetry/test
```
