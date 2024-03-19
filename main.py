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

random_word = get_word()

def get_hint (new_definition):
    print ('Your hint is:', new_definition)

def get_hint_2 (unknown_word):
     indexes_word = [i for i, value in enumerate (unknown_word) if value == '_']
     random_index = random.choice (indexes_word)
     


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
        print (session ['random_word'])
     
    def get_index (variable, unknown_word, random_word):
        positions = [i for i, letter in enumerate (random_word) if letter == variable]
        for position in positions:
            unknown_word[position] = variable
        return unknown_word

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
        session ['hint_used'] = 'hint_used'
    
    if 'hint_2_used' not in session:
        session ['hint_used'] = 'hint_2_used'

    if 'value' not in session:
        session ['value'] = 0

    if 'result' not in session:
        session ['result'] = 'result'

    print (session ['random_word'])

    if request.method =='POST':
        guess = request.form ['guess']
        hangman_game_func (guess,  session ['random_word'], session ['random_definition'])
        return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'], value = session ['value'])
      
    return render_template ('game.html', unknown_word = session ['unknown_word'])

@app.route ('/hints', methods = ['POST', 'GET'])
def get_hint ():
     if request.method == 'POST':
        session ['random_word'] = get_word()[0]
        session ['random_definition'] = get_word()[1]
        flash (session ['random_definition'])
        return render_template ('game.html')

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

