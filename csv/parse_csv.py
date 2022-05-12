import csv
import math

dict = {}
header = []

def read_csv(fileName):
    csvFile = open(fileName, 'r')
    reader = csv.reader(csvFile)

    for index,info in enumerate(reader):
        if index == 0:
            init_dict(info)
        else:
            complete_dict(info)
    
    write_csv()

def init_dict(titles):
    for i in range(len(titles)):
        if i < len(titles) - 2:
            header.append(titles[i])
            column = []
            dict[titles[i]] = column
    

def complete_dict(info):
    keys = list(dict.keys())
    for i in range(len(keys)):
        dict[keys[i]].append(float(info[i]))

def write_csv():
    data = []
    column_data = []
    for item in dict.values():
        column = list(item)
        column.sort(reverse = True)
        column_data.append(column[math.floor(len(column) * 0.05) - 1])
    data.append(column_data)

    with open('结果.csv', 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)

if __name__ == "__main__":
    file_name = input("请输入文件名: ")
    read_csv(file_name)
    print('结果已经输出到：结果.csv')
    input('press any key to exit')