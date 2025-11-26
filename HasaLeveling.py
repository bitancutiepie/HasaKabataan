import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import pygame
import mysql.connector
import webbrowser 

# --- GLOBAL CONSTANTS ---
ASSETS_DIR = "assets" # for the pathing ng image dapat nasa assets

# NEW: Sound effect file path
CLICK_SOUND_PATH = os.path.join(ASSETS_DIR, "clicksoundeffect.wav") # directory of the sound fx

# PORTRAIT Constants (Root Window) - view of the landing and avatar frame
WINDOW_WIDTH = 520
WINDOW_HEIGHT = 956
SLIDER_WIDTH_PORTRAIT = 200
PORTRAIT_Y = WINDOW_HEIGHT - 40 # Position for the volume slider at the bottom
ICON_SIZE = 20 # Small icons for the portrait view
APP_ICON_SIZE = 32 # Size for the main app icon

# LANDSCAPE Constants (Toplevel Window) - This is the main dashboard/game screen (wide view)
LANDSCAPE_WIDTH = 1366
LANDSCAPE_HEIGHT = 768

# LANDSCAPE SLIDER CONSTANTS
LANDSCAPE_SLIDER_WIDTH = 150
LANDSCAPE_ICON_SIZE = 25
LANDSCAPE_SLIDER_X = LANDSCAPE_WIDTH - LANDSCAPE_SLIDER_WIDTH - 110 
LANDSCAPE_SLIDER_Y = 700 # Volume slider near the bottom right of the landscape screen

# --- AVATAR & USERNAME TEXT CONSTANTS (For Frame 3 - The Dashboard) ---
AVATAR_CENTER_X = 1080  # Where the character avatar sits (right side)
AVATAR_CENTER_Y = 130 
USERNAME_TEXT_X = 450 # Where the HUGE username text goes (left side)
USER_NAME_TEXT_Y = 125

# Avatar Dimensions for Individual Scaling - Makes sure our characters look right!
MALE_AVATAR_DIMS = (560, 315)
FEMALE_AVATAR_DIMS = (522, 273) 

# --- TUTORIAL FRAME ICON CONSTANTS ---
TUTORIAL_ICON_X = 240 # X-position for the large skill icon on the tutorial/problem frames (left side)
TUTORIAL_ICON_Y = 455 
TUTORIAL_ICON_DIMS = (160, 203)

# --- PROBLEM SOLVER BUTTON CONSTANTS ---
REVEAL_ANSWER_DIMS = (240, 130)
REVEAL_ANSWER_COORDS = (740, 530) # Position for the 'Reveal Answer' button

BACK_PROBLEM_DIMS = (220, 110)
BACK_PROBLEM_COORDS = (160, 580) # Position for the 'Back' button on problem/answer frames

# --- ANSWER FRAME BUTTON CONSTANTS (New) ---
ADDSKILL_BUTTON_DIMS = (220, 110)
ADDSKILL_BUTTON_COORDS = (1255, 625) # Position for the 'Add Skill' button

# --- QOL ADDITION: LANDSCAPE USERNAME DISPLAY ---
LANDSCAPE_USERNAME_X = LANDSCAPE_WIDTH - 50 # Near the right edge
LANDSCAPE_USERNAME_Y = 30 # Near the top
LANDSCAPE_USERNAME_FONT = ("Arial Black", 16, "bold")


# --- TUTORIAL YOUTUBE LINKS ---
TUTORIAL_LINKS = {
    # Replace these with real links once the game is live!
    "Python": {
        1: "https://www.youtube.com/watch?v=UBZs0-gUZsU&list=PLVnJhHoKgEmpbmB-Lrb2m4wwq5IPgLHnG", 
        2: "https://www.youtube.com/watch?v=uVO_bElzTbI&list=PLVnJhHoKgEmpbmB-Lrb2m4wwq5IPgLHnG&index=2",
        3: "https://www.youtube.com/watch?v=AvlYWx0T-fo&list=PLVnJhHoKgEmpbmB-Lrb2m4wwq5IPgLHnG&index=3",
        4: "https://www.youtube.com/watch?v=d4itGdI6Zaw&list=PLVnJhHoKgEmpbmB-Lrb2m4wwq5IPgLHnG&index=4",
        5: "https://www.youtube.com/watch?v=ZLrNYnye4r4&list=PLVnJhHoKgEmpbmB-Lrb2m4wwq5IPgLHnG&index=5" 
    },
    # ... other languages ...
    "Java": {
    1: "https://www.youtube.com/watch?v=8HXqOHH2ocM&list=PLVnJhHoKgEmpzFnP_wofuPrUfa0xoxT4f",
    2: "https://www.youtube.com/watch?v=lePkYEGt2es&list=PLVnJhHoKgEmpzFnP_wofuPrUfa0xoxT4f&index=2",
    3: "https://www.youtube.com/watch?v=76b2d6ozN_k&list=PLVnJhHoKgEmpzFnP_wofuPrUfa0xoxT4f&index=3",
    4: "https://www.youtube.com/watch?v=LzeUR6JJBZo&list=PLVnJhHoKgEmpzFnP_wofuPrUfa0xoxT4f&index=4",
    5: "https://www.youtube.com/watch?v=m8Qo5vT-5MY&list=PLVnJhHoKgEmpzFnP_wofuPrUfa0xoxT4f&index=5"
    },
    "HTML": {
    1: "https://www.youtube.com/watch?v=29l2qxSJSIw&list=PLVnJhHoKgEmoQ_6hXCKNDa2zTlzu5xe4k",
    2: "https://www.youtube.com/watch?v=pU8B8dEMeTo&list=PLVnJhHoKgEmoQ_6hXCKNDa2zTlzu5xe4k&index=2",
    3: "https://www.youtube.com/watch?v=EP8JQhiQb4Q&list=PLVnJhHoKgEmoQ_6hXCKNDa2zTlzu5xe4k&index=3",
    4: "https://www.youtube.com/watch?v=EP8JQhiQb4Q&list=PLVnJhHoKgEmoQ_6hXCKNDa2zTlzu5xe4k&index=4",
    5: "https://www.youtube.com/watch?v=EP8JQhiQb4Q&list=PLVnJhHoKgEmoQ_6hXCKNDa2zTlzu5xe4k&index=5"
},
    "C++": {
    1: "https://www.youtube.com/watch?v=vwzlg-wSDH0&list=PLVnJhHoKgEmrAk6XdaioMlfmpD_ahnA-B",
    2: "https://www.youtube.com/watch?v=Nma5TNskoJo&list=PLVnJhHoKgEmrAk6XdaioMlfmpD_ahnA-B&index=2",
    3: "https://www.youtube.com/watch?v=Nma5TNskoJo&list=PLVnJhHoKgEmrAk6XdaioMlfmpD_ahnA-B&index=3",
    4: "https://www.youtube.com/watch?v=Nma5TNskoJo&list=PLVnJhHoKgEmrAk6XdaioMlfmpD_ahnA-B&index=4",
    5: "https://www.youtube.com/watch?v=Nma5TNskoJo&list=PLVnJhHoKgEmrAk6XdaioMlfmpD_ahnA-B&index=5"
    },

    "MySQL": {
    1: "https://www.youtube.com/watch?v=VHbU59oNoAg&list=PLVnJhHoKgEmpKvMh-wio-7FOouf9Fa0a8",
    2: "https://www.youtube.com/watch?v=sCrc0iJHGWc&list=PLVnJhHoKgEmpKvMh-wio-7FOouf9Fa0a8&index=2",
    3: "https://www.youtube.com/watch?v=sCrc0iJHGWc&list=PLVnJhHoKgEmpKvMh-wio-7FOouf9Fa0a8&index=3",
    4: "https://www.youtube.com/watch?v=sCrc0iJHGWc&list=PLVnJhHoKgEmpKvMh-wio-7FOouf9Fa0a8&index=4",
    5: "https://www.youtube.com/watch?v=sCrc0iJHGWc&list=PLVnJhHoKgEmpKvMh-wio-7FOouf9Fa0a8&index=5"
}
}

# --- TUTORIAL PLAY BUTTON CONFIGURATION ---
PLAY_BUTTONS_DIMS = (156.1, 47.3) # Dimensions for the small 'play' buttons
PLAY_BUTTONS_CONFIG = [
    # Coordinates are for the center of the image
    {"tag": "play1_btn", "path": "play1.png", "dims": PLAY_BUTTONS_DIMS, "coords": (514, 422), "button_num": 1},
    {"tag": "play2_btn", "path": "play2.png", "dims": PLAY_BUTTONS_DIMS, "coords": (773, 422), "button_num": 2},
    {"tag": "play3_btn", "path": "play3.png", "dims": PLAY_BUTTONS_DIMS, "coords": (1037, 422), "button_num": 3},
    {"tag": "play4_btn", "path": "play4.png", "dims": PLAY_BUTTONS_DIMS, "coords": (654, 598), "button_num": 4},
    {"tag": "play5_btn", "path": "play5.png", "dims": PLAY_BUTTONS_DIMS, "coords": (921, 598), "button_num": 5},
]

