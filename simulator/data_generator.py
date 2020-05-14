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
        print("[!] float mode: '" + mode + "' not supported")
        exit()

    return value

# handle bool value
def bool_generate(settings, last_value):

    # check if there is a weight
    if 'weight' in settings.keys():

        # error handling
        if settings['weight'] > 100 or settings['weight'] < 0:
            weight = 0
        else:
            weight = settings['weight']
    # calculate weight and allow switch if random is over weight
    if random.randint(0,100) > weight:
        return False if calculations.random_direction() == -1 else True
    else:
        return last_value

# handle integer value
def integer_generate(settings, last_value):
    mode = settings['mode']

    if mode == 'random':
        value = int(random.triangular(settings['from'], settings['average'], settings['to']))

    elif mode == 'linear':
        distance_1   = abs(last_value - settings['to'])
        distance_2   = abs(last_value - settings['from'])
        min_distance = distance_1 if distance_1 < distance_2 else distance_2
        value        = int(last_value + (min_distance * (calculations.random_direction() * random.betavariate(2,100))))

    else:
        print("[!] integer mode: '" + mode + "' not supported")
        exit()

    return value

# handle string value
def string_generate(settings):
    try:
        possibilities = settings['possibilities']
    except:
        print("[*] string fields must have a 'possibilities' attribute")
    if str(type(possibilities)) == "<class 'list'>":
        index = random.randint(0,len(possibilities)-1)
    else:
        print("[!] possibilites must be a list")
        exit()

    return possibilities[index]

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
            value = string_generate(field_settings)
            print("[*] field: " + field)
            print("[*] value: " + str(value))
        elif type == 'integer':
            value = integer_generate(field_settings,0)
            print("[*] field: " + field)
            print("[*] value: " + str(value))
        elif type == 'bool':
            value = bool_generate(field_settings, True)
            print("[*] field: " + field)
            print("[*] value: " + str(value))
        else:
            print("[!] type not available")
            return False

    return True
        #for attribute in json_data[field]:
