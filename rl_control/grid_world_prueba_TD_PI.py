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

# AGENTE ACTOR-CRÍTICO (PI via TD)
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
        exp_prefs = np.exp(prefs - np.max(prefs)) # Estabilidad numérica
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
                
                # --- CÁLCULO DEL TD ERROR (La señal que guía a ambos) ---
                reward = env.get_reward()
                # Delta = R + gamma * V(s') - V(s)
                td_error = reward + self.gamma * self.state_values[env.state] - self.state_values[old_s]
                
                # 1. ACTUALIZAR CRÍTICO (Evaluación)
                self.state_values[old_s] += self.lr_v * td_error
                
                # 2. ACTUALIZAR ACTOR (Mejora de Política)
                # Si td_error > 0, la acción fue buena; si es < 0, fue mala.
                self.policy[old_s][action] += self.lr_p * td_error
            
            self.history_v.append(list(self.state_values.values()))

    def show_results(self):
        # Mostrar Valores
        # print("\n--- Critic Values V(s) ---")
        # for i in range(BOARD_ROWS):
        #     print("-" * 37)
        #     print("| " + " | ".join(f"{self.state_values[(i,j)]:6.2f}" for j in range(BOARD_COLS)) + " |")
        # print("-" * 37)

        print("\n+-- Critic Values V(s) table --+")
        for i in range(BOARD_ROWS):
            print("-" * 37)
            row = "| "
            for j in range(BOARD_COLS):
                # Lógica de símbolos para el Crítico
                if (i, j) == BLOCKED_STATE:
                    val_str = "  na  "
                elif (i, j) == WIN_STATE:
                    val_str = "  +   "
                elif (i, j) == LOSE_STATE:
                    val_str = "  -   "
                else:
                    # Imprimimos el valor numérico con 2 decimales
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

    # def plot_data(self):
    #     data = np.array(self.history_v)
    #     plt.figure(figsize=(10, 6))
    #     plt.plot(data)
    #     plt.title("Convergencia de Valores (Crítico) en Actor-Critic")
    #     plt.xlabel("Episodios")
    #     plt.ylabel("Valor V(s)")
    #     plt.show()

    # def plot_data(self):
    #     data = np.array(self.history_v)
    #     plt.figure(figsize=(12, 8))
        
    #     # Obtenemos las llaves (coordenadas) en el orden en que se guardaron
    #     # para poner el label correcto a cada columna de 'data'
    #     states_order = list(self.state_values.keys())
        
    #     for idx in range(data.shape[1]):
    #         state = states_order[idx]
    #         # No graficamos los estados terminales si prefieres (suelen ser constantes)
    #         # O los graficamos todos para ver el panorama completo
    #         plt.plot(data[:, idx], label=f"Estado {state}")
        
    #     plt.title("Convergencia de Valores V(s) por Coordenada (Actor-Critic)")
    #     plt.xlabel("Episodios")
    #     plt.ylabel("Valor Estimado V(s)")
        
    #     # Ponemos la leyenda fuera para que no tape las líneas
    #     plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small', ncol=2)
    #     plt.grid(True, alpha=0.3)
    #     plt.tight_layout()
    #     plt.show()

    # def plot_data(self):
    #     plt.rcParams.update({
    #         "text.usetex": True, # Pon True si tienes LaTeX instalado en el sistema, 
    #                               # si no, el motor interno de Matplotlib lo hará igual de bien.
    #         "font.family": "serif",
    #         "text.latex.preamble": r"\usepackage{amsmath}", # <--- ESTO FALTA
    #     })

    #     data = np.array(self.history_v)
    #     plt.figure(figsize=(12, 8))
        
    #     states_order = list(self.state_values.keys())
        
    #     # FORZAR PALETA TAB20
    #     colormap = plt.get_cmap('tab20')
    #     colors = [colormap(i) for i in np.linspace(0, 1, len(states_order))]
        
    #     for idx in range(data.shape[1]):
    #         state = states_order[idx]
    #         # Usamos el color del índice correspondiente
    #         plt.plot(data[:, idx], label=f"Estado {state}", color=colors[idx])
        
    #     plt.title("Convergencia de Valores V(s) por estado usando TD - PI (Actor-Critic)", fontsize=16)
    #     plt.xlabel("Episodios", fontsize=12)
    #     plt.ylabel("Valor predicho V(s)", fontsize=12)
    #     plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=12, ncol=2)
    #     plt.grid(True, alpha=0.3)
    #     plt.tight_layout()
    #     plt.show()

    def plot_data(self):
        # --- CONFIGURACIÓN ESTILO LATEX ---
        plt.rcParams.update({
            "text.usetex": True,
            "font.family": "serif",
            "text.latex.preamble": r"\usepackage{amsmath}",
        })

        data = np.array(self.history_v)
        fig, axs = plt.subplots(BOARD_ROWS, BOARD_COLS, figsize=(15, 10))
        
        # Título formal en LaTeX
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
                
                # Título del subplot: s = (i, j)
                axs[i, j].set_title(f'Estado ({i},{j})', fontsize=12)
                
                # Etiquetas de ejes minimalistas
                if j == 0: axs[i, j].set_ylabel(r'$V(s)$')
                if i == BOARD_ROWS - 1: axs[i, j].set_xlabel(r'$\text{Episodios}$')
                
                axs[i, j].grid(True, alpha=0.3, linestyle='--')
                
                # Colores de fondo para estados especiales
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
    agent.train(1) # Entrenamos un poco más para que el Actor se asiente
    agent.show_results()
    agent.plot_data()