import random


def time_regex(time_info, time_format):
    if time_format == 'api':
        time_info = time_info.replace(':', '-').replace('T', '-').replace('Z', '-')
        split = time_info.split('-')
        h, m = time_prefix(int(split[3]), int(split[4]))
        return h, m
    elif time_format == 'lib':
        split = time_info.split(' ')[1].split(':')
        h, m = time_prefix(int(split[0]) + 15 % 24, int(split[1]))
        return h, m
    return 'not supported time format'


def time_prefix(h, m):
    if h < 10:
        h = '0' + str(h)
    if m < 10:
        m = '0' + str(m)
    return h, m


def time_random():
    h = random.randint(0, 24)
    m = random.randint(0, 60)
    h, m = time_prefix(h, m)
    return f'{h}:{m}'
