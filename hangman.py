from wordnik import *
import requests, string, os
class HangmanGame(object):
    def __init__(self, word):
        self.word = word
        self.partial_word = " " * len(self.word)
        self.guesses = []
        self.misses = 0
        self.complete = False
        self.won = False
        self.lost = False
        self.pending_message = "Welcome to Hangman!"
        for i, c in enumerate(self.word):
            if c in ["-", " ", "'"]:
                self.partial_word = self.partial_word[0:i] + c + self.partial_word[(i+1):len(self.partial_word)]

    def start_game(self):
        while not self.complete and not (self.won or self.lost):
            self.draw_hangman()
            if self.pending_message is not None:
                print self.pending_message
                self.pending_message = None
            user_input = raw_input("Enter a guess: ").lower()
            if self.is_valid_guess(user_input):
                try:
                    success = self.guess(user_input)
                    if success:
                        self.pending_message = "Good guess! You're a step closer to saving the hangman."
                    else:
                        self.pending_message = "Uh-oh! That guess was wrong."
                except LetterAlreadyGuessed:
                    self.pending_message = "You already guessed that letter."
        if self.won:
            self.draw_hangman()
            print "You win! Congratulations!"
        elif self.lost:
            self.draw_hangman()
            print "You lose. The correct word was '%s'." % self.word

    def is_valid_guess(self, input):
        if len(input) == 1:
            if input in string.letters:
                return True
            else:
                self.pending_message = "Please enter letters only."
                return False
        else:
            self.pending_message = "Please enter a single character."
            return False
    
    def guess(self, letter):
        is_good_guess = False
        if letter in self.guesses:
            raise LetterAlreadyGuessed()
        else:
            self.guesses.append(letter)
            for i, c in enumerate(self.word):
                if letter == c.lower():
                    is_good_guess = True
                    self.partial_word = self.partial_word[0:i] + c + self.partial_word[(i+1):len(self.partial_word)]
            is_completed = True
            for c in self.partial_word:
                if c == " ":
                    is_completed = False
            if is_completed:
                self.complete = True
                self.won = True
        if not is_good_guess:
            self.misses += 1
            if self.misses > 5:
                self.complete = True
                self.lost = True
        return is_good_guess

    def draw_hangman(self):
        os.system(["clear", "cls"][os.name == "nt"])
        print ""
        print HangmanOutput.HANGMAN[self.misses]
        print ""
        print self.partial_word.replace(" ", "_")
        print "Guesses: %s" % " ".join(self.guesses)
        print ""
    
class HangmanOutput():
    HANGMAN = [
        r"""
            ______
           |      |
           |
           |
           |
           |
           |
        ___|___
        """,
        r"""
            ______
           |      |
           |      O
           |
           |
           |
           |
        ___|___
        """,
        r"""
            ______
           |      |
           |      O
           |      |
           |
           |
           |
        ___|___
        """,
        r"""
            ______
           |      |
           |     \O
           |      |
           |
           |
           |
        ___|___
        """,
        r"""
            ______
           |      |
           |     \O/
           |      |
           |
           |
           |
        ___|___
        """,
        r"""
            ______
           |      |
           |     \O/
           |      |
           |     /
           |
           |
        ___|___
        """,
        r"""
            ______
           |      |
           |     \O/
           |      |
           |     / \
           |
           |
        ___|___
        """,
    ]

class LetterAlreadyGuessed(Exception):
    pass    

class WordGenerator(object):
    def __init__(self, api_key):
        self.api_key = api_key
        
    def random_word(self):
        r = requests.get("http://api.wordnik.com/v4/words.json/randomWord", params={'api_key': self.api_key})
        return r.json()["word"]

wordgen = WordGenerator("abe6602c297a0284440020e82c20faf152f3611c98b1db3bc")
hg = HangmanGame(wordgen.random_word())

try:
    hg.start_game()
except KeyboardInterrupt:
    print "Goodbye!"
