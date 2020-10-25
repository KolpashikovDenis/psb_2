import sys, re
from datetime import datetime

pattern_ip = '[1-9]{1,3}\\.[1-9]{1,3}\\.[1-9]{1,3}\\.([5-9][\\d]|100)'
pattern_user = '(?<=]\s)(.*?)(?=\s\d)'
pattern_func = '(?<=\s\/)(.*?)(?=\s)'
pattern_host = '[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}'
pattern_time = '(?<=\[)(.*?)(?=])'
pattern_size = '(?<=Data\s)(.*?)(?=\s)'
pattern_send = 'sendData'
pattern_receive = 'receiveData'

def func1(array):
    user_dict = dict()
    for line in array:
        # Получаю из каждой строки массива юзера и вызванную им функцию
        u = re.search(pattern_user, line)[0]
        f = re.search(pattern_func, line)[0]

        # тут ищу в словаре вхождение юзера, если есть достаю вложенный словарь с функцией и частотой вызова
        a = user_dict.get(u)
        if a:
            t = dict()
            b = a.get(f, 0)
            if b == 0:
                t[f] = 1
                a.update(t)
            else:
                t[f] = b + 1
                a.update(t)
        else:
            t = dict()
            t[f] = 1
            user_dict[u] = t
    keys = user_dict.keys()
    fOut = open(sys.argv[2], 'w')
    #print('1) Most used methods')
    fOut.write('1) Most used methods\n')
    for key in keys:
        a = dict()
        a = user_dict.get(key)
        b = max(a, key=a.get)
        #print('\t{} - /{}'.format(key, b))
        fOut.write('\t{} - /{}\n'.format(key, b))
    fOut.write('\n')
    fOut.close()

def func2(array):
    arr_host = dict()
    for line in array:
        host = re.search(pattern_host, line)[0]
        item_host = arr_host.get(host, 0)
        if item_host == 0:
            arr_host[host]=1
        else:
            arr_host[host] = item_host + 1

    b = max(arr_host, key=arr_host.get)

    # Тут ищем время первого обращения и последнего обращения к самому популярному хосту
    line_first = str()
    line_last = str()
    for line in array:
        if line.find(b) != -1:
            line_first = line
            break

    array.reverse()
    for line in array:
        if line.find(b) != -1:
            line_last = line
            break
    m1 = re.search(pattern_time, line_first)
    m2 = re.search(pattern_time, line_last)
    date1 = datetime.strptime(m1[0], '%a %b %d %H:%M:%S GMT+03:00 %Y')
    date2 = datetime.strptime(m2[0], '%a %b %d %H:%M:%S GMT+03:00 %Y')
    fOut = open(sys.argv[2], 'a')
    fOut.write('2) Busiest host - {0}\n'.format(b))
    fOut.write('\tFirst connection time - [{0}]\n\tLast connection time - [{1}]\n\n'
          .format(date1.strftime('%d.%m.%Y %H:%M:%S'), date2.strftime('%d.%m.%Y %H:%M:%S')))
    fOut.close()
    # print('Busiest host - {0}'.format(b))
    # print('\tFirst connection time - ({0})\n\tLast connection time - ({1})'
    #       .format(date1.strftime('%d.%m.%Y %H:%M:%S'), date2.strftime('%d.%m.%Y %H:%M:%S')))
    # print()

def func3(array):
    bis_minute = dict()
    sended = int()
    received = int()
    for line in array:
        # Получаем время с точностью до минуты
        d = datetime.strptime(re.search(pattern_time, line)[0], '%a %b %d %H:%M:%S GMT+03:00 %Y')
        dt_str = d.strftime('%d.%m.%Y %H:%M')
        if bis_minute.get(dt_str) is None:
            t = dict()
            t['receiveData'] = 0
            t['sendData'] = 0
            bis_minute[dt_str] = t

        m = re.search(pattern_receive, line)
        s = bis_minute.get(dt_str)
        if m != None:
            received = int(re.search(pattern_size, line)[0])
            a = s['receiveData']
            s['receiveData'] = a + received

        m = re.search(pattern_send, line)
        if m != None:
            sended = int(re.search(pattern_size, line)[0])
            a = s['sendData']
            s['sendData'] = a + sended

    tmp_dict = dict()
    for key in bis_minute.keys():
        t = dict()
        t = bis_minute.get(key)
        a = int(t.get('sendData'))
        b = int(t.get('receiveData'))
        tmp_dict[key] = a + b

    c = max(tmp_dict, key=tmp_dict.get)
    t = bis_minute.get(c)
    # print('3) Busiest minute - [{0}]\n\tbyte sent - {1}\n\tbyte received - {2}'.format(c, t['sendData'], t['receiveData']))
    fOut = open(sys.argv[2], 'a')
    fOut.write('3) Busiest minute - [{0}]\n\tbyte sent - {1}\n\tbyte received - {2}'.format(c, t['sendData'], t['receiveData']))
    fOut.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print('Параметры запуска:')
        print('\tpython {0} <inputFile> <outputFile>')
        sys.exit(-1)
    array = list()

    # Условие №2
    with open(sys.argv[1]) as file:
        for row in file:
            m = re.search(pattern_ip, row)
            if not m:
                array.append(row)

    # Условие задания №3
    func1(array)

    # Условие задания №4
    func2(array)

    # Условие задания №5
    func3(array)

    print('Done.')

