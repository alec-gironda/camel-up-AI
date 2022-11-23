from collections import deque
import copy as cp
import random
import pickle
import time
import pandas as pd
import tensorflow as tf
import numpy as np
import os

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

    def __init__(self,board_state,dice_left,bets_left,camel_spots, player1 = False):
        #can likely get rid of the board state, no?
        self.board_state = board_state
        self.dice_left = dice_left
        self.bets_left = bets_left
        self.camel_spots = camel_spots
        self.expected_value = 0
        self.player1 = player1

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

    def key(self):
        res = self.get_hashable_board_state()
        res.extend(self.get_hashable_dice_left())
        res.extend(self.get_hashable_bets_left())
        res.extend(self.get_hashable_camel_spots())
        return tuple(res)

    def __hash__(self):
        return hash(self.key())
    #overriding == operator
    def __eq__(self, other):
        return isinstance(other, GameStateNode) and self.key() == other.key()

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


    def __init__(self,network):
        super().__init__()

        self.model = tf.keras.models.load_model(network)


    def make_move(self,gamestate : GameStateNode):

        moveType = 0
        maxChild = 0
        children = gamestate.expand(self.bets_made)
        flag = False

        if children:
            child_np_array = np.asarray(np.asarray([np.asarray(child[0].key()) for child in children]))
            preds = self.model.predict(child_np_array,verbose = False)
            move = np.argmax(preds)

            maxChild = children[move][0]
            moveType = children[move][1]

        else:
            return None

        if moveType == "roll":
            self.money +=1
        else:
            self.bets_made[moveType[0]] = moveType[1]

        # print(maxChild.board_state)
        return maxChild

class Simulate:

    def __init__(self):

        self.game_tup_x = []
        self.game_tup_labels = []
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


    def SimulateGame(self,state,game_type, network1 = None, network2 = None):
        player1 = None
        player2 = None

        if game_type == 0: #random vs random
            player1 = RandomPlayer()
            player2 = RandomPlayer()
        elif game_type == 1: #smart vs random
            player1 = SmartPlayer(network1)
            player2 = RandomPlayer()
        else: #smart vs smart
            player1 = SmartPlayer(network1)
            player2 = SmartPlayer(network2)

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

                    for state in self.model_dict:
                        self.game_tup_x.append(state.key())
                        self.game_tup_labels.append(players[0].money)

                        self.model_dict[state] = players[0].money

                    return self.game_tup_x,self.game_tup_labels, result

class Network:
    def __init__(self,x_train,y_train):

        self.x_train = np.asarray(x_train)
        self.y_train = np.asarray(y_train)

        self.model = None

    def compile(self):

        self.model = tf.keras.models.Sequential()
        self.model.add(tf.keras.layers.Flatten())
        self.model.add(tf.keras.layers.Dense(100,activation = tf.nn.relu))
        self.model.add(tf.keras.layers.Dense(1))

        optim = tf.keras.optimizers.Adam(learning_rate=0.01)

        self.model.compile(optimizer=optim,loss='mean_squared_error',metrics=tf.keras.metrics.RootMeanSquaredError())

        pass

    def train_model(self):

        self.model.fit(self.x_train,self.y_train,epochs=100)

        pass

    def save_model(self,name):

        self.model.save(name)

        pass




if __name__ == "__main__":

    #starting game configs
    board_state = {1:[1,2,3],2:[4,5],3:[],4:[],5:[],6:[],7:[],8:[],9:[],10:[],11:[],12:[],13:[],14:[],15:[],16:[],17:[],18:[],19:[],20:[]}
    bets_left = {1:[2,3,5],2:[2,3,5],3:[2,3,5],4:[2,3,5],5:[2,3,5]}
    bets_made = {}
    dice_left = set([1,2,3,4,5])
    camel_spots = {1:[1,0],2:[1,1],3:[1,2],4:[2,0],5:[2,1]} #arbitrarily selecting starting locations for our camels
    money = 0

    root = GameStateNode(board_state,dice_left,bets_left,camel_spots)

    x_train = []
    y_train = []

    print("simulating")
    outcome = [0,0,0]

    for i in range(1000):

        print(i)
        sim = Simulate()
        sim_x, sim_y, res = sim.SimulateGame(root,0)

        x_train.extend(sim_x)
        y_train.extend(sim_y)
        if res == 1:
            outcome[0] +=1
        elif res == 2:
            outcome[1] +=1
        else:
            outcome[2] +=1

    new_network = Network(x_train,y_train)
    new_network.compile()
    new_network.train_model()
    new_network.save_model("random_model")

        #print(f"res: {res}")
    print(f"Simulated random game: {outcome}")


    x_train = []
    y_train = []

    print("simulating")
    outcome = [0,0,0]

    for i in range(1000):

        print(i)
        sim = Simulate()
        sim_x, sim_y, res = sim.SimulateGame(root,1,"random_model")

        x_train.extend(sim_x)
        y_train.extend(sim_y)
        if res == 1:
            outcome[0] +=1
        elif res == 2:
            outcome[1] +=1
        else:
            outcome[2] +=1

    os.rename("random_model","prev_model")


    new_network = Network(x_train,y_train)
    new_network.compile()
    new_network.train_model()
    new_network.save_model("new_model")
        #print(f"res: {res}")
    print(f"Simulating first weighted game: {outcome}")

    for _ in range(5):

        x_train = []
        y_train = []

        print("simulating")
        i=0
        outcome = [0,0,0]

        for i in range(1000):

            print(i)
            sim = Simulate()
            sim_x, sim_y, res = sim.SimulateGame(root,2,"new_model","prev_model")

            x_train.extend(sim_x)
            y_train.extend(sim_y)
            if res == 1:
                outcome[0] +=1
            elif res == 2:
                outcome[1] +=1
            else:
                outcome[2] +=1

        os.rename("new_model","prev_model")

        new_network = Network(x_train,y_train)
        new_network.compile()
        new_network.train_model()
        new_network.save_model("new_model")
            #print(f"res: {res}")
        print(f"Simulating weighted game: {outcome}")

    # for _ in range(5):



    # curr = GameStateNode({1:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0),2:(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)})



# B G O W R
# 0 0 0 0 0
# 0 0 0 0 0
# 0 0 1 0 0
# 0 1 0 0 0
# 1 0 0 0 0
