import re 

sql = '''SELECT \t/*+ [goods-api].GoodsDetailDAO.getGdItemInfo */\t\t\t\titemT.GOODS_NO\t\t        , GROUP_CONCAT(DISTINCT itemT.ITEM_NO separator ',') AS ITEM_NO\t\t        , itemT.OPT_NM\t\t        , itemT.OPT_VAL\t\t\t\t, optT.OPT_SEQ\t\t\t\t \t\t  FROM (\t\t\t\tSELECT /*+ [goods-api].GoodsDetailDAO.getGdItemInfo */\t\t\t\t\t\tgd_item_opt.ITEM_NO\t\t\t            , GOODS_NO\t\t\t\t\t\t, OPT_NM\t\t\t\t\t\t, OPT_VAL\t\t\t\t  FROM gd_item. , gd_item_opt\t\t\t\t WHERE gd_item_opt.ITEM_NO = gd_item.ITEM_NO\t\t\t\t ) itemT\t\t INNER JOIN gd_goods_opt optT\t        ON itemT.GOODS_NO = optT.GOODS_NO\t\t   AND itemT.OPT_NM = optT.OPT_NM\t\t \t\t   AND optT.GOODS_NO = '1000000644'\t\t   \t \t\t    \t\t   AND optT.OPT_SEQ = '1'\t\t GROUP BY itemT.GOODS_NO, itemT.OPT_NM, itemT.OPT_VAL, optT.OPT_SEQ;'''

#pat = re.compile("\[w+-api\]w+\W")
pat = re.compile("(?<=\W)(?:GD|AT|CC|CH|DP|ET|MB|OM|PR|ST)\_[\_\w]+(?=\W)",re.I)
m = pat.findall(sql)
print(m)
print(len(m))
#print(m.group(1))