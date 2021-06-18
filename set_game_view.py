import tkinter
from set_game import Card
from set_game import GameState
from tkinter import PhotoImage
import time
BASE = 'assets/'
EXT = '.png'
class SetGameView:

    def __init__(self):
        self.highscore = ''
        highscore_file = open(BASE+'highscore.txt')
        
        
        if len(line:=highscore_file.readline())!=0:
            self.highscore = line
            
        self._root_window = tkinter.Tk()
        self._root_window.title(f'Set Game - Highscore: {round(float(self.highscore),2)}')
        self.start = time.time()
        game = GameState()
        game.create_board()
        self.board = game.get_board()
        self.score = 0
        self.chosen = []
        self.buttons = []
        self.found = []
        self.sets = game.get_sets()
        self._reset_button = None
        images = game.get_image_addresses()
        self.photos = []
        for i in images:
            self.photos.append(PhotoImage(file = (self._get_image_address(i))))
        
        self._label = tkinter.Label(master = self._root_window, text = ""
                                    ,font=("Menlo", 25))
        self._label.grid(row = 4, column = 0, columnspan = 3, padx = 10,
                         pady = 10,sticky = tkinter.W + tkinter.E )
        self._score_label = tkinter.Label(master = self._root_window, text = 'Count'
                                    ,font=("Menlo", 25))
        self._score_label.grid(row = 4, column = 3,  padx = 10,
                         pady = 10,sticky = tkinter.E  )
        self._score_label['text'] = f'Count: {self.score}'
        self._card1 = self._create_button(0,0,0)
        self._card2 = self._create_button(0,1,1)       
        self._card3 = self._create_button(0,2,2)
        self._card4 = self._create_button(0,3,3)
        self._card5 = self._create_button(1,0,4)
        self._card6 = self._create_button(1,1,5)
        self._card7 = self._create_button(1,2,6)
        self._card8 = self._create_button(1,3,7)
        self._card9 = self._create_button(2,0,8)
        self._card10 = self._create_button(2,1,9)
        self._card11= self._create_button(2,2,10)
        self._card12 = self._create_button(2,3,11)  
        self._root_window.rowconfigure(0, weight = 1)
        self._root_window.columnconfigure(0, weight =1)
        self._root_window.rowconfigure(1, weight = 1)
        self._root_window.columnconfigure(1, weight =1)
        self._root_window.rowconfigure(2, weight = 1)
        self._root_window.columnconfigure(2, weight =1)
        self._root_window.columnconfigure(3, weight =1)
        self._root_window.rowconfigure(4, weight = 1)
        
    def _get_image_address(self, string):
        return BASE + string + EXT
    
    def _create_button(self, row, col, number):
        button = tkinter.Button(
            master = self._root_window, image = self.photos[number]
            )
        button.configure(command = self._create_button_command(button, row,col))
        button.grid(
            row = row, column = col, padx = 10, pady = 10,
            sticky = tkinter.W + tkinter.E + tkinter.S+tkinter.N)
        button.photo = self.photos[number]
        button['highlightbackground'] = "#FFFFFF"
        self.buttons.append(button)
        return button
    
    def _create_button_command(self, button, row, col):
        def command():
            
            if self.board[row][col] not in self.chosen:
            
                self.chosen.append(self.board[row][col])
              
                button['highlightbackground'] = "#4287f5"
                self._label['text'] = ''
                
                if len(self.chosen) == 3:
                    button['highlightbackground'] = "#4287f5"
                    
                    check_set = set([card.as_tuple() for card in self.chosen])
                    if check_set in self.sets:
                        
                        self._update_score()
                        word = 'set' if self.score == 1 else 'sets'
                        if self.score != 1:
                            self._label['text'] = f'Great! {self.score} {word} found!'
                        self.sets.remove(check_set)
                        self.found.append(check_set)
                        
                    elif check_set in self.found:
                        self._label['text'] = f'You already found this set!'
                    else:
                        self._label['text'] = 'Not a set!'
                    
                    
                    self._unchoose_all()
                    self.chosen = []
                         
            else:
                button['highlightbackground'] = "#FFFFFF"
                self.chosen.remove(self.board[row][col])
                
        return command

    def _unchoose_all(self):
        for button in self.buttons:
            button['highlightbackground'] = "#FFFFFF"
    def _update_score(self):
        self.score += 1
        self._score_label['text'] = f'Count: {self.score}'
        if self.score == 1:
            self._game_over(time = time.time() - self.start)

    def _game_over(self, time):
        self._label['text'] = f'You took {round(time, 2)} seconds to complete this puzzle'
        if self.highscore == '':
           self._set_high(time)
        elif time < float(self.highscore) :
            self._set_high(time)
        
        self._create_reset_button()

    def _set_high(self, time):
        file = open(BASE+'highscore.txt','w')
        file.write(str(time))
        

    def _create_reset_button(self):
        
        def reset():
            self._root_window.destroy()
            new = SetGameView()
            new.run()
        button = tkinter.Button(master= self._root_window,
                                text = 'Play Again!', font = 'menlo', command = reset)

        self._reset_button = button
        self._reset_button.grid(row = 4, column = 2,padx = 10,
                         pady = 10,sticky = tkinter.E  )
        
    def run(self) -> None:
        self._root_window.mainloop()
               
if __name__ == '__main__':
    SetGameView().run()
