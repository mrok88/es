import requests
import json
from datetime import timedelta, date
import datetime
from es02 import es02


#테스트를 위한 메인 함수 
if __name__ == "__main__":
    es = es02()
    #es.load_data2('2018.01.07')
    es.load_datas2(date(2017,12,1),date(2018,1,8))
    es.parse()
    print(es.dset)