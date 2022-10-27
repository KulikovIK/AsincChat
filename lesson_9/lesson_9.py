import subprocess
from ipaddress import ip_address
from tabulate import tabulate


def get_ip_from_hostname(address: str) -> str:
    output = subprocess.Popen(f'nslookup {address}', shell=True, stdout=subprocess.PIPE)
    return output.stdout.readlines()[0].decode('utf-8')[9:-1]


def get_check_line(address: str) -> bytes:
    result = subprocess.Popen(f'ping -c 3 {address}', shell=True, stdout=subprocess.PIPE)
    return result.stdout.readlines()[-2:-1][0].split(b',')[2]


def host_ping(address_list: list) -> dict:
    result = {'Reachable': [],
              'Unreachable': []}
    for address in address_list:
        try:
            ipv4 = ip_address(address)
        except ValueError:
            ipv4 = get_ip_from_hostname(address)

        check_line = get_check_line(ipv4)
        if check_line.startswith(b' 100%'):
            print(f'Узел {ipv4} недоступен')
            result['Unreachable'].append(ipv4)
            continue
        print(f'Узел {ipv4} доступен')
        result['Reachable'].append(ipv4)

    return result


def host_range_ping(address_range: str) -> dict:
    address_list = []
    address = address_range.split(' - ')
    start_ip = ip_address(address[0])
    end_ip = ip_address(address[1])

    while start_ip <= end_ip:
        address_list.append(start_ip)
        start_ip += 1

    result = host_ping(address_list)
    return result


def host_range_ping_tab(address: dict):
    print(tabulate(address, headers='keys', tablefmt='pipe'))


if __name__ == '__main__':
    host_ping(['ya.ru', '192.168.0.1'])
    host_range_ping('10.0.0.1 - 10.0.0.4')
    host_range_ping_tab(host_range_ping('8.8.8.8 - 8.8.8.9'))
