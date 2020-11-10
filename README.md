### Usage
iot device simulator built for custom data

### Prerequisites
- Python 3
- Boto3

### Usage
```
usage: simulator [-h] [--region REGION] [--simulation-table SIMULATION_TABLE]
                 [--iot-topic IOT_TOPIC] [--data DATA]
                 [--interval MESSAGE_INTERVAL]
                 [--simulation-length SIMULATION_DURATION] [--profile PROFILE]
                 [--debug] [-v]

iot device simulator

optional arguments:
  -h, --help            show this help message and exit
  --region REGION, -r REGION
                        specify the aws region (default: us-west-2)
  --simulation-table SIMULATION_TABLE, -T SIMULATION_TABLE
                        specify a dynamodb table for storing simulation state. (default: null)
  --iot-topic IOT_TOPIC, -t IOT_TOPIC
                        specify a topic to publish to (default: 'simulator/test')
  --data DATA, -d DATA  data schema file to use
  --interval MESSAGE_INTERVAL, -i MESSAGE_INTERVAL
                        message interval in milliseconds (default: 1000)
  --simulation-length SIMULATION_DURATION, -l SIMULATION_DURATION
                        simulation length in seconds (default: 60)
  --profile PROFILE     aws profile to use (default: null)
  --debug               show debug logs
  -v, --verbose         show info logs


```
#### Example Execution
```
> python simulator --profile malachi -t "test"
[*] welcome to the iot device simulator !

[*] beginning simulation ...
{'ResponseMetadata': {'RequestId': '9b8a6624-a100-bb14-326b-ec9b93728932', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/json', 'content-length': '65', 'date': 'Tue, 10 Nov 2020 20:40:52 GMT', 'x-amzn-requestid': '9b8a6624-a100-bb14-326b-ec9b93728932', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}
{'ResponseMetadata': {'RequestId': 'd0a66891-eb69-662d-9a05-5fa69bde8def', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/json', 'content-length': '65', 'date': 'Tue, 10 Nov 2020 20:40:53 GMT', 'x-amzn-requestid': 'd0a66891-eb69-662d-9a05-5fa69bde8def', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}
{'ResponseMetadata': {'RequestId': 'aca449f9-3fa6-2c25-8691-6d9ab0776db0', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/json', 'content-length': '65', 'date': 'Tue, 10 Nov 2020 20:40:54 GMT', 'x-amzn-requestid': 'aca449f9-3fa6-2c25-8691-6d9ab0776db0', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}
{'ResponseMetadata': {'RequestId': '4a1b3a75-725a-fb30-71a5-392c19cd0e39', 'HTTPStatusCode': 200, 'HTTPHeaders': {'content-type': 'application/json', 'content-length': '65', 'date': 'Tue, 10 Nov 2020 20:40:55 GMT', 'x-amzn-requestid': '4a1b3a75-725a-fb30-71a5-392c19cd0e39', 'connection': 'keep-alive'}, 'RetryAttempts': 0}}
```
![Example Output](/images/iot-core.png)

#### Creating Data Schema
You can define the type of data your simulator publishes.

##### Types
- float
- int
- bool
- string

##### Valid Attributes for each type
- float
  - type: should be set to "float"
  - from: minimum
  - to: maximum
  - average: average
  - mode: should be set to "linear" or "random"
    - random: random generation
    - linear: data points appear linear in sequence
- int
  - type: should be set to "int"
  - from: minimum
  - to: maximum
  - average: average
  - mode: should be set to "linear" or "random"
    - random: random generation
    - linear: data points appear linear in sequence
- bool
  - type: should be set to "bool"
  - weight(optional): number between 0 and 100, 100 being impossible to switch states (e.g. false --> true), 0 being most likely to switch states
- string
  - type: should be set to "string"
  - possibilities: list of possible values (string)
```
valid_field_attributes = {"float":{"type":"string","from":"float","to":"float","average":"float","mode":"string"},"int":{"type":"string","from":"float","to":"float","average":"float","mode":"string"}, "bool":{"type":"string","weight":"float"}, "string":{"type":"string","possibilities":"string"}}
```

example data:
```
{
  "temperature": {
    "type": "float",
    "from": -100,
    "to": 100,
    "average": 30,
    "mode": "random"
  },
  "speed": {
    "type": "integer",
    "from": 0,
    "to": 250,
    "average": 60,
    "mode": "linear"
  },
  "message": {
    "type": "string",
    "possibilities": ["HELLO", "WORLD"]
  },
  "powered_on": {
    "type": "bool",
    "weight": 50
  }
}
```
#### Running at Scale
subdirectory: `./terraform` includes configuration for infrastructure to run simulations at scale.

Resources:
- DynamoDB Table: Tracks active simulations
- ASG: Fleet of EC2 instances to run simulations

##### Test Initiation
Use SSM Runcommand or another ssh mechanism to trigger commands across the fleet.
