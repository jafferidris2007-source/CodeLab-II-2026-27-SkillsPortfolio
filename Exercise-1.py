import tkinter as tk
import random
from PIL import Image, ImageTk #NEW - Pillow (pip install pillow) lets the background pictures resize smoothly.

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
page = 1 #NEW - This variable stores which of the six pages is showing.

#NEW - Colours and font taken from the Surf Maths example.
INK, RED, SEA, GREEN, SAND = "#183c46", "#ab3f2e", "#096879", "#1b7f4b", "#ecd199"
FONT = "Trebuchet MS"
DESIGN_W, DESIGN_H = 1920, 1080 #The size the background pictures were drawn at. Every box below uses this size.

#NEW - Page 6 (results) uses the same picture as page 5.
BACKGROUNDS = {1: "Math-Quiz_first-page.png", 2: "Math-Quiz_second-page.png", 3: "Math-Quiz_third-page.png",
               4: "Math-Quiz_fourth-page.png", 5: "Math-Quiz_fifth-page.png", 6: "Math-Quiz_fifth-page.png"}

#Creates the main application window.
root = tk.Tk()#Creates the window.
root.title("Math Challenge")#Used to display Math challenge at the top of the window.
root.geometry("960x540")#Creates the window with how many pixels (same 16:9 shape as the pictures).
root.minsize(480, 270)
root.configure(bg=SAND)

#NEW - One canvas fills the window. The background picture and the progress bar are drawn on it.
screen = tk.Canvas(root, bg=SAND, highlightthickness=0)
screen.pack(fill="both", expand=True)
bg_item = screen.create_image(0, 0, anchor="nw")

widgets = [] #NEW - every label/entry/button is stored here so it can be repositioned when the window is resized.
loaded = {}

#NEW - Registers a widget with the pages it appears on, its box (x1, y1, x2, y2) in picture coordinates and its text size.
def addWidget(widget, pages, box, size, bold=True):
    widgets.append((widget, pages, box, size, bold))
    return widget

#NEW - Creates a button that blends into the picture (its face is cut out of the background).
def makeButton(text, command, color="white"):
    return tk.Button(screen, text=text, command=command, compound="center", fg=color, activeforeground=color,
                     bd=0, highlightthickness=0, relief="flat", cursor="hand2")


#All the TKinter Label's, that are uesd to display text inside a window.
#The titles are already in the background pictures, so there is no title label any more.

#To display "Question 3 of 10" (NEW).
progress_label = addWidget(tk.Label(screen, compound="center", bd=0, fg=INK), (5, 6), (470, 175, 950, 245), 40)

#To display the instructions and feedback.
question_label = addWidget(tk.Label(screen, text="", compound="center", bd=0, fg=SEA), (5, 6), (450, 605, 1470, 735), 40, False)

#To Display the current maths question.
problem_label = addWidget(tk.Label(screen, text="", compound="center", bd=0, fg=INK), (5, 6), (450, 330, 1470, 470), 86)

#To display the player's current score.
score_label = addWidget(tk.Label(screen, text="Score: 0", compound="center", bd=0, fg=RED), (5, 6), (970, 175, 1450, 245), 40)

#It creates an input box so the player's can answer.
answer_entry = addWidget(tk.Entry(screen, justify="center", bg="white", fg=INK, relief="flat",
                                  highlightthickness=3, highlightcolor=SEA, highlightbackground="#eaa96b"),
                         (5,), (800, 490, 1120, 585), 56, False)


#All the Tkinter Functions

#NEW - Shows feedback in the feedback label; green for good news, red for bad news.
def feedback(text, color=RED):
    question_label.config(text=text, fg=color)

#NEW - Draws the progress bar. It only counts questions that are FINISHED (correct, or both attempts used).
def updateProgress():
    screen.delete("bar")
    if page not in (5, 6):
        return
    done = max(0, question_number - (0 if question_finished else 1))
    progress_label.config(text="Quiz complete!" if page == 6 else "Question " + str(question_number) + " of 10")
    x1, x2, y, thick = 500, 1420, 290, 30
    X, Y = lambda v: left + v * scale, top + y * scale
    screen.create_line(X(x1), Y, X(x2), Y, width=thick * scale, capstyle="round", fill="#e3bd7c", tags="bar")
    if done:
        end = x1 + (x2 - x1) * done / 10
        screen.create_line(X(x1), Y, X(end), Y, width=thick * scale, capstyle="round", fill="#37aaa9", tags="bar")
        r = thick * 0.75 * scale
        screen.create_oval(X(end) - r, Y - r, X(end) + r, Y + r, fill="#ef5350", outline="white", width=3, tags="bar")

#NEW - Resizes the background and repositions every widget for the current page and window size.
def layout():
    global scale, left, top, bg_photo
    w, h = screen.winfo_width(), screen.winfo_height()
    if w < 100 or h < 100:
        return
    scale = min(w / DESIGN_W, h / DESIGN_H) #Keeps the 16:9 shape, so the buttons always line up with the artwork.
    left, top = (w - DESIGN_W * scale) / 2, (h - DESIGN_H * scale) / 2
    name = BACKGROUNDS[page]
    if name not in loaded:
        loaded[name] = Image.open(name).convert("RGB").resize((DESIGN_W, DESIGN_H))
    source = loaded[name]
    bg_photo = ImageTk.PhotoImage(source.resize((round(DESIGN_W * scale), round(DESIGN_H * scale)), Image.LANCZOS))
    screen.itemconfig(bg_item, image=bg_photo)
    screen.coords(bg_item, left, top)
    for widget, pages, (x1, y1, x2, y2), size, bold in widgets:
        if page not in pages:
            widget.place_forget()
            continue
        bw, bh = round((x2 - x1) * scale), round((y2 - y1) * scale)
        widget.config(font=(FONT, -max(8, round(size * scale)), "bold" if bold else "normal"))
        if not isinstance(widget, tk.Entry):
            widget.image = ImageTk.PhotoImage(source.crop((x1, y1, x2, y2)).resize((bw, bh), Image.LANCZOS))
            widget.config(image=widget.image, wraplength=bw - 10)
        widget.place(x=round(left + x1 * scale), y=round(top + y1 * scale), width=bw, height=bh)
    updateProgress()

