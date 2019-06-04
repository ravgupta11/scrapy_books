import json
import locale
import re
import sys


def project(view, attribute_list, count):
    strings = []
    attribute_list_full = ['tag', 'title', 'rating', 'price', 'image_urls', 'product_desc']

    if len(attribute_list) == 0:
        attribute_list = attribute_list_full[:]

    for entry in view:
        s = {}
        for attribute in attribute_list:
            s[attribute] = entry[attribute]
        strings.append(s)
    if count:
        print(len(strings))
    else:
        with open('query_result', 'w') as f:
            json.dump(strings, f)


def is_number(parameter_i):
    if parameter_i.isdigit():
        parameter_i = int(parameter_i)
    elif parameter_i.replace('.', '', 1).isdigit():
        parameter_i = float(parameter_i)
    return parameter_i


def check(instance, condition_list):
    for condition in condition_list:
        parameter1 = condition['attr1']
        parameter2 = condition['attr2']
        decimal_point_char = locale.localeconv()['decimal_point']
        if parameter1 == 'price':
            v2 = float(re.sub(r'[^0-9' + decimal_point_char + r']+', '', parameter2))
            v1 = float(re.sub(r'[^0-9' + decimal_point_char + r']+', '', instance[parameter1]))
        else:
            v2 = parameter2
            v1 = instance[parameter1]
        operator = condition['o']
        if (operator == '=' and v1 != v2):
            return False
        if ((operator == '>') and v1 <= v2):
            return False
        if ((operator == '<') and v1 >= v2):
            return False
        if ((operator == '>=') and v1 < v2):
            return False
        if ((operator == '<=') and v1 > v2):
            return False
    return True


def sigma(db, condition_list):
    if (len(condition_list) == 0):
        return db
    view = []
    for entry in db:
        if check(entry, condition_list):
            view.append(entry)
    return view


def read_input():
    option_1 = ''
    line_1 = ''
    option_2 = ''
    line_2 = ''
    option_3 = ''
    count = False

    try:
        option_1 = sys.argv[1]
        line_1 = sys.argv[2]
        option_2 = sys.argv[3]
        line_2 = sys.argv[4]
        option_3 = sys.argv[5]
    except:
        pass

    condition_list = []
    attribute_list = []
    if option_1 == '-q':
        condition_list = [dict(zip(['attr1', 'o', 'attr2'], list(condition.split()))) for condition in
                          list(line_1.split(', '))]

    if option_2 == '-a':
        attribute_list = list(line_2.split(', '))

    if option_3 == '-c':
        count = True

    return {'q': condition_list, 'a': attribute_list, 'c': count}


def main():
    par = read_input()
    with open('data_base.json', 'r') as f:
        db = json.load(f)
    # print (db)
    view = sigma(db, par['q'])
    project(view, par['a'], par['c'])


if __name__ == '__main__':
    main()
