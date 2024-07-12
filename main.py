import tkinter as tk



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


    def buttonColor(name):
        if name["bg"] == "red":
            name["bg"] = "white"
        elif name["bg"] == "white":
            name["bg"] = "red"

    # Add six buttons in the center
    button1 = tk.Button(button_frame, text=f"Char 1", bg='white', command=lambda:buttonColor(button1))
    button1.grid(row=1, column=1, padx=10, pady=10)

    button2 = tk.Button(button_frame, text=f"Char 2", bg='white', command=lambda:buttonColor(button2))
    button2.grid(row=1, column=2, padx=10, pady=10)

    button3 = tk.Button(button_frame, text=f"Char 3", bg='white', command=lambda:buttonColor(button3))
    button3.grid(row=2, column=1, padx=10, pady=10)

    button4 = tk.Button(button_frame, text=f"Char 4", bg='white', command=lambda:buttonColor(button4))
    button4.grid(row=2, column=2, padx=10, pady=10)

    button5 = tk.Button(button_frame, text=f"Char 5", bg='white', command=lambda:buttonColor(button5))
    button5.grid(row=3, column=1, padx=10, pady=10)

    button6 = tk.Button(button_frame, text=f"Char 6", bg='white', command=lambda:buttonColor(button6))
    button6.grid(row=3, column=2, padx=10, pady=10)

    # Make sure the buttons resize appropriately
    for i in range(2):
        button_frame.columnconfigure(i, weight=1)
    for i in range(3):
        button_frame.rowconfigure(i, weight=1)

    # Add a confirm button below the other buttons
    confirm_button = tk.Button(frame, text="Confirm", bg='white')
    confirm_button.pack(pady=20)

    return root

def createWindow():
    root = tk.Tk()
    root.title("Backroad Brawl")
    root.geometry("500x400")
    root.configure(bg='blue')

    return root

def main():
    app = createWindow()
    menuLayout(app)
    app.mainloop()

if __name__ == "__main__":
    main()
