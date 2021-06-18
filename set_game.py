#list of 81 3-tuples 
from random import sample
from random import choice
from random import randint
import itertools

class Card:

    def __init__(self, color, number, fill, shape):
        self.color = color
        self.fill = fill
        self.number = number
        self.shape = shape
        
        self.image = self.get_image_string()
        
    

    def __str__(self):
        return str((self.color,self.fill,self.number, self.shape))
    def as_tuple(self):
        return (self.color,self.number,self.fill, self.shape)

    def get_image_string(self):
        return f'{self.color[0]}{self.number}{self.fill[0]}{self.shape[0]}'
    



class GameState:

    
    
    
    def __init__(self):
        self.board = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.sets = []
    def _get_dozen_random_cards(self) -> set:
        possible_colors = {'green', 'red', 'purple'}
        possible_fills = {'empty','lined', 'solid'}
        possible_numbers = {1,2,3}
        possible_shapes = {'oval', 'diamond', 'squiggle'}
        atts = (possible_colors,  possible_numbers,possible_fills, possible_shapes)
        possible_cards = set(itertools.product(*atts))
        
        cards = set(sample(possible_cards, k = 12))
        return cards

    def _is_set(self,card1,card2,card3):
        colors = (card1[0], card2[0], card3[0])
        fills = (card1[1], card2[1],card3[1])
        numbers = (card1[2], card2[2], card3[2])
        shapes = (card1[3], card2[3], card3[3])
        atts = (colors,fills,shapes,numbers)
        
        if all(self._all_same(att) or self._all_different(att) for att in atts):
            self.sets.append({card1,card2,card3})
            
            return True
        return False
    def _all_same(self,atts):
        return atts[0] == atts[1] == atts[2]

    def _all_different(self,atts):
        return len({atts[0] , atts[1] , atts[2]}) == 3

    def _get_valid_dozen(self):
        while True:
            new_cards = self._get_dozen_random_cards()
            
            new_combs = set(itertools.combinations(new_cards, 3))
            sets = sum([self._is_set(a1,a2,a3) for a1,a2,a3 in new_combs])
            if sets == 6 and len(set(new_cards)) == 12:
                self.sets = self.sets[-6:]
                return new_cards
            
          
    def create_board(self):
        cards = self._get_valid_dozen()
        cards = list(cards)
        rows = len(self.board)
        cols = len(self.board[0])
        for r in range(0,rows):
            for c in range(0,cols):
                rand = randint(0,len(cards)-1)
                new_card = Card(*cards[rand])
                self.board[r][c] = new_card
                del cards[rand]
                

    
    def get_board(self):
        return self.board

    def get_image_addresses(self):
        rows = len(self.board)
        cols = len(self.board[0])
        addresses = []
        for r in range(0,rows):
            for c in range(0,cols):
                addresses.append(self.board[r][c].get_image_string())
        return addresses

    def board_as_tuples(self):
        rows = len(self.board)
        cols = len(self.board[0])
        s = set()
        for r in range(0,rows):
            for c in range(0,cols):
                s.add(self.board[r][c].as_tuple())
        print(s)

    def get_sets(self):
        return self.sets
        
        

        
        
