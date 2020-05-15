import json
import random
import calculations
import simple_data_cache

# handle float value
def float_generate(settings, last_value):

    # check last value
    if last_value is None:
        last_value = random.uniform(settings['from'], settings['to'])

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

    # check last value
    if last_value is None:
        last_value = True if random.randint(-1,1) > 0 else False

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

    # check last value
    if last_value is None:
        last_value = random.randint(settings['from'], settings['to'])
        #last_value = 250
    mode = settings['mode']

    if mode == 'random':
        value = int(random.triangular(settings['from'], settings['average'], settings['to']))

    elif mode == 'linear':
        low          = abs(last_value - settings['to'])
        #print("[&] low: " + str(low))
        high         = abs(last_value - settings['from'])
        #print("[&] high: " + str(high))
        direction    = calculations.random_direction()
        #print("[&] direction: " + str(direction))
        if direction > 0:
            go = high * direction
        else:
            go = low * direction
        #print("[&] go: " + str(go))
        value = int(last_value + (go * random.betavariate(2,100)))

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

    data = {}

    for field in schema:
        type = schema[field]["type"]
        field_settings = schema[field]

        # get last value from data store if it exists
        last_value = simple_data_cache.get_value(field)

        if type == 'float':
            value = float_generate(field_settings, last_value)

        elif type == 'string':
            value = string_generate(field_settings)

        elif type == 'integer':
            value = integer_generate(field_settings, last_value)

        elif type == 'bool':
            value = bool_generate(field_settings, last_value)

        else:
            print("[!] type not available")
            return False

        data_point = {field:value}
        simple_data_cache.store_value(data_point)
        data.update(data_point)

    return data
