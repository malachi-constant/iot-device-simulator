import boto3
import json
import random
from datetime import datetime, timedelta, tzinfo
import time
import argparse
import sys
import uuid
import os

### Populate Sample Trips into Array
sample_trips = []
for file in os.listdir("./files"):
    if file.endswith(".csv"):
        sample_trips.append(file)

### Get Program Args
parser = argparse.ArgumentParser(description='IoT Device Simulator Built for Mojio Sample Data')
parser.add_argument('--region', dest='region', required=False, default='us-west-2',help='Specify the AWS Region')
parser.add_argument('--iot-endpoint', dest='iot_endpoint', required=False, default='a28t31er3mx77a-ats.iot.us-west-2.amazonaws.com',help='Specify the AWS IoT Core Endpoint to publish to.')
parser.add_argument('--simulation-table', dest='simulation_table', required=False, default='simulation-table',help='Specify a DynamoDB Table for storing simulation state.')
parser.add_argument('--iot-topic', dest='iot_topic', required=False, default='mojio/simulator_rule',help='Specify a IoT Topic to Publish to.')
parser.add_argument('--trip', dest='trip', required=False,help='Use specific sample trip. e.g. xaa.csv. This must exist in your "files/" directory')
parser.add_argument('--profile', dest='profile', required=False,help='AWS Profile to use.')

args = parser.parse_args()

### Set vars and connections
objectPrefix = 'files'
timing_array = []
sim_id = str(random.randint(10000000,99999999))
iot_core_endpoint = args.iot_endpoint
iot_topic = args.iot_topic
region = args.region
profile = args.profile
simulation_table = args.simulation_table
dynamodb = boto3.resource('dynamodb', region_name=region)

def exit_handler():
    print ('My application is ending!')


class FixedOffset(tzinfo):
    """offset_str: Fixed offset in str: e.g. '-0400'"""
    def __init__(self, offset_str):
        sign, hours, minutes = offset_str[0], offset_str[1:3], offset_str[4:]
        offset = (int(hours) * 60 + int(minutes)) * (-1 if sign == "-" else 1)
        self.__offset = timedelta(minutes=offset)
        # NOTE: the last part is to remind about deprecated POSIX GMT+h timezones
        # that have the opposite sign in the name;
        # the corresponding numeric value is not used e.g., no minutes
        '<%+03d%02d>%+d' % (int(hours), int(minutes), int(hours)*-1)
    def utcoffset(self, dt=None):
        return self.__offset
    def tzname(self, dt=None):
        return self.__name
    def dst(self, dt=None):
        return timedelta(0)
    def __repr__(self):
        return 'FixedOffset(%d)' % (self.utcoffset().total_seconds() / 60)

def convertTimestamp(timestamp):
    date_with_tz = timestamp
    date_str, tz = date_with_tz[:-6], date_with_tz[-6:]
    dt_utc = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%f")
    dt = dt_utc.replace(tzinfo=FixedOffset(tz))
    return dt


def findMSDifference (start_time, end_time):
    start_timestamp = convertTimestamp(start_time)
    end_timestamp = convertTimestamp(end_time)
    duration_time = end_timestamp - start_timestamp;
    duration_ms = duration_time.seconds * 1000

    return duration_ms;

