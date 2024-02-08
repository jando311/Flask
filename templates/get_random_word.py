cursor.execute ('SELECT * FROM my_table ORDER BY RANDOM () LIMIT 1')

random_row = cursor.fetchone ()

conn.close()

if random_row:
    random_word, random_definition = random_row

word = random_word
unknown_word = list (len (word)*'*')

print (unknown_word)