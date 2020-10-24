import sys, re
pattern_ip = '[1-9]{1,3}\\.[1-9]{1,3}\\.[1-9]{1,3}\\.([5-9][\\d]|100)'
pattern_user = '(?<=]\s)(.*?)(?=\s\d)'
pattern_func = '(?<=\s\/)(.*?)(?=\s)'

def func1(array):
    user_array = dict()
    for line in array:


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('Задайте входной текстовый файл')
        sys.exit(-1)
    array = list()
    with open(sys.argv[1]) as file:
        for row in file:
            line = file.readline()
            m = re.search(pattern_ip, line)
            if not m:
                array.append(line)

    # файл прочитан, с учётом условия №2

    print(str(len(array)))
