#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:25:43 2023

@author: zaneleakibo-betts
"""
import sqlite3
from datetime import datetime, timedelta
from book import Book
from libdata import LibData

class Account:
    
    def __init__(self, Id, Name, l_books_borrowed=[], l_books_reserved=[]):
        self.Id = Id
        self.Name = Name
        self.l_books_borrowed = l_books_borrowed
        self.l_books_reserved = l_books_reserved
        # self.history_return = history_return
        # self.acc_fine = acc_fine

        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()


    
    def get_l_books_borrowed(self):
        self.c.execute("""SELECT Books.isbn, Books.title FROM Books, borrow
                           WHERE borrow.BookId = Books.BookId
                           AND borrow.user_id = :Id""",{'Id': str(self.Id)})
        books = self.c.fetchall()
        if not books:
            print('You have not reserved any book yet!')
            print('')
        else:
            print('')
            print('*********************')
            print('*')
            for book in books:
                print(f"{book[0]} - {book[1]}")
            print('')
        self.conn.commit()
            
    def get_l_books_reserved(self):
        self.c.execute("""SELECT Books.isbn, Books.title FROM Books, reserve_book
                           WHERE reserve_book.isbn = Books.isbn
                           AND reserve_book.user_id = :Id""",{'Id': str(self.Id)})
        r_books = self.c.fetchall()
        if not r_books:
            print('You have not reserved any book yet!')
            print('')
        else:
            print('')
            print('*********************')
            print('*')
            
            
    def get_account_info(self):
        print(f"Account Holder: {self.Name}")
        print('')
        print('*********************')
        print('* List Of Borrowed Books *')
        print('*********************')
        self.get_l_books_borrowed()
        print('*********************')
        print('* List Of Reserved Books *')
        print('*********************')
        self.get_l_books_reserved()
