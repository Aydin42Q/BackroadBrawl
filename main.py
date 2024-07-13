import tkinter as tk
from tkinter import ttk
import random

# Global variables for character selection and supercharged state
playerChar = ""  # Stores the player's character choice
cpuChar = ""     # Stores the CPU's character choice
superCharged = False  # Indicates if the supercharged state is active

# Function to get move names based on player's character
def moveNames(playerChar):
    if playerChar == "Char 1":
        moves = [
            "Volcanic Viper", "Fafnir", "Burst",
            "Gun Flame", "Bandit Bringer", "Guard"
        ]
    return moves

# Function to get super move names based on player's character
def superMoveNames(playerChar):
    if playerChar == "Char 1":
        moves = ["Faultless Defense", "Tyrant Rave", "Heavy Mob Cemetery"]
    return moves

# Function to calculate damage based on move and accuracy
def calcDmg(move, superCharged):
    accuracy = random.randint(0, 100)  # Random accuracy value
    dmg = 0  # Initialize dmg with a default value

    # Determine damage based on move accuracy
    match move:
        case "Volcanic Viper":
            if accuracy > 20:
                dmg = random.randint(7, 13)
            else:
                dmg = 0
        case "Fafnir":
            if accuracy > 70:
                dmg = random.randint(15, 30)
            else:
                dmg = 0
        case _:
            dmg = 0  # Default damage if move does not match any cases
    return dmg

