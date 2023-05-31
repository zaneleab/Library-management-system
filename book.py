#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:12:29 2023

@author: zaneleakibo-betts
"""


from datetime import datetime, timedelta
import sqlite3
class Book:
    def __init__(self,isbn,title,author,language_code,available=3,):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.language_code = language_code
        self.available = available
        
        self.conn = sqlite3.connect('db.db')
        self.c = self.conn.cursor()

    def __repr__(self): 
        return f"{self.isbn} {self.title}, {self.author}, {self.language_code}{self.available}"
    
    
    import json
    #reads json file
    #def loadBooks():
        #with open('books.json',  encoding="utf-8") as fd:
            #books= json.load(fd)
            #for b in books:
                #print(b)
                #nb= Book(b['isbn'],b["title"],b["authors"], b["language_code"])
                
                #insertBook(nb)
    #inserts books into database table            
    #def insertBook(b):
        #print(b)    
        #with conn:
            #c.execute("INSERT INTO books VALUES(:isbn,:title,:authors,:language,:available)",{'isbn':b.isbn,'title':b.title,'authors':b.author, 'language': b.language_code, 'available':b.available})
    
    @staticmethod           
    def returnBook(isbn, Id):
        try:
            ava = Book.checkAvailability(isbn)
            conn = sqlite3.connect('db.db')
            c = conn.cursor()
            c.execute(""" 
                UPDATE books 
                SET available = :nava 
                WHERE isbn = :isbn
            """, {'nava': ava + 1, 'isbn': isbn})
            conn.commit()
            #Book.updateAvailability(ava+1,isbn)
            c.execute("""
                DELETE FROM borrow 
                WHERE isbn = :isbn 
                AND id IN (SELECT id FROM borrow WHERE isbn = :isbn)
            """, {'isbn': isbn})
           # # Add returned book to book_history table
           #  date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
           #  c.execute("""
           #  INSERT INTO book_history(isbn, user_id, BookId, date) 
           #  SELECT isbn, user_id, BookId, :date
           #  FROM borrow
           #  WHERE isbn = :isbn AND user_id = :user_id
           #  """, {'isbn': isbn, 'user_id': user_id, 'date': date})
           
            conn.commit()
            print('Book has been returned')
        except sqlite3.Error as e:
            print("An error occurred:", e)
    
    
    def checkAvailability(isbn):
        try:
            conn = sqlite3.connect("db.db")
            c = conn.cursor()
    
            c.execute("""
                  select available from Books
                  where isbn = :isbn        
                  """,{'isbn':str(isbn)})
    
            result = c.fetchone()
            if result is not None:
                ava = result[0]
            else:
                ava = 0
            conn.commit()
            return ava
        except sqlite3.Error as e:
            print("An error occurred:", e)
        


  
    def updateAvailability(number, isbn):
        try:
            conn = sqlite3.connect('db.db')
            c = conn.cursor()
            c.execute(""" 
                          update books set
                          available = :nava
                          where isbn = :isbn
                          """ , {'nava' : number, 'isbn':str(isbn)})
            conn.commit()
            print(f"Availability for ISBN {isbn} updated to {number}.")
        except sqlite3.Error as e:
            print("An error occurred:", e)
        
   
    @staticmethod
    def borrowBook(isbn, BookId, user_id, date):
        try:
            #book = Book(isbn, title=None, author=None, language_code=None)
            ava = Book.checkAvailability(isbn)
            if ava > 0:
                conn = sqlite3.connect('db.db')
                c = conn.cursor()
                c.execute("""
                          insert into borrow(isbn, BookId,user_id, date)
                          values(:isbn, :BookId, :user_id, :date)              
                          """,{'isbn': isbn,'BookId': str(BookId), 'user_id': str(user_id),'date': date })
    
                
                c.execute("""
                          UPDATE Books
                          SET available = :available
                          WHERE isbn = :isbn
                          """, {'available': ava - 1, 'isbn': isbn})
                conn.commit()
            
                print(f"ISBN {isbn} is borrowed by you")
            else:
                print('The book is not available')
        except sqlite3.Error as e:
             print("An error occurred:", e)       

    @staticmethod
    def getBookIdByIsbn(isbn):
        try:
            import sqlite3
            conn = sqlite3.connect("db.db")
            c = conn.cursor()
            c.execute("""
                      select BookId from Books
                      where isbn = :is          
                      """,{'is':isbn})
            result = c.fetchone()
            
            conn.commit()
            conn.close()
            return result[0]
        except sqlite3.Error as e:
             print("An error occurred:", e) 
                
            
        
    @staticmethod
    def fine_Amount(Id, isbn):
        try:
            conn = sqlite3.connect("db.db")
            c = conn.cursor()
    
            c.execute(""" SELECT COUNT(*) FROM borrow
                      WHERE isbn=:isbn""", {'isbn':isbn})
            count = c.fetchone()[0]
    
            if count == 0:
                print('The user has not borrowed this book.')
                return 0
    
        # Get the latest date the book was borrowed
            c.execute(""" SELECT date FROM borrow
                      WHERE isbn=:isbn
                      ORDER BY date DESC
                      LIMIT 1""", {'isbn':isbn})
            borrow_date_str = c.fetchone()[0]
            borrow_date = datetime.strptime(borrow_date_str, '%Y-%m-%d %H:%M')
    
        
            # Calculate the fine amount
            daysOverdue = (datetime.now() - borrow_date).days
            fineAmount = 0
            if daysOverdue > 7:
                fineAmount = max(daysOverdue - 7, 0) * 1 # £1 per day
    
            if fineAmount > 0:
                print(f"The book is {daysOverdue} days overdue. \n The fine amount is £{fineAmount}.")
    
            conn.commit()
            conn.close()
    
            return fineAmount
        except sqlite3.Error as e:
         print("An error occurred:", e) 
    
    @staticmethod
    def reserveBook(isbn, user_id):
        try:
        # Check if the book is available
            ava = Book.checkAvailability(isbn)
            if ava > 0:
                # Calculate the return time for the reservation
                return_time = datetime.now() + timedelta(hours=4)
    
                # Reserve the book
                conn = sqlite3.connect('db.db')
                c = conn.cursor()
                c.execute("""
                          INSERT INTO reserve_book(isbn, user_id, return_time)
                          VALUES (:isbn, :user_id, :return_time)
                          """, {'isbn': str(isbn), 'user_id': user_id, 'return_time': return_time})
                conn.commit()
    
                # Update the availability of the book
                Book.updateAvailability(ava - 1, isbn)
    
                print(f"ISBN {isbn} is reserved for 4 hours by you")
                print(f"Please make sure to borrow the book before {return_time.strftime('%Y-%m-%d %H:%M:%S')}")
            else:
                print('The book is not available')
                
        except sqlite3.Error as e:
          print("An error occurred:", e) 

    
    #loadBooks()
            
    
        