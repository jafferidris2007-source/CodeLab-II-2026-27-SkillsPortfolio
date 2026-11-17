import tkinter as tk

root = tk.Tk()
root.title("Math Challenge")
root.geometry("600x459")

title = tk.Label(root, text="Math Challenge", font=("Arial", 24))
title.pack()

question_label = tk.Label(root, text="Choose Your Difficulty.",font=("Arial", 18))
question_label.pack(pady = 30)

button_Easy = tk.Button(root, text = "Easy", font =("Arial", 18))
button_Easy.pack(pady = 10)

button_Medium = tk.Button(root, text = "Medium", font = ("Arial", 18))
button_Medium.pack(pady = 10)

button_Hard = tk.Button(root, text = "Hard", font = ("Arial", 18))
button_Hard.pack(pady = 10)

root.mainloop()