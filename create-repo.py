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