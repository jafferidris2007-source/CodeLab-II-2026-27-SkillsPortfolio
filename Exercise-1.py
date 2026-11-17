import tkinter as tk
import random

difficulty = ""
num1 = 0
num2 = 0
operation = ""

root = tk.Tk()
root.title("Math Challenge")
root.geometry("600x459")

title = tk.Label(root, text="Math Challenge", font=("Arial", 24))
title.pack()

question_label = tk.Label(root, text="Choose Your Difficulty.",font=("Arial", 18))
question_label.pack(pady = 30)

problem_label = tk.Label(root, text="Your question will appear here", font=("Arial", 20))
problem_label.pack(pady=20)

def choose_easy():
    global difficulty
    difficulty = "Easy"
    question_label.config(text="Easy difficulty selected!")
    displayProblem()

def choose_medium():
    global difficulty
    difficulty = "Medium"
    question_label.config(text="Medium difficulty selected!")
    displayProblem()
    
def choose_hard():
    global difficulty
    difficulty = "Hard"
    question_label.config(text="Hard difficulty selected!")
    displayProblem()

def randomInt():
    if difficulty == "Easy":
        return random.randint(1, 9)
    elif difficulty == "Medium":
        return random.randint(10, 99)
    elif difficulty == "Hard":
        return random.randint(1000, 9999)

def displayProblem():
    global num1, num2

    num1 = randomInt()
    num2 = randomInt()

    decideOperation()
    problem_label.config(text=f"{num1} {operation} {num2}")

def decideOperation():
    global operation

    operation = random.choice(["+","-"])

    return operation


button_Easy = tk.Button(root, text = "Easy", font =("Arial", 18), command=choose_easy)
button_Easy.pack(pady = 10)

button_Medium = tk.Button(root, text = "Medium", font = ("Arial", 18), command=choose_medium)
button_Medium.pack(pady = 10)

button_Hard = tk.Button(root, text = "Hard", font = ("Arial", 18), command=choose_hard)
button_Hard.pack(pady = 10)

root.mainloop()

