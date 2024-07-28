import tkinter as tk
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import random

# Global variables for character selection and super charge
playerChar = ""  # Stores the player's character choice 
cpuChar = ""  # Stores the CPU's character choice 
playerStatus = {}  # Stores current player status and their durations
cpuStatus = {}  # Stores current cpu status and their durations
superCharge = 0  # Indicates the amount of super charge
cpuSuperCharge = 0 # Indicates the super charge of the cpu
burstCharge = True # Tracks if Sol Badguy is able to use burst
image_change = False  # Tracks if an image change is required


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
    elif playerChar == "Goku" and ("Super Saiyan" not in status):
        moves = {"Transformation": "yellow"}
    elif playerChar == "Goku":
        moves = {}
    else:
        moves = {}  # Default empty super moves dictionary
    return moves

def moveLogic(move, superCharge, attacker_status, defender_status):
    global burstCharge
    global image_change
    accuracy = random.randint(0, 100)  # Random accuracy value
    dmg = 0  # Initialize dmg with a default value
    attacker_status_effects = attacker_status.copy()
    defender_status_effects = defender_status.copy()
    move_message = f"{move} logic not coded yet"
    

    # Move-specific damage ranges and accuracy minimums
    damage_ranges = {
        "Volcanic Viper": (15, 25),
        "Fafnir": (35, 55),
        "Burst": (0, 0),  # No damage, special effects
        "Gun Flame": (7, 15),
        "Bandit Bringer": (12, 18),
        "Guard": (0, 0),  # No damage, special effects
        "Ki Blast": (7, 15),
        "Kamehameha": (25, 45),
        "Ki Gathering": (0, 0),  # No damage, special effects
        "Spirit Bomb": (80, 80),  # Special case handled separately
        "Instant Transmission": (0, 0),  # No damage, special effects
        "Transformation": (0, 0),  # No damage, special effects
        "Faultless Defense": (0, 0),  # No damage, special effects
        "Super Ki Blast": (20, 40),
        "Super Kamehameha": (30, 60),
        "Ki Blast Barrage": (15, 50),
        "Destructo Disc": (30, 35),
        "Tyrant Rave": (40, 80),  
        "Heavy Mob Cemetery": (60, 100),  
        "Transformation": (0, 0)  # No damage, special effects
    }

    accuracy_minimums = {
        "Volcanic Viper": 10,
        "Fafnir": 60,
        "Burst": 0,  # Not based on accuracy (Status move)
        "Gun Flame": 0, # Not based on accuracy (Garunteed hit move)
        "Bandit Bringer": 5,
        "Guard": 0,  # Not based on accuracy (Status move)
        "Ki Blast": 0, # Not based on accuracy (Garunteed hit move)
        "Kamehameha": 60,
        "Ki Gathering": 0,  # Not based on accuracy (Status move)
        "Spirit Bomb": 0,  # Not based on accuracy (Status move)
        "Instant Transmission": 50, # Accuracy based status move
        "Transformation": 0,  # Not based on accuracy (Status move)
        "Faultless Defense": 0,  # Not based on accuracy (Status move)
        "Super Ki Blast": 40,
        "Super Kamehameha": 60,
        "Ki Blast Barrage": 20,
        "Destructo Disc": 50,
        "Tyrant Rave": 0,  # Not based on accuracy (Garunteed hit move)
        "Heavy Mob Cemetery": 50  
    }

    # Determine damage and effects based on move accuracy
    if move in accuracy_minimums:
        min_accuracy = accuracy_minimums[move]
        if accuracy > min_accuracy:
            if move in damage_ranges:
                dmg_range = damage_ranges[move]
                if move == "Spirit Bomb":
                    # Special handling for Spirit Bomb
                    if "Spirit Bomb Charge" in attacker_status:
                        if attacker_status["Spirit Bomb Charge"] == 1:
                            dmg = dmg_range[0]  # Spirit Bomb does fixed damage
                            del attacker_status_effects["Spirit Bomb Charge"]
                            move_message = "causing 80 damage!!!!"
                        elif attacker_status["Spirit Bomb Charge"] == 2:
                            move_message = "charging Spirit Bomb (second turn)"
                    else:
                        attacker_status_effects["Spirit Bomb Charge"] = 3
                        move_message = "charging Spirit Bomb (first turn)"
                else:
                    dmg = random.randint(dmg_range[0], dmg_range[1])
                    move_message = f"causing {dmg} damage!"
            else:
                move_message = "no damage range defined for this move"
        else:
            move_message = "but it missed!"
    else:
        move_message = "move not recognized"
    
    if move == "Burst":
        defender_status_effects["Stunned"] = 1
        attacker_status_effects["Accuracy Boost"] = 3
        move_message = "applying Stunned status and gaining Accuracy Boost!"
        burstCharge = False
    elif move == "Guard":
        attacker_status_effects["Damage Reduction"] = 1
        move_message = "gaining Damage Reduction!"
    elif move == "Ki Gathering":
        attacker_status_effects["Damage Boost"] = 3
        move_message = "gaining Damage Boost!"
    elif move == "Instant Transmission":
        if accuracy > 50:
            attacker_status_effects["Damage Negation"] = 1
            move_message = "dodging all incoming damage!"
        else:
            move_message = "but failed to dodge damage!"
    elif move == "Transformation":
        attacker_status_effects["Super Saiyan"] = float('inf')
        move_message = "transforming into Super Saiyan!"
    elif move == "Faultless Defense":
        attacker_status_effects["Damage Negation"] = 1
        move_message = "negating all incoming damage!"
    elif move == "Transformation":
        attacker_status_effects["Super Saiyan"] = float('inf')
        move_message = "transforming into Super Saiyan!"
        image_change = True  # Indicate image change

    if "Damage Boost" in attacker_status_effects:
        dmg = dmg * 1.5
    if "Damage Reduction" in defender_status_effects:
        dmg = dmg * 0.5
    if "Damage Negation" in defender_status_effects:
        dmg = 0
    
    return dmg, move_message, attacker_status_effects, defender_status_effects
