import sys, re
import operator

pattern_ip = '[1-9]{1,3}\\.[1-9]{1,3}\\.[1-9]{1,3}\\.([5-9][\\d]|100)'
pattern_user = '(?<=]\s)(.*?)(?=\s\d)'
pattern_func = '(?<=\s\/)(.*?)(?=\s)'
pattern_host = '[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}\.[\d]{1,3}'

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
    for key in keys:
        a = dict()
        a = user_dict.get(key)
        b = max(a, key=a.get)
        print('Юзер {}, часто используемая функция: {}, кол-во вызовов {}'.format(key, b, a.get(b)))

def func2(array):
    arr_host = dict()
    for line in array:
        host = re.search(pattern_host, line)[0]
        item_host =



if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Задайте входной текстовый файл')
        sys.exit(-1)
    array = list()

    # Условие №2
    with open(sys.argv[1]) as file:
        for row in file:
            line = file.readline()
            m = re.search(pattern_ip, line)
            if not m:
                array.append(line)

    # Условие задания №3
    #func1(array)

    # Условие задания №4
    func2(array)

