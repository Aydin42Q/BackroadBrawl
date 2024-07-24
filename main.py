import tkinter as tk
from tkinter import ttk
import random

# Global variables for character selection and super charge
playerChar = ""  # Stores the player's character choice 
cpuChar = ""  # Stores the CPU's character choice 
playerStatus = []  # Stores current player status
cpuStatus = []  # Stores current cpu status
superCharge = 0  # Indicates the amount of super charge

# Function to get move names based on player's character, also includes move color in the dictionary
def moves(char, status=[]):
    if char == "Sol Badguy":
        moves = {
            "Volcanic Viper": "lightpink", "Fafnir": "lightpink", "Burst": "lightblue",
            "Gun Flame": "lightpink", "Bandit Bringer": "lightpink", "Guard": "lightgreen"
        }
    elif char == "Goku":
        for x in status:
            if x == "Super Saiyan":
                moves = {"Super Ki Blast": "pink", "Super Kamehameha": "pink", "Ki Gathering": "lightblue",
                         "Ki Blast Barrage": "pink", "Spirit Bomb": "lightgrey", "Instant Transmission": "lightyellow"}
                break
        else:
            moves = {
                "Ki Blast": "lightpink", "Kamehameha": "lightpink", "Ki Gathering": "lightblue",
                "Destructo Disc": "lightpink", "Spirit Bomb": "lightgrey", "Instant Transmission": "lightyellow"
            }
    else:
        moves = {}  # Default empty moves dictionary
    return moves

# Function to get super move names based on player's character
def superMoves(playerChar, status):
    if playerChar == "Sol Badguy":
        moves = {"Faultless Defense": "green", "Tyrant Rave": "red", "Heavy Mob Cemetery": "red"}
    elif playerChar == "Goku":
        moves = {"Transformation": "yellow"}
    else:
        moves = {}  # Default empty super moves dictionary
    return moves

# Function to run move logic, such as calculating damage based on move and accuracy, or giving the character a status effect
def moveLogic(move, superCharge, attacker_status, defender_status):
    accuracy = random.randint(0, 100)  # Random accuracy value
    dmg = 0  # Initialize dmg with a default value
    attacker_status_effects = attacker_status.copy()
    defender_status_effects = defender_status.copy()
    move_message = f"{move} logic not coded yet"

    # Determine damage and effects based on move accuracy
    if move == "Volcanic Viper":
        if accuracy > 20:
            dmg = random.randint(7, 13)
            move_message = f"causing {dmg} damage!"
        else:
            move_message = "but it missed!"
    elif move == "Fafnir":
        if accuracy > 70:
            dmg = random.randint(15, 30)
            move_message = f"causing {dmg} damage!"
        else:
            move_message = "but it missed!"
    elif move == "Burst":
        defender_status_effects.append("Stunned")
        attacker_status_effects.append("Accuracy Boost")
        move_message = "applying Stunned status and gaining Accuracy Boost!"
    elif move == "Guard":
        attacker_status_effects.append("Damage Reduction")
        move_message = "gaining Damage Reduction!"
    elif move == "Ki Gathering":
        attacker_status_effects.append("Damage Boost")
        move_message = "gaining Damage Boost!"
    elif move == "Spirit Bomb":
        # Implementing three separate turns logic is omitted for simplicity
        if "Spirit Bomb Charge" in attacker_status:
            if attacker_status.count("Spirit Bomb Charge") == 2:
                dmg = 80
                attacker_status_effects = [status for status in attacker_status if status != "Spirit Bomb Charge"]
                move_message = "causing 80 guaranteed damage!"
            else:
                attacker_status_effects.append("Spirit Bomb Charge")
                move_message = "charging Spirit Bomb (second turn)"
        else:
            attacker_status_effects.append("Spirit Bomb Charge")
            move_message = "charging Spirit Bomb (first turn)"
    elif move == "Instant Transmission":
        if accuracy > 50:
            attacker_status_effects.append("Damage Negation")
            move_message = "dodging all incoming damage!"
        else:
            move_message = "but failed to dodge damage!"
    elif move == "Transformation":
        attacker_status_effects.append("Super Saiyan")
        move_message = "transforming into Super Saiyan!"
    elif move == "Faultless Defense":
        attacker_status_effects.append("Damage Negation")
        move_message = "negating all incoming damage!"
    
    return dmg, move_message, attacker_status_effects, defender_status_effects