# Function to update status effects and their durations
def update_status_effects(status_effects):
    to_remove = []
    for effect in list(status_effects.keys()):
        if status_effects[effect] > 0:
            status_effects[effect] -= 1
        if status_effects[effect] == 0:
            to_remove.append(effect)
    for effect in to_remove:
        del status_effects[effect]

# Class representing the game layout
class GameLayout:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Layout")
        self.master.geometry("800x425")
        self.master.config(bg="lightblue")

        # Load and set the images for characters
        self.character_left_image = self.get_character_image(playerChar, playerStatus)
        self.character_right_image = self.get_character_image(cpuChar, cpuStatus)

        # Character placeholders with images
        self.character_left = tk.Label(master, image=self.character_left_image, bg="lightblue", width=200, height=200)
        self.character_right = tk.Label(master, image=self.character_right_image, bg="lightblue", width=200, height=200)
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
        global burstCharge
        buttons_text = moves(playerChar, playerStatus)
        super_moves_text = superMoves(playerChar, playerStatus)

        # Create buttons for regular moves
        for i, (text, color) in enumerate(buttons_text.items()):
            if text == "Burst" and burstCharge == False:
                btn = tk.Button(self.moves_frame, text=text, width=20, height=2, bg="grey", state=tk.DISABLED)
            else:
                btn = tk.Button(self.moves_frame, text=text, width=20, height=2, bg=color, command=lambda m=text, c=color: [self.super_moves_increment(), self.handle_turn(m, c)])
            btn.grid(row=i // 3, column=i % 3, padx=10, pady=5)

        self.super_moves_frame = tk.Frame(self.master, bg="lightpink")
        self.super_moves_frame.grid(row=1, column=3, padx=20, pady=20)

        # Create buttons for super moves
        for i, (text, color) in enumerate(super_moves_text.items()):
            btn = tk.Button(self.super_moves_frame, text=text, width=20, height=2, bg=color, command=lambda m=text: self.handle_super_move(m))
            btn.pack(pady=5)

        
    def update_character_images(self):
        self.character_left_image = self.get_character_image(playerChar, playerStatus)
        self.character_right_image = self.get_character_image(cpuChar, cpuStatus)
        self.character_left.config(image=self.character_left_image)
        self.character_right.config(image=self.character_right_image)

         # Method to load character images
    def get_character_image(self, char, status):
        if char == "Sol Badguy":
            image_path = "BackroadBrawl/Sol_Badguy.png"
        elif char == "Goku":
            if "Super Saiyan" in status:
                image_path = "BackroadBrawl/Goku_SSJ.png"
            else:
                image_path = "BackroadBrawl/Goku.png"
        else:
            return None
        
        img = Image.open(image_path)
        img = img.resize((200, 200), Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)


    # Method to handle player turn and move to the next state
    def handle_turn(self, move, color):
        global playerStatus
        global cpuStatus
        global image_change
        update_status_effects(playerStatus)
        dmg, move_message, new_player_status, new_cpu_status = moveLogic(move, superCharge, playerStatus, cpuStatus)
        playerStatus = new_player_status
        cpuStatus = new_cpu_status

        if image_change:
            self.update_character_images()  # Refresh character images
            image_change = False  # Reset the flag

        self.decrement_health("right", dmg)
        
        self.remove_buttons()
        print(playerStatus)
        print(cpuStatus)
        if "Stunned" in cpuStatus:
            self.display_turn_info(f"Player used {move}, {move_message}", self.reset_buttons)
            cpuStatus["Stunned"] -= 1
            if cpuStatus["Stunned"] == 0:
                cpuStatus.pop("Stunned")
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
            self.display_turn_info(f"Player used Super Move: {move}, {move_message}", self.cpu_turn)
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
        moveType = 0
        global cpuStatus
        global playerStatus
        global cpuSuperCharge
        global burstCharge
        update_status_effects(cpuStatus)
        moves_list = list(moves(cpuChar, cpuStatus).keys())
        super_moves_list = list(superMoves(cpuChar, cpuStatus).keys())
        if burstCharge == False and "Burst" in moves_list:
            moves_list.remove("Burst")
        if moves_list:
            moveTypeChoice = random.randint(0, 2)
            if cpuSuperCharge < 4:
                move = random.choice(moves_list)
                moveType = 1
            elif cpuSuperCharge >= 4 and cpuChar == "Goku" and "Super Saiyan" not in cpuStatus:
                move = random.choice(super_moves_list)
                moveType = 2
            elif cpuSuperCharge >= 4 and moveTypeChoice == 2 and "Super Saiyan" not in cpuStatus:
                move = random.choice(super_moves_list)
                moveType = 0
            else:
                move = random.choice(moves_list)
                moveType = 1
            dmg, move_message, new_cpu_status, new_player_status = moveLogic(move, superCharge, cpuStatus, playerStatus)
            
            cpuStatus = new_cpu_status
            playerStatus = new_player_status
            self.decrement_health("left", dmg)
            if moveType == 1: 
                cpuSuperCharge += 1
            elif moveType == 2:
                cpuSuperCharge -= 4
            if "Stunned" in playerStatus:
                self.display_turn_info(f"CPU used {move}, {move_message}", self.cpu_turn)
                playerStatus["Stunned"] -= 1
                if playerStatus["Stunned"] == 0:
                    playerStatus.pop("Stunned")
            else:
                self.display_turn_info(f"CPU used {move}, {move_message}", self.reset_buttons)

    # Method to reset buttons for player turn
    def reset_buttons(self):
        self.moves_frame = tk.Frame(self.master, bg="blue")
        self.moves_frame.grid(row=2, column=0, columnspan=3, pady=20)
        self.create_buttons()  # Recreate buttons

    # Method to decrement health for left or right character
    def decrement_health(self, side, amount):
        if side == "left":
            self.health_left["value"] = max(self.health_left["value"] - amount, 0)
            if self.health_left["value"] <= 0:
                GameLayout.show_result_window("lose", self.master)
        else:
            self.health_right["value"] = max(self.health_right["value"] - amount, 0)
            if self.health_right["value"] <= 0:
                GameLayout.show_result_window("win", self.master)
    
    # Method to increment super moves
    def super_moves_increment(self):
        global superCharge
        if superCharge < 7:
            self.segments[superCharge].config(bg="yellow")
            superCharge += 1

    @staticmethod
    def show_result_window(result, root):
        for widget in root.winfo_children():
            widget.destroy()
        # Create a new window for the result
        result_window = root
        result_window.title("Game Over")

        # Set the size of the window
        result_window.geometry("600x400")
        result_window.config(bg="lightblue")

        # Load and display the appropriate image and message
        if result == "win":
            img = Image.open("BackroadBrawl/celebration.png")
            message = "Congratulations! You have won the game!"
        else:
            img = Image.open("BackroadBrawl/defeat.png")
            message = "Sorry, you lost the game. Better luck next time!"

        # Resize the image to fit the window
        img = img.resize((600, 300), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)

        img_label = tk.Label(result_window, image=img, bg="lightblue")
        img_label.image = img  # Keep a reference to avoid garbage collection
        img_label.pack(pady=20)

        message_label = tk.Label(result_window, text=message, font=('Helvetica', 16), bg="lightblue")
        message_label.pack(pady=10)

        # Add a button to close the result window and the main application
        def close_all():
            root.quit()  # Stops the Tkinter event loop
            root.destroy()  # Properly destroys the main window and all child windows

        close_button = tk.Button(result_window, text="Close", command=close_all)
        close_button.pack(pady=20)


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