# --- DATABASE CONFIGURATION ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",           
    "password": "jayvee101", # Make sure to use a strong, private password for production!
    "database": "hasaleveling_db"
}

# SKILL BUTTON CONFIGURATION (Left Side of Dashboard - Frame 3)
SKILL_BUTTONS = [
    # These buttons link to the tutorial/problem selection for each skill
    {"tag": "pythonskill_btn", "path": "pythonskill.png", "dims": (219, 137), "coords": (137, 411), "handler": lambda e: on_skill_button_click("Python")},
    {"tag": "javaskill_btn", "path": "javaskill.png", "dims": (223, 139), "coords": (325, 408), "handler": lambda e: on_skill_button_click("Java")},
    {"tag": "htmlskill_btn", "path": "htmlskill.png", "dims": (219, 137), "coords": (137, 513), "handler": lambda e: on_skill_button_click("HTML")},
    {"tag": "c++skill_btn", "path": "c++skill.png", "dims": (223, 139), "coords": (327, 514), "handler": lambda e: on_skill_button_click("C++")},
    {"tag": "mysqlskill_btn", "path": "mysqlskill.png", "dims": (220, 137), "coords": (224, 614), "handler": lambda e: on_skill_button_click("MySQL")},
]

# BASE SKILL PROGRESS BAR CONFIGURATION (Right Side of Dashboard - Frame 3)
BASE_SKILL_PROGRESS_BARS = [
    # Defines where the progress bars are drawn and what data they connect to
    {"skill": "HTML", "db_key": "html_progress", "x": 981, "y": 371, "w": 308, "h": 31, "color": "#007BA7"}, 
    {"skill": "C++", "db_key": "cplusplus_progress", "x": 981, "y": 432, "w": 308, "h": 31, "color": "#A03472"}, 
    {"skill": "MySQL", "db_key": "mysql_progress", "x": 981, "y": 491, "w": 308, "h": 31, "color": "#00A79D"}, 
    {"skill": "Python", "db_key": "python_progress", "x": 981, "y": 558, "w": 308, "h": 31, "color": "#D33842"}, 
    {"skill": "Java", "db_key": "java_progress", "x": 981, "y": 616, "w": 308, "h": 31, "color": "#007BA7"}, 
]


# --- GLOBAL STATE/DATA ---
class AppState:
    """
    This class holds all the important information that needs to be accessed
    across different windows, frames, and functions. It's the brain of the app!
    """
    def __init__(self):
        self.root = None # The main Tkinter window (portrait mode)
        self.current_canvas = None # The current screen being shown
        self.landscape_window = None # The big secondary window for the game content
        self.gender_label = None # Label for showing selected gender
        self.volume_slider_root = None # Slider in the main window
        self.volume_slider_landscape = None # Slider in the game window
        self.app_icon_ref = None # Reference to prevent the app icon from being garbage collected
        self.icon_ref_portrait = None
        self.icon_label_portrait = None
        self.icon_ref_landscape = None
        self.icon_label_landscape = None
        self.button_data = {} # Stores info for all the cool pulsing buttons!
        self.selected_gender = None # 'Male' or 'Female'
        self.user_name = None # The current user's name
        self.bg_ref = None # Reference to the background image
        self.initial_volume = 50.0 # Starting volume percentage
        self.banner_char_ref = None # Reference to the character avatar on the dashboard
        self.skill_bar_refs = [] # References to progress bar elements
        self.db_progress_data = {} # Stores the user's progress fetched from the database
        self.user_list = {} # List of users for the login/delete screen
        self.tutorial_icon_ref = None # Reference to the skill icon on tutorial frame
        self.current_tutorial_skill = None # Which skill's tutorial/problem are we looking at?
        self.click_sound = None # Pygame Sound object for the click effect
        self.current_problem_number = None # Keeps track of the current problem (1-5)
        
STATE = AppState() # Create the single global state object

# =============================
# Database Functions - Where we talk to MySQL!
# =============================

def get_db_connection():
    """Tries to connect to the MySQL database using DB_CONFIG."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        error_message = f"Database Connection Error: {err}"
        print(error_message)
        # Only show the error once to avoid spamming the user if DB is down
        if STATE.db_progress_data.get("status") != "failed":
            messagebox.showerror("Database Error", f"Could not connect to MySQL.\nPlease check your DB_CONFIG.\n\nError: {err}")
            STATE.db_progress_data["status"] = "failed"
        return None

def fetch_all_users():
    """Pulls all usernames and genders from the database for the login/selection screen."""
    conn = get_db_connection()
    if not conn:
        return {} # No connection, no users
    try:
        cursor = conn.cursor()
        query = "SELECT username, gender FROM user_progress"
        cursor.execute(query)
        user_data = {username: gender for (username, gender) in cursor}
    except mysql.connector.Error as err:
        print(f"Database Query Error: {err}")
        user_data = {}
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return user_data

def get_user_progress(username):
    """Fetches a specific user's skill progress from the database."""
    conn = get_db_connection()
    # If DB is down, use safe default values (10%)
    if not conn:
        return {
            "html_progress": 0.10, "cplusplus_progress": 0.10, 
            "mysql_progress": 0.10, "python_progress": 0.10, 
            "java_progress": 0.10, "status": "default_used"
        }

    try:
        cursor = conn.cursor(dictionary=True) # Returns results as a dictionary (super handy!)
        query = "SELECT html_progress, cplusplus_progress, mysql_progress, python_progress, java_progress, gender FROM user_progress WHERE username = %s"
        cursor.execute(query, (username.upper(),)) # Names are stored uppercase for consistency
        data = cursor.fetchone()
        
        if data:
            # Convert progress values (which are strings from DB) to floats
            progress_data = {key: float(value) for key, value in data.items() if key != 'gender'}
            progress_data["status"] = "success"
            STATE.selected_gender = data['gender'] # Update the global gender state
            return progress_data
        
        # Should only happen if a new user is created and immediately queried (which shouldn't happen here)
        return {key: 0.10 for key in ["html_progress", "cplusplus_progress", "mysql_progress", "python_progress", "java_progress"]}

    except mysql.connector.Error as err:
        messagebox.showwarning("Database Warning", "Could not fetch user progress. Using default values.")
        return {key: 0.10 for key in ["html_progress", "cplusplus_progress", "mysql_progress", "python_progress", "java_progress"]}
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# NEW FUNCTION: Update user progress by a specified amount
def update_user_progress(username, db_key, increment):
    """
    Increases a user's skill progress in the database, capping it at 1.0 (100%).
    Called when a problem is completed!
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    # We need to map the nice skill name (e.g., "Python") to the database column name (e.g., "python_progress")
    skill_map = {
        "HTML": "html_progress",
        "C++": "cplusplus_progress",
        "MySQL": "mysql_progress",
        "Python": "python_progress",
        "Java": "java_progress"
    }
    column_name = skill_map.get(db_key) 
    if not column_name:
        print(f"Error: Invalid skill name provided: {db_key}")
        return False
        
    try:
        cursor = conn.cursor()
        # The 'LEAST(column + increment, 1.0)' ensures we never go over 100% (1.0)
        update_query = f"""
        UPDATE user_progress 
        SET {column_name} = LEAST({column_name} + %s, 1.0) 
        WHERE username = %s
        """
        cursor.execute(update_query, (increment, username.upper()))
        conn.commit()
        return cursor.rowcount > 0 # Returns True if a row was updated
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to update progress for {db_key}: {err}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def insert_new_user(username, gender):
    """Adds a brand new user to the database, setting all skills to 10% progress."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO user_progress (username, gender, html_progress, cplusplus_progress, mysql_progress, python_progress, java_progress)
        VALUES (%s, %s, 0.10, 0.10, 0.10, 0.10, 0.10)
        """
        cursor.execute(insert_query, (username.upper(), gender))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        if err.errno == 1062: # MySQL error code for duplicate entry (username already exists)
            messagebox.showerror("Registration Error", "That username already exists!")
        else:
            messagebox.showerror("Database Error", f"Failed to register new user: {err}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def delete_user_progress(username):
    """Deletes a user's entire profile from the database."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        delete_query = "DELETE FROM user_progress WHERE username = %s"
        cursor.execute(delete_query, (username.upper(),))
        conn.commit()
        if cursor.rowcount > 0:
            return True
        else:
            messagebox.showwarning("Delete Error", f"User '{username}' not found.")
            return False
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to delete user: {err}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

# =============================
# Helper Functions - Small, useful tools
# =============================

def log_coordinates(event):
    """A helpful developer tool to see where the user clicked on the canvas."""
    print(f"Clicked Coordinates (X, Y): {event.x}, {event.y}")