### Parse Trip File and create JSON
def parseData(trip_data, trip_selection) :
    data_JSON = []
    timingArray = []
    device_id = str(random.randint(10000,99999)) ## Generate device id for simulation
    trip_id   = uuid.uuid4().hex
    lines = trip_data.split('\n')
    line_number = len(lines);


    for i in range(line_number-1) :
        columns = lines[i].strip().split(',');
        if (i > 1):
            previous_columns = lines[i-1].strip().split(',')
            timing_array.append(findMSDifference(previous_columns[1], columns[1]))
        dev = [];
        message_id = uuid.uuid4().hex
        dev.append({
          "message_id": message_id,
          "trip_id": trip_id,
          "device_id": device_id,
          "devicetime": columns[1],
          "eventId": columns[2],
          ## dev_acceleration: columns[3],
          ## dev_accl_magnitude: columns[4],
          ## dev_accl_x_force : columns[5],
          ## dev_accl_y_force: columns[6],
          ## dev_accl_z_force: columns[7],
          "dev_ext_bat_voltage": columns[8],
          "dev_int_bat_voltage": columns[9],
          #"dev_nw_carrier": columns[10],
          "dev_nw_cell_sig_str": columns[11],
          "dev_nw_conn_roaming": columns[12],
          "dev_nw_conn_type": columns[13],
          "veh_coolant_temp": columns[14],
          "veh_dtc_count": columns[15],
          "veh_engine_fuel_rate": columns[16],
          "veh_engine_load": columns[17],
          "veh_engine_oil_temp": columns[18],
          "veh_fuel_level": columns[19],
          "veh_fuel_pressure": columns[20],
          "veh_ima_pressure": columns[21],
          "veh_intake_air_temp": columns[22],
          "veh_maf_air_flow": columns[23],
          "veh_mil_status": columns[24],
          "veh_real_odo": columns[25],
          "veh_rpm": columns[26],
          "veh_speed": columns[27],
          "veh_throttle_pos": columns[28],
          "veh_tire_lf_pressure": columns[29],
          "veh_tire_lr_pressure": columns[30],
          "veh_tire_rf_pressure": columns[31],
          "veh_tire_rr_pressure": columns[32],
          "veh_virt_odo": columns[33],
          "gps_alt": columns[34],
          "gps_fix_status": columns[35],
          "gps_fix_time": columns[36],
          "gps_hacc": columns[37],
          "gps_hdop": columns[38],
          "gps_heading": columns[39],
          "gps_lat": columns[40],
          "gps_lon": columns[41],
          "gps_lost_lock_duration": columns[42],
          "gps_lost_lock_time": columns[43],
          "gps_num_sat": columns[44],
          "gps_pdop": columns[45],
          "gps_speed": columns[46],
          "gps_vacc": columns[47],
          "gps_vdop": columns[48]})

        data_JSON.append(dev);


        if (columns[2] == "VEH_TRIP_MOVING_STOPPED") :
            ### Get timestamp and difference in milliseconds between first timestamp and last return that as an interval
            first_timestamp = lines[1].strip().split(',')[1]
            simulationDuration = findMSDifference(first_timestamp,columns[1]);

    print('[*] Simulation Duration: ' + str(simulationDuration/1000) + " seconds")

    return data_JSON

def runSimulator():
    if profile is not None:
        boto3.setup_default_session(profile_name=profile)
        print("[*] Using AWS Profile: " + str(profile))

    sampleTrip = sample_trips[random.randint(0,(len(sample_trips)-1))]
    if args.trip is not None:
        sampleTrip = args.trip

    print("[*] Using Sample Trip: " + sampleTrip)

    trip_selection = sampleTrip[2]
    print("[*] Trip Identifier = " + trip_selection)

    path = objectPrefix + "/" + sampleTrip
    print ("[*] Path: " + path)
    try:
        file_object  = open(path,"r")
    except:
        print("Sample Trip File: " + path + " Does not exist")
        exit()
    trip_data = file_object.read()

    trip_json = parseData(trip_data, trip_selection)

    first_item = json.dumps(trip_json[0][0])
    second_item = json.loads(first_item)
    print("[*] Device Id: " + str(second_item['device_id']))
    print("[*] Total Messages in Simulation: " + str(len(trip_json)))
    total_messages = str(len(trip_json))

    print("[*] Simulation Id: " + sim_id)
    try:
        sim_table = dynamodb.Table(simulation_table)
        sim_table.put_item(
           Item={
                'simulation-id': sim_id,
                'state': 'RUNNING',
                'device_id': str(second_item['device_id']),
                'number_of_messages': total_messages
            }
        )
    except:
        print("\nDynamoDB Table for Simulation State Not Found.\n No table will be used...")
        time.sleep(2)

    iot_client = boto3.client('iot-data', region_name=region)

    print("\n[*] Simulation Starting...\n")

    for i in range(1,len(trip_json)):

        print("[*] Publishing Message...\n")

        ts = time.time()
        st = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')
        print("[*] Publish time: " + st)
        pt = str(int(time.time() * 1000))
        msg_data = trip_json[i][0]
        msg_data['publish_time'] = pt
        payload = json.dumps(msg_data)
        print(payload)
        # Change topic, qos and payload
        response = iot_client.publish(
            topic= iot_topic,
            qos=0,
            payload=payload
        )

        if (i < len(trip_json) - 2):
            print("[*] Waiting " + str(timing_array[i-1]) + " ms...\n")
        if (i != (len(trip_json)-1)):
            time.sleep(timing_array[i-1]/1000)

    try:
        sim_table.delete_item(
        Key={
            'simulation-id': sim_id,
        }
        )
    except:
        print("\nDynamoDB Table for Simulation State Not Found.\n No record to delete...")
        time.sleep(2)




### Main
try:
    runSimulator()
except KeyboardInterrupt:
    print("[*] Ending Simulation: " + sim_id + "")
    try:
        sim_table = dynamodb.Table(simulation_table)
        sim_table.delete_item(
        Key={
            'simulation-id': sim_id,
        }
        )
    except:
        print("\nDynamoDB Table for Simulation State Not Found.\n No record to delete...")
        time.sleep(2)

print("[*] Simulation Completed")
