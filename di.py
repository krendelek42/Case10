import random as r
from math import ceil
refueling_information = open('azs.txt', encoding='utf-8')
clients_information = open('input.txt', encoding='utf-8')
price_gas = {'АИ-80':50, 'АИ-92':44, 'АИ-95':47, 'АИ-98':58}
gas_inf = {} # тут будет храниться вся инфа про азс
'''Это читаем инфу про азс'''
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
'''это читаем инфу про клиентов'''
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
    '''просто текст что клиент встал в очередь'''
    refueling_time = refuel_time(amount_of_gas)
    return 'В ' + str(time) + ' новый клиент:  ' + str(time) + ' ' + str(mark_of_gas) + ' ' + str(amount_of_gas) + ' ' + \
           str(refueling_time) + ' встал в очередь к автомату №' + str(number)

def client_refueled(time, amount_of_gas, mark_of_gas):
    '''просто текст когда клиент уехал'''
    refueling_time = refuel_time(amount_of_gas)
    new_time = add_time(time, refueling_time)
    return 'В ' + new_time + ' клиент ' + time + ' ' + mark_of_gas + ' ' + str(amount_of_gas) + ' ' + \
           str(refueling_time) + ' заправил свой автомобиль и покинул АЗС.'

number_azs = gas_inf.keys() # тут номера заправок
azs_client = dict.fromkeys(number_azs, 0) # тут отслеживается очередб по заправкам

def azs_inf(gas_inf, mark_of_gas, azs_client, time, amount_of_gas, refueling_time):
    ''' тут добавляется очередь к заправкам, если заято - клиент уезжает'''
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
    ''' просто функция которая вытаскивает ключ из словаря по значению'''
    for k, v in d.items():
        if v == value:
            return k
def client_left_azs(time, mark_of_gas, amount_of_gas, refueling_time):
    print('В', time,  'новый клиент:',time, mark_of_gas, amount_of_gas, refueling_time, 'не смог заправить автомобиль и покинул АЗС.')

def refuel_time(amount_of_gas):
    ''' высчитывает сколько времени на заправку нужно'''
    t = r.choice([9,10, 11])
    if int(amount_of_gas) % 10:
        time = ceil(int(amount_of_gas) / t)
    else:
        time = ceil(ceil(int(amount_of_gas) / 10) * 10 / t)
    return time


def azs_avt(gas_inf, azs_client):
    '''инфа про атвоматы и очереди в них'''
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
    ''' функция высчитывает во сколько клиент закончит заправляться'''
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

old_time = '00:00'
i = 0 #номер клиента в общем списке
a = [] #список клиентов, которые уезжают в данный момент
f = [] #список клиентов на заправке
while old_time[:2] < '24':
    time = client_inf[i][0]
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
                print(client_refueled(j[0], j[1], j[2]))
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