def load_pil_image(filename, width, height, mode='RGBA'):
    """
    Loads an image, resizes it, and handles missing files by showing a
    friendly 'MISSING' placeholder. Always returns an Image object.
    """
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        # QoL Addition: Better visual for missing asset
        placeholder = Image.new(mode, (width, height), color='red')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(placeholder)
        draw.text((10, 10), f"MISSING:\n{filename}", fill=(255, 255, 255))
        print(f"Warning: Asset not found: {path}")
        return placeholder
    img = Image.open(path).convert(mode)
    # LANCZOS is a high-quality resampling filter for resizing images
    return img.resize((width, height), Image.Resampling.LANCZOS) 

def draw_skill_progress_bar(canvas, bar_data):
    """
    Draws the segmented progress bar for a skill on the dashboard.
    It looks super cool because it's not just a single rectangle!
    """
    x, y, w, h = bar_data["x"], bar_data["y"], bar_data["w"], bar_data["h"]
    progress = bar_data["progress"] # A float between 0.0 and 1.0
    color = bar_data["color"]
    skill = bar_data["skill"]
    
    padding = 2             
    segment_width = 4       
    gap_width = 1           
    
    # Draw the black background and white border for the whole bar
    canvas.create_rectangle(
        x, y, x + w, y + h, 
        outline="#FFFFFF", 
        width=2,
        fill="#000000",
        tags=f"{skill}_bar_outline"
    )
    
    inner_x_start = x + padding
    inner_y_top = y + padding
    inner_y_bottom = y + h - padding
    usable_width = w - 2 * padding
    segment_unit_width = segment_width + gap_width
    num_total_units = usable_width // segment_unit_width # How many segments fit
    num_segments_to_fill = int(num_total_units * progress) # How many segments should be colored
    
    # Loop through and draw each little segment
    for i in range(num_total_units):
        start_x = inner_x_start + (i * segment_unit_width)
        end_x = start_x + segment_width
        
        if i < num_segments_to_fill:
            fill_color = color # Use the skill's color (filled progress)
        else:
            fill_color = "#333333" # Use a darker gray (unfilled progress)
            if i % 2 == 0:
                 fill_color = "#444444" # Add a slight checkerboard effect to unfilled parts
        
        canvas.create_rectangle(
            start_x, inner_y_top, end_x, inner_y_bottom, 
            outline="",
            fill=fill_color,
            tags=f"{skill}_bar_segment_{i}"
        )

    # Display the percentage text over the bar
    percent_text = f"{int(progress * 100)}%"
    text_x = x + w - 30 
    text_y = y + h / 2
    
    text_id = canvas.create_text(
        text_x, text_y, 
        text=percent_text, 
        font=("Arial", 10, "bold"), 
        fill="#FFFFFF",
        anchor="center",
        tags=f"{skill}_percent_text"
    )
    STATE.skill_bar_refs.append(text_id)

# NEW: Sound playing function
def play_click_sound():
    """Plays a short click sound effect when the user interacts with a button."""
    if STATE.click_sound:
        try:
            STATE.click_sound.play()
        except pygame.error as e:
            # If the sound object is invalid, just skip it and move on
            pass
    else:
        # Load the sound if it hasn't been loaded yet (and if Pygame is initialized)
        try:
            STATE.click_sound = pygame.mixer.Sound(CLICK_SOUND_PATH)
            STATE.click_sound.play()
        except pygame.error as e:
            print(f"Error loading or playing click sound: {e}")
        except FileNotFoundError:
            print(f"Error: Click sound file not found at {CLICK_SOUND_PATH}")

# ---------------------------------------------------------
# ANIMATION & BINDING FUNCTIONS - The magic behind the pulsing buttons!
# ---------------------------------------------------------
def pulse(tag):
    """
    The main animation loop for a single button. It makes the button gently
    grow and shrink when the mouse is hovering over it.
    """
    try:
        canvas_ref = STATE.current_canvas
        if not canvas_ref or not canvas_ref.winfo_exists(): return
    except: return

    data = STATE.button_data.get(tag)
    if not data: return
    
    STEP = 0.002
    MIN_SCALE = 1.00 # Original size
    MAX_SCALE = 1.05 # Max 5% bigger 

    if data["hover"]:
        # If hovering, grow or shrink slightly for the pulse effect
        if data["growing"]:
            data["scale"] = min(MAX_SCALE, data["scale"] + STEP)
            if data["scale"] >= MAX_SCALE: data["growing"] = False
        else:
            data["scale"] = max(MIN_SCALE, data["scale"] - STEP)
            if data["scale"] <= MIN_SCALE: data["growing"] = True
    else:
        # If not hovering, shrink back down to original size
        data["scale"] = max(MIN_SCALE, data["scale"] - STEP)
        
    # Stop the pulse animation once it's back to normal size and the mouse left
    if not data["hover"] and data["scale"] == MIN_SCALE:
        if data["job"]:
            STATE.root.after_cancel(data["job"])
            data["job"] = None
        # Make sure the image is the correct base size when animation stops
        new_photo = ImageTk.PhotoImage(data["base_img"])
        canvas_ref.itemconfig(tag, image=new_photo)
        data["current_photo"] = new_photo
        return

    # Calculate the new size based on the current scale
    original_w, original_h = data["base_img"].size
    new_w = int(original_w * data["scale"])
    new_h = int(original_h * data["scale"])
    
    # Resize the image and update the canvas item
    resized_pil = data["base_img"].resize((new_w, new_h), Image.Resampling.BILINEAR)
    new_photo = ImageTk.PhotoImage(resized_pil)
    
    canvas_ref.itemconfig(tag, image=new_photo)
    data["current_photo"] = new_photo
    
    # Schedule the next step of the pulse
    data["job"] = STATE.root.after(15, lambda: pulse(tag))

def on_enter(event, tag):
    """Fired when the mouse moves over a button. Starts the pulse and changes the cursor."""
    STATE.root.config(cursor="hand2") # Change cursor to a hand to show it's clickable
    data = STATE.button_data.get(tag)
    if data:
        data["hover"] = True
        if data["job"] is None:
            data["growing"] = True # Start the animation loop if it's not already running
            pulse(tag)

def on_leave(event, tag):
    """Fired when the mouse moves off a button. Stops the pulse and resets the cursor."""
    STATE.root.config(cursor="")
    data = STATE.button_data.get(tag)
    if data:
        data["hover"] = False # Tell the pulse function to shrink back to normal

def create_pulsing_button(canvas, tag, filename, dims, coords, click_handler, disable_pulse=False):
    """
    Creates an image button on the canvas, sets it up for the cool pulse animation,
    and binds the click sound and the main handler.
    """
    w, h = dims
    # Load the base image
    pil_base = load_pil_image(filename, round(w), round(h), mode='RGBA') 
    photo = ImageTk.PhotoImage(pil_base)
    
    # Draw the image on the canvas
    canvas.create_image(*coords, image=photo, anchor="center", tags=tag)
    
    # Store a reference to prevent the image from disappearing (garbage collection)
    if not hasattr(canvas, f"{tag}_img_ref"):
        setattr(canvas, f"{tag}_img_ref", photo) 

    # Initialize the button data for the pulse animation
    if not disable_pulse:
        STATE.button_data[tag] = { "base_img": pil_base, "scale": 1.0, "growing": True, 
                                    "hover": False, "job": None, "current_photo": photo }
    else:
        # For buttons that should be clickable but not animated
        STATE.button_data[tag] = { "base_img": pil_base, "scale": 1.0, "growing": False, 
                                    "hover": False, "job": None, "current_photo": photo }

    
    if not disable_pulse:
        # Bind the animation handlers
        canvas.tag_bind(tag, "<Enter>", lambda e: on_enter(e, tag))
        canvas.tag_bind(tag, "<Leave>", lambda e: on_leave(e, tag))
        
        # MODIFIED: Wrap the original handler to play sound first
        def wrapped_handler(event):
            play_click_sound()
            click_handler(event)
            
        canvas.tag_bind(tag, "<Button-1>", wrapped_handler)
    else:
        # For non-pulsing buttons (like the skill icons that navigate back)
        canvas.tag_bind(tag, "<Enter>", lambda e: STATE.root.config(cursor="hand2"))
        canvas.tag_bind(tag, "<Leave>", lambda e: STATE.root.config(cursor=""))
        canvas.tag_bind(tag, "<Button-1>", lambda e: (play_click_sound(), click_handler(e)))


# ---------------------------------------------------------
# AUDIO CONTROL FUNCTIONS & SLIDER CREATION
# ---------------------------------------------------------
def set_volume(value):
    """Sets the music volume based on the slider value (0-100)."""
    try:
        volume = float(value) / 100.0
        pygame.mixer.music.set_volume(volume)
        STATE.initial_volume = float(value) # Save the volume for the next session
    except pygame.error:
        pass # Ignore if pygame isn't working

