#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 13:02:17 2023

@author: zaneleakibo-betts
# """
from book import Book
from  libdata import LibData
from account import Account
from librarian import Librarian
from user import User, Student,Staff

#creates table in sqlite database
import sqlite3
conn = sqlite3.connect("db.db")

#conn = sqlite3.connect('db.db')
#c=conn.cursor()
#c.execute("INSERT INTO Users VALUES(1,'Zanele','Betts','user1','user1', 'student')")
#c.execute("INSERT INTO Users VALUES(2,'Gareth','Betts','user2','user2','staff')")
#c.execute("INSERT INTO Users VALUES(3,'Isaac','Betts','user3','user3','librarian')")
#conn.commit()
#conn.close()

class LibraryManSystem:
    
    
    def __init__(self): 
        #runs the login function
        LibraryManSystem.login() #instantiates the LMS
        #LibraryManSystem.Register() #runs the register function
        
        
    @staticmethod       
    def Register():
        
        try:
                 
                 Id = input("Enter your Id ")
                 Name = input("Enter your name ")
                 UserName = input("Enter your username ")
                 Password = input("Enter your password ")
                 Role = input("Enter your User Type ")
                 
                 c = conn.cursor()
                 c.execute(""" 
                           INSERT INTO users (Id, name, username, password, role)
                           VALUES (:Id, :name, :username, :password, :role)              
                           """, {'Id': Id, 'name': Name, 'username': UserName, 'password': Password, 'role': Role})
                
                 
                 conn.commit()
                 conn.close() 
                 print(f"{Name} , thank you for registering with the Library System")
 
        except sqlite3.Error as error:
            print("Error while connecting to SQLite", error)
     
    @staticmethod    
    def authenticate(username,password):
        try:
            conn = sqlite3.connect("db.db")
            c = conn.cursor()
            c.execute(""" 
                  SELECT Id, name, Role FROM users
                  WHERE username = :uName AND password = :pass
                  """, {'uName': username, 'pass': password})
            result = c.fetchone()
            #authenticates the login by checking the credentials and comparing them to the credentials on the databse
            if not result:
                return {'IsExist' : False}
            else:
                return {'IsExist' : True , 'Id': result[0] , 'Name': result[1], 
                        'Role': result[2]}
            conn.commit()
            conn.close()
            
        except sqlite3.Error as error:
            print("Error while connecting to SQLite", error)

        
    def login():
        while True: #a loop to prevent the programme from stopping when 
             print("\nWelcome to BCU Lib System")
             username = input("Enter username: ")
             password = input("Enter your password: ")
             result = LibraryManSystem.authenticate(username, password)
             if result['IsExist'] == True:
                 print(f"Welcome {result['Name']}....")
                 if result['Role'] == 'student':
                    s = Student(result['Name'], result['Id'])
                    s.menu()
                 if result['Role'] == 'staff':
                    st = Staff(result['Name'],result['Id'])
                    st.menu()
                 if result['Role'] == 'librarian':
                    l = Librarian(result['Name'],result['Id'])
                    l.menu()
                    
             else:
                 print("Login failure")
         

bcu = LibraryManSystem()




