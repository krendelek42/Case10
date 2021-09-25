import random as r
refueling_information = open('azs.txt', encoding='utf-8')
clients_information = open('input.txt', encoding='utf-8')
price_gas = {'АИ-80':50, 'АИ-92':44, 'АИ-95':47, 'АИ-98':58}
t = [1,2]
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

def client_got_in_line(time, amount_of_gas, mark_of_gas, number, refueling_time):
    print('В', time, 'новый клиент: ',time, mark_of_gas, amount_of_gas, refueling_time ,'встал в очередь к автомату №', number)

def client_refueled(time, amount_of_gas, mark_of_gas, refueling_time):
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
    if new_minutes < 10:
        new_new_minutes = '0' + str(new_minutes)
    new_new_time = new_new_hours + ':' + new_new_minutes
    print('В', new_new_time, 'клиент',  time, mark_of_gas, amount_of_gas, refueling_time,  'заправил свой автомобиль и покинул АЗС.')

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

for client in client_inf:
    time = client[0]
    amount_of_gas = client[1]
    mark_of_gas = client[2]
    hours, minutes = list(map(int, time.split(':')))
    refueling_time = r.choice(t)*amount_of_gas
    min_o = azs_inf(gas_inf, mark_of_gas, azs_client)
    num = azs_client[min_o]
    num += 1
    azs_client[min_o] = num
    print(azs_client)



