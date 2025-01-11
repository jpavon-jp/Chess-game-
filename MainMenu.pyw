import tkinter as tk  # Use it to create the GUI.
from PIL import Image, ImageTk  # Use Pillow for image manipulation and recizing.
import subprocess
import os
from tkinter import messagebox # It give us the popup dialogs for displaying messages as warnings or errors.
import sys
from tkinter import simpledialog # Enables simple input dialogs for getting user input as text or numbers

# Base directory for dynamic paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the base directory of the script
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "Menu")  # It is the directory for assets like images

# Function to start the game
def start_game():
    """Start the game."""
    # Here it checks if all selections (mode, style, language) are made, and if not it'll show a message box that will show us a warning. Also in this code I used two types of message boxes, I used showwarning and showinfo.
    if not selected_mode.get() or not selected_style.get() or not selected_language.get():
        tk.messagebox.showwarning("Missing Selection", "Please select mode, style, and language before starting!")
        return

    # Show name input window based on selected mode
    get_player_names(selected_mode.get())

# Function to get player names based on the selected mode
def get_player_names(mode):
    """Open a custom window to get player names based on the game mode."""
    
    # Function to submit the names and start the game
    def submit_names():
        # Here it get the entered names and ensure they are not empty
        p1_name = player1_entry.get().strip()
        p2_name = player2_entry.get().strip() if mode == "1 VS 1" else "AI"

        if not p1_name or (mode == "1 VS 1" and not p2_name):
            tk.messagebox.showwarning("Missing Names", "Please fill in all the fields!") # And if one field of the names is empty it will popup a message box with the warning.
            return

        # Close the name input window
        name_window.destroy()

        # Start the game with the selected style, names, and language
        main_menu_root.destroy()  # Close the main menu window
        subprocess.Popen([  # Run the game script with appropriate arguments
            "python",
            os.path.join(BASE_DIR, "Chess.pyw"),
            selected_style.get(),
            p1_name,
            p2_name,
            selected_language.get()
        ])
    
    # Create the name input window
    name_window = tk.Toplevel(main_menu_root)  # Create a new top-level window, main_menu_root is the principal window
    name_window.title("Enter Player Names") 
    icon_path = os.path.join(BASE_DIR, "assets", "Menu", "Chess-Logo.ico")
    name_window.iconbitmap(icon_path)  # Set the window's icon

    # Here I define the window dimensions and position it at the center of the screen
    window_width = 400
    window_height = 300
    screen_width = name_window.winfo_screenwidth()
    screen_height = name_window.winfo_screenheight()
    x_position = (screen_width // 2) - (window_width // 2)
    y_position = (screen_height // 2) - (window_height // 2)
    name_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    name_window.configure(bg="#4A646C")

    # Title and input fields for player names
    tk.Label(name_window, text="Enter Player Names", font=("Arial", 20, "bold"), bg="#4A646C", fg="white").pack(pady=10)
    tk.Label(name_window, text="Player 1 Name:", font=("Arial", 14), bg="#4A646C", fg="white").pack(pady=5)
    player1_entry = tk.Entry(name_window, font=("Arial", 14))  # Input for Player 1
    player1_entry.pack(pady=5)

    # Player 2 Name Entry (if applicable)
    if mode == "1 VS 1":
        tk.Label(name_window, text="Player 2 Name:", font=("Arial", 14), bg="#4A646C", fg="white").pack(pady=5)
        player2_entry = tk.Entry(name_window, font=("Arial", 14))  # Input for Player 2
        player2_entry.pack(pady=5)
    else:
        player2_entry = None  # AI will be used for Player 2 in single-player mode

    # Here is the Confirm Button to start the game
    tk.Button(name_window, text="Start Game", font=("Arial", 14, "bold"), bg="#E87A59", fg="white",
              command=submit_names).pack(pady=20)

# Main menu function to create and display the menu
def main_menu():
    """Create and display the main menu."""
    global main_menu_root, selected_mode, selected_style, selected_language 

    # Create the main menu window
    main_menu_root = tk.Tk() # main window
    main_menu_root.title("Welcome to Chess") # name of the window
    main_menu_root.configure(bg="#4A646C") # window color 
    main_menu_root.state("zoomed")  # Maximize the window on startup
    icon_path = os.path.join(BASE_DIR, "assets", "Menu", "Chess-Logo.ico") # the path to find the icon
    main_menu_root.iconbitmap(icon_path)  # Set the window's icon

    # Initialize variables to store the selected options
    selected_mode = tk.StringVar()
    selected_style = tk.StringVar()
    selected_language = tk.StringVar()

    # Main frame to hold the content
    main_container = tk.Frame(main_menu_root, bg="#4A646C") 
    main_container.pack(expand=True)

    # Title Label
    tk.Label(main_container, text="Welcome to Chess", font=("Arial", 45, "bold"), bg="#4A646C", fg="white").pack(pady=20) # Here I create the label of the title, and I asset the font name, size and color.

    # Game Mode Selection
    tk.Label(main_container, text="Choose your game mode:", font=("Arial", 19, "bold"), bg="#4A646C", fg="white").pack(pady=10)
    mode_frame = tk.Frame(main_container, bg="#4A646C")
    mode_frame.pack()

    # Mode Selection (1 vs 1)
    for mode, file in [("1 VS 1", "1vs1.png")]:
        img_path = os.path.join(ASSETS_DIR, file) # path to find the images 
        img = Image.open(img_path).resize((230, 130), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        btn = tk.Radiobutton(mode_frame, image=img, variable=selected_mode, value=mode, indicatoron=False,
                             bg="#4A646C", selectcolor="#4A646C", borderwidth=0)
        btn.image = img
        btn.pack(side="left", padx=10)

    # Style Selection
    tk.Label(main_container, text="Choose your style:", font=("Arial", 19, "bold"), bg="#4A646C", fg="white").pack(pady=10)
    style_frame = tk.Frame(main_container, bg="#4A646C")
    style_frame.pack()

    # Style Options (Baby, Wood, Spooky, etc.)
    for style, file in [("Baby", "baby.png"), ("Wood", "wood.png"), ("Spooky", "spooky.png"), ("Nightly", "nightly.png"), ("Love", "love.png")]:
        img_path = os.path.join(ASSETS_DIR, file)
        img = Image.open(img_path).resize((80, 80), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        container = tk.Frame(style_frame, bg="#4A646C")
        container.pack(side="left", padx=20)
        tk.Radiobutton(container, image=img, variable=selected_style, value=style, indicatoron=False,
                       bg="#4A646C", borderwidth=0).pack()
        container.image = img
        tk.Label(container, text=style, font=("Arial", 14), bg="#4A646C", fg="white").pack()

    # Language Selection
    tk.Label(main_container, text="Choose your language:", font=("Arial", 19, "bold"), bg="#4A646C", fg="white").pack(pady=10)
    language_frame = tk.Frame(main_container, bg="#4A646C")
    language_frame.pack()

    # Language Options (Spanish, English, Turkish)
    for lang, file in [("Spanish", "spanish.png"), ("English", "english.png"), ("Turkish", "turkish.png")]:
        img_path = os.path.join(ASSETS_DIR, file)
        img = Image.open(img_path).resize((70, 50), Image.Resampling.LANCZOS)
        img = ImageTk.PhotoImage(img)
        container = tk.Frame(language_frame, bg="#4A646C")
        container.pack(side="left", padx=20)
        tk.Radiobutton(container, image=img, variable=selected_language, value=lang, indicatoron=False,
                       bg="#4A646C", borderwidth=0).pack()
        container.image = img

    # Play Button
    play_path = os.path.join(ASSETS_DIR, "play.png")
    play_img = Image.open(play_path).resize((250, 150), Image.Resampling.LANCZOS)
    play_img = ImageTk.PhotoImage(play_img)
    tk.Button(main_container, image=play_img, command=start_game, bg="#4A646C", borderwidth=0).pack(pady=20)
    main_menu_root.image = play_img  # Prevent garbage collection of the image
    
    # Corner Images (Decorative)
    corner_left_path = os.path.join(ASSETS_DIR, "corner_left.png")
    corner_right_path = os.path.join(ASSETS_DIR, "corner_right.png")
    corner_left = Image.open(corner_left_path).resize((100, 100), Image.Resampling.LANCZOS)
    corner_right = Image.open(corner_right_path).resize((100, 100), Image.Resampling.LANCZOS)
    corner_left_img = ImageTk.PhotoImage(corner_left)
    corner_right_img = ImageTk.PhotoImage(corner_right)

    # Place corner images at specific positions
    tk.Label(main_menu_root, image=corner_left_img, bg="#4A646C").place(x=20, y=main_menu_root.winfo_screenheight() - 120)
    tk.Label(main_menu_root, image=corner_right_img, bg="#4A646C").place(x=main_menu_root.winfo_screenwidth() - 120, y=main_menu_root.winfo_screenheight() - 120)

    # Keep references to avoid garbage collection
    main_menu_root.corner_left_img = corner_left_img
    main_menu_root.corner_right_img = corner_right_img

    # Run the main menu event loop
    main_menu_root.mainloop()

# Entry point for the program
if __name__ == "__main__":
    main_menu()
