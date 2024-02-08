import pandas as pd 
import sqlite3
import csv

csv_file = 'clean_dictionary.csv'

conn = sqlite3.connect ('dictionary.db')
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
    
cursor.execute ('SELECT * FROM my_table ORDER BY RANDOM () LIMIT 1')

random_row = cursor.fetchone ()

conn.close()

if random_row:
    random_word, random_definition = random_row

word = random_word
unknown_word = list (len (word)*'*')

print (unknown_word)




