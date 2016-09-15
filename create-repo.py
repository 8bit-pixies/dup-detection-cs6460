# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 09:32:47 2016

@author: Chapman
"""

from elasticsearch import Elasticsearch
import csv

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# https://tryolabs.com/blog/2015/02/17/python-elasticsearch-first-steps/
# pump csv file into elasticsearch repo...

with open('omscs-compiled-faq', 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    for idx, row in enumerate(csvreader):
        if idx == 0: continue
        es.index(index='faq', doc_type='faq-type', id=idx, body={
            'question': row[0],
            'answer': row[1],
            'source': row[2]
        })


# try a search 
query = es.search(index="faq", body={"query": {"match": {'question':'How do I register?'}}})

import pprint

pprint.pprint(query['hits']['hits'])


