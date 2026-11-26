
import os
import math
import time
import sys
import tkinter as tk
import tkinter.font as tkfont
import random #will allow us to select a random joke.

# LIBRARIES (install with:  pip install pygame pillow)
#Pillow is used to resize the images smoothly (needed for full-screen) and to load the window icon.
import importlib

try:
    Image = importlib.import_module("PIL.Image")
    ImageTk = importlib.import_module("PIL.ImageTk")
    ImageDraw = importlib.import_module("PIL.ImageDraw")
    ImageFont = importlib.import_module("PIL.ImageFont")
except ModuleNotFoundError as error:
    if error.name == "PIL" or (error.name and error.name.startswith("PIL.")):
        raise SystemExit("Pillow is required. Install it with: python -m pip install pillow") from error
    raise
try:
    pygame = importlib.import_module("pygame")
except ModuleNotFoundError as error:
    if error.name == "pygame":
        raise SystemExit("pygame is required. Install it with: python -m pip install pygame") from error
    raise

#NEW - makes every file name below (images, sounds, font, jokes) load from the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Creates the main application window.
root = tk.Tk()#Creates the window.
root.title("Alexa Tell Me a Joke")#Used to display Alexa Tell Me a Joke at the top of the window.
root.geometry("960x540")#Creates the window with how many pixels.
root.resizable(True, True)#CHANGED - the window can now be resized.
root.minsize(480, 270)
root.configure(bg="black")#Black bars are shown if the window is not exactly 16:9.

#The background images were drawn at 1440x810, so every position below is written for that size
#and then multiplied by SCALE so it still lines up at any window size.
DESIGN_W, DESIGN_H = 1440, 810
WIN_W, WIN_H = 960, 540
REF_SCALE = WIN_W / DESIGN_W
SCALE = WIN_W / DESIGN_W#CHANGED - SCALE is now recalculated whenever the window size changes.


# settings you may want to tweak (all positions are in the 1440x810 image size).
JOKE_AREA = (168, 90, 1060, 700)#a large square displays area on page 2. Jokes are centred in it.
VOLUME_AREA = (1130, 15, 1385, 180)#the two volume sliders (just above the four buttons).
JOKE_SETUP_SIZE = 34#Joke text size in 1440x810 pixels.
JOKE_PUNCHLINE_SIZE = 30#Punchline text size.
HOVER_COLOR_ON_WHITE = "#ffd23f"#Hover text colour for the white START button.
HOVER_COLOR_ON_BLACK = "#ff4d00"#Hover text colour for the black buttons on page 2.


#Helper functions for the backgrounds and the image-buttons.

#Scales a number from the 1440x810 image size to the window size.
def s(value):
    return int(round(value * SCALE))

#scales a font size so the text grows and shrinks with the window.
def fs(size):
    return max(6, int(round(size * SCALE / REF_SCALE)))

#Loads a background image.
def loadBackground(filename):
    image = Image.open(filename).convert("RGB")
    if image.size != (DESIGN_W, DESIGN_H):
        image = image.resize((DESIGN_W, DESIGN_H), Image.LANCZOS)
    return image

#Cuts the button-shaped area out of the background im so the real Tkinter button looks like part of the picture.
def cropButtonImage(background, x1, y1, x2, y2):
    width, height = max(1, s(x2) - s(x1)), max(1, s(y2) - s(y1))
    piece = background.crop((x1, y1, x2, y2)).resize((width, height), Image.LANCZOS)
    return ImageTk.PhotoImage(piece, master=root)


