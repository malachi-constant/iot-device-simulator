import json
import random
import calculations

# handle float value
def float_generate(settings, last_value):
    mode = settings['mode']

    if mode == 'random':
        value = round(random.triangular(settings['from'], settings['average'], settings['to']),5)

    elif mode == 'linear':
        distance_1   = abs(last_value - settings['to'])
        distance_2   = abs(last_value - settings['from'])
        min_distance = distance_1 if distance_1 < distance_2 else distance_2
        value        = round(last_value + (min_distance * (calculations.random_direction() * random.betavariate(2,100))),5)

    else:
        print("[!] float mode:" + mode + " not supported")
        exit()

    return value

# handle bool value
def bool_generate(settings):
    return True

# handle integer value
def integer_generate(settings):
    return True

# handle string value
def string_generate(settings):
    return True

# generate data point
def generate(schema):
    for field in schema:
        type = schema[field]["type"]
        field_settings = schema[field]

        if type == 'float':
            value = float_generate(field_settings, 0.0)
            print("[*] field: " + field)
            print("[*] value: " + str(value))
        elif type == 'string':
            string_generate(field_settings)
        elif type == 'integer':
            integer_generate(field_settings)
        elif type == 'bool':
            bool_generate(field_settings)
        else:
            print("[!] type not available")
            return False

    return True
        #for attribute in json_data[field]:
