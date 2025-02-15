import tkinter as tk
from tkinter import messagebox, ttk
import random

class SequenceGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Juego de Secuencia Numérica")
        self.root.geometry("600x400")
        self.root.configure(bg="#E6F7FF")
        
        self.score = 0
        self.difficulty = "Fácil"
        self.time_limit = 5  # Tiempo límite en segundos
        self.timer_running = False
        self.game_started = False  # Controla si el juego ha comenzado
        
        self.create_widgets()
        self.start_game()  # Comienza el juego automáticamente cuando se inicializa
    
    def create_widgets(self):
        title = tk.Label(self.root, text="¡Bienvenido al Juego de Secuencias!", font=("Arial", 18, "bold"), bg="#E6F7FF", fg="#004D99")
        title.pack(pady=10)
        
        self.label_score = tk.Label(self.root, text="Puntuación: 0", font=("Arial", 14), bg="#E6F7FF", fg="#004D99")
        self.label_score.pack(pady=5)
        
        self.label_sequence = tk.Label(self.root, text="Secuencia en curso...", font=("Arial", 18, "bold"), bg="#E6F7FF", fg="#004D99")
        self.label_sequence.pack(pady=20)
        
        self.label_hint = tk.Label(self.root, text="", font=("Arial", 12, "italic"), bg="#E6F7FF", fg="#FF5733")
        self.label_hint.pack(pady=5)
        
        self.label_timer = tk.Label(self.root, text=f"Tiempo restante: {self.time_limit}s", font=("Arial", 12, "bold"), bg="#E6F7FF", fg="#FF0000")
        self.label_timer.pack(pady=5)
        
        self.entry_answer = tk.Entry(self.root, font=("Arial", 16), justify="center")
        self.entry_answer.pack(pady=10)
        
        self.button_submit = tk.Button(self.root, text="Responder", command=self.check_answer, font=("Arial", 14), bg="#4CAF50", fg="white", state=tk.DISABLED)
        self.button_submit.pack(pady=10)
        
        difficulty_frame = tk.Frame(self.root, bg="#E6F7FF")
        difficulty_frame.pack(pady=10)
        
        tk.Label(difficulty_frame, text="Dificultad:", font=("Arial", 12, "bold"), bg="#E6F7FF").pack(side=tk.LEFT, padx=5)
        self.difficulty_select = ttk.Combobox(difficulty_frame, values=["Fácil", "Medio", "Difícil"], state="readonly")
        self.difficulty_select.set("Fácil")
        self.difficulty_select.pack(side=tk.LEFT, padx=5)
    
    def start_game(self):
        if self.game_started:
            return  # Evita reiniciar el juego si ya está en curso
        
        self.game_started = True
        self.score = 0
        self.label_score.config(text="Puntuación: 0")
        self.button_submit.config(state=tk.NORMAL)
        self.new_sequence()
    
    def new_sequence(self):
        if not self.game_started:
            return
        
        self.difficulty = self.difficulty_select.get()
        
        if self.difficulty == "Fácil":
            self.sequence = [random.randint(1, 10) * (2**i) for i in range(4)]
            self.label_hint.config(text="Pista: Multiplicación por 2")
            self.correct_answer = self.sequence[-1] * 2
        elif self.difficulty == "Medio":
            self.sequence = [random.randint(1, 5) * (i + 1) for i in range(4)]
            self.label_hint.config(text="Pista: Suma de un patrón")
            self.correct_answer = self.sequence[-1] + (self.sequence[-1] - self.sequence[-2])
        else:
            self.sequence = [random.randint(1, 10) * (i**2) for i in range(4)]
            self.label_hint.config(text="Pista: Secuencia basada en potencias")
            self.correct_answer = self.sequence[-1] + (self.sequence[-1] - self.sequence[-2])
        
        self.label_sequence.config(text=f"{', '.join(map(str, self.sequence[:-1]))}, ?")
        self.entry_answer.delete(0, tk.END)
        self.start_timer()
    
    def start_timer(self):
        self.time_remaining = self.time_limit
        self.timer_running = True
        self.update_timer()
    
    def update_timer(self):
        if self.timer_running and self.time_remaining > 0:
            self.label_timer.config(text=f"Tiempo restante: {self.time_remaining}s")
            self.time_remaining -= 1
            self.root.after(1000, self.update_timer)
        elif self.time_remaining == 0:
            self.timer_running = False
            messagebox.showerror("¡Tiempo agotado!", "Se acabó el tiempo. Inténtalo de nuevo.")
            self.new_sequence()
    
    def check_answer(self):
        if not self.timer_running:
            return
        
        try:
            user_answer = int(self.entry_answer.get())
            if user_answer == self.correct_answer:
                self.timer_running = False
                self.score += 100
                self.label_score.config(text=f"Puntuación: {self.score}")
                messagebox.showinfo("¡Correcto!", random.choice(["¡Excelente!", "¡Bien hecho!", "¡Sigue así!", "¡Eres un genio!"]))
                self.new_sequence()
            else:
                messagebox.showerror("¡Incorrecto!", random.choice(["¡Sigue intentando!", "¡No te rindas!", "¡Tú puedes!", "¡Prueba otra vez!"]))
        except ValueError:
            messagebox.showwarning("Error", "Ingresa un número válido")

if __name__ == "__main__":
    root = tk.Tk()
    game = SequenceGame(root)
    root.mainloop()
