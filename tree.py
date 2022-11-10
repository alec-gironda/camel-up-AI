from collections import deque
import copy

class GameStateNode:
"""Create an instance of a game state for Camel up

    Parameters
    ----------
    board_state : dict of [square: (tuple of len(25) with 5 slots for each camel (for placement purposes))]
        Training ECG data
    dice_left : set
        A set of the remaining dice inside of the pyramid
    bets_left : dict of [camel #: (payout 1, payout 2, payout 3)]
        Testing ECG data
    bets_made : dict
        dict of bets made by the current player (s?)
    camel_spots : dict of [camel # : (current square, camel positioning on square)]
        dictionary containing the locations and stackings of camels
    money : int
        Current amount of money the player holds

    Returns
    -------
    GameStateNode
        A unique game state of camel up

    """
    def __init__(self,board_state,dice_left,bets_left,money):
        #can likely get rid of the board state, no?
        self.board_state = board_state
        self.dice_left = dice_left
        self.bets_left = bets_left
        self.bets_made = bets_made
        self.camel_spots = camel_spots
        self.money = money


    def is_complete(self):
        #more to figure out with this

        #for now, loop through camels to check to see if any of them are beyond the square 16
        for key, val in self.camel_spots:
            if val > 16:
                return True
        return False

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
        for die in self.dice_left:
            for i in range (1,4): #possible outcomes on the die
                #update the position of camel # die

                children.append(GameStateNode())


        return children

#class DiceRoller:


if __name__ == "__main__":

    #likely don't need board state anymore, either
    #board_state = {i+1:tuple(0 for i in range(25)) for i in range(17)}
    bets_left = {1:(5,3,2),2:(5,3,2),3:(5,3,2),4:(5,3,2),5:(5,3,2)}
    bets_made = {}
    dice_left = set([1,2,3,4,5])
    camel_spots = {1:(1,0),2:(1,1),3:(1,2),4:(2,0),5:(2,1)} #arbitrarily selecting starting locations for our camels
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