resize_job = None
def onResize(event):
    global resize_job
    if resize_job:
        root.after_cancel(resize_job)
    resize_job = root.after(40, layout)

#NEW - Switches to page 1-6.
def showPage(number):
    global page
    page = number
    layout()
    if page == 5:
        answer_entry.focus_set()

#It displays the difficulty selection menu (page 2).
def displayMenu():
    showPage(2)

#Functions for selecting the easy difficulty for the math question.
def choose_easy():
    global difficulty #It allows the function to change the variable created outside it.
    difficulty = "Easy" #It stores the difficulty selected by the player, which is easy in this case.
    showPage(3) #Goes to the rules page.

#Functions for selecting the moderate difficulty for the math question.
def choose_medium():
    global difficulty
    difficulty = "Moderate"
    showPage(3)

#Functions for selecting the advanced difficulty for the math question.
def choose_hard():
    global difficulty
    difficulty = "Advanced"
    showPage(3)

#NEW - Page 3 -> page 4 (ready screen) -> page 5 (the quiz) after 2.5 seconds.
def paddleOut():
    showPage(4)
    root.after(2500, startQuiz)

def startQuiz():
    showPage(5)
    displayProblem()

#It generates random numbers depending on the selected difficulty.
def randomInt():
    if difficulty == "Easy":
        return random.randint(1, 9) #It generates a random number between 1 and 9, same for the other two.
    elif difficulty == "Moderate":
        return random.randint(10, 99)#Oh and return sends that number back to wherever the function was called.
    elif difficulty == "Advanced":
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
    problem_label.config(text=f"{num1} {operation} {num2} = ?")
    feedback("Type your answer below!", SEA)
    answer_entry.focus_set()
    updateProgress()

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
        feedback("Please enter an answer!") 
        return #stops the function if no answer was entered.

    #It make's sure the answer is a valid number.
    try:
        user_answer = int(user_answer)
    except ValueError:
        feedback("Please enter a valid number!")
        return

    #It compare's the players answer with the correct answer, to see if it correct
    if user_answer == correct_answer:
        question_finished = True
        updateProgress() #The bar only moves once the question is finished.

        #It award's the player 10 points for the first attempt, if the answer is correct
        if attempts == 0:
            score += 10
            feedback("Correct! well done! You earned 10 points!", GREEN)
            score_label.config(text ="Score: " + str(score))
            root.after(1000, nextQuestion)

        #IT award's the player 5 points for the second attempt..
        else:
            score += 5
            feedback("Correct! You earned 5 points!", GREEN)
            score_label.config(text="Score: " + str(score))
            root.after(1000, nextQuestion)

    else:
        #It increase's the number of attempts after a wrong answer
        attempts += 1

        if attempts < 2:
            feedback("Incorrect! Try again. One attempt left!")
            answer_entry.select_range(0, tk.END)
            
        else:
            #Finish the question when both attempts are used.
            question_finished = True
            updateProgress()
            feedback("No more attempts! The answer was " + str(correct_answer))
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

#It displays the final score and grade (page 6).
def displayResults():
    grade = calculateGrade()#It calls your grade function and stores the result.

    feedback("Quiz completed!", SEA)
    problem_label.config(text="Final Score: " + str(score) + "/100")
    score_label.config(text="Grade: " + grade)#It displays the player's grade
    showPage(6)

#It resets all the quiz variables so the player can play again.
def playAgain():
    global difficulty, score, question_number, attempts, question_finished

    difficulty = ""
    score = 0
    question_number = 0
    attempts = 0
    question_finished = False

    #It resets the labels and answer box.
    problem_label.config(text="")
    score_label.config(text="Score: 0")
    answer_entry.delete(0, tk.END)
    displayMenu()#Back to the difficulty page (page 2).


#All the TKinter buttons. In Tkinter, we use tk.Button() to create a button. 

#Page 1 - Start, over the red button shape.
start_button = addWidget(makeButton("Start", displayMenu), (1,), (728, 764, 1198, 885), 46)

#Page 2 - one button over each surfboard.
button_Easy = addWidget(makeButton("Easy", choose_easy), (2,), (440, 418, 845, 548), 40)
button_Medium = addWidget(makeButton("Moderate", choose_medium), (2,), (432, 584, 852, 718), 40)
button_Hard = addWidget(makeButton("Advanced", choose_hard), (2,), (428, 768, 858, 903), 40)

#Page 3 - Paddle Out, over the red button shape.
paddle_button = addWidget(makeButton("Paddle Out", paddleOut), (3,), (709, 832, 1180, 952), 46)

#Page 5 - the button used to submit an answer by the player
submit_button = addWidget(makeButton("Check Answer", isCorrect), (5,), (728, 765, 1198, 885), 46)

#Page 6 - the button that allows the player to replay the quiz.
replay_button = addWidget(makeButton("Play Again", playAgain), (6,), (728, 765, 1198, 885), 46)

#NEW - Pressing Enter also checks the answer (only on page 5).
root.bind("<Return>", lambda event: isCorrect() if page == 5 else None)
screen.bind("<Configure>", onResize)

showPage(1)

#root.mainloop() starts the window and keeps it running, thats why it's at the end of the whole code.
root.mainloop()