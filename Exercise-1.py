import tkinter as tk
import random

difficulty = ""
num1 = 0
num2 = 0
operation = ""
correct_answer = 0
attempts = 0
score = 0
question_number = 0
question_finished = False

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
    global num1, num2, attempts, question_number, question_finished

    num1 = randomInt()
    num2 = randomInt()

    attempts = 0
    answer_entry.delete(0, tk.END)

    question_number += 1

    question_finished = False

    decideOperation()
    calculateAnswer()
    problem_label.config(text=f"Question {question_number} : {num1} {operation} {num2}")


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
    global attempts, score, question_finished

    if attempts >= 2:
        return

    if question_finished:
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
        question_finished = True

        if attempts == 0:
            score += 10
            question_label.config(text = "Correct! well done! You earned 10 points!")
            score_label.config(text ="Score: " + str(score))
            root.after(1000, nextQuestion)

        else:
            score +=5
            question_label.config(text = "Correct! You earned 5 points!")
            score_label. config(text ="Score: " + str(score))
            root.after(1000, nextQuestion)

    else:
        attempts += 1

        if attempts < 2:
            question_label.config(text = "Incorrect! Try again. One attempt left! ")
            

        else:
            question_finished = True
            question_label.config(text = "No more attempts! The answer was" + str(correct_answer))
            root.after(1000, nextQuestion)

def nextQuestion():
    if question_number < 10:
        displayProblem()

    else:
        question_label.config(text = "Quiz completed!")
        problem_label.config(text = "You finished all 10 questions!")
    
        
button_Easy = tk.Button(root, text = "Easy", font =("Arial", 18), command=choose_easy)
button_Easy.pack(pady = 10)

button_Medium = tk.Button(root, text = "Medium", font = ("Arial", 18), command=choose_medium)
button_Medium.pack(pady = 10)

button_Hard = tk.Button(root, text = "Hard", font = ("Arial", 18), command=choose_hard)
button_Hard.pack(pady = 10)

submit_button = tk.Button (root, text = "Submit Answer", font = ("Arial", 16), command=isCorrect)
submit_button.pack(pady=10)

root.mainloop()

