from elasticsearch5 import Elasticsearch
import chardet
import pickle
es = Elasticsearch(['https://search-el-dev-znz7hdtpcgghjcq4vatwtc3xiu.ap-northeast-2.es.amazonaws.com:443'])
print(es.info())

page = es.search(
    index = 'slowquery-2018.01.09',
    doc_type = 'elltdev',
    body = { 
        'query' : { 'match_all' : {}}
    }
)
pickle.dump(page,open('es01.pkl','wb'))
#f = open("es01.json",'w')
#data = str(page)
# print(chardet.detect(page))
# f.write(data)
# f.close()