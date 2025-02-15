import tkinter as tk
from tkinter import messagebox, ttk
import random
import math

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Adivina la Operación")
        self.root.geometry("600x500")  # Ajustamos el tamaño de la ventana
        self.root.configure(bg="#F5F5F5")
        
        self.score = 0
        self.difficulty = "Fácil"
        self.time_limit = 5  # Tiempo límite inicial en segundos
        self.timer_running = False
        self.game_started = False
        self.is_timer_active = False
        
        self.create_widgets()
    
    def create_widgets(self):
        # Título de la aplicación
        title = tk.Label(self.root, text="Adivina la Operación", font=("Arial", 24, "bold"), bg="#3C8DAD", fg="white")
        title.pack(pady=20)
        
        # Puntuación
        self.label_score = tk.Label(self.root, text="Puntuación: 0", font=("Arial", 16), bg="#F5F5F5", fg="#3C8DAD")
        self.label_score.pack(pady=5)
        
        # Mensaje de la operación
        self.label_operation = tk.Label(self.root, text="Operación: ?", font=("Arial", 18, "bold"), bg="#F5F5F5", fg="#3C8DAD")
        self.label_operation.pack(pady=20)
        
        # Entrada para la respuesta
        self.entry_answer = tk.Entry(self.root, font=("Arial", 16), justify="center")
        self.entry_answer.pack(pady=10)
        
        # Botón para enviar la respuesta
        self.button_submit = tk.Button(self.root, text="Responder", command=self.check_answer, font=("Arial", 14), bg="#4CAF50", fg="white", state=tk.DISABLED, width=20)
        self.button_submit.pack(pady=10)
        
        # Dificultad
        difficulty_frame = tk.Frame(self.root, bg="#F5F5F5")
        difficulty_frame.pack(pady=10)
        
        tk.Label(difficulty_frame, text="Dificultad:", font=("Arial", 14, "bold"), bg="#F5F5F5").pack(side=tk.LEFT, padx=5)
        self.difficulty_select = ttk.Combobox(difficulty_frame, values=["Fácil", "Medio", "Difícil"], state="readonly", font=("Arial", 14))
        self.difficulty_select.set("Fácil")
        self.difficulty_select.pack(side=tk.LEFT, padx=5)
        
        # Botón para iniciar el juego
        self.button_start = tk.Button(self.root, text="Iniciar Partida", command=self.start_game, font=("Arial", 16, "bold"), bg="#2196F3", fg="white", relief=tk.RAISED, height=2, width=20)
        self.button_start.pack(pady=20)
        
        # Temporizador
        self.label_timer = tk.Label(self.root, text=f"Tiempo restante: {self.time_limit}s", font=("Arial", 14, "bold"), bg="#F5F5F5", fg="#FF0000")
        self.label_timer.pack(pady=5)
    
    def start_game(self):
        if self.game_started:
            return  # Evitar reiniciar el juego si ya está en curso
        
        self.game_started = True
        self.score = 0
        self.label_score.config(text="Puntuación: 0")
        self.button_submit.config(state=tk.NORMAL)
        self.label_operation.config(text="Operación en curso...")
        self.button_start.config(state=tk.DISABLED, text="Juego en progreso...")
        self.new_operation()
    
    def new_operation(self):
        if not self.game_started:
            return
        
        self.difficulty = self.difficulty_select.get()
        
        # Generación de operaciones aleatorias
        self.operation_type = random.choice(["+", "-", "*", "/", "**", "sqrt"])
        
        if self.difficulty == "Fácil":
            self.num1 = random.randint(1, 10)
            self.num2 = random.randint(1, 10)
        elif self.difficulty == "Medio":
            self.num1 = random.randint(10, 50)
            self.num2 = random.randint(10, 50)
        else:
            self.num1 = random.randint(50, 100)
            self.num2 = random.randint(50, 100)
        
        # Evitar división por cero
        if self.operation_type == "/":
            self.num2 = random.randint(1, 10)
        
        # Crear la operación
        if self.operation_type == "+":
            self.correct_answer = self.num1 + self.num2
        elif self.operation_type == "-":
            self.correct_answer = self.num1 - self.num2
        elif self.operation_type == "*":
            self.correct_answer = self.num1 * self.num2
        elif self.operation_type == "/":
            self.correct_answer = round(self.num1 / self.num2, 2)
        elif self.operation_type == "**":
            self.correct_answer = self.num1 ** self.num2
        elif self.operation_type == "sqrt":
            self.correct_answer = round(math.sqrt(self.num1), 2)
        
        # Mostrar la operación en la interfaz y las opciones de respuesta
        self.operation_word = self.get_operation_word(self.operation_type)
        self.label_operation.config(text=f"¿Qué operación genera el resultado: {self.correct_answer}?")
        
        self.entry_answer.delete(0, tk.END)
        
        if self.score >= 200 and not self.is_timer_active:
            self.start_timer()
    
    def get_operation_word(self, operation_type):
        # Devolver el nombre de la operación según el tipo
        if operation_type == "+":
            return "Suma"
        elif operation_type == "-":
            return "Resta"
        elif operation_type == "*":
            return "Multiplicación"
        elif operation_type == "/":
            return "División"
        elif operation_type == "**":
            return "Potencia"
        elif operation_type == "sqrt":
            return "Raíz cuadrada"
    
    def start_timer(self):
        self.time_remaining = 10  # Empieza la cuenta regresiva a partir de 10 segundos
        self.is_timer_active = True
        self.update_timer()
    
    def update_timer(self):
        if self.is_timer_active and self.time_remaining > 0:
            self.label_timer.config(text=f"Tiempo restante: {self.time_remaining}s")
            self.time_remaining -= 1
            self.root.after(1000, self.update_timer)
        elif self.time_remaining == 0:
            self.is_timer_active = False
            messagebox.showerror("¡Tiempo agotado!", "Se acabó el tiempo. ¡Inténtalo de nuevo!")
            self.game_started = False
            self.start_game()
    
    def check_answer(self):
        if not self.game_started:
            return
        
        user_answer = self.entry_answer.get().strip().lower()
        
        if user_answer == self.operation_word.lower():  # Verificar la respuesta
            self.score += 100
            self.label_score.config(text=f"Puntuación: {self.score}")
            messagebox.showinfo("¡Correcto!", random.choice([
                "¡Excelente!",
                "¡Bien hecho!",
                "¡Sigue así!",
                "¡Impresionante!"
            ]))
            
            if self.score >= 200:
                self.start_timer()
            self.new_operation()
            
            # Subir dificultad cada 100 puntos
            if self.score % 100 == 0:
                self.update_difficulty()
        else:
            messagebox.showerror("¡Incorrecto!", random.choice([
                "¡Sigue intentándolo!",
                "¡No te rindas!",
                "¡Tú puedes!",
                "¡Prueba otra vez!"
            ]))
    
    def update_difficulty(self):
        if self.score >= 100 and self.difficulty == "Fácil":
            self.difficulty = "Medio"
            self.difficulty_select.set("Medio")
        elif self.score >= 200 and self.difficulty == "Medio":
            self.difficulty = "Difícil"
            self.difficulty_select.set("Difícil")

if __name__ == "__main__":
    root = tk.Tk()
    game = MathGame(root)
    root.mainloop()
