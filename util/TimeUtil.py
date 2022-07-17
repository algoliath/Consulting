import random


def time_format(raw_format, time_format):
    if time_format == 'api':
        raw_format = raw_format.replace(':', '-').replace('T', '-').replace('Z', '-')
        split = raw_format.split('-')
        h, m = time_prefix(split[3], split[4])
        return h, m
    elif time_format == 'lib':
        split = raw_format.split(' ')[1].split(':')
        h, m = time_prefix(split[0] + 15 % 24, split[1])
        return h, m
    elif time_format == 'log':
        split = raw_format.split('~')
        start_h, start_m = split[0].split(':')
        time_prefix(start_h, start_m)
        end_h, end_m = split[1].split(':')
        time_prefix(end_h, end_m)
        return start_h, end_h
    return 'not supported time format'


def time_prefix(h, m):
    h = int(h)
    m = int(m)
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
