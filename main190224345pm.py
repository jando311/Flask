from flask import Flask, redirect, url_for, render_template, request, session, flash 
from datetime import timedelta 
import pandas as pd 
import sqlite3
import csv 

app = Flask (__name__)
app.secret_key = 'whipe'

random_word = None
random_definition = None 

conn = sqlite3.connect('dictionary.db')
cursor = conn.cursor ()

cursor.execute ('SELECT * FROM my_table ORDER BY RANDOM() LIMIT 1')
random_row = cursor.fetchone()

conn.close 

if random_row:
    random_word, random_definition = random_row 

     
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

    def get_index (variable, unknown_word):
        positions = [i for i, letter in enumerate (random_word) if letter == variable]
        for position in positions:
            unknown_word[position] = variable
        print (unknown_word)
        return unknown_word
         

    def hangman_game_func (guess, random_word):
        print (random_word)
        print (guess)
        unknown_word = session ['unknown_word']
        tries = session ['tries']
        guessed_letters = session ['guessed_letters']


        print (tries)
        print (unknown_word) 
            
        if guess in guessed_letters and len(guess) == 1:
                    flash ("You already guessed that, try again!") 
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])
                    

        if guess in random_word and len(guess)==1 and guess.isalpha:
                    guessed_letters.append(guess) 
                    session ['unknown_word'] = get_index (guess, unknown_word)
                    if unknown_word == list (random_word):
                         flash ('You won, press the "New Game" Button if you want to play again!')
                    elif tries == 0:
                         flash ('You loose, press the "New Game" Button if you want to play again!')
                    else:
                        flash ("Congratulations, you found a Letter!")
                    print (unknown_word)
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])

           
            
        if guess in session ['guessed_letters']:
                    flash ("You already guessed that, try again!") 
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])

                     

        if guess != random_word and len(guess)==1 and guess.isalpha:
                    session ['tries'] -= 1
                    guessed_letters.append(guess)
                    flash ("No, not in the word!")
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])

                      

        if guess != random_word:
                    tries -= 1
                    print ("No, not the word!")
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])
        


                  


    
    if 'unknown_word' not in session:
        session ['unknown_word'] = list ( len (random_word)* '_')

    if 'guessed_letters' not in session:
        session ['guessed_letters'] = []   
    
    if 'tries' not in session:
        session ['tries'] = 6 

    if 'hint_used' not in session:
        session ['hint_used'] = 'hint_used'
    
    if 'hint_2_used' not in session:
        session ['hint_used'] = 'hint_2_used'

    if 'variable' not in session:
        session ['variable'] = 'variable'

    if 'result' not in session:
        session ['result'] = 'result'

    if request.method =='POST':
        guess = request.form ['guess']
        hangman_game_func (guess, random_word)
        return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])
  

    return render_template ('game.html', unknown_word = session ['unknown_word'])


@app.route ('/endgame', methods = ['POST'])
def endgame ():
    if request.method == 'POST':
        session ['unknown_word'] = list ( len (random_word)* '_')
        session ['guessed_letters'] = []   
        session ['tries'] = 6 
        session ['variable'] = 'variable'
        session ['result'] = 'result'
        return redirect (url_for ('game'))
     
if __name__ == '__main__':
    app.run(debug=True) 