# Class representing the game layout
class GameLayout:
    global playerChar
    global cpuChar
    global superCharged

    def __init__(self, master):
        self.master = master
        self.master.title("Game Layout")
        self.master.geometry("800x400")
        self.master.config(bg="lightblue")

        # Character placeholders
        self.character_left = tk.Label(master, bg="green", width=20, height=10)
        self.character_right = tk.Label(master, bg="green", width=20, height=10)
        self.character_left.grid(row=1, column=0, padx=20, pady=20)
        self.character_right.grid(row=1, column=2, padx=20, pady=20)

        # Health bars
        self.health_left = ttk.Progressbar(master, length=200, maximum=100)
        self.health_right = ttk.Progressbar(master, length=200, maximum=100)
        self.health_left.grid(row=0, column=0, padx=20, pady=10)
        self.health_right.grid(row=0, column=2, padx=20, pady=10)
        self.health_left["value"] = 100
        self.health_right["value"] = 100

        # Segmented bar for Super Moves
        self.super_moves_frame = tk.Frame(master, bg="pink", width=140, height=60)
        self.super_moves_frame.grid(row=1, column=1)
        self.super_moves_label = tk.Label(self.super_moves_frame, text="SUPER CHARGE", bg="red", width=15)
        self.super_moves_label.pack(pady=5)

        self.segments = []  # List to hold segments for super move indicator
        for i in range(7):
            segment = tk.Label(self.super_moves_frame, bg="grey", width=2, height=1)
            segment.pack(side=tk.LEFT, padx=1)
            self.segments.append(segment)

        # Buttons for moves
        self.create_buttons()

    # Method to create buttons for moves and super moves
    def create_buttons(self):
        moves_frame = tk.Frame(self.master, bg="blue")
        moves_frame.grid(row=2, column=0, columnspan=3, pady=20)

        buttons_text = moveNames(playerChar)
        super_moves_text = superMoveNames(playerChar)

        # Create buttons for regular moves
        for i, text in enumerate(buttons_text):
            btn = tk.Button(moves_frame, text=text, width=20, height=2, bg="lightpink", command=lambda m=text: [self.increment_super_moves, self.decrement_health("right", calcDmg(m, superCharged))])
            btn.grid(row=i//3, column=i%3, padx=10, pady=5)

        super_moves_frame = tk.Frame(self.master, bg="lightpink")
        super_moves_frame.grid(row=1, column=3, padx=20, pady=20)

        # Create buttons for super moves
        for i, text in enumerate(super_moves_text):
            btn = tk.Button(super_moves_frame, text=text, width=20, height=2, bg="lightgreen", command=self.super_moves_increment)
            btn.pack(pady=5)

    # Method to increment super move segments
    def increment_super_moves(self, segments_filled):
        for i in range(7):
            if i < segments_filled:
                self.segments[i].config(bg="red")
            else:
                self.segments[i].config(bg="grey")

    # Method to decrement health bar based on character
    def decrement_health(self, character, value):
        if character == "left":
            self.health_left["value"] -= value
        elif character == "right":
            self.health_right["value"] -= value

    # Method to increment super moves indicator
    def super_moves_increment(self):
        segments_filled = sum(1 for segment in self.segments if segment.cget("bg") == "red")
        if segments_filled < 7:
            self.increment_super_moves(segments_filled + 1)
            if segments_filled == 7:
                superCharged = True

# Function to create the menu layout
def menuLayout(root):
    # Create a frame to hold the content
    frame = tk.Frame(root, bg='blue')
    frame.pack(expand=True, fill='both')

    # Add a label at the top
    title_label = tk.Label(frame, text="Backroad Brawl", font=('Helvetica', 16), bg='blue', fg='white')
    title_label.pack(pady=20)

    # Add a label with instructions above the buttons
    instructions_label = tk.Label(frame, text="Choose your character, red is yours, blue is the CPU", font=('Helvetica', 10), bg='blue', fg='white')
    instructions_label.pack(pady=10)

    # Create a frame for the buttons
    button_frame = tk.Frame(frame, bg='blue')
    button_frame.pack(expand=True)

    # Function to handle character selection
    def charSelect(name):
        global playerChar
        global cpuChar
        if playerChar == "" and name["bg"] != "blue":
            name["bg"] = "red"
            playerChar = name["text"]
        elif playerChar != "" and name["bg"] == "red":
            name["bg"] = "white"
            playerChar = ""
        elif playerChar != "" and cpuChar == "" and name["bg"] != "red":
            name["bg"] = "blue"
            cpuChar = name["text"]
        elif cpuChar != "" and name["bg"] == "blue":
            name["bg"] = "white"
            cpuChar = ""
        print("player char is " + playerChar)
        print('cpu char is ' + cpuChar)

    # Add six buttons in the center
    button1 = tk.Button(button_frame, text=f"Char 1", bg='white', command=lambda: charSelect(button1))
    button1.grid(row=1, column=1, padx=10, pady=10)

    button2 = tk.Button(button_frame, text=f"Char 2", bg='white', command=lambda: charSelect(button2))
    button2.grid(row=1, column=2, padx=10, pady=10)

    button3 = tk.Button(button_frame, text=f"Char 3", bg='white', command=lambda: charSelect(button3))
    button3.grid(row=2, column=1, padx=10, pady=10)

    button4 = tk.Button(button_frame, text=f"Char 4", bg='white', command=lambda: charSelect(button4))
    button4.grid(row=2, column=2, padx=10, pady=10)

    button5 = tk.Button(button_frame, text=f"Char 5", bg='white', command=lambda: charSelect(button5))
    button5.grid(row=3, column=1, padx=10, pady=10)

    button6 = tk.Button(button_frame, text=f"Char 6", bg='white', command=lambda: charSelect(button6))
    button6.grid(row=3, column=2, padx=10, pady=10)

    # Make sure the buttons resize appropriately
    for i in range(2):
        button_frame.columnconfigure(i, weight=1)
    for i in range(3):
        button_frame.rowconfigure(i, weight=1)

    # Add a confirm button below the other buttons
    confirm_button = tk.Button(frame, text="Confirm", bg='white', command=lambda: switch_to_game(root))
    confirm_button.pack(pady=20)

    return root

# Function to switch to the game layout
def switch_to_game(root):
    for widget in root.winfo_children():
        widget.destroy()
    GameLayout(root)

# Function to create the main window
def createWindow():
    root = tk.Tk()
    root.title("Backroad Brawl")
    root.geometry("500x500")
    root.configure(bg="blue")

    menuLayout(root)

    root.mainloop()

# Main entry point for the program
if __name__ == "__main__":
    createWindow()
