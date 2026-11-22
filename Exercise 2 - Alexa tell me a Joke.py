import tkinter as tk
import random #will allow us to select a random joke.

#Creates the main application window.
root = tk.Tk()#Creates the window.
root.title("Alexa Tell Me a Joke")#Used to display Alexa Tell Me a Joke at the top of the window.
root.geometry("600x459")#Creates the window with how many pixels.

#All the TKinter Label's, that are uesd to display text inside a window.
#To Display the game title
title_label = tk.Label(root, text="Alexa Tell Me a Joke", font=("Arial", 24))#root tells Tkinter which window the label should be in.
title_label.pack(pady=20)#pack() will place label inside the windo, I will use grid later.

#This label will eventually display the setup of our randomly selected joke
setup_label = tk.Label(root, text="", font=("Arial", 16))
setup_label.pack(pady=20)#pady=20 adds 20 pixels of spacing around the text.

#This label will display the punchline when the user clicks the button.
punchline_label = tk.Label(root, text="", font=("Arial",14))
punchline_label.pack(pady=10)


#All the TKinter buttons. In Tkinter, we use tk.Button() to create a button.

#It creates a button with the requested text.  
joke_button = tk.Button(root, text="Alexa tell me a joke")
joke_button.pack(pady=10)


file = open("randomJokes.txt", "r")#Python opens "randomJokes.txt"(file) to read its contents.
jokes = file.readlines()#This reads the file and stores each line
file.close()#This closes the file after we've finished reading it.

#This line gets the first joke from our list, removes unnecessary whitespace and newline, and separates the setup and punchline wherever it finds a ?
selected_joke = random.choice(jokes)#It selects a random joke from our list.
joke_parts = selected_joke.strip().split("?")

setup = joke_parts[0]#contains the joke's question.
punchline = joke_parts[1]#contains the answer of the question.
#just To check whether it works

#root.mainloop() starts the window and keeps it running, thats why it's at the end of the whole code.
root.mainloop()