import matplotlib.pyplot as plt
import numpy as np

BOARD_ROWS      = 3
BOARD_COLS      = 4
WIN_STATE       = (0, 3)
LOSE_STATE      = (1, 3)
BLOCKED_STATE   = (1, 1)
START           = (2, 0)

class State:
    def __init__(self, state=START):
        self.state = state
        self.is_end = False

    def get_reward(self):
        if self.state == WIN_STATE: return 1
        if self.state == LOSE_STATE: return -1
        return 0

    def check_end(self):
        if self.state == WIN_STATE or self.state == LOSE_STATE:
            self.is_end = True

    def get_next_position(self, action):
        moves = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        dr, dc = moves[action]
        nxt_state = (self.state[0] + dr, self.state[1] + dc)

        if 0 <= nxt_state[0] < BOARD_ROWS and 0 <= nxt_state[1] < BOARD_COLS:
            if nxt_state != BLOCKED_STATE:
                return nxt_state
        return self.state

# Agente actor-critico (PI via TD)
class ActorCriticAgent:
    def __init__(self):
        self.actions = ["up", "down", "left", "right"]
        self.lr_v = 0.1    # Learning rate del Crítico
        self.lr_p = 0.2    # Learning rate del Actor (más agresivo para notar cambios)
        self.gamma = 0.99
        
        # TABLA 1: El Crítico (Valor de los estados)
        self.state_values = {(i, j): 0.0 for i in range(BOARD_ROWS) for j in range(BOARD_COLS)}
        
        # TABLA 2: El Actor (Preferencias/Política)
        # Inicializamos con preferencias iguales para todas las acciones
        self.policy = {(i, j): {a: 0.0 for a in self.actions} 
                       for i in range(BOARD_ROWS) for j in range(BOARD_COLS)}
        
        self.history_v = []

    def get_probs(self, state):
        # Usamos Softmax para convertir preferencias en probabilidades reales
        prefs = np.array([self.policy[state][a] for a in self.actions])
        exp_prefs = np.exp(prefs - np.max(prefs)) # Estabilidad numerica
        return exp_prefs / exp_prefs.sum()

    def choose_action(self, state):
        probs = self.get_probs(state)
        return np.random.choice(self.actions, p=probs)

    def train(self, rounds):
        for _ in range(rounds):
            env = State(START)
            while not env.is_end:
                old_s = env.state
                action = self.choose_action(old_s)
                
                # Moverse
                env.state = env.get_next_position(action)
                env.check_end()
                
                # Calculo del TD error (La señal que guia a ambos)
                reward = env.get_reward()
                # Delta = R + gamma * V(s') - V(s)
                td_error = reward + self.gamma * self.state_values[env.state] - self.state_values[old_s]
                
                # 1. Actualizar critico (evaluacion)
                self.state_values[old_s] += self.lr_v * td_error
                
                # 2. Actualizar actor (Mejora de Politica)
                # Si td_error > 0, la accion fue buena; si es < 0, fue mala.
                self.policy[old_s][action] += self.lr_p * td_error
            
            self.history_v.append(list(self.state_values.values()))

    def show_results(self):
        print("\n+-- Critic Values V(s) table --+")
        for i in range(BOARD_ROWS):
            print("-" * 37)
            row = "| "
            for j in range(BOARD_COLS):
                # Logica de simbolos para el critico
                if (i, j) == BLOCKED_STATE:
                    val_str = "  na  "
                elif (i, j) == WIN_STATE:
                    val_str = "  +   "
                elif (i, j) == LOSE_STATE:
                    val_str = "  -   "
                else:
                    # Imprimimos el valor numerico con 2 decimales
                    val_str = f"{self.state_values[(i, j)]:6.2f}"
                
                row += val_str + " | "
            print(row)
        print("-" * 37)

        # Mostrar Política
        print("\n+-- Actor Policy table --+")
        icons = {"up": "  ^  ", "down": "  v  ", "left": "  <  ", "right": "  >  "}
        for i in range(BOARD_ROWS):
            print("-" * 33)
            row = "| "
            for j in range(BOARD_COLS):
                if (i, j) == BLOCKED_STATE: row += "  na  | "
                elif (i, j) == WIN_STATE: row += "   +  | "
                elif (i, j) == LOSE_STATE: row += "   -  | "
                else:
                    best_a = max(self.policy[(i, j)], key=self.policy[(i, j)].get)
                    row += icons[best_a] + " | "
            print(row)
        print("-" * 33)

    def plot_data(self):
        # Latex 
        plt.rcParams.update({
            "text.usetex": True,
            "font.family": "serif",
            "text.latex.preamble": r"\usepackage{amsmath}",
        })

        data = np.array(self.history_v)
        fig, axs = plt.subplots(BOARD_ROWS, BOARD_COLS, figsize=(15, 10))
        
        # fig.suptitle(r'$\text{Convergencia de Valores } V(s) \text{ usando } TD \text{ - PI (Actor-Critic)}$', fontsize=16)
        fig.suptitle(f'Convergencia de Valores V(s) usando TD - PI (Actor-Critic)', fontsize=16)

        states_order = list(self.state_values.keys())
        colormap = plt.get_cmap('tab20')
        colors = [colormap(i) for i in np.linspace(0, 1, len(states_order))]
        
        idx = 0
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                # Graficamos en el subplot correspondiente
                axs[i, j].plot(data[:, idx], color=colors[idx], linewidth=2)
                
                axs[i, j].set_title(f'Estado ({i},{j})', fontsize=12)
                
                if j == 0: axs[i, j].set_ylabel(r'$V(s)$')
                if i == BOARD_ROWS - 1: axs[i, j].set_xlabel(r'$\text{Episodios}$')
                
                axs[i, j].grid(True, alpha=0.3, linestyle='--')
                
                if (i, j) == BLOCKED_STATE:
                    axs[i, j].set_facecolor('#f0f0f0')
                elif (i, j) == WIN_STATE:
                    axs[i, j].set_facecolor('#e6ffed')
                elif (i, j) == LOSE_STATE:
                    axs[i, j].set_facecolor("#e7b6c2c5")
                
                idx += 1
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

if __name__ == "__main__":
    agent = ActorCriticAgent()
    agent.train(1)
    agent.show_results()
    agent.plot_data()