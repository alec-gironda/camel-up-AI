from collections import deque
import copy as cp
import random

class GameStateNode:

    def __init__(self,board_state,dice_left,bets_left,camel_spots):
        #can likely get rid of the board state, no?
        self.board_state = board_state
        self.dice_left = dice_left
        self.bets_left = bets_left
        self.camel_spots = camel_spots

    def is_complete(self):
        #more to figure out with this
        for i in range(16,20):
            if len(self.board_state[i])>0:
                return True,i
        return False,-1

    def expand(self,bets_made = {}):

        children = []

        for possible_bet in self.bets_left:
            if possible_bet not in bets_made:
                new_bets_left = cp.deepcopy(self.bets_left)
                payout = new_bets_left[possible_bet].pop()
                if len(new_bets_left[possible_bet])==0:
                    del new_bets_left[possible_bet]

                child = GameStateNode(self.board_state,self.dice_left,new_bets_left,self.camel_spots)
                children.append((child,(possible_bet,payout)))


        #roll

        for die in self.dice_left:
            new_dice_left = cp.deepcopy(self.dice_left)
            new_dice_left.discard(die)
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


                child = GameStateNode(new_board_state,new_dice_left,self.bets_left,new_camel_spots)
                children.append((child,"roll"))

        return children

    def __hash__(self):
        return hash((frozenset(self.board_state),frozenset(self.dice_left),frozenset(self.bets_left),frozenset(self.camel_spots)))

    #overriding == operator
    def __eq__(self, other):
        return isinstance(other, GameStateNode) and self.board_state == other.board_state and self.dice_left == other.dice_left and self.bets_left == other.bets_left and self.camel_spots == other.camel_spots


class SinglePlayerGameStateNode(GameStateNode):
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
        super().__init__(board_state,dice_left,bets_left,camel_spots)
        self.bets_made = bets_made
        self.money = money

    def get_payout(self,indx):
        payout = 0
        bet = self.board_state[indx].pop()
        if bet in self.bets_made:
            payout = self.bets_made[bet]
        return payout

    def expand_single(self):

        children = []

        for possible_bet in self.bets_left:
            new_bets_left = cp.deepcopy(self.bets_left)
            bet_payout = new_bets_left[possible_bet].pop()
            del new_bets_left[possible_bet]
            new_bets_made = cp.deepcopy(self.bets_made)
            new_bets_made[possible_bet] = bet_payout

            child = SinglePlayerGameStateNode(self.board_state,self.dice_left,new_bets_left,new_bets_made,self.camel_spots,self.money)
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


                child = SinglePlayerGameStateNode(new_board_state,new_dice_left,self.bets_left,self.bets_made,new_camel_spots,new_money)
                children.append(child)

        return children

    def __hash__(self):
        return hash((frozenset(self.board_state),frozenset(self.dice_left),frozenset(self.bets_left),frozenset(self.bets_made),frozenset(self.camel_spots),self.money))

    #overriding == operator
    def __eq__(self, other):
        return isinstance(other, GameStateNode) and self.board_state == other.board_state and self.dice_left == other.dice_left and self.bets_left == other.bets_left and self.bets_made ==other.bets_made and self.camel_spots == other.camel_spots and self.money == other.money

class RandomPlayer:

    """
    Random Player, takes in a state and returns one with a random move
    """

    def __init__(self):
        self.money = 0
        self.bets_made = {}

    def get_payout(self,state,indx):
        payout = 0
        tmp_state = cp.deepcopy(state)
        camel = tmp_state.board_state[indx].pop()
        if camel in self.bets_made:
            payout = self.bets_made[camel]
            del self.bets_made[camel]
        return payout

    def make_move(self,gamestate : GameStateNode):
        #possible moves:
        #0: roll dice
        #1: bet on camel 1
        #2: bet on camel 2
        #3: bet on camel 3
        #4: bet on camel 4
        #5: bet on camel 5

        move = 0
        children = gamestate.expand(self.bets_made)
        if children:
            move = random.randint(0,len(children)-1) #inclusive
        else:
            return None

        if children[move][1] == "roll":
            self.money +=1
        else:
            self.bets_made[children[move][1][0]] = children[move][1][1]

        return children[move][0]