#Window icon
try:
    icon_source = Image.open("pixel-brush-icon.png").convert("RGBA")
    #Turn the plain white outside background transparent so the icon doesn't look like a white box.
    corner = icon_source.getpixel((0, 0))
    if corner[3] == 255 and min(corner[:3]) > 235:
        ImageDraw.floodfill(icon_source, (0, 0), (0, 0, 0, 0), thresh=30)
    icon_source.thumbnail((64, 64), Image.LANCZOS)
    icon_square = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    icon_square.paste(icon_source, ((64 - icon_source.width) // 2, (64 - icon_source.height) // 2), icon_source)
    window_icon = ImageTk.PhotoImage(icon_square, master=root)
    root.iconphoto(True, window_icon)#Shows the icon in the top-left corner of the window.
except Exception as error:
    print("Could not load pixel-brush-icon.png:", error)


#Sound: background music + button sounds
music_volume = 0.5#Starting volumes (0.0 - 1.0). The sliders show these values at the start.
sfx_volume = 0.7
hover_sound = None
click_sound = None
audio_ok = False

try:
    pygame.mixer.init()
    audio_ok = True
except pygame.error as error:
    print("Audio could not start:", error)

if audio_ok:
    try:
        hover_sound = pygame.mixer.Sound("button-hover-sound-effect.mp3")
        hover_sound.set_volume(sfx_volume)
    except Exception as error:
        print("Could not load button-hover-sound-effect.mp3:", error)
    try:
        click_sound = pygame.mixer.Sound("button-click-sound.mp3")
        click_sound.set_volume(sfx_volume)
    except Exception as error:
        print("Could not load button-click-sound.mp3:", error)
    try:
        pygame.mixer.music.load("Sneaky-Adventure.mp3")
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(loops=-1)#loops=-1 makes the music repeat forever.
    except Exception as error:
        print("Could not play Sneaky-Adventure.mp3:", error)

def playHover():
    if hover_sound is not None:
        hover_sound.play()

def playClick():
    if click_sound is not None:
        click_sound.play()


#Custom font (kongtext.ttf) - which i used ONLY for the jokes and punchlines
def loadCustomFont(path):
    path = os.path.abspath(path)
    family = "Kongtext"
    try:
        family = ImageFont.truetype(path, 12).getname()[0]#Reads the real family name from the font file.
    except Exception:
        pass
    try:
        if sys.platform.startswith("win"):
            import ctypes
            ctypes.windll.gdi32.AddFontResourceExW(path, 0x10, 0)
        else:
            ExtraFont = __import__("tkextrafont", fromlist=["Font"]).Font#pip install tkextrafont.
            ExtraFont(file=path, family=family)
    except Exception as error:
        print("Could not register kongtext.ttf:", error)
    if family in tkfont.families():
        return family
    print("kongtext.ttf did not load - using a backup font for the jokes.")
    return "Courier New"

JOKE_FONT = loadCustomFont("kongtext.ttf")


#Out of the two pages. Only one page is shown at a time.
#Both pages now live inside "stage".
stage = tk.Frame(root, bg="black")
welcome_page = tk.Frame(stage, bg="black")#Page 1 - Welcome screen.
joke_page = tk.Frame(stage, bg="black")#Page 2 - Main joke screen.

#Aleaxa (1) is the background for page 1 and Aleaxa (2) is the background for page 2.
background1 = loadBackground("Aleaxa1.png")
background2 = loadBackground("Aleaxa2.png")
background1_photo = None#These are filled in by applyLayout() every time the window size changes.
background2_photo = None

#Labels that hold the background pictures, they fill each whole page.
background1_label = tk.Label(welcome_page, bd=0)
background1_label.place(x=0, y=0, relwidth=1, relheight=1)
background2_label = tk.Label(joke_page, bd=0)
background2_label.place(x=0, y=0, relwidth=1, relheight=1)


#All the TKinter Label's, that are used to display text inside a window.

#CHANGED - the joke and punchline are now drawn on a Canvas (instead of two Labels).
joke_canvas = tk.Canvas(joke_page, bd=0, highlightthickness=0)
joke_bg_item = joke_canvas.create_image(0, 0, anchor="nw")
joke_bg_photo = None
joke_w, joke_h = 1, 1

#This text item will display the setup of our randomly selected joke.
setup_text = joke_canvas.create_text(0, 0, text="", fill="white", justify="center", anchor="center")

#This text item will display the punchline when the user clicks the button.
punchline_text = joke_canvas.create_text(0, 0, text="", fill="#ffe680", justify="center", anchor="center")


#All the variables used to store the jokes.
setup = ""
punchline = ""
punchline_visible = False


#Reads the jokes from the text file.
file = open("randomJokes.txt", "r")#Python opens "randomJokes.txt" to read its contents.
jokes = file.readlines()#This reads the file and stores each line.
file.close()#This closes the file after we've finished reading it.


#Joke animation (drop-in with a bounce, punchline pops up, pixel confetti burst)
PARTICLE_COLORS = ["#ffec27", "#ff77a8", "#29adff", "#00e436", "#ffffff", "#ffa300"]
anim_jobs = {}
particles = []
particle_job = None

def easeOutCubic(t):
    return 1 - (1 - t) ** 3

def easeOutBack(t):
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def easeOutBounce(t):
    n1, d1 = 7.5625, 2.75
    if t < 1 / d1:
        return n1 * t * t
    elif t < 2 / d1:
        t -= 1.5 / d1
        return n1 * t * t + 0.75
    elif t < 2.5 / d1:
        t -= 2.25 / d1
        return n1 * t * t + 0.9375
    t -= 2.625 / d1
    return n1 * t * t + 0.984375

#Moves a text item from y_from to y_to. It is time-based, so it stays smooth on slow and fast computers.
def tweenY(item, y_from, y_to, duration, easing, done=None):
    if item in anim_jobs:
        root.after_cancel(anim_jobs.pop(item))
    start = time.perf_counter()

    def step():
        t = (time.perf_counter() - start) * 1000 / duration
        if t >= 1:
            joke_canvas.coords(item, joke_w / 2, y_to)
            anim_jobs.pop(item, None)
            if done:
                done()
            return
        joke_canvas.coords(item, joke_w / 2, y_from + (y_to - y_from) * easing(t))
        anim_jobs[item] = root.after(16, step)
    step()

def cancelAnimations():
    for job in list(anim_jobs.values()):
        root.after_cancel(job)
    anim_jobs.clear()

def clearParticles():
    global particle_job
    if particle_job is not None:
        root.after_cancel(particle_job)
        particle_job = None
    for p in particles:
        joke_canvas.delete(p["id"])
    particles.clear()

def stepParticles():
    global particle_job
    particle_job = None
    for p in particles[:]:
        p["life"] += 1
        if p["life"] >= p["max"]:
            joke_canvas.delete(p["id"])
            particles.remove(p)
            continue
        p["vy"] += 0.35 * SCALE / REF_SCALE#gravity
        p["x"] += p["vx"]
        p["y"] += p["vy"]
        size = p["size"] * (1 - p["life"] / p["max"])#shrinks as it fades out
        joke_canvas.coords(p["id"], p["x"], p["y"], p["x"] + size, p["y"] + size)
    if particles:
        particle_job = root.after(16, stepParticles)

#A burst of little pixel squares from the given point.
def burst(x, y, count=22):
    size = max(3, s(9))
    for _ in range(count):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(2, 7) * SCALE / REF_SCALE
        particles.append({"id": joke_canvas.create_rectangle(x, y, x + size, y + size,
                                                              fill=random.choice(PARTICLE_COLORS), outline=""),
                          "x": x, "y": y, "vx": math.cos(angle) * speed, "vy": math.sin(angle) * speed - 2,
                          "life": 0, "max": random.randint(28, 44), "size": size})
    if particle_job is None:
        stepParticles()

#Height of a text item in pixels.
def textHeight(item):
    box = joke_canvas.bbox(item)
    if not box or not joke_canvas.itemcget(item, "text"):
        return 0
    return box[3] - box[1]

#Works out where the setup and punchline should sit so that together they are centred.
def jokeTargets():
    cy = joke_h / 2
    if not punchline_visible:
        return cy, cy
    gap = s(50)
    hs, hp = textHeight(setup_text), textHeight(punchline_text)
    top = cy - (hs + gap + hp) / 2
    return top + hs / 2, top + hs + gap + hp / 2

#Puts the text straight into its centred position (used when the window is resized).
def placeJokeText():
    setup_y, punch_y = jokeTargets()
    joke_canvas.coords(setup_text, joke_w / 2, setup_y)
    joke_canvas.coords(punchline_text, joke_w / 2, punch_y)


#This function selects a random joke from the list.
def selectJoke():
    global setup, punchline

    selected_joke = random.choice(jokes)#It selects a random joke from our list.
    joke_parts = selected_joke.strip().split("?")

    setup = joke_parts[0] + "?"#Contains the joke's question (the "?" is added back because split() removes it).
    punchline = joke_parts[1]#Contains the answer to the question.


#This function displays the setup of a random joke.
def tellJoke():
    global punchline_visible
    selectJoke()
    punchline_visible = False
    cancelAnimations()
    clearParticles()
    joke_canvas.itemconfig(setup_text, text=setup)
    joke_canvas.itemconfig(punchline_text, text="")
    setup_y, _ = jokeTargets()
    #The setup drops in from above and bounces into position.
    tweenY(setup_text, -textHeight(setup_text), setup_y, 750, easeOutBounce)


#This function displays the punchline of the selected joke.
def showPunchline():
    global punchline_visible
    if not setup or punchline_visible:
        return
    punchline_visible = True
    joke_canvas.itemconfig(punchline_text, text=punchline)
    setup_y, punch_y = jokeTargets()
    current_setup_y = joke_canvas.coords(setup_text)[1]
    #The setup glides up while the punchline pops up from the bottom with a little overshoot.
    tweenY(setup_text, current_setup_y, setup_y, 450, easeOutCubic)
    tweenY(punchline_text, joke_h + textHeight(punchline_text), punch_y, 650, easeOutBack,
           done=lambda: burst(joke_w / 2, punch_y))


#This function selects and displays another random joke.
def nextJoke():
    tellJoke()


#This function closes the application.
def quitApplication():
    if audio_ok:#NEW - stops the music (and all sounds) when the application closes.
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    root.destroy()

#the Quit button waits a moment so its click sound can be heard before the program closes.
def quitWithSound():
    root.after(250, quitApplication)

root.protocol("WM_DELETE_WINDOW", quitApplication)#Also stops the music when the window's X button is used.


#This function switches from the welcome page (page 1) to the joke page (page 2).
def showJokePage():
    welcome_page.place_forget()
    joke_page.place(x=0, y=0, relwidth=1, relheight=1)
    start_record["hovered"] = False#resets the START button's hover colour.
    start_button.config(fg=start_record["color"])


#Full-screen (F11 to switch, Esc to leave). The maximise button also works.
is_fullscreen = False

def toggleFullscreen(event=None):
    global is_fullscreen
    is_fullscreen = not is_fullscreen
    root.attributes("-fullscreen", is_fullscreen)

def exitFullscreen(event=None):
    global is_fullscreen
    if is_fullscreen:
        is_fullscreen = False
        root.attributes("-fullscreen", False)

root.bind("<F11>", toggleFullscreen)
root.bind("<Escape>", exitFullscreen)


#In Tkinter, we use tk.Button() to create a button.
button_records = []#remembers every button so they can be repositioned when the window size changes.

#plays the click sound and then runs the button's normal function.
def withClickSound(command):
    def run():
        playClick()
        command()
    return run

#hover effect: text colour changes and the hover sound plays ONCE when the cursor enters.
def onButtonEnter(record):
    if record["hovered"]:
        return
    record["hovered"] = True
    record["button"].config(fg=record["hover_color"])
    playHover()

def onButtonLeave(record):
    record["hovered"] = False
    record["button"].config(fg=record["color"])

#Puts a button at the right size and position for the current window size.
def layoutButton(record):
    x1, y1, x2, y2 = record["box"]
    record["image"] = cropButtonImage(record["background"], x1, y1, x2, y2)
    font = record["font"]
    button = record["button"]
    button.config(image=record["image"], font=(font[0], fs(font[1]), *font[2:]))
    button.image = record["image"]#Keeps a reference so Python doesn't delete the picture.
    button.place(x=s(x1), y=s(y1), width=s(x2) - s(x1), height=s(y2) - s(y1))

#Creates a real tk.Button that sits exactly on top of a button-shaped area in the background.
def makeImageButton(parent, background, box, text, command, font, color, hover_color="#ff4d00"):
    button = tk.Button(parent, text=text, compound="center",
                       font=font, fg=color, command=withClickSound(command),
                       bd=0, highlightthickness=0, relief="flat", cursor="hand2",
                       activeforeground=hover_color)
    record = {"button": button, "background": background, "box": box, "font": font,
              "color": color, "hover_color": hover_color, "hovered": False, "image": None}
    button.bind("<Enter>", lambda event, r=record: onButtonEnter(r))
    button.bind("<Leave>", lambda event, r=record: onButtonLeave(r))
    button_records.append(record)
    layoutButton(record)
    return button, record


#Page 1 - the START button, placed over the button-shaped area in Aleaxa (1).
start_button, start_record = makeImageButton(welcome_page, background1, (497, 552, 733, 636),
                                             "START", showJokePage, ("Arial", 16, "bold"), "white",
                                             HOVER_COLOR_ON_WHITE)

#Page 2 - the four buttons, placed over the four button-shaped areas in Aleaxa (2), from top to bottom.

#It creates a button that selects and displays a random joke.
joke_button, _ = makeImageButton(joke_page, background2, (1130, 190, 1385, 275),
                                 "Alexa, Tell Me a Joke", tellJoke, ("Arial", 10, "bold"), "black",
                                 HOVER_COLOR_ON_BLACK)

#It creates a button that displays the punchline.
punchline_button, _ = makeImageButton(joke_page, background2, (1130, 297, 1385, 383),
                                      "Show Punchline", showPunchline, ("Arial", 11, "bold"), "black",
                                      HOVER_COLOR_ON_BLACK)

#It creates a button that selects another random joke.
next_button, _ = makeImageButton(joke_page, background2, (1130, 405, 1385, 490),
                                 "Next Joke", nextJoke, ("Arial", 11, "bold"), "black",
                                 HOVER_COLOR_ON_BLACK)

#It creates a button that closes the application.
quit_button, _ = makeImageButton(joke_page, background2, (1138, 552, 1378, 637),
                                 "Quit", quitWithSound, ("Arial", 11, "bold"), "black",
                                 HOVER_COLOR_ON_BLACK)


# Volume sliders (page 2, directly above the four buttons)

#The panel takes the colour of the background picture behind it so it blends in.
_vx = (VOLUME_AREA[0] + VOLUME_AREA[2]) // 2
_vy = (VOLUME_AREA[1] + VOLUME_AREA[3]) // 2
_r, _g, _b = background2.getpixel((_vx, _vy))[:3]
panel_bg = "#%02x%02x%02x" % (_r, _g, _b)
panel_fg = "black" if (0.299 * _r + 0.587 * _g + 0.114 * _b) > 140 else "white"

#Each slider changes ONLY its own volume, so they never affect each other.
def setMusicVolume(value):
    music_label.config(text="Music Volume: " + str(int(float(value))) + "%")
    if audio_ok:
        pygame.mixer.music.set_volume(float(value) / 100)

def setSfxVolume(value):
    sfx_label.config(text="Button Sounds: " + str(int(float(value))) + "%")
    if hover_sound is not None:
        hover_sound.set_volume(float(value) / 100)
    if click_sound is not None:
        click_sound.set_volume(float(value) / 100)

volume_panel = tk.Frame(joke_page, bg=panel_bg)
volume_panel.pack_propagate(False)

def makeSlider(command):
    return tk.Scale(volume_panel, from_=0, to=100, resolution=1, orient="horizontal", showvalue=False,
                    command=command, bd=0, highlightthickness=0, relief="flat", sliderrelief="flat",
                    troughcolor="#1d2b53", bg="#ffa300", activebackground="#ffec27", cursor="hand2")

music_label = tk.Label(volume_panel, text="", font=("Arial", 10, "bold"), fg=panel_fg, bg=panel_bg, anchor="w")
music_label.pack(fill="x")
music_scale = makeSlider(setMusicVolume)
music_scale.pack(fill="x", pady=(0, 6))

sfx_label = tk.Label(volume_panel, text="", font=("Arial", 10, "bold"), fg=panel_fg, bg=panel_bg, anchor="w")
sfx_label.pack(fill="x")
sfx_scale = makeSlider(setSfxVolume)
sfx_scale.pack(fill="x")
sfx_scale.bind("<ButtonRelease-1>", lambda event: playClick())#Lets you hear the new button-sound level.

music_scale.set(int(music_volume * 100))
sfx_scale.set(int(sfx_volume * 100))


#Re-lays out everything whenever the window size changes.
#The 16:9 picture is scaled as large as possible and kept centred, so the buttons always line up with it.

last_size = (0, 0)
resize_job = None

def applyLayout():
    global SCALE, last_size, resize_job, background1_photo, background2_photo, joke_bg_photo, joke_w, joke_h
    resize_job = None
    width, height = root.winfo_width(), root.winfo_height()
    if width < 100 or height < 100 or (width, height) == last_size:
        return
    last_size = (width, height)
    SCALE = min(width / DESIGN_W, height / DESIGN_H)

    stage_w, stage_h = s(DESIGN_W), s(DESIGN_H)
    stage.place(relx=0.5, rely=0.5, anchor="center", width=stage_w, height=stage_h)

    #Backgrounds
    background1_photo = ImageTk.PhotoImage(background1.resize((stage_w, stage_h), Image.LANCZOS), master=root)
    background2_photo = ImageTk.PhotoImage(background2.resize((stage_w, stage_h), Image.LANCZOS), master=root)
    background1_label.config(image=background1_photo)
    background2_label.config(image=background2_photo)

    #Buttons
    for record in button_records:
        layoutButton(record)

    #Volume sliders
    vx1, vy1, vx2, vy2 = VOLUME_AREA
    volume_panel.place(x=s(vx1), y=s(vy1), width=s(vx2) - s(vx1), height=s(vy2) - s(vy1))
    for label in (music_label, sfx_label):
        label.config(font=("Arial", fs(10), "bold"))
    for scale in (music_scale, sfx_scale):
        scale.config(width=max(10, s(22)), sliderlength=max(14, s(32)))

    #Joke display area (text stays centred)
    jx1, jy1, jx2, jy2 = JOKE_AREA
    joke_w, joke_h = max(1, s(jx2) - s(jx1)), max(1, s(jy2) - s(jy1))
    joke_canvas.place(x=s(jx1), y=s(jy1), width=joke_w, height=joke_h)
    joke_canvas.config(width=joke_w, height=joke_h)
    joke_bg_photo = cropButtonImage(background2, jx1, jy1, jx2, jy2)
    joke_canvas.itemconfig(joke_bg_item, image=joke_bg_photo)
    wrap = int(joke_w * 0.9)
    joke_canvas.itemconfig(setup_text, font=(JOKE_FONT, -max(8, s(JOKE_SETUP_SIZE))), width=wrap)
    joke_canvas.itemconfig(punchline_text, font=(JOKE_FONT, -max(8, s(JOKE_PUNCHLINE_SIZE))), width=wrap)
    cancelAnimations()
    clearParticles()
    placeJokeText()

def onConfigure(event):
    global resize_job
    if event.widget is not root:
        return
    if resize_job is not None:
        root.after_cancel(resize_job)
    resize_job = root.after(60, applyLayout)

root.bind("<Configure>", onConfigure)


#The program starts on the welcome page.
welcome_page.place(x=0, y=0, relwidth=1, relheight=1)#CHANGED - was welcome_page.pack()
root.update_idletasks()
applyLayout()


#root.mainloop() starts the window and keeps it running, that's why it's at the end of the whole code.
root.mainloop()