def start_music(music_file_path):
    """Initializes Pygame mixer, loads the background music, and plays it on a loop."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(music_file_path)
        pygame.mixer.music.set_volume(STATE.initial_volume / 100.0) 
        pygame.mixer.music.play(-1) # The -1 makes it loop forever (until the app closes)
        STATE.initial_volume = pygame.mixer.music.get_volume() * 100
    except pygame.error as e:
        # Print a warning if music fails but don't crash the app
        pass
    except Exception as e:
        pass

def create_volume_slider(parent_window, is_portrait):
    """
    Creates the volume slider and its speaker icon. This is used on both
    the portrait (main) and landscape (game) windows.
    """
    # Determine which state variables to use based on the window size
    if is_portrait:
        slider_attr = "volume_slider_root"
        icon_label_attr = "icon_label_portrait"
        icon_ref_attr = "icon_ref_portrait"
        slider_width = SLIDER_WIDTH_PORTRAIT
        y_position = PORTRAIT_Y
        icon_size = ICON_SIZE
    else:
        slider_attr = "volume_slider_landscape"
        icon_label_attr = "icon_label_landscape"
        icon_ref_attr = "icon_ref_landscape"
        slider_width = LANDSCAPE_SLIDER_WIDTH
        y_position = LANDSCAPE_SLIDER_Y 
        icon_size = LANDSCAPE_ICON_SIZE

    # Clean up any existing slider/label before creating new ones
    current_slider = getattr(STATE, slider_attr)
    if current_slider: current_slider.destroy()
    current_label = getattr(STATE, icon_label_attr)
    if current_label and current_label.winfo_exists(): current_label.destroy()
    setattr(STATE, icon_label_attr, None)

    # Styling the slider to look a bit better
    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TScale", background=parent_window['bg'], troughcolor="#444444")
    
    slider = ttk.Scale(
        parent_window, from_=0, to=100, orient='horizontal', 
        command=set_volume, style="TScale"
    )
    slider.set(STATE.initial_volume) # Set to the saved volume level
    setattr(STATE, slider_attr, slider)

    # Create the speaker icon image
    icon_pil = load_pil_image("sound.png", icon_size, icon_size, mode='RGBA')
    icon_photo = ImageTk.PhotoImage(icon_pil)
    setattr(STATE, icon_ref_attr, icon_photo) 

    # Calculate positioning
    if is_portrait:
        total_width = slider_width + 10 + icon_size
        start_x = (WINDOW_WIDTH - total_width) // 2 # Center the slider
        slider_y_offset = (25 - icon_size) // 2 
    else:
        start_x = LANDSCAPE_SLIDER_X # Position it on the right side
        slider_y_offset = (25 - icon_size) // 2 

    icon_label = tk.Label(parent_window, image=icon_photo, bg=parent_window['bg'], bd=0)
    setattr(STATE, icon_label_attr, icon_label)
    icon_label.place(x=start_x, y=y_position + slider_y_offset)
    slider.place(x=start_x + icon_size + 10, y=y_position, width=slider_width)
    
    # Make sure the slider and icon are on top of other canvas elements
    if parent_window.winfo_class() != "Tk": # For the Toplevel window
        parent_window.after(10, slider.lift)
        parent_window.after(10, icon_label.lift)
    else: # For the main Tk window
        STATE.root.after(10, slider.lift)
        STATE.root.after(10, icon_label.lift)


# ---------------------------------------------------------
# FRAME LOGIC - The heart of the application's screen flow
# ---------------------------------------------------------
def clear_current_frame():
    """
    Cleans up the current screen: stops all pulsing animations,
    destroys the current canvas, and resets references. Essential before
    drawing a new screen!
    """
    # 1. Stop all current animations
    for data in STATE.button_data.values():
        if data.get("job"):
            try:
                STATE.root.after_cancel(data["job"])
            except ValueError:
                pass
            data["job"] = None
    STATE.button_data.clear() 
    
    # 2. Destroy the canvas
    if STATE.current_canvas: STATE.current_canvas.destroy()
    STATE.current_canvas = None
    
    # 3. Clear references (to help with memory/garbage collection)
    STATE.bg_ref = None 
    STATE.banner_char_ref = None 
    STATE.skill_bar_refs = [] 
    STATE.tutorial_icon_ref = None 
    STATE.current_problem_number = None 

def on_tutorial_nav_click(event):
    """Handler for the 'Tutorial' button in the landscape view."""
    if STATE.current_tutorial_skill:
        # If a skill was recently clicked on the dashboard, go straight to its tutorial
        show_fourth_frame(STATE.current_tutorial_skill)
    else:
        # Otherwise, tell the user to pick a skill first
        messagebox.showwarning("Skill Selection Required", "Please click a skill button on the left side of the Dashboard (Python, Java, etc.) to view its tutorial.")

def create_nav_buttons(canvas, win):
    """
    Draws the four main navigation buttons (Home, Tutorial, Problems, Exit)
    at the bottom of all landscape screens.
    """
    NAV_BAR_Y_CENTER = 730 
    
    NAV_BUTTONS = [
        {"tag": "homenav_btn", "path": "homenav.png", "dims": (52, 65), "coords": (343, NAV_BAR_Y_CENTER), "handler": lambda e: show_third_frame()},
        {"tag": "tutorialnav_btn", "path": "tutorialnav.png", "dims": (82, 60), "coords": (563, NAV_BAR_Y_CENTER), "handler": on_tutorial_nav_click}, 
        {"tag": "problemsnav_btn", "path": "problemsnav.png", "dims": (84, 60), "coords": (783, NAV_BAR_Y_CENTER), "handler": lambda e: show_fifth_frame()},
        {"tag": "exitnav_btn", "path": "exitnav.png", "dims": (73, 65), "coords": (1003, NAV_BAR_Y_CENTER), "handler": lambda e: on_nav_exit_click(win)},
    ]
    for btn in NAV_BUTTONS:
        # All nav buttons pulse!
        create_pulsing_button(canvas, btn["tag"], btn["path"], btn["dims"], btn["coords"], btn["handler"], disable_pulse=False)


def create_main_menu():
    """Frame 1: The very first screen with the background image, Access, and Exit."""
    clear_current_frame()
    STATE.root.deiconify() # Show the main (portrait) window
    
    canvas = tk.Canvas(STATE.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, 
                       highlightthickness=0, bg=STATE.root['bg'])
    canvas.pack(fill="both", expand=True)
    STATE.current_canvas = canvas
    canvas.bind("<Button-1>", log_coordinates) # For debugging coordinates
    
    # Draw background
    bg_image = load_pil_image("bg.png", WINDOW_WIDTH, WINDOW_HEIGHT, mode='RGB')
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    STATE.bg_ref = bg_photo 

    BUTTONS = [
        {"tag": "exit_btn", "path": "exit.png", "dims": (126, 43), "coords": (204, 878), "handler": on_exit_click},
        {"tag": "access_btn", "path": "access_game.png", "dims": (126, 43), "coords": (328, 878), "handler": on_access_game_click},
    ]

    for btn in BUTTONS:
        create_pulsing_button(canvas, btn["tag"], btn["path"], btn["dims"], btn["coords"], btn["handler"])
        
    create_volume_slider(STATE.root, is_portrait=True)

def show_second_frame():
    """Frame 2: Character/Gender Selection screen (still in portrait mode)."""
    clear_current_frame()
    STATE.root.deiconify() 
    # Close the landscape window if it was somehow open
    if STATE.landscape_window:
        STATE.landscape_window.destroy()
        STATE.landscape_window = None

    STATE.selected_gender = None # Reset state for new selection
    STATE.user_name = None 

    canvas = tk.Canvas(STATE.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, 
                       highlightthickness=0, bg=STATE.root['bg'])
    canvas.pack(fill="both", expand=True)
    STATE.current_canvas = canvas
    
    # Draw background
    bg2_image = load_pil_image("bg2.png", WINDOW_WIDTH, WINDOW_HEIGHT, mode='RGB')
    bg2_photo = ImageTk.PhotoImage(bg2_image)
    canvas.create_image(0, 0, image=bg2_photo, anchor="nw")
    STATE.bg_ref = bg2_photo 

    CHAR_DIMS = (277, 278)
    CHARACTERS = [
        {"tag": "female_select", "path": "female.png", "coords": (131, 627), "gender": "Female"},
        {"tag": "male_select", "path": "male.png", "coords": (399, 621), "gender": "Male"},
    ]

    for char in CHARACTERS:
        handler = lambda e, g=char["gender"]: on_gender_click(g)
        create_pulsing_button(canvas, char["tag"], char["path"], CHAR_DIMS, char["coords"], handler)
        
    NEXT_DIMS = (249, 120)
    create_pulsing_button(canvas, "next_btn", "nextChar.png", NEXT_DIMS, (263, 850), on_next_char_click)
    
    # Setup the label that shows the selected gender
    STATE.gender_label = tk.Label(canvas, text="", font=("Arial", 16, "bold"), 
                                  bg="#000000", fg="white", relief="flat")
    create_volume_slider(STATE.root, is_portrait=True)


def create_landscape_window(title, close_handler):
    """
    The function responsible for creating the big, wide-screen game window (Toplevel).
    All the main game content (Dashboard, Tutorials, Problems) uses this window.
    """
    clear_current_frame()
    STATE.root.withdraw() # Hide the small portrait window

    if STATE.landscape_window:
        STATE.landscape_window.destroy()
        STATE.landscape_window = None
    
    win = tk.Toplevel(STATE.root)
    win.title(title)
    win.resizable(True, True) 
    win.configure(bg="#101030") # Cool dark background color
    STATE.landscape_window = win
    
    # Center the new window on the screen
    center_x = (STATE.root.winfo_screenwidth() - LANDSCAPE_WIDTH) // 2
    center_y = (STATE.root.winfo_screenheight() - LANDSCAPE_HEIGHT) // 2
    win.geometry(f"{LANDSCAPE_WIDTH}x{LANDSCAPE_HEIGHT}+{center_x}+{center_y}")
    
    # What happens when the user clicks the 'X' button on the window
    win.protocol("WM_DELETE_WINDOW", close_handler)

    canvas = tk.Canvas(win, width=LANDSCAPE_WIDTH, height=LANDSCAPE_HEIGHT, 
                       highlightthickness=0, bg=win['bg']) 
    canvas.pack(fill="both", expand=True)
    STATE.current_canvas = canvas 
    create_volume_slider(win, is_portrait=False) # Add the landscape volume slider

    # QoL Addition: Display user name on top right for context
    if STATE.user_name:
        canvas.create_text(
            LANDSCAPE_USERNAME_X, LANDSCAPE_USERNAME_Y, 
            text=f"USER: {STATE.user_name.upper()}", 
            font=LANDSCAPE_USERNAME_FONT, 
            fill="#FFFFFF", 
            anchor="e"
        )

    return win, canvas

def show_third_frame():
    """Frame 3: The Dashboard! Shows user progress, avatar, and skill buttons."""
    # Basic check to make sure we have a user logged in
    if STATE.user_name is None or STATE.selected_gender is None:
        messagebox.showwarning("Error", "Missing user data. Please complete user selection or creation.")
        create_main_menu()
        return

    # Fetch the latest progress from the database
    STATE.db_progress_data = get_user_progress(STATE.user_name)

    # What happens when the 'X' button is clicked (signs out)
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu()
        
    win, canvas = create_landscape_window(f"Hasa Leveling - Dashboard: {STATE.user_name}", close_handler)

    # Draw background
    dashboard_image = load_pil_image("dashboard.png", LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
    dashboard_photo = ImageTk.PhotoImage(dashboard_image)
    canvas.create_image(0, 0, image=dashboard_photo, anchor="nw")
    STATE.bg_ref = dashboard_photo 
    
    # Draw the giant username text
    # A subtle shadow is added by drawing a slightly offset, dark blue version first
    canvas.create_text(
        USERNAME_TEXT_X + 2, USER_NAME_TEXT_Y + 2, 
        text=STATE.user_name.upper(), font=("Arial Black", 93, "bold"), fill="#3399FF", anchor="center", tags="user_name_shadow"
    )
    canvas.create_text(
        USERNAME_TEXT_X, USER_NAME_TEXT_Y, 
        text=STATE.user_name.upper(), font=("Arial Black", 93, "bold"), fill="#FFFFFF", anchor="center", justify="center", tags="user_name_text"
    )
    
    # Draw the character avatar based on the selected gender
    char_filename = "maledashboard.png" if STATE.selected_gender == "Male" else "femaledashboard.png"
    dims = MALE_AVATAR_DIMS if STATE.selected_gender == "Male" else FEMALE_AVATAR_DIMS 
        
    char_pil = load_pil_image(char_filename, *dims, mode='RGBA')
    char_photo = ImageTk.PhotoImage(char_pil)
    STATE.banner_char_ref = char_photo 
    canvas.create_image(AVATAR_CENTER_X, AVATAR_CENTER_Y, image=char_photo, anchor="center", tags="character_avatar")
    
    # Draw all the skill progress bars using the data we fetched
    for bar in BASE_SKILL_PROGRESS_BARS:
        # Check the progress data, using 10% as a fallback if the DB is weird
        progress_value = STATE.db_progress_data.get(bar["db_key"], 0.10)
        bar_data = bar.copy()
        bar_data["progress"] = progress_value
        draw_skill_progress_bar(canvas, bar_data)
        
    # Draw the bottom navigation bar and the skill buttons (left side)
    create_nav_buttons(canvas, win)
    for btn in SKILL_BUTTONS:
        create_pulsing_button(canvas, btn["tag"], btn["path"], btn["dims"], btn["coords"], btn["handler"])

def on_skill_button_click(skill_name):
    """
    Called when a skill button (Python, Java, etc.) on the Dashboard is clicked.
    Saves the skill and navigates to the Tutorial frame.
    """
    STATE.current_tutorial_skill = skill_name 
    show_fourth_frame(skill_name)

def open_tutorial_link(button_num):
    """Opens the corresponding YouTube link in the user's default web browser."""
    skill = STATE.current_tutorial_skill
    if not skill:
        messagebox.showerror("Error", "No skill selected for tutorial video playback.")
        return
    skill_links = TUTORIAL_LINKS.get(skill)
    if not skill_links:
        messagebox.showerror("Error", f"No tutorial links defined for skill: {skill}")
        return
    link = skill_links.get(button_num)
    if link and link.startswith("http"):
        try:
            webbrowser.open_new_tab(link) # This is the function that opens the browser!
        except Exception as e:
            messagebox.showerror("System Error", f"Failed to open link. Please ensure you have a web browser installed. Error: {e}")
    else:
        messagebox.showwarning("Link Missing", f"Link for {skill} Tutorial {button_num} is not set or invalid in TUTORIAL_LINKS.")

