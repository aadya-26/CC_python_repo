import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Aad's GUI")
root.geometry("400x300")

# Create a label to display a message
label = tk.Label(root, text="Click the button", font=("Helvetica", 16))
label.pack(pady=20)

# Function to change the button color and update the label text
def on_button_click():
    label.config(text="Button clicked!")
    button.config(bg="lightblue")

# Create a button that triggers the on_button_click function when clicked
button = tk.Button(root, text="Click Me", font=("Helvetica", 14), command=on_button_click)
button.pack(pady=20)

# Start the GUI event loop
root.mainloop()
