__author__ = 'Taras'
# -*- coding: utf-8 -*-
from random import choice
from colors import bcolors
import sqlite3

class word:
    def __init__(self,path):
        self.checks = 10 #quantity of times to remember
        # creating
        self.conn = sqlite3.connect('example.db')
        try:
            self.conn.execute('''CREATE TABLE words
              (id INTEGER PRIMARY KEY       AUTOINCREMENT,
              word           VARCHAR    NOT NULL,
              translation    VARCHAR    NOT NULL,
              checks         INT        DEFAULT 0);''')
        except sqlite3.OperationalError: pass
        try:
            self.conn.execute('''CREATE TABLE player
              (id INTEGER PRIMARY KEY       AUTOINCREMENT,
              name           VARCHAR    NOT NULL,
              statistics     VARCHAR);''')
        except sqlite3.OperationalError: pass
        # End of creation
        #Start of insertion
        self.wordList = {x.rstrip().split('\t')[2].lower():x.rstrip().split('\t')[3] for x in open(path,'r')} #read all words from file
        for w,t in self.wordList.items():
            if not list(self.conn.execute("SELECT * FROM words WHERE word='"+w+"'")):
                self.conn.execute("INSERT INTO words (word,translation) VALUES (?,?)", (w,t))
        self.conn.commit()
        #End of Insertion

    def generateList(self,count):
        self.words = dict()
        for row in self.conn.execute("SELECT * FROM words WHERE checks < " + str(self.checks) +  " ORDER BY RANDOM() LIMIT "+str(count)):
            self.words.update({row[1]:row[2]})
        self.count = len(self.words)

class game:
    def __init__(self,path): #initializing game
        self.words = word(path)
    def play(self,func,count=10):
        self.words.generateList(count)
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
            self.words.conn.execute("UPDATE words SET checks = checks+1 WHERE word='"+w+"'")
            self.words.conn.commit()
        else: print(bcolors.FAIL + "Incorrect!" + bcolors.ENDC + " Correct answer: ",bcolors.OKBLUE+w+bcolors.ENDC)

    def choose(self,w,t):
        print("Word:\t\t\t" + bcolors.BOLD +  w + bcolors.ENDC)
        words = {t,}
        while len(words) < 5:
            words.update([choice(list(self.words.wordList.values()))])

        words = list(words)
        print(words)
        try:
            if t == words[int(input("Your answer:\t"))-1]:
                self.rightAnswersCount +=1 #if correct answer - increment player's result
                print(bcolors.HEADER+"Correct!"+bcolors.ENDC)
                self.words.conn.execute("UPDATE words SET checks = checks+1 WHERE word='"+w+"'")
                self.words.conn.commit()
            else: print(bcolors.FAIL + "Incorrect!" + bcolors.ENDC + " Correct answer: ",bcolors.OKBLUE+t+bcolors.ENDC)
        except: print(bcolors.FAIL + "Incorrect!" + bcolors.ENDC + " Correct answer: ",bcolors.OKBLUE+t+bcolors.ENDC)

class player:
    def __init__(self,name):
        self.name = name
        self.statistics = []
        game.words.conn.execute("INSERT INTO player (name) VALUES ('"+name+"')")
        self.id = next(game.words.conn.execute("SELECT last_insert_rowid() FROM player"))[0]
        game.words.conn.commit()
    def start(self,mode):
        print("-"*5,"Start","-"*5)
        game.play(mode)
    def end(self):
        self.statistics +=[game.rightAnswersCount*100/game.words.count,]
        game.words.conn.execute("UPDATE player SET statistics = '"+str(self.statistics)+"' WHERE id='"+str(self.id)+"'")
        game.words.conn.commit()
        print("-"*5,"End","-"*5)
    def showStatistics(self):
        print("Full statistics: ",self.statistics)
        print("Average: ", sum(self.statistics)/len(self.statistics))
        print("Max: ", max(self.statistics))
        print("Min: ", min(self.statistics))

if __name__ == '__main__':
    game = game('test.tsv')
    player = player(input("Enter your name: "))
    while 1:
        mode = str(input("Enter your mode (print/choose): "))
        try: player.start(mode)
        except: print(bcolors.FAIL+"Wrong mode name!"+bcolors.ENDC)
        player.end()
        if not bool(int(input("Try again? (0/1): "))): break
    print('*'*10,"Game over",'*'*10)
    print("Thank tou for playing. Your statistics' below")
    player.showStatistics()