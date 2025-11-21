import tkinter as tk
from PIL import Image, ImageTk
import os

# =============================
# Window setup
# =============================
root = tk.Tk()
root.title("Portrait Window")

# Portrait size
window_width = 520
window_height = 956

# Center the window
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x}+{y}")
root.resizable(False, False)

# =============================
# Load background
# =============================
bg_path = os.path.join("assets", "bg.png")
if not os.path.exists(bg_path):
    raise FileNotFoundError(f"Background image not found: {bg_path}")

bg_image = Image.open(bg_path)
bg_image = bg_image.resize((window_width, window_height), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# =============================
# Function to remove white around button
# =============================
def load_button_remove_white(path, width, height):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Button image not found: {path}")
    img = Image.open(path).convert("RGBA")
    # Remove almost-white pixels
    datas = img.getdata()
    new_data = []
    for item in datas:
        if item[0] > 240 and item[1] > 240 and item[2] > 240:  # white threshold
            new_data.append((255, 255, 255, 0))  # fully transparent
        else:
            new_data.append(item)
    img.putdata(new_data)
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    return ImageTk.PhotoImage(img)

# =============================
# Buttons
# =============================
accept_photo = load_button_remove_white(os.path.join("assets", "accept.png"), 126, 43)
accept_button = tk.Button(root, image=accept_photo, borderwidth=0)
accept_button.place(x=265, y=857)

# Exit button
exit_photo = load_button_remove_white(os.path.join("assets", "exit.png"), 126, 43)
exit_button = tk.Button(root, image=exit_photo, borderwidth=0, command=root.destroy)
exit_button.place(x=141, y=857)

# =============================
# Run application
# =============================
root.mainloop()
