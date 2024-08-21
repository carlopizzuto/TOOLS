#!/usr/bin/env python3

import tkinter as tk

class AlwaysOnTopTextInput:
    def __init__(self, root):
        self.root = root
        self.root.title("Input Window")

        # Set the window's background color to black
        self.root.configure(bg='black')

        # Make the window always on top
        self.root.attributes("-topmost", True)

        # Assuming 200px by 100px size for the window
        window_width = 400
        window_height = 200

        # Get screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate x and y coordinates for the Tk root window
        x = screen_width - window_width
        y = 0  # Top of the screen

        # Set the dimensions of the window and where it is placed
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')

        # Create a Text widget with a specified font size (e.g., 14 points)
        self.text_input = tk.Text(self.root, height=5, width=40, bg="black", fg="white",
                                  insertbackground="white", font=("Helvetica", 18))
        self.text_input.pack(pady=20, padx=20, fill='both', expand=True)

def main():
    root = tk.Tk()
    app = AlwaysOnTopTextInput(root)
    root.mainloop()

if __name__ == "__main__":
    main()
