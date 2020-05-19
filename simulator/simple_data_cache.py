import logging

# data store
data_store = {}

# store value in data store
def store_value (data):

    try:
        data_store.update(data)
    except:
        logging.error("[!] data point was not stored...")
        return False
    return True

# get value from data store
def get_value (field):

    try:
        value = data_store[field]
        return value
    except:
        # return none if no value exists for field
        return None
