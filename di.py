# Dokukina K.A. 65%
# Ignatovich D.M. 50%
# Kozlova L.A. 40%


import random as r
from math import ceil
refueling_information = open('azs.txt', encoding='utf-8')
clients_information = open('input.txt', encoding='utf-8')
price_gas = {'АИ-80':50, 'АИ-92':44, 'АИ-95':47, 'АИ-98':58}
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

client_inf = []
for line in clients_information:
    all_inf = list(map(str, line[:-1].split(' ')))
    time = all_inf[0]
    amount_of_gas = int(all_inf[1])
    mark_of_gas = all_inf[2]
    inf = [time, amount_of_gas, mark_of_gas]
    client_inf.append(inf)


def client_got_in_line(time, amount_of_gas, mark_of_gas, number):
    '''A function that displays the text that the client has entered the queue
    :param time: car arrival time.
    :param amount_of_gas: fuel quantity
    :param mark_of_gas: mark of petrol
    :param number: machine number
    :return: text
    '''
    refueling_time = refuel_time(amount_of_gas)
    return 'В ' + str(time) + ' новый клиент:  ' + str(time) + ' ' + str(mark_of_gas) + ' ' + str(amount_of_gas) + ' ' + \
           str(refueling_time) + ' встал в очередь к автомату №' + str(number)

def client_refueled(time, amount_of_gas, mark_of_gas):
    '''
    A function that displays the text that the customer has refueled his car.
    :param time: car arrival time.
    :param amount_of_gas: fuel quantity
    :param mark_of_gas: mark of petrol
    :return: text
    '''
    refueling_time = refuel_time(amount_of_gas)
    new_time = add_time(time, refueling_time)
    return 'В ' + new_time + ' клиент ' + time + ' ' + mark_of_gas + ' ' + str(amount_of_gas) + ' ' + \
           str(refueling_time) + ' заправил свой автомобиль и покинул АЗС.'

number_azs = gas_inf.keys()
azs_client = dict.fromkeys(number_azs, 0)

def azs_inf(gas_inf, mark_of_gas, azs_client, time, amount_of_gas, refueling_time):
    '''
    A function that calculates the queue of machines.
    :param gas_inf: information about machines
    :param mark_of_gas: mark of petrol
    :param azs_client: information about the queue at the machines
    :param time: car arrival time.
    :param amount_of_gas: fuel quantity
    :param refueling_time: car refueling time
    :return: text that the car did not have time to refuel or the number of the machine
    '''
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
                all_ochered.remove(min_ochered)
                min_avt = ''
            else:
                min_avt = get_key(azs_client, min_ochered)
        if isinstance(min_avt, int) == True:
            return min_avt
        else:
            return client_left_azs(time, mark_of_gas, amount_of_gas, refueling_time)
    else:
        ochered = azs_client[all_avt[0]]
        if gas_inf[all_avt[0]][0] >= ochered + 1:
            return all_avt[0]
        else:
             return client_left_azs(time, mark_of_gas, amount_of_gas, refueling_time)

def get_key(d, value):
    '''
    Helper function that retrieves a key from a dictionary by value.
    :param d: dictionary
    :param value: value
    :return: key
    '''
    for k, v in d.items():
        if v == value:
            return k
def client_left_azs(time, mark_of_gas, amount_of_gas, refueling_time):
    '''
    A function that issues a test that the customer was unable to refuel the vehicle.
    :param time: car arrival time
    :param mark_of_gas: mark of petrol
    :param amount_of_gas: fuel quantity
    :param refueling_time: car refueling time
    :return: text
    '''
    print('В', time,  'новый клиент:',time, mark_of_gas, amount_of_gas, refueling_time, 'не смог заправить автомобиль и покинул АЗС.')

def refuel_time(amount_of_gas):
    '''
    A function that calculates how long it will take to refuel the vehicle.
    :param amount_of_gas: fuel quantity
    :return: car refueling time
    '''
    t = r.choice([9,10, 11])
    if int(amount_of_gas) % 10:
        time = ceil(int(amount_of_gas) / t)
    else:
        time = ceil(ceil(int(amount_of_gas) / 10) * 10 / t)
    return time


