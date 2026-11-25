import tkinter as tk
import random #will allow us to select a random joke.
from PIL import Image, ImageTk #Pillow lets us resize the background images so they fit the window.

#Creates the main application window.
root = tk.Tk()#Creates the window.
root.title("Alexa Tell Me a Joke")#Used to display Alexa Tell Me a Joke at the top of the window.
root.geometry("960x540")#Creates the window with how many pixels (same 16:9 shape as the background images).
root.resizable(False, False)#Keeps the window the same size so the buttons always line up with the images.

#The background images were drawn at 1440x810, so every position below is written for that size
#and then multiplied by SCALE so it still lines up when the window is 960x540.
WIN_W, WIN_H = 960, 540
SCALE = WIN_W / 1440


#Helper functions for the backgrounds and the image-buttons.

#Scales a number from the 1440x810 image size to the window size.
def s(value):
    return int(round(value * SCALE))

#Loads a background image and resizes it to fit the window.
def loadBackground(filename):
    image = Image.open(filename).convert("RGB")
    return image.resize((WIN_W, WIN_H), Image.LANCZOS)

#Cuts the button-shaped area out of the background so the real Tkinter button looks like part of the picture.
def cropButtonImage(background, x1, y1, x2, y2):
    return ImageTk.PhotoImage(background.crop((s(x1), s(y1), s(x2), s(y2))))

#Creates a real tk.Button that sits exactly on top of a button-shaped area in the background.
def makeImageButton(parent, background, box, text, command, font, color):
    x1, y1, x2, y2 = box
    button_image = cropButtonImage(background, x1, y1, x2, y2)
    button = tk.Button(parent, text=text, image=button_image, compound="center",
                       font=font, fg=color, command=command,
                       bd=0, highlightthickness=0, relief="flat", cursor="hand2",
                       activeforeground=color)
    button.image = button_image#Keeps a reference so Python doesn't delete the picture.
    button.place(x=s(x1), y=s(y1), width=s(x2) - s(x1), height=s(y2) - s(y1))
    return button


#The two pages. Only one page is shown at a time.
welcome_page = tk.Frame(root, width=WIN_W, height=WIN_H)#Page 1 - Welcome screen.
joke_page = tk.Frame(root, width=WIN_W, height=WIN_H)#Page 2 - Main joke screen.

#Aleaxa (1) is the background for page 1 and Aleaxa (2) is the background for page 2.
background1 = loadBackground("Aleaxa1.png")
background2 = loadBackground("Aleaxa2.png")
background1_photo = ImageTk.PhotoImage(background1)
background2_photo = ImageTk.PhotoImage(background2)

#Labels that hold the background pictures (they fill each whole page).
tk.Label(welcome_page, image=background1_photo, bd=0).place(x=0, y=0, relwidth=1, relheight=1)
tk.Label(joke_page, image=background2_photo, bd=0).place(x=0, y=0, relwidth=1, relheight=1)


#All the TKinter Label's, that are used to display text inside a window.

#To Display the game title
#The title is already part of the Aleaxa (1) background picture, so this label is no longer shown.
title_label = tk.Label(root, text="Alexa Tell Me a Joke", font=("Arial", 24))#root tells Tkinter which window the label should be in.
#title_label.pack(pady=20)#pack() will place label inside the window, I will use grid later.

#The jokes are shown on the sky inside the large square area, so the labels use the sky colour as their background.
sky_color = "#%02x%02x%02x" % background2.getpixel((s(600), s(150)))

#This label will display the setup of our randomly selected joke.
setup_label = tk.Label(joke_page, text="", font=("Arial", 20, "bold"), fg="white", bg=sky_color,
                       wraplength=s(780), justify="center")
setup_label.place(x=s(168), y=s(90), width=s(892), height=s(110))#Inside the large square area (top part).

#This label will display the punchline when the user clicks the button.
punchline_label = tk.Label(joke_page, text="", font=("Arial", 18), fg="#ffe680", bg=sky_color,
                           wraplength=s(780), justify="center")
punchline_label.place(x=s(168), y=s(210), width=s(892), height=s(90))#Inside the large square area, just below the setup.


#All the variables used to store the jokes.
setup = ""
punchline = ""


#Reads the jokes from the text file.
file = open("randomJokes.txt", "r")#Python opens "randomJokes.txt" to read its contents.
jokes = file.readlines()#This reads the file and stores each line.
file.close()#This closes the file after we've finished reading it.


#All the Tkinter Functions

#This function selects a random joke from the list.
def selectJoke():
    global setup, punchline

    selected_joke = random.choice(jokes)#It selects a random joke from our list.
    joke_parts = selected_joke.strip().split("?")

    setup = joke_parts[0] + "?"#Contains the joke's question (the "?" is added back because split() removes it).
    punchline = joke_parts[1]#Contains the answer to the question.


#This function displays the setup of a random joke.
def tellJoke():
    selectJoke()
    setup_label.config(text=setup)
    punchline_label.config(text="")


#This function displays the punchline of the selected joke.
def showPunchline():
    punchline_label.config(text=punchline)


#This function selects and displays another random joke.
def nextJoke():
    tellJoke()


#This function closes the application.
def quitApplication():
    root.destroy()


#This function switches from the welcome page (page 1) to the joke page (page 2).
def showJokePage():
    welcome_page.pack_forget()
    joke_page.pack()


#All the Tkinter buttons. In Tkinter, we use tk.Button() to create a button.

#Page 1 - the START button, placed over the button-shaped area in Aleaxa (1).
start_button = makeImageButton(welcome_page, background1, (497, 552, 733, 636),
                               "START", showJokePage, ("Arial", 16, "bold"), "white")

#Page 2 - the four buttons, placed over the four button-shaped areas in Aleaxa (2), from top to bottom.

#It creates a button that selects and displays a random joke.
joke_button = makeImageButton(joke_page, background2, (1130, 190, 1385, 275),
                              "Alexa, Tell Me a Joke", tellJoke, ("Arial", 10, "bold"), "black")

#It creates a button that displays the punchline.
punchline_button = makeImageButton(joke_page, background2, (1130, 297, 1385, 383),
                                   "Show Punchline", showPunchline, ("Arial", 11, "bold"), "black")

#It creates a button that selects another random joke.
next_button = makeImageButton(joke_page, background2, (1130, 405, 1385, 490),
                              "Next Joke", nextJoke, ("Arial", 11, "bold"), "black")

#It creates a button that closes the application.
quit_button = makeImageButton(joke_page, background2, (1138, 552, 1378, 637),
                              "Quit", quitApplication, ("Arial", 11, "bold"), "black")


#The program starts on the welcome page.
welcome_page.pack()


#root.mainloop() starts the window and keeps it running, that's why it's at the end of the whole code.
root.mainloop()