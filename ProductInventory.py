'''A program that enables selection of products for purchase and updates their stock levels'''

# -*- coding: utf-8 -*-
"""
Created on 3 March 2020; re-coded 6 July 2020

@author: Charles Umesi
"""

from abc import ABC, abstractmethod
import os
import sys
import pandas as pd


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.mode.chained_assignment = None  # default='warn'
# You may want to enable (i.e., hashtag) chained_assignment until you are comfortable with your data


'''This program has classes, abstract classes and subclasses'''

class Product:
    
    '''Provides information on product'''
    
    #Initiation of classes managed by Product
    def __init__(self):
        self.item = self.Item()
        self.identity = self.Identity()
        self.quantity = self.Quantity()
        
    '''Abstract class'''
        
    class Item(ABC):
        
        def search_and_purchase(self):
            pass
        
    '''Subclasses'''
    
    class Identity(Item):
        
        '''Enables search for the product being sought for purchase'''
        
        def search_and_purchase(self):
            
            # Reads from main inventory file of items
            df1 = pd.read_csv('ProductInventory.csv') # MAKE SURE THIS FILE IS NOT OPEN(ED) DURING TRANSACTION(S)!
               
            product = input('Enter name of item : ')
            if any(df1['Item'].str.contains(product.upper())) == True:
                print(df1[df1['Item'].str.contains(product.upper())])
                del df1
                return Product.Quantity.search_and_purchase(self)
            
            elif all(df1['Item'].str.contains(product.upper())) == False:
                print('Item not found; try again.')
                del df1
                return Product.Identity.search_and_purchase(self)        
            
    class Quantity(Item):
        
        '''Enables selection and purchase of the desired product'''
        
        def search_and_purchase(self):
            
            # Reads from main inventory file of items or a temporary one (if it has been created)
            df2 = pd.DataFrame()
            if os.path.isfile('ProductInventory_transient.csv') == True:
                df2 = pd.read_csv('ProductInventory_transient.csv')
            else:
                df2 = pd.read_csv('ProductInventory.csv')
            df2
            
            # Creates an empty basket for item(s) purchased
            basket = pd.DataFrame()
            
            # Defines a mechanism for increasing contents of basket
            increase_basket = pd.DataFrame()
        
            # Enables selection of the required item from a possible choice of items
            index = eval(input('Enter index of required item (number on far left) : '))
        
            # Enables entry of the required quantity of the item you wish to purchase subject to stock level
            quantity = eval(input('Enter required quantity : '))
            if quantity <= df2.loc[index,'Quantity']:
                basket = basket.append(df2[df2['Item']==df2.loc[index,'Item']])
                print('Item added to basket')
            else:
                print('Insufficient stock; try again.')
                return Product.Identity.search_and_purchase(self)
            basket
            basket.loc[index,'Quantity'] = quantity
            basket.loc[index,'Value'] = basket.loc[index,'Price']*basket.loc[index,'Quantity']
                
            # Saves basket
            if os.path.isfile('Basket.csv') == True:
                addToThis = pd.read_csv('Basket.csv')
                increase_basket = pd.concat([addToThis,basket])
                increase_basket.to_csv('Basket.csv',index=False)        
            else:
                basket.to_csv('Basket.csv',index=False)
        
            # Saves basket in money format for the customer's invoice
            basket.loc[index,'Price'] = '£' + "%.2f"%basket.loc[index,'Price']
            basket.loc[index,'Value'] = '£' + "%.2f"%basket.loc[index,'Value']
            if os.path.isfile('Money_Basket.csv') == True:
                addToThis2 = pd.read_csv('Money_Basket.csv')
                increase_basket = pd.concat([addToThis2,basket])
                increase_basket.to_csv('Money_Basket.csv',index=False)   
            else:
                basket.to_csv('Money_Basket.csv',index=False)
        
            # Alters stock level in a created temporary inventory file as a result of purchase
            df2.loc[index,'Quantity'] = df2.loc[index,'Quantity'] - quantity
            df2.loc[index,'Value'] = df2.loc[index,'Price']*df2.loc[index,'Quantity']
            df2.to_csv('ProductInventory_transient.csv',index=False)  # This is the temporary inventory file
            del df2
        
            # Option to continue purchasing or checkout (or bail out (unintentionally) - see else keyword below)
            further = input('Do you wish to purchase a further item? (Y/N) : ')
            if further == 'Y' or further == 'y':
                return Product.Identity.search_and_purchase(self)
            elif further == 'N' or further == 'n':
                exit = further  # Note that exit(further) is less reliable than exit = further
                
            # In case the customer enters an input other than Y/n or N/n, accidentally or deliberately
            else:
                del basket
                del increase_basket
                os.remove('Basket.csv')
                os.remove('Money_Basket.csv')
                os.remove('ProductInventory_transient.csv')
                print('Transaction cancelled. You have not been charged.')
                sys.exit()
                
            '''END OF PRODUCT CLASS'''
        
class Inventory:
    
    '''Alters stock levels of products in the main file following purchase'''
 
    # Initiation of classes managed by Inventory
    def __init__(self):
        self.items = self.Items()
        self.levels = self.Levels()
        
    '''Abstract class'''
        
    class Items(ABC):
        
        def amend_levels(self):
            pass
        
    '''Subclass'''
    
    class Levels(Items):
        
        def amend_levels(self):
            
            # Reads data from updated stock level in temporary inventory file
            df3 = pd.read_csv('ProductInventory_transient.csv')
        
            # Retrieves saved basket
            retrieveBasket = pd.read_csv('Basket.csv')
        
            # Retrieves saved basket in money format
            retrieveMoney = pd.read_csv('Money_Basket.csv')

            # Converts float quantity for purchase into integer values for the customer's invoice
            y = (retrieveMoney['Quantity']).astype(int)
    
            # Sums up purchases in money format for the customer's invoice
            total_money = '£' + "%.2f"% sum(retrieveBasket['Value'])
            
            # Produces invoice of purchase(s) by the customer 
            invoice = pd.concat([retrieveMoney[['Item','Price']],y,retrieveMoney['Value']],axis=1)
            print(invoice.to_string(index=False))
            print(f'Total: {total_money}')
            
            # Confirms purchases and makes any necessary final readjustment of stock in the main inventory file before deleting temporary files
            y = df3[df3['Code'] =='Total'].index[0]
            z = df3.loc[y,'Value'] 
            confirm = input('Confirm (Y/N) : ')
            if confirm == 'Y' or confirm == 'y':
                df3.loc[y,'Value'] = sum(df3['Value']) - z
                df3.to_csv('ProductInventory.csv',index=False) # This is the main inventory file     
                del retrieveBasket
                os.remove('Basket.csv')
                del retrieveMoney
                os.remove('Money_Basket.csv')
                del df3
                os.remove('ProductInventory_transient.csv')        
                print('Thank you for your purchase.')
                
            elif confirm == 'N' or confirm == 'n':
                del retrieveBasket
                os.remove('Basket.csv')
                del retrieveMoney
                os.remove('Money_Basket.csv')
                del df3
                os.remove('ProductInventory_transient.csv') 
                print('Transaction cancelled. You have not been charged.')                
            
            # In case the customer enters an input other than Y/n or N/n, accidentally or deliberately  
            else:
                del retrieveBasket
                os.remove('Basket.csv')
                del retrieveMoney
                os.remove('Money_Basket.csv')
                del df3
                os.remove('ProductInventory_transient.csv') 
                print('Transaction cancelled. You have not been charged.')



'__main__'
c = Product()
d = c.Identity()
d.search_and_purchase()
e = Inventory()
f = e.Levels()
f.amend_levels()