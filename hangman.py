import random
from user_hangman import UsersDB

class Hangman:
    def __init__(self):
        self.hangman = ' ______''\n''|      |''\n''|      *''\n''|     ***''\n''|     * *''\n''|_______'
        self.mistake = 0
        
    def __repr__(self):
        return self.hangman
        
    def handle_mistake (self):
        self.mistake += 1
        if self.mistake == 1:
            self.hangman= self.hangman.replace('*', 'O', 1)
        elif self.mistake == 2:
            self.hangman= self.hangman.replace('*', '@', 2)
            self.hangman= self.hangman.replace('@', '*', 1)
            self.hangman= self.hangman.replace('@', '|', 1)
        elif self.mistake == 3:
            self.hangman= self.hangman.replace('*', '/', 1)
        elif self.mistake == 4:
            self.hangman= self.hangman.replace('*', '\\', 1)
        elif self.mistake == 5:
            self.hangman= self.hangman.replace('*', '/', 1)
        elif self.mistake == 6:
            self.hangman= self.hangman.replace('*', '\\', 1)
        
    def is_hung(self):
        return self.mistake >= 6    
    
        
class WordPicker:
    def __init__(self):
        with open('easy_medium_words.txt', 'r') as file:
            self.list_word_easy = [word.strip() for word in file.read().splitlines() if len(word) <= 6]
        with open('easy_medium_words.txt', 'r') as file:
            self.list_word_medium = [word.strip() for word in file.read().splitlines() if len(word) > 6]
        with open('hard_words.txt', 'r') as file:
            self.list_word_hard = file.read().splitlines()
     
    @classmethod       
    def ask_difficulty(cls):
        while True:
            difficulty = input ('Select a level difficulty : Easy (E), Medium (M) or Hard (H): ').lower()
            if difficulty in ('e', 'm', 'h'):
                break
            else:
                print (f"You need to write 'E', 'M' or 'H' only")
        return difficulty
    
    def chose_word(self, difficulty):
        if difficulty == 'e':
            word = random.choice(self.list_word_easy)
        if difficulty == 'm':
            word = random.choice(self.list_word_medium)
        if difficulty == 'h':
            word = random.choice(self.list_word_hard)
        return word
    
class UserInterface:
    def __init__(self):
        self.list_letters = []
        
    def input_letter(self):
             
        while True:
            letter = input('Chose a letter : ').lower()
            if letter.isalpha() == False:
                print ('You need to write a letter')
                continue
            if len(letter) > 1:
               print ('You need to write only one letter')
               continue
            if letter in self.list_letters :
                print ('You already picked that letter, chose another one')
                continue
            break
        
        self.list_letters.append(letter)   
        return letter 
    
class Game:
    def __init__(self, word):
        self.word = word.lower()
        self.guessed_word = ['_']*len(word)
        self.hangman = Hangman()
        
    def __repr__(self):
        return ' '.join(self.guessed_word) + '\n' + str(self.hangman)
        
    def check_letter(self,letter):
        if letter.lower() in self.word:
            for idx, char in enumerate(self.word):
                if char == letter :
                    self.guessed_word[idx] = letter
                    
        else:
            self.hangman.handle_mistake()
    
    def check_win(self):
        if self.guessed_word == list(self.word):
            return True
        else:
            return False
        
    def check_hang(self):
        return self.hangman.is_hung()
        
   

        
def main():
    print ('Hello and Welcome in my Hangman Game!')
    user = UsersDB()
    user.register_or_connect()
    play = True
    while play == True:
    
        difficulty = WordPicker.ask_difficulty()
        picker = WordPicker()
        word_to_guess = picker.chose_word(difficulty)
        ui = UserInterface()
        game = Game (word_to_guess)
        print (game)
        while True:
            user_letter = ui.input_letter()        
            game.check_letter(user_letter) 
            print (game)       
            if game.check_win() == True:
                print('Congratulations you guessed the word')
                win = True
                user.add_results(win)
                break
            if game.check_hang() == True:
                print (f'You lost! The word to guess was {word_to_guess}')
                win = False
                user.add_results(win)
                break
        play_again = input ('Do you want to play again ? Y / N ').lower()
        if play_again != 'y' :
            play = False
            
        
    user.display_results()
            
        
main()
        
    
        
            
            