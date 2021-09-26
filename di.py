from random import randint
from math import ceil

refueling_information = open('azs.txt', encoding='utf-8')
clients_information = open('input.txt', encoding='utf-8')
price_gas = {'АИ-80': 50, 'АИ-92': 44, 'АИ-95': 47, 'АИ-98': 58}
gas_inf = {}
for line in refueling_information:
    all_inf = list(map(str, line[:-1].split(' ')))
    number = int(all_inf[0])
    all_inf.pop(0)
    max_line = int(all_inf[0])
    all_inf.pop(0)
    if len(all_inf) > 1:
        petrol = []
        for mark in range(len(all_inf)):
            petrol.append(all_inf[mark])
    else:
        petrol = all_inf[0]
    gas_inf[number] = max_line, petrol
print(gas_inf)

client_inf = []
for line in clients_information:
    all_inf = list(map(str, line[:-1].split(' ')))
    time = all_inf[0]
    amount_of_gas = int(all_inf[1])
    mark_of_gas = all_inf[2]
    inf = [time, amount_of_gas, mark_of_gas]
    client_inf.append(inf)
print(client_inf)


def client_got_in_line(time, amount_of_gas, mark_of_gas, number):
    refueling_time = servise_time(amount_of_gas)
    return 'В ' + time + ' новый клиент:  ' + time + ' ' + mark_of_gas + ' ' + str(amount_of_gas) + ' ' + \
           str(refueling_time) + ' встал в очередь к автомату №' + number


def client_refueled(time, amount_of_gas, mark_of_gas):
    refueling_time = servise_time(amount_of_gas)
    new_time = add_time(time, refueling_time)
    return 'В ' + new_time + ' клиент ' + time + ' ' + mark_of_gas + ' ' + str(amount_of_gas) + ' ' + \
           str(refueling_time) + ' заправил свой автомобиль и покинул АЗС.'


number_azs = gas_inf.keys()
azs_client = dict.fromkeys(number_azs, 0)


def azs_inf(gas_inf, mark_of_gas, azs_client):
    all_avt = []
    all_ochered = []
    for i in gas_inf:
        x = gas_inf[i]
        n = x[1]
        if isinstance(n, list) == True:
            for j in n:
                if j == mark_of_gas:
                    all_avt.append(i)
        else:
            if n == mark_of_gas:
                all_avt.append(i)
    if len(all_avt) > 1:
        for i in all_avt:
            ochered = azs_client[i]
            all_ochered.append(ochered)
        min_avt = ''
        while min_avt == '' and len(all_ochered) != 0:
            min_ochered = min(all_ochered)
            min_avt = get_key(azs_client, min_ochered)
            max_line = gas_inf[min_avt][0]
            if max_line < min_ochered + 1:
                all_ochered.remove(min(all_ochered))
                min_avt = ''
            else:
                min_avt = get_key(azs_client, min_ochered)
            return min_avt
    else:
        if gas_inf[all_avt[0]][0] >= all_avt[0] + 1:
            return all_avt[0]


def get_key(d, value):
    for k, v in d.items():
        if v == value:
            return k


def servise_time(gas_volume):
    t = randint(9, 11)
    if int(gas_volume) % 10:
        time = ceil(int(gas_volume) / t)
    else:
        time = ceil(ceil(int(gas_volume) / 10) * 10 / t)
    return time


def add_time(time, refueling_time):
    new_time = list(map(int, time.split(':')))
    minute = new_time[1] + refueling_time
    hour = new_time[0]
    while minute > 59:
        hour += 1
        minute -= 60
    if minute < 10:
        minute = '0' + str(minute)
    if hour < 10:
        hour = '0' + str(hour)
    return str(hour) + ':' + str(minute)


for client in client_inf:
    time = client[0]
    amount_of_gas = client[1]
    mark_of_gas = client[2]
    hours, minutes = list(map(int, time.split(':')))
    refueling_time = servise_time(amount_of_gas)
    min_o = azs_inf(gas_inf, mark_of_gas, azs_client)
    num = azs_client[min_o]
    num += 1
    azs_client[min_o] = num
    print(azs_client)

