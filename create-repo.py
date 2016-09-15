# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 09:32:47 2016

@author: Chapman
"""

from elasticsearch import Elasticsearch
import csv

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# load the files into ES
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
query = es.search(index="faq", body={"query": {"match": {'question':'registration'}}})

pretty_string = """The best answer returned by ES is: 
    {}

from source: 
    {}
match question: 
    {}
"""

print(pretty_string.format(query['hits']['hits'][0]['_source']['answer'], 
                           query['hits']['hits'][0]['_source']['source'],
                           query['hits']['hits'][0]['_source']['question']))


"""
# query - "registration"

The best answer returned by ES is: 
    You will be issued a time ticket usually about ten days before classes start that tells you when to log in and register. There will be an email usually a few days before time tickets are assigned that explains the process in excruciating detail. To see when time tickets will be issued, check out the [Academic Calendar](http://www.registrar.gatech.edu/calendar/).

from source: 
    reddit
match question: 
    How does registration work for new students?

"""