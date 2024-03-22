import random


# First, create array that takes in all unguessed_letters
word = ['h', 'o', 'u', 's', 'e']
unknown_word = list (len (word)*'_')
guessed_letters = ['h']
unguessed_letters = [letter for letter in word if letter not in guessed_letters]

# Second choose random letter of unguessed and replace it inside the unknown word

if unguessed_letters:
    random_letter = random.choice(unguessed_letters)
    index = word.index(random_letter)
    unknown_word[index] = random_letter
    guessed_letters.append(random_letter)

print (unknown_word)