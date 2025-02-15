import tkinter as tk
import random
from tkinter import messagebox

class PuzzleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Rompecabezas de Números")
        self.score = 0
        self.level = 1
        self.time_limit = 60
        self.lives = 2
        self.target_sum = random.randint(12, 20)
        self.selected_tile = None
        self.board = []
        self.timer_running = False  # Para controlar si el temporizador está corriendo
        self.create_widgets()

    def create_widgets(self):
        self.menu_frame = tk.Frame(self.root, bg="lightblue")
        self.menu_frame.pack(pady=20)

        # Botón para iniciar el juego
        self.start_button = tk.Button(self.menu_frame, text="Comenzar Juego", font=("Arial", 16),
                                      command=self.start_game_button, bg="green", fg="white", relief="raised")
        self.start_button.pack(pady=10)

        # Instrucciones
        self.instructions_label = tk.Label(self.menu_frame, text="¡Haz clic en las casillas para intercambiarlas y alcanzar el objetivo!", font=("Arial", 12), bg="lightblue")
        self.instructions_label.pack(pady=10)

        # Estadísticas
        self.score_label = tk.Label(self.menu_frame, text=f"Puntuación: {self.score}", font=("Arial", 12), bg="lightblue")
        self.score_label.pack(side=tk.LEFT, padx=10)

        self.time_label = tk.Label(self.menu_frame, text=f"Tiempo: {self.time_limit}", font=("Arial", 12), bg="lightblue")
        self.time_label.pack(side=tk.LEFT, padx=10)

        self.lives_label = tk.Label(self.menu_frame, text=f"Vidas: {self.lives}", font=("Arial", 12), bg="lightblue")
        self.lives_label.pack(side=tk.LEFT, padx=10)

        self.target_label = tk.Label(self.menu_frame, text=f"Objetivo: {self.target_sum}", font=("Arial", 12), bg="lightblue")
        self.target_label.pack(side=tk.LEFT, padx=10)

    def generate_complex_board(self):
        # Generamos el tablero con valores aleatorios entre 1 y 5
        self.board = [random.randint(1, 5) for _ in range(16)]

    def start_game_button(self):
        # Deshabilitar el botón de inicio después de hacer clic
        self.start_button.config(state=tk.DISABLED)

        # Reestablecer el tiempo, puntuación, nivel y vidas
        self.time_limit = 60
        self.score = 0
        self.level = 1
        self.lives = 2
        self.target_sum = random.randint(12, 20)
        self.timer_running = False  # Reinicia el estado del temporizador

        # Generar el tablero y mostrarlo
        self.generate_complex_board()
        self.create_board_buttons()

        # Actualizar las estadísticas
        self.update_lives()
        self.update_score()
        self.update_target()

        # Iniciar el temporizador
        self.start_timer()

    def create_board_buttons(self):
        # Asegurarse de eliminar el marco de botones existente, si hay uno
        if hasattr(self, 'board_frame'):
            self.board_frame.destroy()

        # Crear el marco de los botones del tablero
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(pady=20)

        # Crear los botones para el tablero
        self.buttons = []
        for i in range(4):
            row = []
            for j in range(4):
                btn = tk.Button(self.board_frame, text="", width=5, height=2, font=("Arial", 16, "bold"),
                                bg=random.choice(["#FF6347", "#4CAF50", "#008CBA", "#FFD700", "#FF69B4", "#8A2BE2"]),
                                relief="raised", command=lambda x=i, y=j: self.select_tile(x, y))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)
        self.update_board()

    def update_board(self):
        # Actualizar los botones con los valores del tablero
        for i in range(4):
            for j in range(4):
                value = self.board[i * 4 + j]
                self.buttons[i][j].config(text=str(value))

    def select_tile(self, x, y):
        # Seleccionar el tile para intercambiar
        if self.selected_tile is None:
            self.selected_tile = (x, y)
        else:
            self.swap_tiles(x, y)
            self.selected_tile = None

    def swap_tiles(self, x, y):
        # Intercambiar los tiles seleccionados
        x1, y1 = self.selected_tile
        idx1, idx2 = x1 * 4 + y1, x * 4 + y
        self.board[idx1], self.board[idx2] = self.board[idx2], self.board[idx1]
        self.update_board()
        self.check_sum_condition()

    def check_sum_condition(self):
        # Verificar si las sumas de filas y columnas cumplen con el objetivo
        row_sums = [sum(self.board[i * 4:(i + 1) * 4]) for i in range(4)]
        col_sums = [sum(self.board[i::4]) for i in range(4)]

        if all(s == self.target_sum for s in row_sums) and all(s == self.target_sum for s in col_sums):
            self.score += 100
            self.update_score()
            self.level_up()

    def level_up(self):
        # Aumentar el nivel y el objetivo
        self.level += 1
        self.target_sum = random.randint(12, 20) + self.level * 2
        self.time_limit += 10
        messagebox.showinfo("Nivel Avanzado", f"¡Felicidades! Has alcanzado el nivel {self.level}")
        self.generate_complex_board()
        self.update_board()
        self.update_target()

    def start_timer(self):
        # Iniciar el temporizador solo si no está corriendo
        if not self.timer_running:
            self.timer_running = True
            self.update_timer()

    def update_timer(self):
        # Actualizar el tiempo y manejar el temporizador
        if self.time_limit > 0:
            self.time_limit -= 1
            self.time_label.config(text=f"Tiempo: {self.time_limit}")
            self.root.after(1000, self.update_timer)
        else:
            self.lose_life()

    def lose_life(self):
        # Manejar la pérdida de vida
        if self.lives > 1:
            self.lives -= 1
            self.time_limit = 60
            self.timer_running = False  # Detener el temporizador
            messagebox.showwarning("Oportunidad Perdida", f"¡Cuidado! Te quedan {self.lives} vidas. ¡Sigue intentando!")
            self.update_lives()
        else:
            messagebox.showinfo("Fin del Juego", "Has perdido todas tus vidas. ¡Intenta de nuevo!")
            self.start_game_button()

    def update_lives(self):
        # Actualizar las vidas en la interfaz
        self.lives_label.config(text=f"Vidas: {self.lives}")

    def update_score(self):
        # Actualizar la puntuación en la interfaz
        self.score_label.config(text=f"Puntuación: {self.score}")

    def update_target(self):
        # Actualizar el objetivo en la interfaz
        self.target_label.config(text=f"Objetivo: {self.target_sum}")


if __name__ == "__main__":
    root = tk.Tk()
    game = PuzzleGame(root)
    root.mainloop()
