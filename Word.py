__author__ = 'Taras'
# -*- coding: utf-8 -*-
from random import choice
from colors import bcolors

class word:
    def __init__(self,path):
        self.wordList = {x.rstrip().split('\t')[2].lower():x.rstrip().split('\t')[3] for x in open(path,'r')} #read all words from file
    def generateList(self,count):
        self.count = count
        self.words = set()
        while len(self.words) < self.count: #choosing right quantity of words
            self.words.update([choice(list(self.wordList))]) #avoiding repeats
        self.words = {x:self.wordList.get(x) for x in self.words} #making dictionary

class game:
    def __init__(self,path,count=10): #initializing game
        self.words = word(path)
        self.words.generateList(count)
    def play(self,func):
        self.rightAnswersCount=0
        for w,t in self.words.words.items():
            f = getattr(self,func)
            f(w,t)
        print("Your result is: ",int(self.rightAnswersCount*100/self.words.count), "%")
    def print(self,w,t):
        print("Word:\t\t\t" + t)
        if w == str(input("Your answer:\t")):
            self.rightAnswersCount +=1 #if correct answer - increment player's result
            print(bcolors.HEADER+"Correct!"+bcolors.ENDC)
        else: print(bcolors.FAIL + "Incorrect!" + bcolors.ENDC + " Correct answer: ",bcolors.OKBLUE+w+bcolors.ENDC)

    def choose(self,w,t):
        print("Word:\t\t\t" + bcolors.BOLD +  w + bcolors.ENDC)
        words = {t,}
        while len(words) < 5:
            words.update([choice(list(self.words.wordList.values()))])
        words = list(words)
        print(words)
        try:
            if t == words[int(input("Your answer: "))+1]:
                self.rightAnswersCount +=1 #if correct answer - increment player's result
                print(bcolors.HEADER+"Correct!"+bcolors.ENDC)
            else: print(bcolors.FAIL + "Incorrect!" + bcolors.ENDC + " Correct answer: ",bcolors.OKBLUE+t+bcolors.ENDC)
        except: print(bcolors.FAIL + "Incorrect!" + bcolors.ENDC + " Correct answer: ",bcolors.OKBLUE+t+bcolors.ENDC)

class player:
    def __init__(self,name):
        self.name = name
    def start(self):
        print("-"*5,"Start","-"*5)
        game.print()
    def end(self):
        print("-"*5,"End","-"*5)

if __name__ == '__main__':
    game = game('test.tsv')
    game.play("choose")