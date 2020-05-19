import boto3
import json
import random
import data_generator
import time
import argparse
import pathlib
import logging

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
parser.add_argument("--debug", dest='debug', help="show debug logs",action="store_true")
parser.add_argument("-v", '--verbose', help="show info logs",action="store_true")

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
valid_types            = ["float", "int", "bool", "string"]
valid_field_attributes = {"float":{"type":"string","from":"float","to":"float","average":"float","mode":"string"},"int":{"type":"string","from":"float","to":"float","average":"float","mode":"string"}, "bool":{"type":"string","weight":"float"}, "string":{"type":"string","possibilities":"string"}}

if args.verbose:
    logging.basicConfig(level=logging.INFO)
elif args.debug:
    logging.basicConfig(level=logging.DEBUG)

# boto3 init
if profile is not None:
    boto3.setup_default_session(profile_name=profile)
    logging.info("[*] using aws profile: " + str(profile))
dynamodb               = boto3.resource('dynamodb', region_name=region)
iot_client             = boto3.client('iot-data', region_name=region)


def write_data(payload):
    logging.info("writing to topic: " + iot_topic)
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
    logging.info("[*] validating fields...")
    for field in json_data:
        logging.info("[*] field: " + field)
        # check if field has a type
        try:
            if json_data[field]["type"] in valid_types:
                type = json_data[field]["type"]
                logging.info("\t[*] valid type: '" + type + "'")
        except:
            logging.error("\t[!] field must have a type set")
            return False

        for attribute in json_data[field]:
            # check if field attribute is valid
            if attribute in valid_field_attributes[type]:
                logging.info("\t[*] valid field attribute: " + attribute)
            else:
                logging.info("\t[!] '" + attribute + "' is not a valid attribute for a " + json_data[field]["type"] + " field")
                return False
            value = json_data[field][attribute]
            logging.info("\t\t[*] value: " + str(value))
            expected_type = valid_field_attributes[type][attribute]
            logging.info("\t\t[*] expected type: " + str(expected_type))
            try:
                if expected_type == "float":
                    float(value)
                elif expected_type == "string":
                    str(value)
                else:
                    logging.info(expected_type)
            except:
                print("[!] invalid type: " + value + " is not type: " + expected_type)
                return False

    return True

def open_data(data_location):
    logging.info("[*] data file: " + data_location)

    # open file
    try:
        abs_path = str(pathlib.Path(__file__).parent.absolute())
        file     = open(abs_path + data_location,"r")
    except:
        logging.error("[!] schema file at " + abs_path + data_location + " does not exist")
        exit()
    file_data = file.read()

    # json lint
    try:
        json_data = json.loads(file_data)
    except:
        logging.error("[!] schema file at " + data_location + " is not valid.json.")
        exit()
    logging.info("[*] json is valid")
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
        logging.info("[*] schema is valid")
    else:
        print("[!] exiting...")
        exit()

    for i in range(simulation_length):
        data = data_generator.generate(schema)
        logging.info(data)

        if not write_data(json.dumps(data)):
            logging.warning("[!] message failed to write to iot core endpoint: " + iot_core_endpoint)
            exit()

        time.sleep(message_interval)

if __name__ == '__main__':
    main()
