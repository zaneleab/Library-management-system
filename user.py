#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 23:57:29 2023

@author: zaneleakibo-betts
"""
import sqlite3
from datetime import datetime
#from libdata import LibData
from book import Book
from libdata import LibData
from account import Account


class User:
    def __init__(self,Name, Id):
        self.Name = Name
        self.Id = Id
        
        self.libdata = LibData([]) #creates an instance of LibData
        

        
    def __repr__(self):
        return f"{self.Name}{self.Id}"
    

    
    def returnBook (self):
        isbn = input('Please enter isbn: ')
        Book.returnBook(isbn, self.Id)
        
    
    def fine_Amount(self):
        isbn = input('Please enter isbn: ') 
        Book.fine_Amount(self.Id, isbn)  # call the fine_Amount() method on the book instance

        
    def reserveBook (self):
        isbn = input('Please enter isbn: ') 
        Book.reserveBook(isbn, self.Id) 
    
    def searchBook(self):
        data = input('Please enter search data: ')
        self.libdata.searchBook(data) #calls the searchBook() method in LibData
    
    
    def borrowBook(self):
        isbn = input('Please enter isbn: ')
        BookId = Book.getBookIdByIsbn(isbn)
        date = datetime.now().strftime('%Y-%m-%d %H:%M')
        Book.borrowBook(isbn, BookId, self.Id, date)
        
    def get_account_info(self):
         account = Account(self.Id, self.Name)
         account.get_account_info()
    
    def getBorrowedBook(self):
        

        conn = sqlite3.connect("db.db")
        c = conn.cursor()
        
        c.execute(""" 
                  select Books.isbn, Books.title from Books, borrow
                  where borrow.BookId = Books.BookId
                  and borrow.user_id = :Id
                  """,{'Id': str(self.Id)})
                  
        books = c.fetchall()
        
        if not books:
            print('You have not borrowed any book yet!')
            print('')
        else:   
            print('')
            print('*********************')
            print('* List Of Borowed Book*')
            print('*********************')
            for book in books:
                print(f"{book[0]} - {book[1]}")
            print('')
        
        conn.commit()
        conn.close()   
        
        
class Student(User):
    def __init__(self, Name, Id):
        super().__init__(Name, Id)
        
        
    def menu(self):
        
            while True:
                print("""
                  1. List Of the borrowed Books
                  2. Borrow a Book
                  3. Return a Book
                  4. Check Fine
                  5. Reserve Book
                  6. Search
                  7.Account
                  q. quit
                  """)
                choice = input("\nselect your choice: ")
                f = {
                "1": self.getBorrowedBook,
                "2": self.borrowBook,
                "3": self.returnBook,
                "4": self.fine_Amount,
                "5": self.reserveBook,
                "6": self.searchBook,
                "7": self.get_account_info,
                "q": 'q'}.get(choice,None)
                if f == 'q':
                    break
                if f == None:
                    print("Error, Try Again..")

                else:
                    f()
                    
class Staff(User):
    def __init__(self, name, uid):
            super().__init__(name, uid)
           
            
    def menu(self):
        
            while True:
                print("""
                  1. List Of the borrowed Books
                  2. Borrow a Book
                  3. Return a Book
                  4. Check Fine
                  5. Reserve Book
                  6. Search
                  q. quit
                  """)
                choice = input("\nselect your choice: ")
                f = {
                "1": self.getBorrowedBook,
                "2": self.borrowBook,
                "3": self.returnBook,
                "4": self.fine_Amount,
                "5": self.reserveBook,
                "6": self.searchBook,
                "q": 'q'}.get(choice,None)
                if f == 'q':
                    break
                if f == None:
                    print("Error, Try Again..")

                else:
                    f()
   
  