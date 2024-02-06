from flask import Flask, redirect, url_for, render_template, request, session, flash 
from datetime import timedelta 
import random

app = Flask (__name__)
app.secret_key = 'whipe'

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
        positions = [i for i, letter in enumerate (unknown_word) if letter == variable]
        for position in positions:
            unknown_word[position] = variable  

    def hangman_game_func (guess, word):
        print (word)
        print (guess)
        unknown_word = session ['unknown_word']
        tries = session ['tries']
        guessed_letters = session ['guessed_letters']


        if unknown_word == list (word) or guess == word:
            flash ('You have won! Congratulations!')
            
        elif tries == 0:
            flash ('You are out of tries! Game over!')
        
        else:
            print (tries)
            print (unknown_word) 
            
            if guess in guessed_letters and len(guess) == 1:
                    flash ("You already guessed that, try again!") 
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])
                    

            if guess in word and len(guess)==1 and guess.isalpha:
                    guessed_letters.append(guess) 
                    flash ("Congratulations, you found a Letter!")
                    get_index (guess, unknown_word)
                    session ['unknown_word'] = unknown_word
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])

                    
            
            if guess in session ['guessed_letters']:
                    flash ("You already guessed that, try again!") 
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])

                     

            if guess != word and len(guess)==1 and guess.isalpha:
                    session ['tries'] -= 1
                    guessed_letters.append(guess)
                    flash ("No, not in the word!")
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])

                      

            if guess != word:
                    tries -= 1
                    print ("No, not the word!")
                    return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])
        


                  

    word = 'House'
    
    if 'unknown_list' not in session:
        session ['unknown_word'] = list ( len (word)* '_')

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
        hangman_game_func (guess, word)
        return render_template ('game.html', guessed_letters = session ['guessed_letters'], tries=session ['tries'], unknown_word = session ['unknown_word'], result = session ['result'])
  

    return render_template ('game.html', unknown_word = session ['unknown_word'])


@app.route ('/endgame', methods = ['POST', 'GET'])
def endgame ():
    if request.method == 'POST':
        word = 'House'
        session ['unknown_word'] = list ( len (word)* '_')
        session ['guessed_letters'] = []   
        session ['tries'] = 6 
        session ['variable'] = 'variable'
        session ['result'] = 'result'
        return redirect (url_for ('game'))
     
if __name__ == '__main__':
    app.run(debug=True) 

