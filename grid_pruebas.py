import matplotlib.pyplot as plt
from matplotlib.pyplot import axis
import numpy as np

BOARD_ROWS = 3
BOARD_COLS = 4
WIN_STATE = (0, 3)
LOSE_STATE = (1, 3)
START = (0, 0)
DETERMINISTIC = True


class State:
    def __init__(self, state=START):
        self.board = np.zeros([BOARD_ROWS, BOARD_COLS])
        self.board[1, 1] = -1
        self.state = state
        self.isEnd = False
        self.determine = DETERMINISTIC

    def giveReward(self):
        if self.state == WIN_STATE:
            return 1
        elif self.state == LOSE_STATE:
            return -1
        else:
            return 0

    def isEndFunc(self):
        if (self.state == WIN_STATE) or (self.state == LOSE_STATE):
            self.isEnd = True

    def nxtPosition(self, action):

        if self.determine:
            if action == "arriba":
                nxtState = (self.state[0] - 1, self.state[1])
            elif action == "abajo":
                nxtState = (self.state[0] + 1, self.state[1])
            elif action == "izquierda":
                nxtState = (self.state[0], self.state[1] - 1)
            else:
                nxtState = (self.state[0], self.state[1] + 1)
            # if next state legal
            if (nxtState[0] >= 0) and (nxtState[0] <= (BOARD_ROWS -1)):
                if (nxtState[1] >= 0) and (nxtState[1] <= (BOARD_COLS -1)):
                    if nxtState != (1, 1):
                        return nxtState
            return self.state

    def showBoard(self):
        self.board[self.state] = 1
        for i in range(0, BOARD_ROWS):
            print('-----------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                if self.board[i, j] == 1:
                    token = '*'
                if self.board[i, j] == -1:
                    token = 'z'
                if self.board[i, j] == 0:
                    token = '0'
                out += token + ' | '
            print(out)
        print('-----------------')
  


class Agent:

    def __init__(self):
        self.states = []
        self.actions = ["arriba", "abajo", "izquierda", "derecha"]
        self.State = State()
        self.lr = 0.9
        self.exp_rate = 0.9
        self.gamma = 0.9

        # initial state reward
        self.state_values = {}
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.state_values[(i, j)] = 0 

    def chooseAction(self):
        mx_nxt_reward = 0
        action = ""

        if np.random.uniform(0, 1) <= self.exp_rate:
            action = np.random.choice(self.actions)
        else:
            # accion voraz
            for a in self.actions:
                # si la accion es determinista
                nxt_reward = self.state_values[self.State.nxtPosition(a)]
                if nxt_reward >= mx_nxt_reward:
                    action = a
                    mx_nxt_reward = nxt_reward
        return action

    def takeAction(self, action):
        position = self.State.nxtPosition(action)
        return State(state=position)

    def reset(self):
        self.states = []
        self.State = State()

    def play(self, rounds=1):
        i = 0
        dic_valo = []
        self.numeros_varios = []
        while i < rounds:
    
            if self.State.isEnd:
                # propagación hacia atras 
                reward = self.State.giveReward()

                print("Recompensa de fin de juego", reward)
                for s in reversed(self.states):
                    #reward = self.state_values[s] + self.lr * (reward - self.state_values[s])
                    print(reward)
                    reward = self.gamma*reward
                    print("recompensa + {}*V(s) = {} ".format(self.gamma, reward))
                    self.state_values[s] = round(reward, 3)
                    dic_valo = self.state_values
                    print(dic_valo)
                    numeros = list(dic_valo.values())
                    print(numeros)

                self.reset()
                i += 1

                self.numeros_varios.append(numeros)
                print(type(self.numeros_varios))
                self.arreglo_num_varios = np.array(self.numeros_varios)
                print(type(self.arreglo_num_varios))
                #print(self.arreglo_num_varios)


            else:
                action = self.chooseAction()
                self.states.append(self.State.nxtPosition(action))
                self.State = self.takeAction(action)
                self.State.isEndFunc()

    def showValues(self):
        for i in range(0, BOARD_ROWS):
            print('----------------------------------')
            out = '| '
            for j in range(0, BOARD_COLS):
                out += str(self.state_values[(i, j)]).ljust(6) + ' | '
            print(out)
        print('----------------------------------')

    
    def imprimir_graph(self):
        self.arr = self.arreglo_num_varios
        fig, axs = plt.subplots(3,4)
        fig.suptitle('GW, indice de exploracion: 0.01')
        
        axs[0,0].plot(self.arr[:,0])
        axs[0,0].set_title('V(0,0)')
        axs[0,1].plot(self.arr[:,1])
        axs[0,1].set_title('V(0,1)')
        axs[0,2].plot(self.arr[:,2])
        axs[0,2].set_title('V(0,2)')
        axs[0,3].plot(self.arr[:,3])
        axs[0,3].set_title('V(0,3)')
        axs[1,0].plot(self.arr[:,4])
        axs[1,0].set_title('V(1,0)')
        axs[1,1].plot(self.arr[:,5])
        axs[1,1].set_title('V(1,1)')
        axs[1,2].plot(self.arr[:,6])
        axs[1,2].set_title('V(1,2)')
        axs[1,3].plot(self.arr[:,7])
        axs[1,3].set_title('V(1,3)')
        axs[2,0].plot(self.arr[:,8])
        axs[2,0].set_title('V(2,0)')
        axs[2,1].plot(self.arr[:,9])
        axs[2,1].set_title('V(2,1)')
        axs[2,2].plot(self.arr[:,10])
        axs[2,2].set_title('V(2,2)')
        axs[2,3].plot(self.arr[:,11])
        axs[2,3].set_title('V(2,3)')


        
        for ax in axs.flat:
            ax.label_outer()

        
        print(self.arr)
        plt.show()

  
if __name__ == "__main__":
    ag = Agent()
    ag.play(30)
    print(ag.showValues())
    print(ag.imprimir_graph())
