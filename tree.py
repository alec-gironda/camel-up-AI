from collections import deque
import copy as cp
import random
import pickle
import time
import pandas as pd

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

    def __init__(self,board_state,dice_left,bets_left,camel_spots,parent = None, player1 = False):
        #can likely get rid of the board state, no?
        self.board_state = board_state
        self.dice_left = dice_left
        self.bets_left = bets_left
        self.camel_spots = camel_spots
        self.parent = parent
        self.expected_value = 0
        self.player1 = player1
        # print(self.__key())
    def get_hashable_board_state(self):

        res = [0 for i in range(0,20*5)]

        for key in self.board_state:
            start = (key-1)*5
            res[start:start+len(self.board_state[key])] = self.board_state[key]

        return res

    def get_hashable_bets_left(self):

        res = [0 for i in range(0,5*3)]

        for key in self.bets_left:
            start = (key-1)*3
            res[start:start+len(self.bets_left[key])] = self.bets_left[key]

        return res

    def get_hashable_camel_spots(self):

        res = [0 for i in range(0,5*2)]

        for key in self.camel_spots:
            start = (key-1)*2
            res[start:start+len(self.camel_spots[key])] = self.camel_spots[key]

        return res

    def get_hashable_dice_left(self):

        res = [0 for i in range(5)]

        for die in self.dice_left:
            res[die-1] = 1

        return tuple(res)


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

                child = GameStateNode(self.board_state,self.dice_left,new_bets_left,self.camel_spots,self)
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


                child = GameStateNode(new_board_state,new_dice_left,self.bets_left,new_camel_spots,self)
                children.append((child,"roll"))

        return children

    def __key(self):
        res = self.get_hashable_board_state()
        res.extend(self.get_hashable_dice_left())
        res.extend(self.get_hashable_bets_left())
        res.extend(self.get_hashable_camel_spots())
        return tuple(res)
    def __hash__(self):
        return hash(self.__key())
    #overriding == operator
    def __eq__(self, other):
        return isinstance(other, GameStateNode) and self.__key() == other.__key()


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

class Player:

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

class RandomPlayer(Player):

    """
    Random Player, takes in a state and returns one with a random move
    """

    def __init__(self):
        super().__init__()

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

class SmartPlayer(Player):


    def __init__(self,expected_value_dict):
        super().__init__()
        self.expected_value_dict = expected_value_dict


    def make_move(self,gamestate : GameStateNode):

        moveType = 0
        maxChild = 0
        children = gamestate.expand(self.bets_made)
        flag = False

        if children:
            random_move = random.randint(0,len(children)-1) #inclusive
            maxChild = children[random_move][0]
            maxValue = 0
            moveType = children[random_move][1]
            for child in children:
                if child[0] in self.expected_value_dict:
                    flag = True
                    if self.expected_value_dict[child[0]] > maxValue:
                        maxValue = self.expected_value_dict[child[0]]
                        maxChild = child[0]
                        moveType = child[1]

        else:
            return None

        if flag:
            print("FLAG","\n")
        print(moveType)
        print(maxChild)


        if moveType == "roll":
            self.money +=1
        else:
            self.bets_made[moveType[0]] = moveType[1]

        print(maxChild.board_state)
        return maxChild


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


