import boto3
import logging

# create record in dynamo
def create_simulation_record(dynamo_client, simulation_table, simulation_id, simulation_duration, message_interval):
    logging.info("[*] updating state: + " + simulation_id)
    try:
        dynamo_table = dynamo_client.Table(simulation_table)
        dynamo_table.put_item(
           Item={
                'simulation_id': simulation_id,
                'state': 'RUNNING',
                'duration': simulation_duration,
                'interval': message_interval
            }
        )
    except:
        logging.info("\n[!] dynamodb table: " + simulation_table + " not found")

# delete state record in dynamo
def delete_simulation_record(dynamo_client, simulation_table, simulation_id):
    logging.info("[*] updating state: - " + simulation_id)
    try:
        dynamo_table = dynamo_client.Table(simulation_table)
        sim_table.delete_item(
            Key={
                'simulation_id': simulation_id,
            }
        )
    except:
        logging.info("[!] no state table")
