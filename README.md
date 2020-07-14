# ProductInventory
A Python module that enables selection of products for purchase and updates their stock levels
```python
from abc import ABC, abstractmethod
import os
import sys
import pandas as pd


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None  # default='warn'
# You may want to enable (i.e., hashtag) chained_assignment until you are comfortable with your data


'''This module has classes, abstract classes and subclasses'''

class Product:
    
    '''Provides information on product'''
    
    #Initiation of classes managed by Product
    def __init__(self):
        self.item = self.Item()
        self.identity = self.Identity()
        ...
