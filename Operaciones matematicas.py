import tkinter as tk
from tkinter import messagebox
import random
import time
import math

class MathGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Operaciones Matemáticas Rápidas")
        self.root.geometry("500x350")

        self.score = 0
        self.time_limit = 5
        self.timer_running = False
        self.user_answered = False  

        self.create_widgets()
        self.new_question()

    def create_widgets(self):
        self.label_score = tk.Label(self.root, text="Puntuación: 0", font=("Arial", 14))
        self.label_score.pack(pady=10)

        self.label_question = tk.Label(self.root, text="", font=("Arial", 18))
        self.label_question.pack(pady=20)

        self.entry_answer = tk.Entry(self.root, font=("Arial", 16))
        self.entry_answer.pack(pady=10)

        self.button_submit = tk.Button(self.root, text="Responder", command=self.check_answer, font=("Arial", 14))
        self.button_submit.pack(pady=10)

        self.label_timer = tk.Label(self.root, text="", font=("Arial", 14), fg="red")
        self.label_timer.pack()

    def new_question(self):
        operation_type = random.choice(["+", "-", "×", "÷", "%", "**", "√", "!", "combo"])

        if operation_type in ["+", "-", "×", "÷", "%", "**"]:
            self.num1 = random.randint(10, 100)
            self.num2 = random.randint(1, 50)

            if operation_type == "+":
                self.correct_answer = self.num1 + self.num2
            elif operation_type == "-":
                self.correct_answer = self.num1 - self.num2
            elif operation_type == "×":
                self.correct_answer = self.num1 * self.num2
            elif operation_type == "÷":
                while self.num2 == 0 or self.num1 % self.num2 != 0:
                    self.num2 = random.randint(1, 50)
                self.correct_answer = self.num1 // self.num2
            elif operation_type == "%":
                self.correct_answer = self.num1 % self.num2
            elif operation_type == "**":
                self.num2 = random.randint(2, 3)
                self.correct_answer = self.num1 ** self.num2

            self.label_question.config(text=f"{self.num1} {operation_type} {self.num2} = ?")

        elif operation_type == "√":
            self.num1 = random.randint(1, 15) ** 2
            self.correct_answer = int(math.sqrt(self.num1))
            self.label_question.config(text=f"√{self.num1} = ?")

        elif operation_type == "!":
            self.num1 = random.randint(1, 6)
            self.correct_answer = math.factorial(self.num1)
            self.label_question.config(text=f"{self.num1}! = ?")

        elif operation_type == "combo":
            self.num1 = random.randint(1, 50)
            self.num2 = random.randint(1, 50)
            self.num3 = random.randint(1, 20)
            operation_combo = random.choice(["+ -", "× ÷"])

            if operation_combo == "+ -":
                self.correct_answer = self.num1 + self.num2 - self.num3
                self.label_question.config(text=f"{self.num1} + {self.num2} - {self.num3} = ?")
            else:
                while self.num3 == 0 or (self.num1 * self.num2) % self.num3 != 0:
                    self.num3 = random.randint(1, 20)
                self.correct_answer = (self.num1 * self.num2) // self.num3
                self.label_question.config(text=f"{self.num1} × {self.num2} ÷ {self.num3} = ?")

        self.entry_answer.delete(0, tk.END)
        self.start_time = time.time()
        self.timer_running = True
        self.user_answered = False  
        self.update_timer()

    def update_timer(self):
        if self.timer_running and not self.user_answered:
            elapsed_time = time.time() - self.start_time
            remaining_time = max(0, self.time_limit - int(elapsed_time))
            self.label_timer.config(text=f"Tiempo restante: {remaining_time} s")

            if remaining_time > 0:
                self.root.after(1000, self.update_timer)
            else:
                self.time_up()

    def check_answer(self):
        if not self.timer_running:
            return

        try:
            user_answer = int(self.entry_answer.get())
            self.user_answered = True  
            if user_answer == self.correct_answer:
                self.timer_running = False
                self.score += 1
                self.label_score.config(text=f"Puntuación: {self.score}")
                self.show_message(True)
            else:
                self.show_message(False)
        except ValueError:
            messagebox.showwarning("Error", "Ingresa un número válido")

    def time_up(self):
        if not self.user_answered:  
            self.timer_running = False
            messagebox.showwarning("¡Tiempo agotado!", "Se acabó el tiempo.")
            self.ask_replay()

    def show_message(self, correct):
        success_messages = ["¡Genial!", "¡Bien hecho!", "¡Sigue así!", "¡Eres increíble!", "¡Respuesta correcta!"]
        fail_messages = ["No te rindas, inténtalo de nuevo.", "¡Puedes mejorar!", "Sigue practicando, lo harás mejor."]

        if correct:
            if messagebox.askyesno("¡Correcto!", f"{random.choice(success_messages)}\n¿Jugar de nuevo?"):
                self.new_question()
            else:
                self.root.quit()
        else:
            messagebox.showerror("¡Incorrecto!", "Respuesta incorrecta.")
            self.ask_replay()

    def ask_replay(self):
        if messagebox.askyesno("¿Jugar de nuevo?", random.choice(["No te rindas, inténtalo de nuevo.", "¡Puedes mejorar!", "Sigue practicando, lo harás mejor."])):
            self.new_question()
        else:
            self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = MathGame(root)
    root.mainloop()
