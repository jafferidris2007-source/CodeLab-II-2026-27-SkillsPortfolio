import tkinter as tk
import random

difficulty = ""
num1 = 0
num2 = 0
operation = ""
correct_answer = 0
attempts = 0
score = 0

root = tk.Tk()
root.title("Math Challenge")
root.geometry("600x459")

title = tk.Label(root, text="Math Challenge", font=("Arial", 24))
title.pack()

question_label = tk.Label(root, text="Choose Your Difficulty.",font=("Arial", 18))
question_label.pack(pady = 30)

problem_label = tk.Label(root, text="Your question will appear here", font=("Arial", 20))
problem_label.pack(pady=20)

score_label = tk.Label(root, text = "Score: 0", font = ("Arial", 16))
score_label.pack()

answer_entry = tk.Entry(root, font = ("Arial", 18))
answer_entry.pack(pady=10)

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
    global num1, num2, attempts

    num1 = randomInt()
    num2 = randomInt()

    attempts = 0
    answer_entry.delete(0, tk.END)

    decideOperation()
    calculateAnswer()
    problem_label.config(text=f"{num1} {operation} {num2}")


def decideOperation():
    global operation

    operation = random.choice(["+","-"])

    return operation

def calculateAnswer():
    global correct_answer

    if operation == "+":
        correct_answer = num1 + num2

    elif operation == "-":
        correct_answer = num1 - num2

    return correct_answer

def isCorrect():
    global attempts, score

    if attempts >= 2:
        return

    user_answer = answer_entry.get()

    if user_answer == "":
        question_label.config(text = "Please enter an answer!") 
        return
    
    try:
        user_answer = int(user_answer)
    except ValueError:
        question_label.config(text = "Please enter a valid number!")
        return

    if user_answer == correct_answer:

        if attempts == 0:
            score += 10
            question_label.config(text = "Correct! well done! You earned 10 points!")
            score_label.config(text = "Score:" + str(score))

        else:
            score +=5
            question_label.config(text = "Correct! You earnd 5 points!")

    else:
        attempts += 1

        if attempts < 2:
            question_label.config(text = "Incorrect! Try again. One attempt left! ")

        else:
            question_label.config(text = "No more attempts! The answer was" + str(correct_answer))
    
        
button_Easy = tk.Button(root, text = "Easy", font =("Arial", 18), command=choose_easy)
button_Easy.pack(pady = 10)

button_Medium = tk.Button(root, text = "Medium", font = ("Arial", 18), command=choose_medium)
button_Medium.pack(pady = 10)

button_Hard = tk.Button(root, text = "Hard", font = ("Arial", 18), command=choose_hard)
button_Hard.pack(pady = 10)

submit_button = tk.Button (root, text = "Submit Answer", font = ("Arial", 16), command=isCorrect)
submit_button.pack(pady=10)

root.mainloop()

