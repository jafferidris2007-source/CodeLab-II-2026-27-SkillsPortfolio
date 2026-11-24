
import tkinter as tk
import random #will allow us to select a random joke.

#Creates the main application window.
root = tk.Tk()#Creates the window.
root.title("Alexa Tell Me a Joke")#Used to display Alexa Tell Me a Joke at the top of the window.
root.geometry("600x459")#Creates the window with how many pixels.

#All the TKinter Label's, that are used to display text inside a window.

#To Display the game title
title_label = tk.Label(root, text="Alexa Tell Me a Joke", font=("Arial", 24))#root tells Tkinter which window the label should be in.
title_label.pack(pady=20)#pack() will place label inside the window, I will use grid later.

#This label will display the setup of our randomly selected joke.
setup_label = tk.Label(root, text="", font=("Arial", 16))
setup_label.pack(pady=20)#pady=20 adds 20 pixels of spacing around the text.

#This label will display the punchline when the user clicks the button.
punchline_label = tk.Label(root, text="", font=("Arial", 14))
punchline_label.pack(pady=10)


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

    setup = joke_parts[0]#Contains the joke's question.
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


#All the Tkinter buttons. In Tkinter, we use tk.Button() to create a button.

#It creates a button that selects and displays a random joke.
joke_button = tk.Button(root, text="Alexa tell me a joke", command=tellJoke)
joke_button.pack(pady=10)

#It creates a button that displays the punchline.
punchline_button = tk.Button(root, text="Show Punchline", command=showPunchline)
punchline_button.pack(pady=10)

#It creates a button that selects another random joke.
next_button = tk.Button(root, text="Next Joke", command=nextJoke)
next_button.pack(pady=10)

#It creates a button that closes the application.
quit_button = tk.Button(root, text="Quit", command=quitApplication)
quit_button.pack(pady=10)


#root.mainloop() starts the window and keeps it running, that's why it's at the end of the whole code.
root.mainloop()
