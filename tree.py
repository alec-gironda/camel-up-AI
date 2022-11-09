from collections import deque

class GameStateNode:

    def __init__(self, board_state,dice_left,bets_left):
        self.board_state = board_state
        self.dice_left = dice_left
        self.bets_left = bets_left
        self.bets_made =


    def is_complete(self):
        #more to figure out with this
        if sum(self.board_state[17])>0:
            return True
        return False

    def expand(self):


        return children

#class DiceRoller:


if __name__ == "__main__":

    bets_left = {1:(5,3,2),2:(5,3,2),3:(5,3,2),4:(5,3,2),5:(5,3,2)}
    bets_made = {}

    curr = GameStateNode({1:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),2:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)})

    print(curr.game_state)

# B G O W R
# 0 0 0 0 0
# 0 0 0 0 0
# 0 0 1 0 0
# 0 1 0 0 0
# 1 0 0 0 0
