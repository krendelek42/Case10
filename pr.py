import random as r
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

def client_got_in_line(time, amount_of_gas, mark_of_gas, number, refueling_time):
    '''просто текст что клиент встал в очередь'''
    print('В', time, 'новый клиент: ',time, mark_of_gas, amount_of_gas, refueling_time ,'встал в очередь к автомату №', number)

def client_refueled(time, amount_of_gas, mark_of_gas, refueling_time):
    '''просто текст когда клиент уехал'''
    new_time = list(map(int, time.split(':')))
    hours = int(new_time[0])
    minutes = (new_time[1])
    new_minutes = minutes + refueling_time
    new_hours = hours
    if new_minutes >= 60:
        new_hours = hours + 1
        new_minutes = 0
    if new_hours < 10:
        new_new_hours = '0' + str(new_hours)
    else:
        new_new_hours = str(new_hours)
    if new_minutes < 10:
        new_new_minutes = '0' + str(new_minutes)
    else:
        new_new_minutes = str(new_minutes)
    new_new_time = new_new_hours + ':' + new_new_minutes
    print('В', new_new_time, 'клиент',  time, mark_of_gas, amount_of_gas, refueling_time,  'заправил свой автомобиль и покинул АЗС.')

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
    min_refueling = r.choice([1,2])
    if amount_of_gas%10 == 0:
        refueling_time = min_refueling*(amount_of_gas//10)
    else:
        refueling_time = min_refueling*((amount_of_gas//10) + 1)
    return refueling_time


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


def time_of_old_client(time, refueling_time):
    ''' функция высчитывает во сколько клиент закончит заправляться'''
    new_time = list(map(int, time.split(':')))
    hours = int(new_time[0])
    minutes = (new_time[1])
    new_minutes = minutes + refueling_time
    new_hours = hours
    if new_minutes >= 60:
        new_hours = hours + 1
        new_minutes = 0
    if new_hours < 10:
        new_new_hours = '0' + str(new_hours)
    else:
        new_new_hours = str(new_hours)
    if new_minutes < 10:
        new_new_minutes = '0' + str(new_minutes)
    else:
        new_new_minutes = str(new_minutes)
    new_new_time = new_new_hours + ':' + new_new_minutes
    return new_new_time
''' тут пыталась чтобы все по времени нормально выводилось'''
old_time = ''
for client in client_inf:
    time = client[0]
    amount_of_gas = client[1]
    mark_of_gas = client[2]
    hours, minutes = list(map(int, time.split(':')))
    refueling_time = refuel_time(amount_of_gas)
    finish_time = time_of_old_client(time, refueling_time)

    if isinstance(azs_inf(gas_inf, mark_of_gas, azs_client, time, amount_of_gas, refueling_time), int) == True:
        min_avt = azs_inf(gas_inf, mark_of_gas, azs_client, time, amount_of_gas, refueling_time)
        num = azs_client[min_avt]
        num += 1
        azs_client[min_avt] = num
        if old_time != '' and ((int(old_time[:2]) > int(time[:2])) or (int(old_time[3:]) > int(time[3:]))):
            client_got_in_line(time, amount_of_gas, mark_of_gas, min_avt, refueling_time)
            azs_avt(gas_inf, azs_client)
            client_refueled(time, amount_of_gas, mark_of_gas, refueling_time)
            old_time = time
        elif old_time == '':
            client_got_in_line(time, amount_of_gas, mark_of_gas, min_avt, refueling_time)
            azs_avt(gas_inf, azs_client)
            client_refueled(time, amount_of_gas, mark_of_gas, refueling_time)
            old_time = time
        else:
            client_refueled(time, amount_of_gas, mark_of_gas, refueling_time)
            client_got_in_line(time, amount_of_gas, mark_of_gas, min_avt, refueling_time)
            azs_avt(gas_inf, azs_client)
            old_time = time

    else:
        azs_inf(gas_inf, mark_of_gas, azs_client, time, amount_of_gas, refueling_time)
        azs_avt(gas_inf, azs_client)




