import tkinter as tk
from tkinter import ttk
import random

# Global variables for character selection and super charge
playerChar = ""  # Stores the player's character choice
cpuChar = ""     # Stores the CPU's character choice
playerStatus = [] # Stores current player status
cpuStatus = [] # Stores current cpu status
superCharge = 0  # Indicates the amount of super charge

# Function to get move names based on player's character, also includes move color in the dictionary
def moves(char, status = []):
    if char == "Char 1":
        moves = {
            "Volcanic Viper": "lightpink", "Fafnir" : "lightpink", "Burst" : "lightblue",
            "Gun Flame" : "lightpink", "Bandit Bringer" : "lightpink", "Guard" : "lightgreen"
        }
    elif char == "Char 2":
        for x in status:
            if x == "Super Saiyan" :
                moves = {}
                break
        else:
            moves = {
                "Ki Blast" : "lightpink", "Kamehameha" : "lightpink", "Ki Gathering" : "lightblue",
                "Destructo Disc" : "lightpink", "Spirit Bomb" : "lightgrey", "Instant Transmission" : "lightyellow"
            }
    else:
        moves = {}  # Default empty moves dictionary
    return moves

# Function to get super move names based on player's character
def superMoves(playerChar):
    if playerChar == "Char 1":
        moves = ["Faultless Defense", "Tyrant Rave", "Heavy Mob Cemetery"]
    else:
        moves = []  # Default empty super moves list
    return moves

# Function to run move logic, such as calculating damage based on move and accuracy, or giving the character a status effect
def moveLogic(move, superCharge):
    accuracy = random.randint(0, 100)  # Random accuracy value
    dmg = 0  # Initialize dmg with a default value

    # Determine damage based on move accuracy
    if move == "Volcanic Viper":
        if accuracy > 20:
            dmg = random.randint(7, 13)
        else:
            dmg = 0
    elif move == "Fafnir":
        if accuracy > 70:
            dmg = random.randint(15, 30)
        else:
            dmg = 0
    return dmg

# Class representing the game layout
class GameLayout:
    global playerChar
    global cpuChar
    global superCharge

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
        self.moves_frame = tk.Frame(self.master, bg="blue")
        self.moves_frame.grid(row=2, column=0, columnspan=3, pady=20)

        buttons_text = moves(playerChar)
        super_moves_text = superMoves(playerChar)

        # Create buttons for regular moves
        for i, (text, color) in enumerate(buttons_text.items()):
            btn = tk.Button(self.moves_frame, text=text, width=20, height=2, bg=color, command=lambda m=text, c=color:[self.super_moves_increment(), self.handle_turn(m, c)])
            btn.grid(row=i//3, column=i%3, padx=10, pady=5)

        self.super_moves_frame = tk.Frame(self.master, bg="lightpink")
        self.super_moves_frame.grid(row=1, column=3, padx=20, pady=20)

        # Create buttons for super moves
        for i, text in enumerate(super_moves_text):
            btn = tk.Button(self.super_moves_frame, text=text, width=20, height=2, bg="lightgreen")
            btn.pack(pady=5)

    # Method to handle player turn and move to the next state
    def handle_turn(self, move, color):
        attackMove = color == "lightpink" or color == "red"
        dmg = moveLogic(move, superCharge)
        self.decrement_health("right", dmg)
        self.remove_buttons()
        if dmg == 0 and attackMove:
            self.display_turn_info(f"Player used {move}, it missed!", self.cpu_turn)
        elif dmg != 0 and attackMove:    
            self.display_turn_info(f"Player used {move} causing {dmg} damage!", self.cpu_turn)
        else:
            self.display_turn_info(f"{move} logic not coded yet", self.cpu_turn)

    # Method to remove move buttons
    def remove_buttons(self):
        self.moves_frame.grid_forget()

    # Method to display turn information and a continue button
    def display_turn_info(self, message, next_action):
        self.info_label = tk.Label(self.master, text=message, bg="lightblue")
        self.info_label.grid(row=2, column=0, columnspan=3, pady=20)
        self.continue_button = tk.Button(self.master, text="Continue", command=next_action)
        self.continue_button.grid(row=3, column=1, pady=10)

    # Method to handle CPU turn
    def cpu_turn(self):
        self.info_label.grid_forget()
        self.continue_button.grid_forget()
        move = random.choice(list(moves(cpuChar).keys()))
        attackMove = move in moves(cpuChar) and (moves(cpuChar)[move] == "lightpink" or moves(cpuChar)[move] == "red")
        dmg = moveLogic(move, superCharge)
        self.decrement_health("left", dmg)
        if dmg == 0 and attackMove:
            self.display_turn_info(f"CPU used {move}, it missed!", self.player_turn)
        elif dmg != 0 and attackMove:    
            self.display_turn_info(f"CPU used {move} causing {dmg} damage!", self.player_turn)
        else:
            self.display_turn_info(f"{move} logic not coded yet", self.player_turn)

    # Method to handle player turn
    def player_turn(self):
        self.info_label.grid_forget()
        self.continue_button.grid_forget()
        self.create_buttons()

    # Method to fill super move bar
    def super_bar_fill(self, segments_filled):
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

    # Method with super move bar logic
    def super_moves_increment(self):
        global superCharge
        segments_filled = sum(1 for segment in self.segments if segment.cget("bg") == "red")
        if segments_filled < 7:
            self.super_bar_fill(segments_filled + 1)
        superCharge = segments_filled + 1 if segments_filled < 7 else 7

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
