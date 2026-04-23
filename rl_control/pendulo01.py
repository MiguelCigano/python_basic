import sys
import numpy as np
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton)
from PyQt6.QtCore import QTimer, Qt
import pyqtgraph as pg
from scipy.linalg import solve_discrete_are

class RLS_Pendulum_Final_Reference(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RL Control - Péndulo Físico (Líneas de Referencia DARE)")
        self.resize(1400, 900)
        
        # --- 1. CONFIGURACIÓN DE LA PLANTA ---
        self.A = np.array([[0.99, 0.05], [-0.2, 0.95]]) 
        self.B = np.array([[0.001], [0.05]])
        self.Q = np.diag([10.0, 1.0]) 
        self.R = 1.0                  
        self.gamma = 0.99
        self.f_olvido = 0.995         
        self.N = 5000
        self.n_ls = 15 

        # --- 2. CÁLCULO PREVIO DE REFERENCIAS (SOLO PARA PINTAR) ---
        # Resolvemos Riccati fuera del algoritmo para saber el "Target"
        try:
            P_opt = solve_discrete_are(self.A, self.B, self.Q, self.R)
            K_opt = np.linalg.inv(self.R + self.B.T @ P_opt @ self.B) @ (self.B.T @ P_opt @ self.A)
            H_opt = np.zeros((3, 3))
            H_opt[0:2, 0:2] = self.Q + self.gamma * self.A.T @ P_opt @ self.A
            H_opt[0:2, 2:3] = self.gamma * self.A.T @ P_opt @ self.B
            H_opt[2:3, 0:2] = self.gamma * self.B.T @ P_opt @ self.A
            H_opt[2, 2] = self.R + self.gamma * self.B.T @ P_opt @ self.B
            
            self.W_target = [H_opt[0,0], 2*H_opt[0,1], 2*H_opt[0,2], H_opt[1,1], 2*H_opt[1,2], H_opt[2,2]]
            self.K_target = K_opt.flatten()
        except:
            self.W_target = [0]*6
            self.K_target = [0]*2

        self.reset_variables()
        self.init_ui()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.step)
        self.timer.start(20)

    def reset_variables(self):
        self.H = np.eye(3) * 5.0
        self.actualizar_K()
        self.x = np.array([[0.6], [0.0]]) # Ángulo inicial
        self.W_H = np.zeros((6, 1))
        self.P_n = np.eye(6) * 100 
        self.phi_ls = np.zeros((6, self.n_ls))
        self.phi1_ls = np.zeros((6, self.n_ls))
        self.r_ls = np.zeros((self.n_ls, 1))
        self.iter = 1
        self.theta_history = []
        self.w_history = [[] for _ in range(6)]

    def actualizar_K(self):
        Huu = self.H[2, 2]
        if abs(Huu) < 0.1: Huu = 0.1 * np.sign(Huu) if Huu != 0 else 0.1
        self.K = (-(1.0 / Huu) * self.H[2, 0:2]).reshape(1, 2)
        self.K = np.clip(self.K, -10.0, 10.0)

    def init_ui(self):
        cw = QWidget(); self.setCentralWidget(cw)
        layout = QHBoxLayout(cw)
        left_col = QVBoxLayout()
        
        self.view = pg.PlotWidget(title="Péndulo en Tiempo Real"); self.view.setAspectLocked(True)
        self.view.setXRange(-1.5, 1.5); self.view.setYRange(-1.5, 0.5)
        self.arm = pg.PlotCurveItem(pen=pg.mkPen('w', width=4))
        self.mass = pg.ScatterPlotItem(size=20, brush='b')
        self.view.addItem(self.arm); self.view.addItem(self.mass)
        left_col.addWidget(self.view)
        
        # Gráfica de convergencia con líneas de referencia punteadas
        self.plot_w = pg.PlotWidget(title="Pesos del Crítico W (Sólido) vs Óptimo DARE (Punteado)")
        self.w_curves = []
        for i in range(6):
            color = pg.intColor(i)
            self.w_curves.append(self.plot_w.plot(pen=pg.mkPen(color, width=2)))
            # Línea de referencia inamovible
            t_line = pg.InfiniteLine(pos=self.W_target[i], angle=0, 
                                     pen=pg.mkPen(color, width=1, style=Qt.PenStyle.DashLine))
            self.plot_w.addItem(t_line)
        
        left_col.addWidget(self.plot_w)
        layout.addLayout(left_col, 2)

        right_col = QVBoxLayout()
        self.plot_theta = pg.PlotWidget(title="Ángulo (rad)"); self.curve_theta = self.plot_theta.plot(pen='y')
        right_col.addWidget(self.plot_theta)
        self.lbl = QLabel(); self.lbl.setStyleSheet("background: #111; color: #0f0; font-family: monospace; padding: 10px;")
        right_col.addWidget(self.lbl)
        btn = QPushButton("REINICIAR"); btn.clicked.connect(self.reset_variables); right_col.addWidget(btn)
        layout.addLayout(right_col, 1)

    def step(self):
        if self.iter > self.N: return
        
        # Ruido de exploración (necesario para el aprendizaje)
        noise = 0.1 * np.exp(-0.0005 * self.iter) * np.sin(self.iter * 0.2)
        u = float(self.K @ self.x) + noise
        u = np.clip(u, -15, 15)
        
        xk = self.x
        xk_next = self.A @ xk + self.B * u
        u_next = float(self.K @ xk_next)
        rk = float(xk.T @ self.Q @ xk + (u**2) * self.R)
        
        phi = np.array([xk[0,0]**2, xk[0,0]*xk[1,0], xk[0,0]*u, xk[1,0]**2, xk[1,0]*u, u**2]).reshape(-1, 1)
        phi_next = np.array([xk_next[0,0]**2, xk_next[0,0]*xk_next[1,0], xk_next[0,0]*u_next, 
                             xk_next[1,0]**2, xk_next[1,0]*u_next, u_next**2]).reshape(-1, 1)

        # --- APRENDIZAJE RLS (Sin participación del DARE) ---
        if self.iter <= self.n_ls:
            idx = self.iter - 1
            self.r_ls[idx, 0] = rk
            self.phi_ls[:, idx] = phi.flatten()
            self.phi1_ls[:, idx] = phi_next.flatten()
            if self.iter == self.n_ls:
                diff = self.phi_ls - self.phi1_ls
                self.W_H = np.linalg.pinv(diff @ diff.T + np.eye(6)*1e-6) @ diff @ self.r_ls
        else:
            vec_act = phi - self.gamma * phi_next
            e_dt = rk - float(self.W_H.T @ vec_act)
            p_scaled = self.P_n / self.f_olvido
            den = 1.0 + float(vec_act.T @ p_scaled @ vec_act)
            L = (p_scaled @ vec_act) / den
            
            self.W_H += np.clip(L * e_dt, -10, 10)
            self.P_n = (np.eye(6) - L @ vec_act.T) @ p_scaled
            self.P_n = 0.5 * (self.P_n + self.P_n.T)

            W = self.W_H.flatten()
            self.H = np.array([[W[0], W[1]/2, W[2]/2], [W[1]/2, W[3], W[4]/2], [W[2]/2, W[4]/2, W[5]]])
            self.actualizar_K()

        # --- ACTUALIZACIÓN DE UI ---
        theta = float(xk_next[0,0])
        px, py = np.sin(theta), -np.cos(theta)
        self.arm.setData(x=[0, px], y=[0, py]); self.mass.setData(x=[px], y=[py])
        self.theta_history.append(theta); self.curve_theta.setData(self.theta_history[-800:])
        for j in range(6):
            self.w_history[j].append(float(self.W_H[j]))
            self.w_curves[j].setData(self.w_history[j])

        self.lbl.setText(f"ITER: {self.iter} | THETA: {theta:.3f}\nK RL: [{self.K[0,0]:.2f}, {self.K[0,1]:.2f}]\nK OPT: [{self.K_target[0]:.2f}, {self.K_target[1]:.2f}]")
        self.x = xk_next
        self.iter += 1

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = RLS_Pendulum_Final_Reference(); ex.show()
    sys.exit(app.exec())