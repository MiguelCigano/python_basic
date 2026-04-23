import matplotlib.pyplot as plt
import numpy as np

# Variables globales
BOARD_ROWS = 3
BOARD_COLS = 4
WIN_STATE = (0, 3)
LOSE_STATE = (1, 3)
BLOCKED_STATE = (1, 1)
START = (2, 0)

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
        # Mapeo de movimientos
        moves = {
            "up": (-1, 0), "down": (1, 0),
            "left": (0, -1), "right": (0, 1)
        }
        dr, dc = moves[action]
        nxt_state = (self.state[0] + dr, self.state[1] + dc)

        # Verificar límites y obstáculos
        if 0 <= nxt_state[0] < BOARD_ROWS and 0 <= nxt_state[1] < BOARD_COLS:
            if nxt_state != BLOCKED_STATE:
                return nxt_state
        return self.state

class Agent:
    def __init__(self):
        self.actions = ["up", "down", "left", "right"]
        self.lr = 0.1 # Learning Rate (Alpha)
        self.exp_rate = 0.1 # Epsilon para exploración
        self.gamma = 0.99 # Factor de descuento
        self.state_values = {(i, j): 0.0 for i in range(BOARD_ROWS) for j in range(BOARD_COLS)}
        self.history = []

    def choose_action(self, current_state):
        # Epsilon-greedy
        if np.random.uniform(0, 1) <= self.exp_rate:
            return np.random.choice(self.actions)
        
        # Greedy: buscar la acción con mayor valor futuro
        best_val = -float('inf')
        action = self.actions[0]
        
        temp_env = State(current_state)
        for a in self.actions:
            nxt_pos = temp_env.get_next_position(a)
            val = self.state_values[nxt_pos]
            if val > best_val:
                best_val = val
                action = a
            elif val == best_val: # Romper empates aleatoriamente
                action = np.random.choice([action, a])
        return action

    def train(self, rounds=500):
        for _ in range(rounds):
            env = State(START)
            while not env.is_end:
                old_state = env.state
                action = self.choose_action(old_state)
                
                # Ejecutar acción
                env.state = env.get_next_position(action)
                env.check_end()
                
                # TD(0) Update: V(s) = V(s) + alpha * [Reward + gamma * V(s') - V(s)]
                reward = env.get_reward()
                v_current = self.state_values[old_state]
                v_next = self.state_values[env.state]
                
                self.state_values[old_state] += self.lr * (reward + self.gamma * v_next - v_current)
            
            # Guardar histórico para gráficas
            self.history.append(list(self.state_values.values()))

    # def show_values(self):
    #     print("\n--- TABLA DE VALORES V(s) ---")
    #     for i in range(BOARD_ROWS):
    #         print("-" * 45)
    #         row = "| " + " | ".join(f"{self.state_values[(i, j)]:6.3f}" for j in range(BOARD_COLS)) + " |"
    #         print(row)
    #     print("-" * 45)

    def show_values(self):
        print("\n+------- Values V(s) table -------+")
        for i in range(BOARD_ROWS):
            print("-" * 37)
            row = "| "
            for j in range(BOARD_COLS):
                # 1. Verificamos si es el estado de GANAR
                if (i, j) == WIN_STATE:
                    val_str = "  +   "
                # 2. Verificamos si es el estado de PERDER
                elif (i, j) == LOSE_STATE:
                    val_str = "  -   "
                # 3. Verificamos si es el BLOQUEO
                elif (i, j) == BLOCKED_STATE:
                    val_str = "  na  "
                # 4. Si es una celda normal, imprimimos su valor
                else:
                    val_str = f"{self.state_values[(i, j)]:6.3f}"
                
                row += val_str + " | "
            print(row)
        print("-" * 37)

    # def plot_convergence(self):
    #     data = np.array(self.history)
    #     fig, axs = plt.subplots(BOARD_ROWS, BOARD_COLS, figsize=(15, 10))
    #     fig.suptitle(f'Convergencia de Valores V(s) mediante TD(0)', fontsize=16)
        
    #     idx = 0
    #     for i in range(BOARD_ROWS):
    #         for j in range(BOARD_COLS):
    #             axs[i, j].plot(data[:, idx])
    #             axs[i, j].set_title(f'Estado ({i},{j})')
    #             axs[i, j].grid(True, alpha=0.3)
    #             idx += 1
        
    #     plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    #     plt.show()

    def plot_convergence(self):
        # --- CONFIGURACIÓN ESTILO LATEX ---
        plt.rcParams.update({
            "text.usetex": True, # Pon True si tienes LaTeX instalado en el sistema, 
                                  # si no, el motor interno de Matplotlib lo hará igual de bien.
            "font.family": "serif",
            "text.latex.preamble": r"\usepackage{amsmath}", # <--- ESTO FALTA
        })

        data = np.array(self.history)
        fig, axs = plt.subplots(BOARD_ROWS, BOARD_COLS, figsize=(15, 10))
        fig.suptitle(f'Convergencia de Valores V(s) usando TD - VI', fontsize=16)
        # fig.suptitle(r'$\text{Convergencia de Valores } V(s) \text{ mediante } TD(0)$', fontsize=16)

        # 1. Definimos la misma paleta de colores que en el otro código
        states_order = list(self.state_values.keys())
        colormap = plt.get_cmap('tab20')
        colors = [colormap(i) for i in np.linspace(0, 1, len(states_order))]
        
        idx = 0
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                # 2. Le pasamos el color correspondiente al índice actual
                axs[i, j].plot(data[:, idx], color=colors[idx], linewidth=2)
                
                axs[i, j].set_title(f'Estado ({i},{j})', fontsize=12)
                axs[i, j].grid(True, alpha=0.3)
                
                # 3. Opcional: poner el fondo de un color suave si es el bloqueo o premios
                if (i, j) == BLOCKED_STATE:
                    axs[i, j].set_facecolor('#f0f0f0') # Gris para la pared
                elif (i, j) == WIN_STATE:
                    axs[i, j].set_facecolor('#e6ffed') # Verde suave para ganar
                elif (i, j) == LOSE_STATE:
                    axs[i, j].set_facecolor("#e7b6c2c5")
                
                idx += 1
        
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])
        plt.show()

if __name__ == "__main__":
    ag = Agent()
    ag.train(5000) # Entrenar con más rondas para ver convergencia real
    ag.show_values()
    ag.plot_convergence()