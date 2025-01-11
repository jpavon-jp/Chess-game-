import tkinter as tk
from tkinter import ttk # It provides a modern-themed notebook
from PIL import Image, ImageTk
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the base directory of the script

def create_window_with_pages():
    # Function to center the window on the screen, slightly higher
    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()  # Get the width of the screen
        screen_height = window.winfo_screenheight()  # Get the height of the screen
        x = (screen_width // 2) - (width // 2)  # Calculate x position to center the window
        y = (screen_height // 2) - (height // 2) - 50  # Calculate y position to center and adjust upward
        window.geometry(f"{width}x{height}+{x}+{y}")  # Set the window geometry with the calculated position

    # Function to recursively search for a file in a directory
    def find_file_recursive(start_dir, filename):
        for root, dirs, files in os.walk(start_dir):  # Walk through the directory and its subdirectories
            if filename in files:  # If the filename is found
                return os.path.join(root, filename)  # Return the full file path
        return None  # Return None if the file is not found

    # Automatically find image paths from anywhere within the script's directory
    base_directory = os.path.dirname(os.path.abspath(__file__))  # Get the base directory of the script
    image_files = {
        "General Chess Rules": "general_chess_rules.png",  # Define the image file names
        "Piece Movements": "piece_movements.png",
        "Additional Information": "additional_information.png",
        "About This Game": "about.png",
        "Meet the Team": "team.png",
    }

    # Locate each image file using the recursive search function
    image_paths = {}
    for name, filename in image_files.items():
        path = find_file_recursive(base_directory, filename)  # Find each image file path
        if path is None:
            print(f"Error: File '{filename}' not found in '{base_directory}' or its subdirectories.")  # Print error if file is not found
            return
        image_paths[name] = path  # Store the path for each image

    # Create the main window
    root = tk.Tk()
    root.title("Chess Information")  # Set the window title
    center_window(root, 900, 600)  # Center the window with the adjustment
    icon_path = os.path.join(BASE_DIR, "assets", "Menu", "Chess-Logo.ico")  # Path for the window icon
    root.iconbitmap(icon_path)  # Set the window icon

    # Create a notebook (tabbed interface) for different pages
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)  # Add the notebook to the window

    # Load images for each page
    images = {}
    for name, path in image_paths.items():
        img = Image.open(path)  # Open the image file
        img = img.resize((900, 600), Image.Resampling.LANCZOS)  # Resize the image to fit the window
        images[name] = ImageTk.PhotoImage(img)  # Store the resized image as a PhotoImage object

    # Create a frame for each page and add images to each tab
    for name, img in images.items():
        frame = ttk.Frame(notebook)  # Create a frame for each tab
        notebook.add(frame, text=name)  # Add the frame with the appropriate title
        label = tk.Label(frame, image=img)  # Create a label to hold the image
        label.place(relwidth=1, relheight=1)  # Cover the entire frame with the image
        label.image = img  # Keep a reference to avoid garbage collection

    # Start the Tkinter event loop to make the window interactive
    root.mainloop()

# Run the function to create the window with pages
create_window_with_pages()
