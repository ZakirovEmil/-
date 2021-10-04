from prettytable import PrettyTable
import re
import json
from urllib import request
import subprocess

ip_regex = re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


def get_args(count, info):
    try:
        as_number = info['org'].split()[0]
        provider = ' '.join(info['org'].split()[1::])
        country = info['country'].split()[0]
    except KeyError:
        as_number, provider, country = '*', '*', '*'
    return [f'{count}.', info['ip'], as_number, country, provider]


def get_info(ip):
    return json.loads(request.urlopen('https://ipinfo.io/' + ip + '/json').read())


def check_err(line):
    return 'Unable to resolve' in line \
           or 'Не удается разрешить' in line


def trace_as(address, table):
    tracert = subprocess.Popen(["tracert", address], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    count = 0

    for line in iter(tracert.stdout.readline, ''):
        if not line:
            return

        line = line.decode('cp866').strip()
        ip = re.findall(ip_regex, line)

        if check_err(line):
            print('Unable to resolve')
            return

        if not ip or not line[0].isdigit():
            continue

        count += 1
        print(f'{"".join(ip)}')
        info = get_info(ip[0])
        table.add_row(get_args(count, info))


def create_table():
    table = PrettyTable()
    table.field_names = ['№', 'IP', 'AS', 'Country', 'Provider']
    return table


def is_empty(input):
    return input == ""


def main():
    table = create_table()
    print("Address: ")
    address = input()
    if is_empty(address):
        print("Empty input")
        return
    trace_as(address, table)
    print(table)


if __name__ == '__main__':
    main()
