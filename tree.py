from collections import deque
import copy

class GameStateNode:

    def __init__(self,board_state,dice_left,bets_left,money):
        self.board_state = board_state
        self.dice_left = dice_left
        self.bets_left = bets_left
        self.bets_made = bets_made
        self.money = money


    def is_complete(self):
        #more to figure out with this
        if sum(self.board_state[17])>0:
            return True
        return False

    def expand(self):

        children = []

        #bet

        #need to make sure to remove the key once all bets used
        for possible_bet in self.bets_left:
            new_bets_left = self.bets_left[possible_bet].pop()
            new_bets_made = self.bets_made.copy()
            new_bets_made = self.bets_made[]





        #roll



        return children

#class DiceRoller:


if __name__ == "__main__":

    board_state = {i+1:tuple(0 for i in range(25)) for i in range(17)}
    bets_left = {1:(5,3,2),2:(5,3,2),3:(5,3,2),4:(5,3,2),5:(5,3,2)}
    bets_made = {}
    dice_left = set([1,2,3,4,5])
    money = 0
    print(board_state)

    # curr = GameStateNode({1:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),2:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)})

    # print(curr.game_state)

# B G O W R
# 0 0 0 0 0
# 0 0 0 0 0
# 0 0 1 0 0
# 0 1 0 0 0
# 1 0 0 0 0
