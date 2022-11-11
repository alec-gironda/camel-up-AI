from collections import deque
import copy as cp

class GameStateNode:
    """Create an instance of a game state for Camel up

    Parameters
    ----------
    board_state : dict of [square: [camels in square]]
    dice_left : set
        A set of the remaining dice inside of the pyramid
    bets_left : dict of [camel #: (payout 1, payout 2, payout 3)]
    bets_made : dict
        dict of bets made by the current player (s?)
    camel_spots : dict of [camel # : [current square, camel positioning on square]]
        dictionary containing the locations and stackings of camels
    money : int
        Current amount of money the player holds

    Returns
    -------
    GameStateNode
        A unique game state of camel up

    """

    def __init__(self,board_state,dice_left,bets_left,bets_made,camel_spots,money):
        #can likely get rid of the board state, no?
        self.board_state = board_state
        self.dice_left = dice_left
        self.bets_left = bets_left
        self.bets_made = bets_made
        self.camel_spots = camel_spots
        self.money = money


    def is_complete(self):
        #more to figure out with this
        if len(self.board_state[3])>0:
            return True
        return False


        #for now, loop through camels to check to see if any of them are beyond the square 16
        # for key, val in self.camel_spots:
        #     if val > 16:
        #         return True
        # return False
        #
        # if sum(self.board_state[17])>0:
        #     return True
        # return False

    def get_payout(self):
        payout = 0
        for bet in self.bets_made:
            payout += self.bets_made[bet]
        return payout

    def expand(self):

        children = []

        #make sure there aren't issues with copy. might need to deep copy depending on references

        #bet

        #need to make sure to remove the key once all bets used

        for possible_bet in self.bets_left:
            new_bets_left = cp.deepcopy(self.bets_left)
            bet_payout = new_bets_left[possible_bet].pop()
            #this could cause issues... but basically you can't bet on the same camel twice right?
            #at this point though, the agent would only be taking the 5 coin bets
            del new_bets_left[possible_bet]
            new_bets_made = cp.deepcopy(self.bets_made)
            new_bets_made[possible_bet] = bet_payout

            child = GameStateNode(self.board_state,self.dice_left,new_bets_left,new_bets_made,self.camel_spots,self.money)
            children.append(child)


        #roll

        for die in self.dice_left:
            new_dice_left = cp.deepcopy(self.dice_left)
            new_dice_left.discard(die)
            #add a coin
            new_money = self.money + 1
            for die_roll in range(1,4): #possible outcomes on the die
                new_camel_spots = cp.deepcopy(self.camel_spots)
                new_board_state = cp.deepcopy(self.board_state)
                #update the position of camel # die
                for camel in self.board_state[self.camel_spots[die][0]]:
                    if self.camel_spots[camel][1] >= self.camel_spots[die][1]:
                        new_board_state[self.camel_spots[camel][0]].remove(camel)
                        new_camel_spots[camel][0] += die_roll
                        new_camel_spots[camel][1] = len(new_board_state[new_camel_spots[camel][0]])
                        new_board_state[new_camel_spots[camel][0]].append(camel)

                #print(f"new board state: {new_board_state}, die: {die}, ")



                child = GameStateNode(new_board_state,new_dice_left,self.bets_left,self.bets_made,new_camel_spots,new_money)
                children.append(child)

        #print(f"length of children: {len(children)}")
        return children

    def __hash__(self):
        return hash((frozenset(self.board_state),frozenset(self.dice_left),frozenset(self.bets_left),frozenset(self.bets_made),frozenset(self.camel_spots),self.money))

    #overriding == operator
    def __eq__(self, other):
        return isinstance(other, GameStateNode) and self.board_state == other.board_state and self.dice_left == other.dice_left and self.bets_left == other.bets_left and self.bets_made ==other.bets_made and self.camel_spots == other.camel_spots and self.money == other.money


def BFS(root):

    max_money = 0
    q = deque([root])
    hashset = set()
    hashset.add(root)

    while q:
        print(f"q length: {len(q)}")
        #print(f"unique q vals: {len(set(q))}")
        #print(f"hashset: {len(hashset)}")
        x = q.popleft()
        hashset.add(x)

        if x.is_complete():
            terminal_node_money = x.get_payout() + x.money
            print(terminal_node_money)
            if terminal_node_money > max_money:
                max_money = terminal_node_money

        else:
            children = x.expand()
            for child in children:
                if child not in hashset:
                    "This was the big change (144)"
                    hashset.add(child) #makes the bfs eventually terminate
                    q.append(child)
                # else:
                    #print("SKIPPING")
    return max_money

#class DiceRoller:


if __name__ == "__main__":

    #likely don't need board state anymore, either
    board_state = {1:[1,2,3],2:[4,5],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[],15:[],16:[],17:[]}
    bets_left = {1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]}
    bets_made = {}
    dice_left = set([1,2,3,4,5])
    camel_spots = {1:[1,0],2:[1,1],3:[1,2],4:[2,0],5:[2,1]} #arbitrarily selecting starting locations for our camels
    money = 0

    root = GameStateNode(board_state,dice_left,bets_left,bets_made,camel_spots,money)

    BFS(root)

    # curr = GameStateNode({1:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),2:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)})

    # print(curr.game_state)

# B G O W R
# 0 0 0 0 0
# 0 0 0 0 0
# 0 0 1 0 0
# 0 1 0 0 0
# 1 0 0 0 0
