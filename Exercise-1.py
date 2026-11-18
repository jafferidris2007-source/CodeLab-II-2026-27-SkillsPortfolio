import tkinter as tk
import random

# All the Variables used to keep track of the quiz.
difficulty = "" #This variable will store the player's chosen difficulty.
num1 = 0 
num2 = 0 #These two variables will store the two numbers used in each maths question.
operation = "" #This variable will store either "+" or "-".
correct_answer = 0 #This variable will store the correct answer.
attempts = 0 #This variable will keep track of how many times the player has attempted the current question.
score = 0 #This variable will store the player's total points throughout the game.
question_number = 0 #This variable will track which question the player is currently in.
question_finished = False

#Creates the main application window.
root = tk.Tk()#Creates the window.
root.title("Math Challenge")#Used to display Math challenge at the top of the window.
root.geometry("600x459")#Creates the window with how many pixels.

#All the TKinter Label's, that are uesd to display text inside a window.
#To Display the game title
title = tk.Label(root, text="Math Challenge", font=("Arial", 24))
title.pack()#When creating a label, it doesnt mean it will appear in the window, that's why we need to use pack().

#To display the instructions and feedback.
question_label = tk.Label(root, text="Choose Your Difficulty.",font=("Arial", 18))
question_label.pack(pady = 30)

#To Display the current maths question.
problem_label = tk.Label(root, text="Your question will appear here", font=("Arial", 20))
problem_label.pack(pady=20)

#To display the player's current score.
score_label = tk.Label(root, text = "Score: 0", font = ("Arial", 16))
score_label.pack()

#It creates an input box so the player's can answer.
answer_entry = tk.Entry(root, font = ("Arial", 18)) #creates a box where the player can type.
answer_entry.pack(pady=10)


#All the Tkinter Functions

#It displays the difficulty selection menu.
def displayMenu():
    question_label.config(text="Choose Your Difficulty.")

#Functions for selecting the easy difficulty for the math question.
def choose_easy():
    global difficulty #It allows the function to change the variable created outside it.
    difficulty = "Easy" #It stores the difficulty selected by the player, which is easy in this case.
    
    button_Easy.pack_forget()
    button_Medium.pack_forget()
    button_Hard.pack_forget()

    question_label.config(text="Easy difficulty selected!")
    displayProblem() #This calls the function and display a new question.

#Functions for selecting the medium difficulty for the math question.
def choose_medium():
    global difficulty
    difficulty = "Medium"

    button_Easy.pack_forget()
    button_Medium.pack_forget()
    button_Hard.pack_forget()
    
    question_label.config(text="Medium difficulty selected!")
    displayProblem()

#Functions for selecting the hard difficulty for the math question.
def choose_hard():
    global difficulty
    difficulty = "Hard"

    button_Easy.pack_forget()
    button_Medium.pack_forget()
    button_Hard.pack_forget()

    question_label.config(text="Hard difficulty selected!")
    displayProblem()

#It generates random numbers depending on the selected difficulty.
def randomInt():
    if difficulty == "Easy":
        return random.randint(1, 9) #It generates a random number between 1 and 9, same for the other two.
    elif difficulty == "Medium":
        return random.randint(10, 99)#Oh and return sends that number back to wherever the function was called.
    elif difficulty == "Hard":
        return random.randint(1000, 9999)

#It generates and display a new maths question.
def displayProblem():
    global num1, num2, attempts, question_number, question_finished

    num1 = randomInt() #It generates the first number.
    num2 = randomInt() #It generates the second number.

    #It reset the attempts and clear's the previous answer
    attempts = 0
    answer_entry.delete(0, tk.END)

    #Makes the player move to the next question
    question_number += 1

    #It allow the player to answer the new question 
    question_finished = False
   
    #It choose's an operation and calculate the correct answer as well
    decideOperation()
    calculateAnswer()

    #It show's the main question on the window
    problem_label.config(text=f"Question {question_number} : {num1} {operation} {num2}")

#It randomly choose addition or subtraction
def decideOperation():
    global operation

    operation = random.choice(["+","-"]) #IT stores the randomly selected symbol.

    return operation #It sends the symbol back.

