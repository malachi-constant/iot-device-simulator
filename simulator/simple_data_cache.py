
# data store
data_store = {}

def store_value (data):
    try:
        data_store.update(data)
    except:
        return False
    print(data_store)
    return True