class Simulate:

    def __init__(self):

        self.model_df = pd.DataFrame(columns = ["board_state","dice_left","bets_left","camel_spots","expected_value"])
        self.model_dict = {}

    def get_winner(self, players):
        #returns 1 for player1 dub
        #returns 2 for player 2 dub
        #retruns 3 for player 2 dub

        if players[0].money > players[1].money:
            return 1
        elif players[1].money > players[0].money:
            return 2
        else:
            return 3


    def SimulateRandomGame(self,state):
        player1 = RandomPlayer()
        player2 = RandomPlayer()
        # player3 = RandomPlayer()
        # player4 = RandomPlayer()

        players = [player1,player2] #,player3,player4]
        while True:
            for player in players:

                if player == players[0]: #if player 1
                    self.model_dict[state] = -1
                complete = state.is_complete()
                if not complete[0]:
                    tmp_state = cp.deepcopy(state)
                    if len(state.dice_left) == 0:

                        #reset leg
                        #we can store this so we don't need to search
                        front_camel_indx = 0
                        for i in range(len(tmp_state.board_state)-1,-1,-1):
                            if len(tmp_state.board_state[i])>0:
                                front_camel_indx = i
                                break

                        for p in players:
                            p.money += p.get_payout(tmp_state,front_camel_indx)
                        state = GameStateNode(tmp_state.board_state,set([1,2,3,4,5]),{1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]},tmp_state.camel_spots)
                        state = player.make_move(state)
                    else:
                        state = player.make_move(state)
                else:

                    for p in players:
                        p.money += p.get_payout(state,complete[1])

                    result = self.get_winner(players)

                    for key in self.model_dict:
                        print(key)
                        self.model_df.loc[len(self.model_df.index)] = [key.board_state, key.dice_left, key.bets_left, key.camel_spots,players[0].money]
                        self.model_dict[key] = players[0].money

                    return self.model_dict, result


    def SimulateRandomVsSmartGame(self,state,expected_value_dict):
        player1 = SmartPlayer(expected_value_dict)
        player2 = RandomPlayer()
        # player3 = RandomPlayer()
        # player4 = RandomPlayer()

        players = [player1,player2] #,player3,player4]
        while True:
            for player in players:

                if player == players[0]: #if player 1
                    self.model_dict[state] = players[0].money

                complete = state.is_complete()
                if not complete[0]:
                    tmp_state = cp.deepcopy(state)
                    if len(state.dice_left) == 0:

                        #reset leg
                        #we can store this so we don't need to search

                        front_camel_indx = 0
                        for i in range(len(tmp_state.board_state)-1,-1,-1):
                            if len(tmp_state.board_state[i])>0:
                                front_camel_indx = i
                                break

                        for p in players:
                            p.money += p.get_payout(tmp_state,front_camel_indx)
                        state = GameStateNode(tmp_state.board_state,set([1,2,3,4,5]),{1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]},tmp_state.camel_spots)
                        state = player.make_move(state)
                    else:
                        state = player.make_move(state)
                else:

                    for p in players:
                        p.money += p.get_payout(state,complete[1])

                    result = self.get_winner(players)

                    for key in self.model_dict:
                        self.model_dict[key] = players[0].money

                    return self.model_dict, result


if __name__ == "__main__":

    #starting game configs
    board_state = {1:[1,2,3],2:[4,5],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[],15:[],16:[],17:[],18:[],19:[],20:[]}
    bets_left = {1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]}
    bets_made = {}
    dice_left = set([1,2,3,4,5])
    camel_spots = {1:[1,0],2:[1,1],3:[1,2],4:[2,0],5:[2,1]} #arbitrarily selecting starting locations for our camels
    money = 0


    # root = SinglePlayerGameStateNode(board_state,dice_left,bets_left,bets_made,camel_spots,money)
    # print(BFS(root))

    root = GameStateNode(board_state,dice_left,bets_left,camel_spots)
    # root2 = GameStateNode(board_state,dice_left, bets_left, camel_spots)



    #simulating 1000 games
    p1_wins = 0
    p2_wins = 0
    # p3_wins = 0
    # p4_wins = 0

    print("Starting simulations")
    start_time = time.time()
    ties = 0
    expected_values = {}
    outcome = [0,0,0]
    i=0
    for _ in range(10000):
        print(i,len(expected_values))
        sim = Simulate()
        sim_dict = sim.SimulateRandomGame(root)

        #recording game metrics
        if sim_dict[1] == 1:
            outcome[0] +=1
        elif sim_dict[1] == 2:
            outcome[1] +=1
        else:
            outcome[2] +=1
        i+=1

        expected_values.update(sim_dict[0])
    print("--- %s seconds ---" % (time.time() - start_time))
    print(len(expected_values))

    with open('model.pkl', 'wb') as f:
        pickle.dump(expected_values, f)


    print("loading dict")
    start_time = time.time()
    expected_values = 0
    with open('model.pkl', 'rb') as f:
        expected_values = pickle.load(f)
    print("--- %s seconds ---" % (time.time() - start_time))


    # print(f"Simulating random game: {outcome}")

    # print("simulating")
    # i=0
    # outcome = [0,0,0]
    #
    # for _ in range(10000):
    #
    #     print(i)
    #     newSim = Simulate()
    #     res = newSim.SimulateRandomVsSmartGame(root,expected_values)
    #     if res[1] == 1:
    #         outcome[0] +=1
    #     elif res[1] == 2:
    #         outcome[1] +=1
    #     else:
    #         outcome[2] +=1
    #     i+=1
    #     #print(f"res: {res}")
    # print(f"Simulating weighted game: {outcome}")
    # curr = GameStateNode({1:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),2:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)})



# B G O W R
# 0 0 0 0 0
# 0 0 0 0 0
# 0 0 1 0 0
# 0 1 0 0 0
# 1 0 0 0 0