#It calculates the correct answer to the question
def calculateAnswer():
    global correct_answer

    #It tells us that if the operation is +, Python adds the two numbers, and then stores it correct answer.
    if operation == "+":
        correct_answer = num1 + num2 

    #It tells us that if the operation is -, Python subtracts the two numbers, and then stores it correct answer.
    elif operation == "-":
        correct_answer = num1 - num2

    return correct_answer

#It checks whether the player's answer is correct or not
def isCorrect():
    global attempts, score, question_finished

    #It prevents repeated submissions so the player cannot earn extra points.
    if attempts >= 2:
        return

    if question_finished:
        return

    #It gets the answer entered by the player's
    user_answer = answer_entry.get()

    #It check's if the answer box is not empty
    if user_answer == "":
        question_label.config(text = "Please enter an answer!") 
        return #stops the function if no answer was entered.

    #It make's sure the answer is a valid number.
    try:
        user_answer = int(user_answer)
    except ValueError:
        question_label.config(text = "Please enter a valid number!")
        return

    #It compare's the players answer with the correct answer, to see if it correct
    if user_answer == correct_answer:
        question_finished = True

        #It award's the player 10 points for the first attempt, if the answer is correct
        if attempts == 0:
            score += 10
            question_label.config(text = "Correct! well done! You earned 10 points!")
            score_label.config(text ="Score: " + str(score))
            root.after(1000, nextQuestion)

        #IT award's the player 5 points for the second attempt..
        else:
            score +=5
            question_label.config(text = "Correct! You earned 5 points!")
            score_label. config(text ="Score: " + str(score))
            root.after(1000, nextQuestion)

    else:
        #It increase's the number of attempts after a wrong answer
        attempts += 1

        if attempts < 2:
            question_label.config(text = "Incorrect! Try again. One attempt left! ")
            

        else:
            #Finish the question when both attempts are used.
            question_finished = True
            question_label.config(text = "No more attempts! The answer was" + str(correct_answer))
            root.after(1000, nextQuestion)

#It move's to the next question or finish the quiz.
def nextQuestion():
    if question_number < 10:
        displayProblem()

    else:
        displayResults()

#It give's the player a grade based on their final score.
def calculateGrade():
    if score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 50:
        return "D"
    else:
        return "F"

#It displays the final score and grade.
def displayResults():
    grade = calculateGrade()#It calls your grade function and stores the result.

    question_label.config(text="Quiz completed!")
    problem_label.config(text="Final Score: " + str(score) + "/100")
    score_label.config(text="Grade: " + grade)#It displays the player's grade

    replay_button.pack(pady=10)

#It resets all the quiz variables so the player can play again.
def playAgain():
    global difficulty, score, question_number, attempts, question_finished

    difficulty = ""
    score = 0
    question_number = 0
    attempts = 0
    question_finished = False

    #It resets the labels and answer box.
    displayMenu()
    problem_label.config(text="Your question will appear here")
    score_label.config(text="Score: 0")
    answer_entry.delete(0, tk.END)

    button_Easy.pack(pady=10)
    button_Medium.pack(pady=10)
    button_Hard.pack(pady=10)

    replay_button.pack_forget()
    
#All the TKinter buttons. In Tkinter, we use tk.Button() to create a button. 

#It create's the buttons used to select the easy difficulty       
button_Easy = tk.Button(root, text = "Easy", font =("Arial", 18), command=choose_easy)
button_Easy.pack(pady = 10)

#It create's the buttons used to select the medium difficulty 
button_Medium = tk.Button(root, text = "Medium", font = ("Arial", 18), command=choose_medium)
button_Medium.pack(pady = 10)

#It create's the buttons used to select the hard difficulty 
button_Hard = tk.Button(root, text = "Hard", font = ("Arial", 18), command=choose_hard)
button_Hard.pack(pady = 10)

#It create's the button used to submit an answer by the player
submit_button = tk.Button (root, text = "Submit Answer", font = ("Arial", 16), command=isCorrect)
submit_button.pack(pady=10)

#It creates a button that allows the player to replay the quiz.
replay_button = tk.Button(root, text="Play Again", font=("Arial", 16), command=playAgain)

#root.mainloop() starts the window and keeps it running, thats why it's at the end of the whole code.
root.mainloop()
