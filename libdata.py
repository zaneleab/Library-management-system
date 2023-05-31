#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:19:22 2023

@author: zaneleakibo-betts
"""
from datetime import datetime, timedelta
from book import Book
import sqlite3

class LibData:
    def __init__(self, list_of_books):
        self.list_of_books = list_of_books
       
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()
        
        #creates table in sqlite database
        #c.execute("""CREATE TABLE IF NOT EXISTS  Books(
            #isbn text PRIMARY KEY,
            #title text,
            #author text,
            #language text,
            #available integer
            #)""")
            
        #creates table in sqlite database
        #c.execute("""CREATE TABLE IF NOT EXISTS  borrow(
            #isbn text ,
            #Id integer,
            #BookId integer PRIMARY KEY,
            #date text,
            #FOREIGN KEY (Id) REFERENCES Users(Id),
            #FOREIGN KEY (BookId) REFERENCES Books(Id)
            #)""")
            
        #c.execute("""CREATE TABLE Users(
            #Id integer PRIMARY KEY,
            #Name text,
            #Surname text,
            #Username,
            #Password,
            #Role text
            #)""")
        
        
        # self.c.execute("""CREATE TABLE reserve_book (
        #         Id INTEGER PRIMARY KEY AUTOINCREMENT,
        #         isbn TEXT,
        #         user_id INTEGER,
        #         reserve_time DATETIME,
        #         FOREIGN KEY(isbn) REFERENCES Books(isbn),
        #         FOREIGN KEY(user_id) REFERENCES Users(Id)
        #         )""")
        # self.conn.commit()
        
        #creates table in sqlite database
        #
        #self.conn.close()
       
    def updateAvailability(number, isbn):
        try:
            conn = sqlite3.connect('db.db')
            c = conn.cursor()
            c.execute(""" 
                          update books set
                          available = :nava
                          where isbn = :isbn
                          """ , {'nava' : number, 'isbn':str(isbn)})
        except sqlite3.Error as e:
            print("An error occurred:", e)
            
    def addBook (self,b):
        self.c.execute(""" insert into Books(isbn,title,author, language, available)
        values(:isbn,:title,:author, :language, :available)              
        """,{'isbn': b.isbn, 'title':b.title, 'author' :b.authors,'language' :b.language,'available': b.available })
        
        self.conn.commit()
        
        print(f"The book {b.title} has been sucesfully added")
    
    def deleteBook(self,b): #? not deleting books yet
        
        
        self.c.execute("""DELETE from Books WHERE isbn=:isbn
                  """,
                      {'isbn':b.isbn}) 
        self.conn.commit()
        print(f"The book {b.isbn} has been sucesfully deleted")
        
                                  
        #self.updateAvailibility(b)
                          
    @staticmethod
    def searchBook(data):
            conn = sqlite3.connect("db.db")
            c = conn.cursor()
            data = '%'+data+'%'
            c.execute(""" 
                      select title,author,isbn from Books
                      where title like :d
                      or author like :d
                      or ISBN like :d
                      or language like :d
                    
                      """,{'d':data})
            result = c.fetchall() 
            print('ISBN - Title - Authors')
            i = 1
            for book in result:
                print(f"{i} - {book[2]} - {book[0]} - {book[1]}")
                i = i +1
                
        

   
            
        
    
    
        
