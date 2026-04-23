import sys
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton, QFrame)
from PyQt6.QtCore import QTimer, Qt
import pyqtgraph as pg
from scipy.linalg import solve_discrete_are

class MRA_Final_Theory_Validation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RL Control - Validación Teoría Tabla 7 (Ejemplo 6)")
        self.resize(1300, 850)
        
        # --- Parámetros de la Tabla 6 y 7 ---
        self.A = np.array([[1.8980, -0.9048], [1.0, 0.0]])
        self.B = np.array([[1.0], [0.0]])
        self.Q = np.eye(2)
        self.R = 2.0
        self.gamma = 0.999
        self.f_olvido = 0.99
        self.con_error_k = 0.1
        self.N = 4000
        self.n_ls = 7
        
        # --- Valores Óptimos Extraídos de la Tabla 7 ---
        # Estos son los valores hacia donde DEBE converger W
        self.W_target = [17.2962, -8.6202, 9.5272, 6.0227, -5.5512, 8.1353]
        self.K_target = [1.17138, -0.68253]
        
        self.reset_variables()
        self.init_ui()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)
        self.timer.start(15)

    def reset_variables(self):
        # H inicial "Arbitraria" de la Tabla 7
        # W_init = [16, -7, 7, 7, -4, 9] -> Convertido a Matriz H
        self.H_init = np.array([[16.0, -3.5, 3.5], [-3.5, 7.0, -2.0], [3.5, -2.0, 9.0]])
        self.K = (-(1.0 / self.H_init[2, 2]) * self.H_init[2, 0:2]).reshape(1, 2)
        self.x = np.array([[5.0], [-4.0]])
        self.W_H = np.zeros((6, 1))
        self.P_n = np.eye(6) * 1000 # Escalamiento por 1000 según texto
        self.phi_ls = np.zeros((6, self.n_ls))
        self.phi1_ls = np.zeros((6, self.n_ls))
        self.r_ls = np.zeros((self.n_ls, 1))
        self.iter = 1
        self.pos_history = []
        self.w_history = [[] for _ in range(6)]
        self.h_actual = np.zeros((3, 3))

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)

        # Izquierda: Animación y Pesos W
        left_layout = QVBoxLayout()
        self.canvas = pg.PlotWidget(title="Masa (x_1)")
        self.canvas.showGrid(x=True, y=True)
        self.canvas.setYRange(-2, 2)
        self.rect = pg.ScatterPlotItem(size=30, brush='r')
        self.canvas.addItem(self.rect)
        left_layout.addWidget(self.canvas)

        self.plot_w = pg.PlotWidget(title="Convergencia del Vector W")
        self.plot_w.setXRange(0, self.N)
        self.plot_w.addLegend()
        self.w_curves = []
        for i in range(6):
            color = pg.intColor(i)
            self.w_curves.append(self.plot_w.plot(pen=pg.mkPen(color, width=1), name=f"W{i+1}"))
            # Target de la Tabla 7
            target_line = pg.InfiniteLine(pos=self.W_target[i], angle=0, 
                                          pen=pg.mkPen(color, width=1, style=Qt.PenStyle.DashLine))
            self.plot_w.addItem(target_line)
        
        left_layout.addWidget(self.plot_w)
        main_layout.addLayout(left_layout, stretch=1)

        # Derecha: Posición y Datos
        right_layout = QVBoxLayout()
        self.plot_res = pg.PlotWidget(title="Estados (Figura 52)")
        self.curve_pos = self.plot_res.plot(pen='y')
        right_layout.addWidget(self.plot_res)
        self.plot_res.showGrid(x=True, y=True)

        self.lbl_data = QLabel(""); self.lbl_data.setStyleSheet("font-family: monospace; font-size: 11px;")
        right_layout.addWidget(QLabel("<b>VALIDACIÓN EJEMPLO 6</b>"))
        right_layout.addWidget(self.lbl_data)

        self.btn_reset = QPushButton("REINICIAR ENTRENAMIENTO")
        self.btn_reset.clicked.connect(self.reset_variables)
        right_layout.addWidget(self.btn_reset)
        
        self.lbl_iter = QLabel("Iteración: 0")
        right_layout.addWidget(self.lbl_iter)
        main_layout.addLayout(right_layout, stretch=2)

    def step(self):
        if self.iter > self.N: return
        k = self.iter

        # --- SEÑAL MULTISENOIDAL EXACTA (Ecuación 133) ---
        excitacion = (np.sin(k)**3 * np.cos(k) + 
                      np.sin(2*k)**2 * np.cos(0.46*k) + 
                      np.sin(-1.4*k)**2 * np.cos(0.5*k) + 
                      np.sin(k)**5 + 
                      np.sin(0.5*k)**5 + 
                      0.4 * np.sin(1.99*k)**2 * np.cos(2*k) + 
                      0.4 * np.sin(18.0*k)**5)
        
        noise = 0.40099 * np.exp(-0.000269 * k) * excitacion
        
        # Control y Dinámica
        u = float(np.dot(self.K, self.x)) + noise
        x_curr, x_next = self.x, np.dot(self.A, self.x) + self.B * u
        u2 = float(np.dot(self.K, x_next))
        r_val = float(np.dot(np.dot(x_curr.T, self.Q), x_curr) + (u**2) * self.R)

        # Aprendizaje LS+RLS
        if self.iter <= self.n_ls:
            idx = self.iter - 1
            self.r_ls[idx, 0] = r_val
            self.phi_ls[:, idx] = [x_curr[0,0]**2, x_curr[0,0]*x_curr[1,0], x_curr[0,0]*u, x_curr[1,0]**2, x_curr[1,0]*u, u**2]
            self.phi1_ls[:, idx] = [x_next[0,0]**2, x_next[0,0]*x_next[1,0], x_next[0,0]*u2, x_next[1,0]**2, x_next[1,0]*u2, u2**2]
            if self.iter == self.n_ls:
                diff_phi = self.phi_ls - self.phi1_ls
                self.W_H = np.dot(np.linalg.pinv(np.dot(diff_phi, diff_phi.T)), np.dot(diff_phi, self.r_ls))
        else:
            phi = np.array([x_curr[0,0]**2, x_curr[0,0]*x_curr[1,0], x_curr[0,0]*u, x_curr[1,0]**2, x_curr[1,0]*u, u**2]).reshape(-1, 1)
            phi1 = np.array([x_next[0,0]**2, x_next[0,0]*x_next[1,0], x_next[0,0]*u2, x_next[1,0]**2, x_next[1,0]*u2, u2**2]).reshape(-1, 1)
            vec_act = phi - self.gamma * phi1
            e_dt = r_val - float(np.dot(self.W_H.T, vec_act))
            
            p_scaled = (1.0 / self.f_olvido) * self.P_n
            den = (1.0/(1.0-self.f_olvido)) + float(np.dot(np.dot(vec_act.T, p_scaled), vec_act))
            L = np.dot(p_scaled, vec_act) / den
            self.W_H += L * e_dt
            self.P_n = np.dot((np.eye(6) - np.dot(L, vec_act.T)), p_scaled)

            # --- AQUÍ PONES LA CORRECCIÓN DE SIMETRÍA ---
            self.P_n = 0.5 * (self.P_n + self.P_n.T)
            # --------------------------------------------
            
            W = self.W_H.flatten()
            self.h_actual = np.array([[W[0], W[1]/2, W[2]/2], [W[1]/2, W[3], W[4]/2], [W[2]/2, W[4]/2, W[5]]])

            if abs(e_dt) < self.con_error_k:
                if abs(self.h_actual[2, 2]) > 1e-4:
                    self.K = (-(1.0 / self.h_actual[2, 2]) * self.h_actual[2, 0:2]).reshape(1, 2)

        # Actualización de UI
        self.rect.setData(x=[0], y=[float(x_next[0,0])])
        self.pos_history.append(float(x_next[0,0]))
        self.curve_pos.setData(self.pos_history[-800:])
        
        W_vals = self.W_H.flatten()
        for j in range(6):
            self.w_history[j].append(W_vals[j])
            self.w_curves[j].setData(self.w_history[j])

        self.lbl_data.setText(
            f"K RL:  {self.K[0,0]:.4f}, {self.K[0,1]:.4f}\n"
            f"K OPT: {self.K_target[0]:.4f}, {self.K_target[1]:.4f}\n\n"
            f"W1 (h11): {W_vals[0]:.4f} (Target: {self.W_target[0]})\n"
            f"W6 (h33): {W_vals[5]:.4f} (Target: {self.W_target[5]})"
        )
        self.lbl_iter.setText(f"Iteración: {self.iter} / {self.N}")
        self.x = x_next
        self.iter += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    sim = MRA_Final_Theory_Validation()
    sim.show()
    sys.exit(app.exec())