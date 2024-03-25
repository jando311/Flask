from flask import Flask, redirect, url_for, render_template, request, session, flash 
from datetime import timedelta 
import pandas as pd 
import sqlite3
import csv 
import random 

app = Flask (__name__)
app.secret_key = 'whipe'

def get_word ():
    conn = sqlite3.connect ('small_dictionary.db')
    cursor = conn.cursor ()
    cursor.execute ('SELECT * FROM my_table ORDER BY RANDOM() LIMIT 1')
    random_row = cursor.fetchone()
    conn.close 
    return random_row

def get_index (variable, unknown_word, random_word):
        positions = [i for i, letter in enumerate (random_word) if letter == variable]
        for position in positions:
            unknown_word[position] = variable
        return unknown_word

random_word = get_word()


@app.route('/')
def home ():
    return render_template('home.html')

@app.route ('/login', methods = ['POST', 'GET']) 
def login ():
    if request.method == 'POST':
        user = request.form ['user']
        session['user'] = user
        flash (f'You have been logged in, {user}!')
        return redirect(url_for('user'))
        
    else:
        if 'user' in session:
            flash ('You are already logged in!')
            return redirect (url_for('user'))
        
        return render_template ('login.html')

@app.route ('/dashboard')
def user ():
    return render_template ('dashboard.html')

@app.route ('/logout')
def logout ():
    if 'user' in session:
        user = session ['user']
        flash (f'You have been logged out,{user}')
    session.pop('user', None)
    return redirect (url_for ('login'))


@app.route ('/game', methods = ['POST', 'GET'])
def game ():

    if 'random_word' not in session:
        session ['random_word'] = get_word()[0]
        session ['random_definition'] = get_word()[1]

    def hangman_game_func (guess, word, random_definition):
        unknown_word = session ['unknown_word']
        tries = session ['tries']
        guessed_letters = session ['guessed_letters']    
        
        if guess in guessed_letters and len(guess) == 1:
                    flash ("You already guessed that, try again!") 
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])
                    

        if guess in word and len(guess)==1 and guess.isalpha:
                    guessed_letters.append(guess) 
                    session ['unknown_word'] = get_index (guess, unknown_word, session['random_word'])
                    if unknown_word == list (word):
                         flash ('You won, press the "New Game" Button if you want to play again!')
                    elif tries == 0:
                         flash ('You loose, press the "New Game" Button if you want to play again!')
                    else:
                        flash ("Congratulations, you found a Letter!")
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])

                     
                          
        if guess in session ['guessed_letters']:
                    flash ("You already guessed that, try again!") 
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'], value = session ['value'])

                     

        if guess != word and len(guess)==1 and guess.isalpha:
                    session ['tries'] -= 1
                    session ['value'] += 1
                    guessed_letters.append(guess)
                    flash ("No, not in the word!")
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries = session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'], value = session ['value'])

                      

        if guess != word:
                    tries -= 1
                    session ['value'] += 1
                    print ("No, not the word!")
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries = session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'], value = session ['value'])


    if 'unknown_word' not in session:
        session ['unknown_word'] = list ( len (session ['random_word'])* '_')

    if 'guessed_letters' not in session:
        session ['guessed_letters'] = []   
        
    if 'tries' not in session:
        session ['tries'] = 6 

    if 'hint_used' not in session:
        session ['hint_used'] = False
    
    if 'hint_2_used' not in session:
        session ['hint_2_used'] = False

    if 'value' not in session:
        session ['value'] = 0

    if 'result' not in session:
        session ['result'] = 'result'

    if 'uncovered_word' not in session:
        session ['uncovered_word'] = ''.join(session ['unknown_word'])

    if 'unguessed_letters' not in session:
         session ['unguessed_letters'] = [letter for letter in random_word if letter not in session ['guessed_letters']]
    print (session ['random_word'])

    if request.method =='POST':
        guess = request.form ['guess']
        hangman_game_func (guess,  session ['random_word'], session ['random_definition'])
        return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'], value = session ['value'], hint_used = session ['hint_used'], hint_2_used = session ['hint_2_used'])
      
    return render_template ('game.html', unknown_word = session ['unknown_word'])

@app.route ('/hint1', methods = ['POST', 'GET'])
def get_hint ():
     if request.method == 'POST':
        flash (session ['random_definition'])
        return redirect (url_for ('game'))
     
@app.route ('/hint2', methods = ['POST', 'GET'])
def get_hint2 ():
        
    if request.method == 'POST':
        word = session.get ('random_word', [])
        guessed_letters = session.get ('guessed_letters', [])
        unknown_word = session.get ('unknown_word')
        unguessed_letters = [letter for letter in word if letter not in guessed_letters]
 
        random_letter = random.choice (unguessed_letters)
        session ['unknown_word'] = get_index (random_letter, unknown_word, word)
        guessed_letters.append(random_letter)
        session ['guessed_letters'] = guessed_letters
        
    return redirect (url_for ('game'))

@app.route ('/endgame', methods = ['POST', 'GET'])
def endgame ():
    if request.method == 'POST': 
        random_row = get_word()
        session ['unknown_word'] = list ( len (random_row[0])* '_')
        session ['guessed_letters'] = []   
        session ['tries'] = 6 
        session ['variable'] = 'variable' 
        session ['result'] = 'result'
        session ['random_word'] = random_row[0] 
        session ['random_definition'] = random_row[1]
        session ['hint_used'] = False
        session ['hint_2_used'] = False
        session ['value'] = 0 
        return redirect (url_for ('game'))
     
if __name__ == '__main__':
    app.run(debug=True) 