def azs_avt(gas_inf, azs_client):
    '''
    A function that displays data about vending machines at a gas station.
    :param gas_inf: information about machines
    :param azs_client: information about the queue at the machines
    :return: text about machine
    '''
    for i in gas_inf:
        max_ochered = gas_inf[i][0]
        mark_gas = gas_inf[i][1]
        line_in_azs = azs_client[i]
        if line_in_azs == 0:
            if isinstance(mark_gas, list) == True:
                print('Автомат №', i, 'максимальная очередь:', max_ochered, 'Марки бензина:', *mark_gas, '->')
            else:
                print('Автомат №', i, 'максимальная очередь:', max_ochered, 'Марки бензина:', mark_gas, '->')
        else:
            if isinstance(mark_gas, list) == True:
                print('Автомат №', i, 'максимальная очередь:', max_ochered, 'Марки бензина:', *mark_gas, '->',
                      '*' * line_in_azs)
            else:
                print('Автомат №', i, 'максимальная очередь:', max_ochered, 'Марки бензина:', mark_gas, '->',
                      '*' * line_in_azs)


def add_time(time, refueling_time):
    '''
    A function that calculates the time when the customer will finish refueling.
    :param time: car arrival time
    :param refueling_time: car refueling time
    :return: new time
    '''
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

fuel = {'АИ-92': 0, 'АИ-80': 0, 'АИ-95': 0, 'АИ-98': 0}
unrefueled = set()
fueled = {0}
for i in range(235):
    unrefueled.add(i)
old_time = '00:00'
i = 0
a = []
f = []
while old_time[:2] < '24':
    time = client_inf[i][0]
    benz = client_inf[i][1]
    ai = client_inf[i][2]
    number_of_fueled =i
    amount_of_gas = client_inf[i][1]
    mark_of_gas = client_inf[i][2]
    hours, minutes = list(map(int, time.split(':')))
    refueling_time = refuel_time(amount_of_gas)
    finish_time = add_time(time, refueling_time)
    x = [time, amount_of_gas, mark_of_gas, finish_time, refueling_time]
    if old_time == '00:00':
        min_avt = azs_inf(gas_inf, mark_of_gas, azs_client, time, amount_of_gas, refueling_time)
        num = azs_client[min_avt]
        num += 1
        azs_client[min_avt] = num
        print(client_got_in_line(time, amount_of_gas, mark_of_gas, min_avt))
        i += 1
        x.append(min_avt)
        f.append(x)
        azs_avt(gas_inf, azs_client)
    elif f:
        for j in f:
            if str(j[3]) == old_time:
                fueled.add(number_of_fueled)
                print(client_refueled(j[0], j[1], j[2]))
                benz = j[1]
                ai = j[2]
                fuel[ai]+= benz
                azs_client[j[5]] -= 1
                a.append(j)
                azs_avt(gas_inf, azs_client)
        if a:
            for j in a:
                a.remove(j)
                f.remove(j)
    if (old_time == time) and (old_time != '00:00'):
        if isinstance(azs_inf(gas_inf, mark_of_gas, azs_client, time, amount_of_gas, refueling_time), int) == True:
            min_avt = azs_inf(gas_inf, mark_of_gas, azs_client, time, amount_of_gas, refueling_time)
            num = azs_client[min_avt]
            num += 1
            azs_client[min_avt] = num
            print(client_got_in_line(time, amount_of_gas, mark_of_gas, min_avt))
            i += 1
            x.append(min_avt)
            f.append(x)
            azs_avt(gas_inf, azs_client)

    old_time = add_time(old_time, 1)
print('Количество литров проданное за сутки ', fuel)
sum = 0
for key in fuel:
    sum += fuel[key]*price_gas[key]
print("общая сумма продаж:", sum)
q = set()
q = fueled.difference(unrefueled)
a = set()
if q == a:
    print("количество незаправившихся:",0)
else:
    print("количество незаправившихся:", q)
