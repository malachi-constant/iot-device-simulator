import boto3
import json
import random
import data_generator
import time
import argparse
import pathlib

# get program arguments
parser = argparse.ArgumentParser(description='IoT Device Simulator Built for clevertime Sample Data')
parser.add_argument('--region','-r', dest='region', required=False, default='us-west-2',help='Specify the AWS Region')
parser.add_argument('--iot-endpoint','-e', dest='iot_endpoint', required=False, help='Specify the AWS IoT Core Endpoint to publish to.')
parser.add_argument('--simulation-table','-T', dest='simulation_table', required=False, default='simulation-table',help='Specify a DynamoDB Table for storing simulation state.')
parser.add_argument('--iot-topic','-t', dest='iot_topic', required=False, default='simulator/test',help='Specify a IoT Topic to Publish to.')
parser.add_argument('--data','-d' ,dest='data', required=False, default='sample',help='Data schema file to use.')
parser.add_argument('--interval','-i' ,dest='message_interval', required=False, default=1,help='Message Interval in seconds.')
parser.add_argument('--simulation-length','-l' ,dest='simulation_length', required=False, default=60,help='simulation length in seconds')
parser.add_argument('--profile', dest='profile', required=False,help='AWS Profile to use.')

args = parser.parse_args()

# globals
simulation_id          = str(random.randint(10000000,99999999))
iot_core_endpoint      = args.iot_endpoint
iot_topic              = args.iot_topic
region                 = args.region
profile                = args.profile
simulation_table       = args.simulation_table
message_interval       = args.message_interval
simulation_length      = args.simulation_length
data_location          = "/data/" + args.data + ".json"

# set profile
if profile is not None:
    boto3.setup_default_session(profile_name=profile)
    print("[*] using aws profile: " + str(profile))
    
dynamodb               = boto3.resource('dynamodb', region_name=region)
iot_client             = boto3.client('iot-data', region_name=region)
valid_types            = ["float", "int", "bool", "string"]
valid_field_attributes = {"float":{"type":"string","from":"float","to":"float","average":"float","mode":"string"},"int":{"type":"string","from":"float","to":"float","average":"float","mode":"string"}, "bool":{"type":"string","weight":"float"}, "string":{"type":"string","possibilities":"string"}}

    # try:
    #     sim_table.delete_item(
    #     Key={
    #         'simulation-id': sim_id,
    #     }
    #     )
    # except:
    #     print("\nDynamoDB Table for Simulation State Not Found.\n No record to delete...")
    #     time.sleep(2)

def write_data(payload):
    print("writing to topic: " + iot_topic)
    response = iot_client.publish(
        topic= iot_topic,
        qos=0,
        payload=payload
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return True
    else:
        return False

# validate json schema
def validate_data(json_data):

    # check schema
    print("[*] validating fields...")
    for field in json_data:
        print("[*] field: " + field)
        # check if field has a type
        try:
            if json_data[field]["type"] in valid_types:
                type = json_data[field]["type"]
                print("\t[*] valid type: '" + type + "'")
        except:
            print("\t[!] field must have a type set")
            return False

        for attribute in json_data[field]:
            # check if field attribute is valid
            if attribute in valid_field_attributes[type]:
                print("\t[*] valid field attribute: " + attribute)
            else:
                print("\t[!] '" + attribute + "' is not a valid attribute for a " + json_data[field]["type"] + " field")
                return False
            value = json_data[field][attribute]
            print("\t\t[*] value: " + str(value))
            expected_type = valid_field_attributes[type][attribute]
            print("\t\t[*] expected type: " + str(expected_type))
            try:
                if expected_type == "float":
                    float(value)
                elif expected_type == "string":
                    str(value)
                else:
                    print(expected_type)
            except:
                print("[!] invalid type: " + value + " is not type: " + expected_type)
                return False

    return True

def open_data(data_location):
    print("[*] data file: " + data_location)

    # open file
    try:
        abs_path = str(pathlib.Path(__file__).parent.absolute())
        file     = open(abs_path + data_location,"r")
    except:
        print("[!] schema file at " + abs_path + data_location + " does not exist")
        exit()
    file_data = file.read()

    # json lint
    try:
        json_data = json.loads(file_data)
    except:
        print("[!] schema file at " + data_location + " is not valid.json.")
        exit()
    print("[*] json is valid")
    return json_data

# welcome banner
def welcome():
    print("[*] welcome to the iot device simulator !\n")
    print("[*] beginning simulation ...")

# main entrypoint
def main():

    welcome()

    schema = open_data(data_location)

    if validate_data(schema):
        print("[*] schema is valid")
    else:
        print("[!] exiting...")
        exit()

    for i in range(simulation_length):
        data = data_generator.generate(schema)
        print(data)

        if not write_data(json.dumps(data)):
            print("[!] message failed to write to iot core endpoint: " + iot_core_endpoint)
            exit()

        time.sleep(message_interval)


    # try:
    #     run_simulator()
    # except KeyboardInterrupt:
    #     print("[*] Ending Simulation: " + sim_id + "")
    #     try:
    #         sim_table = dynamodb.Table(simulation_table)
    #         sim_table.delete_item(
    #         Key={
    #             'simulation-id': sim_id,
    #         }
    #         )
    #     except:
    #         print("\nDynamoDB Table for Simulation State Not Found.\n No record to delete...")
    #         time.sleep(2)
    #
    # print("[*] Simulation Completed")

if __name__ == '__main__':
    main()