def BFS(root): #should only be done in a single player game

    max_money = 0
    q = deque([root])
    hashset = set()

    while q:

        x = q.popleft()
        hashset.add(x)

        complete = x.is_complete()
        if complete[0]:
            terminal_node_money = x.get_payout(complete[1]) + x.money
            if terminal_node_money > max_money:
                max_money = terminal_node_money

        else:
            children = x.expand_single()
            for child in children:
                if child not in hashset:
                    hashset.add(child) #makes the bfs eventually terminate
                    q.append(child)
    return max_money

def SimulateRandomGame(state):
    player1 = RandomPlayer()
    player2 = RandomPlayer()

    while True:
        complete = state.is_complete()
        if not complete[0]:
            tmp_state = cp.deepcopy(state)
            state = player1.make_move(state)
            #reset leg
            if not state:
                #we can store this so we don't need to search
                front_camel_indx = 0
                for i in range(len(tmp_state.board_state)-1,-1,-1):
                    if len(tmp_state.board_state[i])>0:
                        front_camel_indx = i
                        break

                player1.money += player1.get_payout(tmp_state,front_camel_indx)
                player2.money += player2.get_payout(tmp_state,front_camel_indx)
                state = GameStateNode(tmp_state.board_state,set([1,2,3,4,5]),{1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]},tmp_state.camel_spots)
                state = player1.make_move(state)
        else:
            player1.money += player1.get_payout(state,complete[1])
            player2.money += player2.get_payout(state,complete[1])
            if player1.money > player2.money:
                print(f"player 1 wins by {player1.money-player2.money} money")
                return (player1.money,1)
            elif player1.money < player2.money:
                print(f"player 2 wins by {player2.money - player1.money} money")
                return (player2.money,2)
            else:
                return (None,3)


        complete = state.is_complete()
        if not complete[0]:
            tmp_state = cp.deepcopy(state)
            state = player2.make_move(state)
            #reset leg
            if not state:
                #we can store this so we don't need to search
                front_camel_indx = 0
                for i in range(len(tmp_state.board_state)-1,-1,-1):
                    if len(tmp_state.board_state[i])>0:
                        front_camel_indx = i
                        break
                player1.money += player1.get_payout(tmp_state,front_camel_indx)
                player2.money += player2.get_payout(tmp_state,front_camel_indx)
                state = GameStateNode(tmp_state.board_state,set([1,2,3,4,5]),{1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]},tmp_state.camel_spots)
                state = player2.make_move(state)
        else:
            player1.money += player1.get_payout(state,complete[1])
            player2.money += player2.get_payout(state,complete[1])
            if player1.money > player2.money:
                print(f"player 1 wins by {player1.money-player2.money} money")
                return (player1.money,1)
            elif player1.money < player2.money:
                print(f"player 2 wins by {player2.money - player1.money} money")
                return (player2.money,2)
            else:
                return(None,3)



if __name__ == "__main__":

    #likely don't need board state anymore, either
    board_state = {1:[1,2,3],2:[4,5],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[],15:[],16:[],17:[],18:[],19:[],20:[]}
    bets_left = {1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]}
    bets_made = {}
    dice_left = set([1,2,3,4,5])
    camel_spots = {1:[1,0],2:[1,1],3:[1,2],4:[2,0],5:[2,1]} #arbitrarily selecting starting locations for our camels
    money = 0


    # root = SinglePlayerGameStateNode(board_state,dice_left,bets_left,bets_made,camel_spots,money)
    #
    # print(BFS(root))

    root = GameStateNode(board_state,dice_left,bets_left,camel_spots)


    p1_wins = 0
    p2_wins = 0
    ties = 0
    for _ in range(1000):
        sim = SimulateRandomGame(root)
        if sim[1] == 1:
            p1_wins +=1
        elif sim[1] ==2:
            p2_wins +=1
        else:
            ties +=1

    print(p1_wins)
    print(p2_wins)
    print(ties)

    # curr = GameStateNode({1:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),2:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)})

    # print(curr.game_state)

# B G O W R
# 0 0 0 0 0
# 0 0 0 0 0
# 0 0 1 0 0
# 0 1 0 0 0
# 1 0 0 0 0
