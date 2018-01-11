import json
import pickle
from pprint import pprint 
import re
import requests
from elasticsearch5 import Elasticsearch
from datetime import timedelta, date
import datetime
import traceback

class es02 :
    def __init__(self):
        self.es = Elasticsearch(['https://search-el-dev-znz7hdtpcgghjcq4vatwtc3xiu.ap-northeast-2.es.amazonaws.com:443'])
        self.set_service()
        pass
    
    def load(self,fname="es01.pkl"):
        self.data = pickle.load( open( fname, "rb" ))

    def load_datas(self,start_date=date(2017, 12, 1),end_date=date(2018,1,9)):
        d = start_date
        delta = datetime.timedelta(days=1)
        while d <= end_date:
            es_date = d.strftime("%Y.%m.%d")
            print(es_date)
            try:
                self.load_data(es_date)
                self.parse()
                #print(es.dset)            
            except Exception:
                print(traceback.format_exc())
            d += delta

    def load_data(self,dt="2018.01.08"):
        es_index = 'slowquery-'+dt
        page = self.es.search(
            index = es_index,
            doc_type = 'elltdev',
            body = { 
                'query' : { 'match_all' : {}}
            }
        )
        self.data = page
    # print("test")


    def load_datas2(self,start_date=date(2017, 12, 1),end_date=date(2018,1,9)):
        d = start_date
        delta = datetime.timedelta(days=1)
        while d <= end_date:
            es_date = d.strftime("%Y.%m.%d")
            print(es_date)
            try:
                self.load_data2(es_date)
                self.parse()
                #print(es.dset)            
            except:
                print("can't not find data")
            d += delta    
    def load_data2(self,dt):
        url = 'https://search-el-dev-znz7hdtpcgghjcq4vatwtc3xiu.ap-northeast-2.es.amazonaws.com:443/slowquery-'+dt+'/elltdev/_search'
        resp = requests.get(url=url)
        self.data = json.loads(resp.text)

    #data = {'took': 1, '_shards': {'total': 5, 'successful': 5, 'failed': 0}, 'timed_out': False, 'hits': {'max_score': 1.0, 'total': 1550, 'hits': [{'_source': {'host': 'omuser[omuser] @  [10.125.224.9]  Id: 1005635', 'Rows_examined': 514, 'query': '''SELECT \t/*+ [goods-api].GoodsDetailDAO.getGdItemInfo */\t\t\t\titemT.GOODS_NO\t\t        , GROUP_CONCAT(DISTINCT itemT.ITEM_NO separator ',') AS ITEM_NO\t\t        , itemT.OPT_NM\t\t        , itemT.OPT_VAL\t\t\t\t, optT.OPT_SEQ\t\t\t\t \t\t  FROM (\t\t\t\tSELECT /*+ [goods-api].GoodsDetailDAO.getGdItemInfo */\t\t\t\t\t\tgd_item_opt.ITEM_NO\t\t\t            , GOODS_NO\t\t\t\t\t\t, OPT_NM\t\t\t\t\t\t, OPT_VAL\t\t\t\t  FROM gd_item , gd_item_opt\t\t\t\t WHERE gd_item_opt.ITEM_NO = gd_item.ITEM_NO\t\t\t\t ) itemT\t\t INNER JOIN gd_goods_opt optT\t        ON itemT.GOODS_NO = optT.GOODS_NO\t\t   AND itemT.OPT_NM = optT.OPT_NM\t\t \t\t   AND optT.GOODS_NO = '1000000644'\t\t   \t \t\t    \t\t   AND optT.OPT_SEQ = '1'\t\t GROUP BY itemT.GOODS_NO, itemT.OPT_NM, itemT.OPT_VAL, optT.OPT_SEQ;'''}}] }}

    # 데이터를 저장하기 위한 영역 
    dset = []
    dtmp = {}

    def set_service(self,svc="goods"):
        self.svc = svc

    def get_dbio(self,sql):
        pat = re.compile("\[\w+\-api][\w|.]+")
        m = pat.findall(sql)
        if  len(m) > 0 :
            return (m[0]).strip()
        else:
            return None

    def get_tables(self,sql):
        pat = re.compile("(?<=\W)(?:GD|AT|CC|CH|DP|ET|MB|OM|PR|ST)\_[\_\w\.]+(?=\W)",re.I)
        tables = pat.findall(sql)
        if len(sql) > 0 :
            return [x.upper()   for x in tables if x.find(".") == -1 ]
        else:
            return None

    def print_kv(self,k,v):
        if ( k in ['host','Rows_examined','Query_time','@timestamp','service','Lock_time']):
            #print(k,":",v)
            self.dtmp[k] = v
        elif ( k in ['query']):
            #print("dbio :", get_dbio(v))
            self.dtmp['dbio'] = self.get_dbio(v)
            #print("tables :",get_tables(v))
            self.dtmp['tables'] = self.get_tables(v)
        elif ( k in ['_source']):
            #print("="*80)
            self.print_data(v)
            if self.dtmp['dbio'] != None  and len(self.dtmp['tables']) > 0 :
                #self.dset[self.dtmp['dbio']] = self.dtmp['tables']  
                if(self.dtmp['service'] == self.svc) :              
                    self.dset.append(self.dtmp['tables'])
            self.dtmp = {}
        else:
            #print(k,":")
            self.print_data(v)


    def print_data(self,d):
        if ( type(d) == dict ):
            for k,v in d.items():            
                self.print_kv(k,v)
        elif( type(d) == list ):
            for item in d:
                self.print_data(item)
        elif( type(d) in [str,int,bool,float] ) :
            pass
        else:
            print("="*80)
            print(type(d))            
    # print_data argement없이 호출하는 함수.            
    def parse(self):
        self.print_data(self.data)

#테스트를 위한 메인 함수 
if __name__ == "__main__":
    es = es02()
    # d = date(2017, 12, 1)
    # delta = datetime.timedelta(days=1)
    # while d <= date(2018,1,9):
    #     es_date = d.strftime("%Y.%m.%d")
    #     print(es_date)
    #     try:
    #         es.load_data(es_date)
    #         es.parse()
    #         print(es.dset.values())            
    #     except:
    #         print("can't not find data")
    #     d += delta
    es.load_data('2018.01.07')
    #es.load_datas(date(2017,12,1),date(2018,1,8))
    es.parse()
    print(es.dset)

