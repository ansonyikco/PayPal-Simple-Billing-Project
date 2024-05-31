# -*- coding: utf-8 -*-
"""
Created on Wed Apr  3 23:53:23 2024

@author: Anson YIK
"""

def display():
    for  i in range(len(Token_book)):
        print ('{} - \n - Reference Number : {} \n - Status : {} \n - Name : {}\n - Amount : {}'.format(str(i),str(Reference_Number_book[i]),str(status_book[i]),str(Name_book[i]),str(Amount_book[i])))
 
Token_book = []
id_book = []
status_book = []
Name_book = []
Amount_book = []
Address_book = []
Amount_book = []
Reference_Number_book = []
