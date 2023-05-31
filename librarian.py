#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 14 12:37:38 2023

@author: zaneleakibo-betts
"""

from libdata import LibData
from user import User
from book import Book

class Librarian(User):
    def __init__(self, name, uid):
            super().__init__(name, uid)
            self.libdata = LibData([])
            
    

    def updateAvailability(isbn,number): 
        try:
            number = input('Enter the number of available books ')
            isbn = input('Enter book isbn ')
            Book.updateAvailability(number, isbn)
        except ValueError:
            print('Error: Invalid input. Number of available books must be a number.')
 
    def addBook(self,b):
        try:
            b.isbn = input('Please enter book isbn')
            b.title = input('Please enter book title: ')
            b.authors = input('Please enter book authors: ')
            b.language = input('Please enter book language ')
            b.available = input('Please enter number of available books: ')
            self.libdata.addBook(b)
        except ValueError:
            print('Error: Invalid input. Number of available books must be a number.')

    
    def searchBook(self):
        data = input('Please enter search data: ')
        self.libdata.searchBook(data)
    
    def deleteBook(self,b):
        b.isbn = input('Please enter isbn: ')
        self.libdata.deleteBook(b)
        
        

    
    def menu(self):
          while True:
              print("""
                1. Add Book
                2. Delete Book
                3. Search 
                4. Update Availability
                q. quit
                """)
              choice = input("\nselect your choice: ")
              f = {
              "1": self.addBook,
              "2": self.deleteBook,
              "3": self.searchBook,
              "4": self.updateAvailability,
              "q": 'q'}.get(choice,None)
              if f == 'q':
                  break
              if f == None:
                  print("Error, Try Again..")

              else:
                 f(self)

    