def on_tutorial_icon_click(event):
    """When the big skill icon on the left is clicked, it goes back to the dashboard."""
    show_third_frame()

def show_fourth_frame(skill_name=None):
    """Frame 4: The Tutorial screen for a specific skill (showing 5 YouTube links)."""
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu() 
        
    win, canvas = create_landscape_window("Hasa Leveling - Tutorials", close_handler)
    
    # Draw background
    tutorial_image = load_pil_image("tutorialbg.png", LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
    tutorial_photo = ImageTk.PhotoImage(tutorial_image)
    canvas.create_image(0, 0, image=tutorial_photo, anchor="nw")
    STATE.bg_ref = tutorial_photo 
    
    if skill_name:
        # Load the skill-specific icon (e.g., tutpython.png)
        skill_filename = f"tut{skill_name.lower().replace('+', '')}.png"
        create_pulsing_button(
            canvas, 
            "tutorial_skill_icon", 
            skill_filename, 
            TUTORIAL_ICON_DIMS, 
            (TUTORIAL_ICON_X, TUTORIAL_ICON_Y), 
            on_tutorial_icon_click # Clicking it goes back to the dashboard
        )

    # Draw the 5 'Play' buttons
    for btn in PLAY_BUTTONS_CONFIG:
        handler = lambda e, num=btn["button_num"]: open_tutorial_link(num)
        create_pulsing_button(canvas, btn["tag"], btn["path"], btn["dims"], btn["coords"], handler, disable_pulse=False)
            
    create_nav_buttons(canvas, win)


# --- MODIFIED FUNCTION: ADDSKILL CLICK HANDLER ---
def on_add_skill_click(skill_name, problem_number):
    """
    Called when the user clicks 'Add Skill' on the Answer Frame.
    This gives the user a 20% progress boost for completing the problem!
    """
    increment = 0.20 # 20%
    if STATE.user_name and skill_name:
        # Update the database
        if update_user_progress(STATE.user_name, skill_name, increment):
            messagebox.showinfo(
                "Skill Added!", 
                f"Congratulations! **{skill_name}** progress updated by 20% for completing Problem #{problem_number}!"
            )
            # After success, immediately jump back to the Dashboard to show the new progress bar!
            show_third_frame()
        else:
            messagebox.showerror(
                "Update Failed",
                f"Could not update progress for {skill_name}. Check database connection or if the progress is already 100%."
            )
    else:
         messagebox.showerror(
            "Error",
            "Missing user or skill data. Cannot update progress."
        )


# --- MODIFIED FUNCTION: PROBLEM SOLVER REVEAL CLICK ---
def on_reveal_answer_click(skill, problem_number):
    """Handles the 'Reveal Answer' button click by showing the answer frame."""
    show_answer_frame(skill, problem_number)


def open_problem_solver(skill, problem_number):
    """
    Called when one of the Problem Folders (1-5) is clicked.
    Navigates to the actual problem question view.
    """
    STATE.current_problem_number = problem_number
    show_problem_solver_frame(skill, problem_number)


# --- NEW FRAME: ANSWER SOLVER VIEW (Frame 8) ---
def show_answer_frame(skill_name, problem_number):
    """
    Frame 8: The screen that displays the solution to the problem.
    It includes the 'Back' and 'Add Skill' buttons.
    """
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu() 
    
    # Create Window
    title = f"Hasa Leveling - {skill_name} Answer {problem_number}"
    win, canvas = create_landscape_window(title, close_handler)
    
    # --- Background Image Logic (answercX.png) ---
    # This tries to load a specific image for the answer (e.g., answerc1.png for C++ problem 1)
    skill_abbr_map = {
        "C++": "c", "Python": "python", "Java": "java", "HTML": "html", "MySQL": "mysql"
    }
    
    skill_abbr = skill_abbr_map.get(skill_name, "c") 
    
    # File naming convention: answerc1.png, answerj1.png, etc.
    bg_filename = f"answer{skill_abbr}{problem_number}.png"
    
    try:
        bg_image = load_pil_image(bg_filename, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
    except Exception:
        # If the answer image is missing, fall back to the generic problems background
        bg_filename = "problemsbg.png" 
        bg_image = load_pil_image(bg_filename, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
        messagebox.showwarning("Image Missing", f"Could not load specific answer background: {bg_filename}. Using generic problem background.")
        
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    STATE.bg_ref = bg_photo 
    
    # ---------------------------------------------------------
    # 1. Back Button: Returns to the question frame (Frame 7)
    # ---------------------------------------------------------
    create_pulsing_button(
        canvas, 
        "back_answer_btn", 
        "problemback.png", 
        BACK_PROBLEM_DIMS, 
        BACK_PROBLEM_COORDS, 
        lambda e: show_problem_solver_frame(skill_name, problem_number)
    )

    # ---------------------------------------------------------
    # 2. Add Skill Button: Gives the user progress if not maxed
    # ---------------------------------------------------------
    
    # Check current progress before drawing the button
    db_key = skill_name.lower().replace('+', '') + "_progress"
    current_progress = STATE.db_progress_data.get(db_key, 0.0)
    
    if current_progress < 1.0:
        # Show the actual clickable 'Add Skill' button
        create_pulsing_button(
            canvas, 
            "add_skill_btn", 
            "addskill.png", 
            ADDSKILL_BUTTON_DIMS, 
            ADDSKILL_BUTTON_COORDS, 
            lambda e: on_add_skill_click(skill_name, problem_number)
        )
    else:
        # Show a text message if the skill is already 100%
        canvas.create_text(
            ADDSKILL_BUTTON_COORDS[0], ADDSKILL_BUTTON_COORDS[1], 
            text="SKILL MAXED!", 
            font=("Arial", 18, "bold"), 
            fill="#FFD700",
            anchor="center"
        )


    # ---------------------------------------------------------
    # Navigation Bar 
    create_nav_buttons(canvas, win)


# --- MODIFIED FRAME: PROBLEM SOLVER VIEW (Frame 7) ---
def show_problem_solver_frame(skill_name, problem_number):
    """
    Frame 7: The screen where the user views the actual question/problem.
    It includes the 'Reveal Answer' button.
    """
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu() 
    
    # Create Window
    title = f"Hasa Leveling - {skill_name} Problem {problem_number}"
    win, canvas = create_landscape_window(title, close_handler)
    
    # --- Background Image Logic (questioncX.png) ---
    # This tries to load a specific image for the question (e.g., questionc1.png)
    skill_abbr_map = {
        "C++": "c",
        "Python": "python",
        "Java": "java",
        "HTML": "html",
        "MySQL": "mysql"
    }
    
    skill_abbr = skill_abbr_map.get(skill_name, "c") 
    
    # File naming convention: questionc1.png, questionj1.png, etc.
    bg_filename = f"question{skill_abbr}{problem_number}.png"
    
    try:
        bg_image = load_pil_image(bg_filename, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
    except Exception:
        # Fallback if the specific question image is missing
        bg_filename = "problemsbg.png" 
        bg_image = load_pil_image(bg_filename, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
        messagebox.showwarning("Image Missing", f"Could not load specific background: {bg_filename}. Using generic problem background.")
        
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    STATE.bg_ref = bg_photo 
    
    # ---------------------------------------------------------
    # 1. Reveal Answer Button: Jumps to the answer screen (Frame 8)
    # ---------------------------------------------------------
    create_pulsing_button(
        canvas, 
        "reveal_answer_btn", 
        "revealbutton.png", 
        REVEAL_ANSWER_DIMS, 
        REVEAL_ANSWER_COORDS, 
        lambda e: on_reveal_answer_click(skill_name, problem_number)
    )

    # ---------------------------------------------------------
    # 2. Back Button: Returns to the problem selection screen (Frame 6)
    # ---------------------------------------------------------
    create_pulsing_button(
        canvas, 
        "back_problem_btn", 
        "problemback.png", 
        BACK_PROBLEM_DIMS, 
        BACK_PROBLEM_COORDS, 
        lambda e: show_problem_selection_frame(skill_name)
    )

    # ---------------------------------------------------------
    # Navigation Bar 
    create_nav_buttons(canvas, win)


# --- NEW FRAME: PROBLEM SELECTION (Frame 6) ---
def show_problem_selection_frame(skill_name):
    """
    Frame 6: The screen with the big skill icon on the left and the 5
    numbered folder icons (Problem 1, 2, 3, etc.) on the right.
    """
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu() 
    
    # Create Window
    title = f"Hasa Leveling - {skill_name} Problems"
    win, canvas = create_landscape_window(title, close_handler)
    
    # --- Background Image (problembg2.png) ---
    bg_image = load_pil_image("problembg2.png", LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    STATE.bg_ref = bg_photo 

    # ---------------------------------------------------------
    # 1. LEFT SIDE: SKILL ICON (Links back to the overall Problems Menu)
    # ---------------------------------------------------------
    skill_filename = f"tut{skill_name.lower().replace('+', '')}.png"
    
    create_pulsing_button(
        canvas, 
        "problem_skill_icon", 
        skill_filename, 
        TUTORIAL_ICON_DIMS, 
        (TUTORIAL_ICON_X, TUTORIAL_ICON_Y), 
        lambda e: show_fifth_frame() # Clicking the icon goes back to the list of skill problem categories
    )

    # Label underneath the skill icon
    
    
    # ---------------------------------------------------------
    # 2. RIGHT SIDE: FOLDER BUTTONS (5 folders)
    # ---------------------------------------------------------
    
    FOLDER_DIMS = (150, 110) 
    FOLDER_Y_OFFSET = 50 

    # We reuse the coordinates from the Play Buttons config, but shift them up slightly
    for i, config in enumerate(PLAY_BUTTONS_CONFIG):
        prob_num = i + 1
        folder_tag = f"folder_{prob_num}_btn"
        folder_path = f"problem{prob_num}.png" # problem1.png, problem2.png, etc.
        
        original_x, original_y = config["coords"]
        folder_coords = (original_x, original_y - FOLDER_Y_OFFSET)
        
        # Handler: Opens the specific problem view (Frame 7)
        handler = lambda e, s=skill_name, n=prob_num: open_problem_solver(s, n)
        
        create_pulsing_button(
            canvas, 
            folder_tag, 
            folder_path, 
            FOLDER_DIMS, 
            folder_coords, 
            handler
        )

    # ---------------------------------------------------------
    # Navigation Bar
    create_nav_buttons(canvas, win)


def show_fifth_frame():
    """Frame 5: The main Problems/Quests Menu. Lists all skill categories (Java, Python, etc.)"""
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu() 

    win, canvas = create_landscape_window("Hasa Leveling - Problems/Quests", close_handler)
    
    problems_bg_image = load_pil_image("problemsbg.png", LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
    problems_bg_photo = ImageTk.PhotoImage(problems_bg_image)
    canvas.create_image(0, 0, image=problems_bg_photo, anchor="nw")
    STATE.bg_ref = problems_bg_photo 
    
    # --- PROBLEM CATEGORY BUTTONS ---
    PROBLEM_BTN_DIMS = (160, 203) 

    # Buttons for each skill category
    PROBLEM_BUTTONS = [
        {"tag": "prob_java",   "path": "tutjava.png",   "coords": (243, 500),    "skill": "Java"},
        {"tag": "prob_html",   "path": "tuthtml.png",   "coords": (463, 500),    "skill": "HTML"},
        {"tag": "prob_c",      "path": "tutc.png",      "coords": (683, 500),    "skill": "C++"}, 
        {"tag": "prob_mysql",  "path": "tutmysql.png",  "coords": (903, 500),    "skill": "MySQL"},
        {"tag": "prob_python", "path": "tutpython.png", "coords": (1123, 500),   "skill": "Python"} 
    ]

    for btn in PROBLEM_BUTTONS:
        # Clicking one goes to the problem *selection* screen for that skill (Frame 6)
        handler = lambda e, s=btn["skill"]: show_problem_selection_frame(s)
        
        create_pulsing_button(
            canvas, 
            btn["tag"], 
            btn["path"], 
            PROBLEM_BTN_DIMS, 
            btn["coords"], 
            handler
        )
            
    create_nav_buttons(canvas, win)


# ---------------------------------------------------------
# DIALOG & PROGRESSION FUNCTIONS - Pop-ups for user management
# ---------------------------------------------------------
def prompt_for_name():
    """
    Shows a custom dialog where the user can enter a new username and register it.
    Uses custom image buttons with pulse effects inside the dialog!
    """
    if STATE.selected_gender is None:
        messagebox.showwarning("Selection Required", "Please select a gender (Male or Female) before proceeding.")
        return

    # --- CONFIGURATION FOR NAME INPUT DIALOG ---
    DIALOG_WIDTH = 350 
    DIALOG_HEIGHT = 300 
    ENTRY_Y = 175 
    BUTTON_Y = 245 
    BUTTON_DIMS = (180, 65) 
    # -------------------------------------------

    dialog = tk.Toplevel(STATE.root)
    dialog.title("Register Character Name")
    dialog.geometry(f"{DIALOG_WIDTH}x{DIALOG_HEIGHT}")
    dialog.transient(STATE.root) # Keeps it on top of the main window
    dialog.grab_set() # Forces user to interact with this dialog only
    
    # Center the dialog nicely
    dialog_x = STATE.root.winfo_x() + (STATE.root.winfo_width() // 2) - (DIALOG_WIDTH // 2)
    dialog_y = STATE.root.winfo_y() + (STATE.root.winfo_height() // 2) - (DIALOG_HEIGHT // 2)
    dialog.geometry(f'+{dialog_x}+{dialog_y}')
    
    # Create Canvas for Background and Custom Buttons
    canvas = tk.Canvas(dialog, width=DIALOG_WIDTH, height=DIALOG_HEIGHT, highlightthickness=0, bg="#000000")
    canvas.pack(fill="both", expand=True)

    # --- Load Background Image ---
    bg_pil = load_pil_image("registerForm.png", DIALOG_WIDTH, DIALOG_HEIGHT, mode='RGB')
    bg_photo = ImageTk.PhotoImage(bg_pil)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    canvas.bg_ref = bg_photo 
    
    # --- Custom Pulse Logic for Dialog ---
    # The pulse logic needs to be re-defined here since it runs relative to the 'dialog' window, not 'STATE.root'
    canvas.dialog_button_data = {}
    # ... pulse_dialog, dialog_on_enter, dialog_on_leave functions are defined here ...
    # (Leaving the internal logic as is to keep the file clean, but noting it's for the dialog's buttons)
    def pulse_dialog(tag):
        data = canvas.dialog_button_data.get(tag)
        if not data: return
        
        STEP = 0.002
        MIN_SCALE = 1.00 
        MAX_SCALE = 1.05 
        canvas_ref = canvas
        
        if data["hover"]:
            if data["growing"]:
                data["scale"] = min(MAX_SCALE, data["scale"] + STEP)
                if data["scale"] >= MAX_SCALE: data["growing"] = False
            else:
                data["scale"] = max(MIN_SCALE, data["scale"] - STEP)
                if data["scale"] <= MIN_SCALE: data["growing"] = True
        else:
            data["scale"] = max(MIN_SCALE, data["scale"] - STEP)
            
        if not data["hover"] and data["scale"] == MIN_SCALE:
            if data["job"]:
                dialog.after_cancel(data["job"])
                data["job"] = None
            new_photo = ImageTk.PhotoImage(data["base_img"])
            canvas_ref.itemconfig(tag, image=new_photo)
            data["current_photo"] = new_photo
            return

        original_w, original_h = data["base_img"].size
        new_w = int(original_w * data["scale"])
        new_h = int(original_h * data["scale"])
        
        resized_pil = data["base_img"].resize((new_w, new_h), Image.Resampling.BILINEAR)
        new_photo = ImageTk.PhotoImage(resized_pil)
        
        canvas_ref.itemconfig(tag, image=new_photo)
        data["current_photo"] = new_photo
        
        data["job"] = dialog.after(15, lambda: pulse_dialog(tag))

    def dialog_on_enter(event, tag): 
        dialog.config(cursor="hand2")
        data = canvas.dialog_button_data.get(tag)
        if data:
            data["hover"] = True
            if data["job"] is None:
                data["growing"] = True 
                pulse_dialog(tag)

    def dialog_on_leave(event, tag):
        dialog.config(cursor="")
        data = canvas.dialog_button_data.get(tag)
        if data:
            data["hover"] = False
    # --- End Custom Pulse Logic ---


    # --- Entry Field for Name ---
    name_entry = tk.Entry(dialog, width=25, font=("Arial", 14)) 
    canvas.create_window(DIALOG_WIDTH // 2, ENTRY_Y, window=name_entry)
    name_entry.focus_set()

    def register_and_proceed():
        """Handles validation and the actual database insertion for a new user."""
        play_click_sound() 
        name = name_entry.get().strip()
        # Validation checks
        if not name:
            messagebox.showwarning("Input Required", "Please enter a name to continue.")
        elif len(name) < 4:
            messagebox.showwarning("Invalid Name", "Name must be at least 4 characters long.")
        elif len(name) > 9:
            messagebox.showwarning("Invalid Name", "Name cannot exceed 9 characters.")
        else:
            # If valid, insert into DB
            if insert_new_user(name, STATE.selected_gender):
                STATE.user_name = name
                dialog.destroy()
                show_third_frame() # Go straight to the Dashboard!

    # --- Register Button (Custom Image) ---
    register_img_pil = load_pil_image("register.png", *BUTTON_DIMS, mode='RGBA')
    register_img_photo = ImageTk.PhotoImage(register_img_pil)
    canvas.register_btn_ref = register_img_photo 
    
    register_btn_id = canvas.create_image(
        DIALOG_WIDTH // 2, BUTTON_Y, 
        image=register_img_photo, 
        anchor="center", 
        tags="register_btn"
    )

    # Setup data for pulse
    canvas.dialog_button_data["register_btn"] = { 
        "base_img": register_img_pil, "scale": 1.0, "growing": True, 
        "hover": False, "job": None, "current_photo": register_img_photo 
    }
    
    # Wrapped handler for the dialog image button
    def dialog_button_handler(event=None): 
        register_and_proceed()

    # Bindings for the custom image button with pulse
    canvas.tag_bind("register_btn", "<Button-1>", dialog_button_handler)
    canvas.tag_bind("register_btn", "<Enter>", lambda e: dialog_on_enter(e, "register_btn"))
    canvas.tag_bind("register_btn", "<Leave>", lambda e: dialog_on_leave(e, "register_btn"))
    
    # Bind the Enter key to the function
    dialog.bind('<Return>', dialog_button_handler)

    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
    STATE.root.wait_window(dialog)


def show_user_selection_dialog(user_data):
    """
    The dialog that pops up after clicking 'Access Game'. It lets the user
    Load an existing user, Delete a user, or Create a new one.
    """
    # --- CONFIGURATION (ADJUST THESE TO MATCH YOUR IMAGES) ---
    DIALOG_WIDTH = 450
    DIALOG_HEIGHT = 450
    BTN_W, BTN_H = (180, 65) 
    COMBOBOX_WIDTH = 30
    COMBOBOX_FONT_SIZE = 14 
    # ---------------------------------------------------------

    dialog = tk.Toplevel(STATE.root)
    dialog.title("Manage User Profiles")
    dialog.geometry(f"{DIALOG_WIDTH}x{DIALOG_HEIGHT}")
    dialog.transient(STATE.root)
    dialog.grab_set()
    
    # Center the dialog
    dialog_x = STATE.root.winfo_x() + (STATE.root.winfo_width() // 2) - (DIALOG_WIDTH // 2)
    dialog_y = STATE.root.winfo_y() + (STATE.root.winfo_height() // 2) - (DIALOG_HEIGHT // 2)
    dialog.geometry(f'+{dialog_x}+{dialog_y}')
    
    canvas = tk.Canvas(dialog, width=DIALOG_WIDTH, height=DIALOG_HEIGHT, highlightthickness=0, bg="#222222")
    canvas.pack(fill="both", expand=True)

    # --- 1. Load Background Image ---
    bg_pil = load_pil_image("userForm.png", DIALOG_WIDTH, DIALOG_HEIGHT, mode='RGB')
    bg_photo = ImageTk.PhotoImage(bg_pil)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    canvas.bg_ref = bg_photo 
    
    # --- Custom Pulse Logic for Dialog ---
    # (Same pulse logic as in prompt_for_name, runs against the dialog canvas)
    canvas.dialog_button_data = {}
    def pulse_dialog(tag):
        # (Internal pulse logic, same as before)
        data = canvas.dialog_button_data.get(tag)
        if not data: return
        STEP = 0.002
        MIN_SCALE = 1.00 
        MAX_SCALE = 1.05 
        canvas_ref = canvas
        if data["hover"]:
            if data["growing"]:
                data["scale"] = min(MAX_SCALE, data["scale"] + STEP)
                if data["scale"] >= MAX_SCALE: data["growing"] = False
            else:
                data["scale"] = max(MIN_SCALE, data["scale"] - STEP)
                if data["scale"] <= MIN_SCALE: data["growing"] = True
        else:
            data["scale"] = max(MIN_SCALE, data["scale"] - STEP)
            
        if not data["hover"] and data["scale"] == MIN_SCALE:
            if data["job"]:
                dialog.after_cancel(data["job"])
                data["job"] = None
            new_photo = ImageTk.PhotoImage(data["base_img"])
            canvas_ref.itemconfig(tag, image=new_photo)
            data["current_photo"] = new_photo
            return

        original_w, original_h = data["base_img"].size
        new_w = int(original_w * data["scale"])
        new_h = int(original_h * data["scale"])
        resized_pil = data["base_img"].resize((new_w, new_h), Image.Resampling.BILINEAR)
        new_photo = ImageTk.PhotoImage(resized_pil)
        canvas_ref.itemconfig(tag, image=new_photo)
        data["current_photo"] = new_photo
        data["job"] = dialog.after(15, lambda: pulse_dialog(tag))

    def dialog_on_enter(event, tag): 
        dialog.config(cursor="hand2")
        data = canvas.dialog_button_data.get(tag)
        if data:
            data["hover"] = True
            if data["job"] is None:
                data["growing"] = True 
                pulse_dialog(tag)

    def dialog_on_leave(event, tag):
        dialog.config(cursor="")
        data = canvas.dialog_button_data.get(tag)
        if data:
            data["hover"] = False
    # --- End Custom Pulse Logic ---


    # --- Data Setup ---
    has_users = bool(user_data)
    usernames = sorted(user_data.keys())
    selected_user_var = tk.StringVar(dialog)
    if has_users:
        selected_user_var.set(usernames[0]) # Default to the first user in the list

    # --- 2. Dropdown (Combobox) to select user ---
    DROPDOWN_X = DIALOG_WIDTH // 2
    DROPDOWN_Y = 195 
    
    style = ttk.Style()
    style.configure("Custom.TCombobox", font=("Arial", COMBOBOX_FONT_SIZE))

    if has_users:
        user_menu = ttk.Combobox(dialog, 
                                 textvariable=selected_user_var, 
                                 values=usernames, 
                                 state="readonly", 
                                 width=COMBOBOX_WIDTH,
                                 style="Custom.TCombobox" 
                                )
        canvas.create_window(DROPDOWN_X, DROPDOWN_Y, window=user_menu)
    else:
        # If no users are found in the DB
        canvas.create_text(DROPDOWN_X, DROPDOWN_Y, text="No users found.", fill="red", font=("Arial", 12, "bold"))

    # --- Button Helpers ---
    def create_dialog_img_button(tag, filename, x, y, handler):
        """Helper to create a simple clickable image button on the dialog canvas."""
        img_pil = load_pil_image(filename, BTN_W, BTN_H, mode='RGBA')
        img_photo = ImageTk.PhotoImage(img_pil)
        
        item_id = canvas.create_image(x, y, image=img_photo, anchor="center", tags=tag)
        
        setattr(canvas, f"{tag}_ref", img_photo)
        
        def wrapped_dialog_handler(event):
            play_click_sound()
            handler(event)
        
        # Setup data for pulse
        canvas.dialog_button_data[tag] = { 
            "base_img": img_pil, "scale": 1.0, "growing": True, 
            "hover": False, "job": None, "current_photo": img_photo 
        }
            
        # Bindings with pulse logic
        if has_users or tag == "create_btn":
            canvas.tag_bind(tag, "<Button-1>", wrapped_dialog_handler)
            canvas.tag_bind(tag, "<Enter>", lambda e: dialog_on_enter(e, tag))
            canvas.tag_bind(tag, "<Leave>", lambda e: dialog_on_leave(e, tag))

    # --- Handlers for Load, Delete, Create ---
    def on_load_click(event):
        """Logs in the selected user and goes to the Dashboard."""
        if not has_users: 
            messagebox.showwarning("No Users", "Please create a user profile first.")
            return
        username = selected_user_var.get()
        if username in user_data:
            STATE.user_name = username
            STATE.selected_gender = user_data[username]
            dialog.destroy()
            show_third_frame() # SUCCESS: Go to Frame 3

    def on_delete_click(event):
        """Prompts for confirmation and deletes the selected user from the DB."""
        if not has_users:
            messagebox.showwarning("No Users", "There are no users to delete.") 
            return
        username = selected_user_var.get()
        confirm = messagebox.askyesno("Confirm Delete", f"Delete user '{username}'?", parent=dialog)
        if confirm:
            if delete_user_progress(username):
                dialog.destroy()
                # Refresh the dialog with the updated user list
                STATE.user_list = fetch_all_users()
                show_user_selection_dialog(STATE.user_list)

    def on_create_click(event):
        """Closes this dialog and goes to the Gender Selection screen (Frame 2)."""
        dialog.destroy()
        show_second_frame()

    # --- 3. Place Custom Buttons ---
    create_dialog_img_button("load_btn", "loaduser.png", x=115, y=295, handler=on_load_click)
    create_dialog_img_button("delete_btn", "deleteuser.png", x=335, y=295, handler=on_delete_click)
    create_dialog_img_button("create_btn", "createuser.png", x=DIALOG_WIDTH//2, y=385, handler=on_create_click)

    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
    STATE.root.wait_window(dialog)


def confirm_action(action, window_to_close):
    """Shows a confirmation dialog before Exiting the app or Signing Out."""
    if action == 'Sign Out':
        confirmation = messagebox.askyesno(
            "Confirm Sign Out", 
            "Are you sure you want to sign out and return to the main menu?"
        )
    else: 
        confirmation = messagebox.askyesno(
            "Confirm Exit", 
            "Are you sure you want to exit the application?"
        )

    if confirmation:
        play_click_sound() # Play sound for the final action
        if action == 'Exit':
            # Stop the background music and quit Pygame before closing the window
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit() 
            except Exception as e:
                pass 
            if window_to_close:
                window_to_close.destroy()
            STATE.root.destroy()
        elif action == 'Sign Out':
            if window_to_close:
                window_to_close.destroy()
            STATE.root.deiconify() 
            create_main_menu() # Go back to Frame 1 (Main Menu)
            
def on_nav_exit_click(landscape_window):
    """The handler for the 'Exit' button on the landscape navigation bar (which means Sign Out)."""
    play_click_sound()
    confirm_action('Sign Out', landscape_window)


# ---------------------------------------------------------
# CLICK HANDLERS (for Main/Portrait Frames)
# ---------------------------------------------------------
def on_access_game_click(event):
    """
    Called from the Main Menu (Frame 1). Fetches all user data
    and opens the Load/Delete/Create User dialog.
    """
    STATE.user_list = fetch_all_users()
    show_user_selection_dialog(STATE.user_list)

def on_exit_click(event=None):
    """Called from the Main Menu (Frame 1). Starts the Exit process."""
    play_click_sound()
    confirm_action('Exit', None)

def on_gender_click(gender):
    """
    Handles male/female avatar clicks on Frame 2. Selects the gender
    or deselects if the same one is clicked again.
    """
    play_click_sound() 
    is_deselecting = (STATE.selected_gender == gender)
    STATE.selected_gender = None if is_deselecting else gender
    # Update the label to show the selection
    if STATE.selected_gender:
        STATE.gender_label.config(text=f"Gender Selected: {gender}")
        STATE.gender_label.place(relx=0.5, rely=0.42, anchor="center") 
        STATE.gender_label.lift()
    else:
        STATE.gender_label.config(text="")
        STATE.gender_label.place_forget() 

def on_next_char_click(event):
    """Called when 'Next' is clicked on Frame 2. Checks if a gender is selected and then prompts for the name."""
    if STATE.selected_gender is None:
        messagebox.showwarning("Selection Required", "Please select a gender (Male or Female) before proceeding.")
        return
    prompt_for_name() # Move to the name registration dialog

# QoL Addition: Check for assets directory before running
def check_assets_dir():
    """A sanity check to make sure the 'assets' folder is where it should be."""
    if not os.path.isdir(ASSETS_DIR):
        messagebox.showerror(
            "Fatal Error: Assets Missing", 
            f"The required assets folder '{ASSETS_DIR}' was not found.\n\nPlease ensure this folder is in the same directory as the script."
        )
        return False
    return True

# =============================
# RUN - The starting point of the whole program!
# =============================
if __name__ == "__main__":
    
    # Check for assets first
    if not check_assets_dir():
        # Exit if assets are missing
        import sys
        sys.exit() 
        
    # Root setup
    root = tk.Tk()
    root.title("Hasa Leveling")
    # Calculate position to center the window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    root.configure(bg="#000000") 
    root.resizable(False, False) # Keep the main window fixed size
    STATE.root = root 

    # Set the application window icon
    try:
        icon_pil = load_pil_image("logoicon.png", APP_ICON_SIZE, APP_ICON_SIZE, mode='RGBA')
        icon_photo = ImageTk.PhotoImage(icon_pil)
        STATE.app_icon_ref = icon_photo 
        root.iconphoto(True, icon_photo)
    except Exception as e:
        pass # If the icon fails, the program still runs

    music_path = os.path.join(ASSETS_DIR, "bgmusic.mp3") 
    start_music(music_path) # Start the background music!
    
    create_main_menu() # Load the very first screen (Frame 1)
    root.mainloop() # Start the Tkinter event loop - the program runs from here!