# Class representing the game layout
class GameLayout:
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
        self.moves_frame = tk.Frame(self.master, bg="blue")
        self.moves_frame.grid(row=2, column=0, columnspan=3, pady=20)
        self.create_buttons()

    # Method to create buttons for moves and super moves
    def create_buttons(self):
        buttons_text = moves(playerChar)
        super_moves_text = superMoves(playerChar, playerStatus)

        # Create buttons for regular moves
        for i, (text, color) in enumerate(buttons_text.items()):
            btn = tk.Button(self.moves_frame, text=text, width=20, height=2, bg=color, command=lambda m=text, c=color: [self.super_moves_increment(), self.handle_turn(m, c)])
            btn.grid(row=i // 3, column=i % 3, padx=10, pady=5)

        self.super_moves_frame = tk.Frame(self.master, bg="lightpink")
        self.super_moves_frame.grid(row=1, column=3, padx=20, pady=20)

        # Create buttons for super moves
        for i, (text, color) in enumerate(super_moves_text.items()):
            btn = tk.Button(self.super_moves_frame, text=text, width=20, height=2, bg=color, command=lambda m=text: self.handle_super_move(m))
            btn.pack(pady=5)

    # Method to handle player turn and move to the next state
    def handle_turn(self, move, color):
        global playerStatus
        global cpuStatus

        attackMove = color == "lightpink" or color == "red"
        dmg, move_message, new_player_status, new_cpu_status = moveLogic(move, superCharge, playerStatus, cpuStatus)
        playerStatus = new_player_status
        cpuStatus = new_cpu_status
        self.decrement_health("right", dmg)
        self.remove_buttons()
        if dmg == 0 and attackMove:
            self.display_turn_info(f"Player used {move}, but it missed!", self.cpu_turn)
        elif dmg != 0 and attackMove:
            self.display_turn_info(f"Player used {move}, causing {dmg} damage! {move_message}", self.cpu_turn)
        else:
            self.display_turn_info(f"Player used {move}, {move_message}", self.cpu_turn)

    # Method to handle super move usage
    def handle_super_move(self, move):
        global superCharge
        global playerStatus
        global cpuStatus
        if superCharge >= 4:
            superCharge -= 4
            for i in range(7):
                if i < superCharge:
                    self.segments[i].config(bg="yellow")
                else:
                    self.segments[i].config(bg="grey")
            dmg, move_message, new_player_status, new_cpu_status = moveLogic(move, superCharge, playerStatus, cpuStatus)
            playerStatus = new_player_status
            cpuStatus = new_cpu_status
            self.decrement_health("right", dmg)
            self.remove_buttons()
            self.display_turn_info(f"Player used Super Move: {move}, causing {dmg} damage! {move_message}", self.cpu_turn)
        else:
            self.display_turn_info("Not enough super charge to use this move!", self.cpu_turn)

    # Method to remove buttons and show message
    def remove_buttons(self):
        for widget in self.moves_frame.winfo_children():
            widget.destroy()
        self.moves_frame.grid_forget()  # Hide the blue frame
        if hasattr(self, 'super_moves_frame'):
            self.super_moves_frame.grid_forget()

    def display_turn_info(self, message, next_state_func):
        # Clear any existing messages and buttons
        self.clear_message()
    
        # Display the new message
        self.info_label = tk.Label(self.master, text=message, bg="lightblue")
        self.info_label.grid(row=3, column=0, columnspan=3, pady=10)
    
        # Create a "Continue" button to proceed to the next state
        self.continue_button = tk.Button(self.master, text="Continue", command=lambda: [self.clear_message(), next_state_func()])
        self.continue_button.grid(row=4, column=0, columnspan=3, pady=10)
    
    def clear_message(self):
        # Remove the message label if it exists
        if hasattr(self, 'info_label'):
            self.info_label.grid_forget()
    
        # Remove the continue button if it exists
        if hasattr(self, 'continue_button'):
            self.continue_button.grid_forget()


    # Method to handle CPU's turn
    def cpu_turn(self):
        global cpuStatus
        global playerStatus
        moves_list = list(moves(cpuChar, cpuStatus).keys())
        if moves_list:
            move = random.choice(moves_list)
            dmg, move_message, new_cpu_status, new_player_status = moveLogic(move, superCharge, cpuStatus, playerStatus)
            
            cpuStatus = new_cpu_status
            playerStatus = new_player_status
            self.decrement_health("left", dmg)
            if dmg == 0:
                self.display_turn_info(f"CPU used {move}, but it missed!", self.reset_buttons)
            else:
                self.display_turn_info(f"CPU used {move}, causing {dmg} damage!", self.reset_buttons)

    # Method to reset buttons for player turn
    def reset_buttons(self):
        self.moves_frame = tk.Frame(self.master, bg="blue")
        self.moves_frame.grid(row=2, column=0, columnspan=3, pady=20)
        self.create_buttons()  # Recreate buttons

    # Method to decrement health for left or right character
    def decrement_health(self, side, amount):
        if side == "left":
            self.health_left["value"] = max(self.health_left["value"] - amount, 0)
        else:
            self.health_right["value"] = max(self.health_right["value"] - amount, 0)

    # Method to increment super moves
    def super_moves_increment(self):
        global superCharge
        if superCharge < 7:
            self.segments[superCharge].config(bg="yellow")
            superCharge += 1

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

    # Adds buttons in the center
    button1 = tk.Button(button_frame, text=f"Sol Badguy", bg='white', command=lambda: charSelect(button1))
    button1.grid(row=1, column=1, padx=10, pady=10)

    button2 = tk.Button(button_frame, text=f"Goku", bg='white', command=lambda: charSelect(button2))
    button2.grid(row=1, column=2, padx=10, pady=10)

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