import pandas as pd 
import sqlite3
import csv

csv_file = 'clean_dictionary.csv'

conn = sqlite3.connect ('small_dictionary.db')
cursor = conn.cursor ()

cursor.execute ('''CREATE TABLE IF NOT EXISTS my_table (
                column1 WORD,
                column2 DEFINITION
                )''')

with open (csv_file, 'r', newline = '', encoding = 'utf-8') as file: 
    csv_reader = csv.reader(file)
    next(csv_reader)
    for row in csv_reader:
        cursor.execute('INSERT INTO my_table VALUES (?,?)', row)

conn.commit()
conn.close() 







