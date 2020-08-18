### clevertime Simulator Usage
iot device simulator built for custom data

### Prerequisites
##### Python3
`brew install python3`
##### Boto3
`pip install boto3`

### Usage
```
usage: simulator [-h] [--region REGION] [--iot-endpoint IOT_ENDPOINT]
                 [--simulation-table SIMULATION_TABLE] [--iot-topic IOT_TOPIC]
                 [--data DATA] [--interval MESSAGE_INTERVAL]
                 [--simulation-length SIMULATION_LENGTH] [--profile PROFILE]
                 [--debug] [-v]

iot device simulator

optional arguments:
  -h, --help            show this help message and exit
  --region REGION, -r REGION
                        specify the aws region
  --iot-endpoint IOT_ENDPOINT, -e IOT_ENDPOINT
                        specify the aws iot core endpoint to publish to
  --simulation-table SIMULATION_TABLE, -T SIMULATION_TABLE
                        specify a dynamodb table for storing simulation state.
  --iot-topic IOT_TOPIC, -t IOT_TOPIC
                        specify a topic to publish to
  --data DATA, -d DATA  data schema file to use
  --interval MESSAGE_INTERVAL, -i MESSAGE_INTERVAL
                        message interval in milliseconds
  --simulation-length SIMULATION_LENGTH, -l SIMULATION_LENGTH
                        simulation length in seconds
  --profile PROFILE     aws profile to use
  --debug               show debug logs
  -v, --verbose         show info logs
```
#### Example Execution
```
python3 iot-device-simulator --region us-east-1 --iot-endpoint a28t31er3mx77a-ats.iot.us-east-1.amazonaws.com --simulation-table simulation-table-name --iot-topic connectedcar/telemetry/test
```
