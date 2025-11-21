import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import pygame
import json
import mysql.connector

# --- GLOBAL CONSTANTS ---
ASSETS_DIR = "assets"

# PORTRAIT Constants (Root Window)
WINDOW_WIDTH = 520
WINDOW_HEIGHT = 956
SLIDER_WIDTH_PORTRAIT = 200
PORTRAIT_Y = WINDOW_HEIGHT - 40
ICON_SIZE = 20
APP_ICON_SIZE = 32

# LANDSCAPE Constants (Toplevel Window)
LANDSCAPE_WIDTH = 1366
LANDSCAPE_HEIGHT = 768

# LANDSCAPE SLIDER CONSTANTS
LANDSCAPE_SLIDER_WIDTH = 150
LANDSCAPE_ICON_SIZE = 25
LANDSCAPE_SLIDER_X = LANDSCAPE_WIDTH - LANDSCAPE_SLIDER_WIDTH - 110 
LANDSCAPE_SLIDER_Y = 700 

# --- AVATAR & USERNAME TEXT CONSTANTS (For Frame 3) ---
# --- AVATAR CONSTANTS ---
AVATAR_CENTER_X = 1080  # X-position for the character avatar image (ADJUSTED to center in the right circle)
AVATAR_CENTER_Y = 130 # Y-position for the character avatar image (ADJUSTED to fit inside the circle)

# --- USERNAME TEXT CONSTANTS ---
USERNAME_TEXT_X = 350 # X-position for the username text 
USER_NAME_TEXT_Y = 125 # Y-position for the username text (ADJUSTED to be lower)

# Avatar Dimensions for Individual Scaling
MALE_AVATAR_DIMS = (560, 315)
FEMALE_AVATAR_DIMS = (522, 273) 

# --- DATABASE CONFIGURATION ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",           
    "password": "jayvee101", 
    "database": "hasaleveling_db"
}

# SKILL BUTTON CONFIGURATION (Left Side)
SKILL_BUTTONS = [
    {"tag": "pythonskill_btn", "path": "pythonskill.png", "dims": (219, 137), "coords": (137, 411), "handler": lambda e: print("Python Skill Clicked")},
    {"tag": "javaskill_btn", "path": "javaskill.png", "dims": (223, 139), "coords": (325, 408), "handler": lambda e: print("Java Skill Clicked")},
    {"tag": "htmlskill_btn", "path": "htmlskill.png", "dims": (219, 137), "coords": (137, 513), "handler": lambda e: print("HTML Skill Clicked")},
    {"tag": "c++skill_btn", "path": "c++skill.png", "dims": (223, 139), "coords": (327, 514), "handler": lambda e: print("C++ Skill Clicked")},
    {"tag": "mysqlskill_btn", "path": "mysqlskill.png", "dims": (220, 137), "coords": (224, 614), "handler": lambda e: print("MySQL Skill Clicked")},
]

# Base SKILL PROGRESS BAR CONFIGURATION (Positions only, progress will come from DB)
BASE_SKILL_PROGRESS_BARS = [
    {"skill": "HTML", "db_key": "html_progress", "x": 981, "y": 371, "w": 308, "h": 31, "color": "#007BA7"}, 
    {"skill": "C++", "db_key": "cplusplus_progress", "x": 981, "y": 432, "w": 308, "h": 31, "color": "#A03472"}, 
    {"skill": "MySQL", "db_key": "mysql_progress", "x": 981, "y": 491, "w": 308, "h": 31, "color": "#00A79D"}, 
    {"skill": "Python", "db_key": "python_progress", "x": 981, "y": 558, "w": 308, "h": 31, "color": "#D33842"}, 
    {"skill": "Java", "db_key": "java_progress", "x": 981, "y": 616, "w": 308, "h": 31, "color": "#007BA7"}, 
]


# --- GLOBAL STATE/DATA ---
class AppState:
    def __init__(self):
        self.root = None
        self.current_canvas = None
        self.landscape_window = None 
        self.gender_label = None
        # Sliders
        self.volume_slider_root = None
        self.volume_slider_landscape = None
        # Icons
        self.app_icon_ref = None 
        self.icon_ref_portrait = None
        self.icon_label_portrait = None
        self.icon_ref_landscape = None
        self.icon_label_landscape = None
        
        # State Data
        self.button_data = {}
        self.selected_gender = None
        self.user_name = None
        self.bg_ref = None 
        self.initial_volume = 50.0
        self.banner_char_ref = None 
        # Skill Progress Bar references to prevent garbage collection
        self.skill_bar_refs = []
        self.db_progress_data = {} 
        self.user_list = {} # Stores {username: gender} for selection

STATE = AppState()

# =============================
# Database Functions
# =============================

def get_db_connection():
    """Attempts to connect to the MySQL database."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        error_message = f"Database Connection Error: {err}"
        print(error_message)
        if STATE.db_progress_data.get("status") != "failed":
            messagebox.showerror("Database Error", f"Could not connect to MySQL.\nPlease check your DB_CONFIG.\n\nError: {err}")
            STATE.db_progress_data["status"] = "failed"
        return None

def fetch_all_users():
    """Fetches all usernames and genders from the database."""
    conn = get_db_connection()
    if not conn:
        return {}
    
    user_data = {}
    try:
        cursor = conn.cursor()
        query = "SELECT username, gender FROM user_progress"
        cursor.execute(query)
        for (username, gender) in cursor:
            user_data[username] = gender
    except mysql.connector.Error as err:
        print(f"Database Query Error: {err}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return user_data

def get_user_progress(username):
    """Fetches skill progress for the given user from the database."""
    conn = get_db_connection()
    if not conn:
        # Fallback if connection fails
        return {
            "html_progress": 0.50, "cplusplus_progress": 0.50, 
            "mysql_progress": 0.50, "python_progress": 0.50, 
            "java_progress": 0.50, "status": "default_used"
        }

    try:
        cursor = conn.cursor(dictionary=True)
        query = "SELECT html_progress, cplusplus_progress, mysql_progress, python_progress, java_progress, gender FROM user_progress WHERE username = %s"
        cursor.execute(query, (username.upper(),))
        data = cursor.fetchone()
        
        if data:
            progress_data = {key: float(value) for key, value in data.items() if key != 'gender'}
            progress_data["status"] = "success"
            
            STATE.selected_gender = data['gender']
            
            return progress_data
        
        return {key: 0.10 for key in ["html_progress", "cplusplus_progress", "mysql_progress", "python_progress", "java_progress"]}

    except mysql.connector.Error as err:
        messagebox.showwarning("Database Warning", "Could not fetch user progress. Using default values.")
        return {key: 0.10 for key in ["html_progress", "cplusplus_progress", "mysql_progress", "python_progress", "java_progress"]}
        
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


def insert_new_user(username, gender):
    """Inserts a new user with default progress into the database."""
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        insert_query = """
        INSERT INTO user_progress (username, gender, html_progress, cplusplus_progress, mysql_progress, python_progress, java_progress)
        VALUES (%s, %s, 0.00, 0.00, 0.00, 0.00, 0.00)
        """
        cursor.execute(insert_query, (username.upper(), gender))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        if err.errno == 1062: 
            messagebox.showerror("Registration Error", "That username already exists!")
        else:
            messagebox.showerror("Database Error", f"Failed to register new user: {err}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def delete_user_progress(username):
    """Deletes a user's progress record from the database."""
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
# Helper Functions
# =============================

def log_coordinates(event):
    """Prints the X and Y coordinates of a click event for debugging."""
    print(f"Clicked Coordinates (X, Y): {event.x}, {event.y}")

def load_pil_image(filename, width, height, mode='RGBA'):
    """Loads, resizes, and returns a PIL Image object with alpha channel."""
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        placeholder = Image.new(mode, (width, height), color='red')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(placeholder)
        draw.text((10, 10), filename, fill=(255, 255, 255))
        return placeholder
    
    img = Image.open(path).convert(mode)
    return img.resize((width, height), Image.Resampling.LANCZOS)

def draw_skill_progress_bar(canvas, bar_data):
    """Draws a custom SEGMENTED styled progress bar on the canvas."""
    x, y, w, h = bar_data["x"], bar_data["y"], bar_data["w"], bar_data["h"]
    progress = bar_data["progress"]
    color = bar_data["color"]
    skill = bar_data["skill"]
    
    padding = 2             
    segment_width = 4       
    gap_width = 1           
    
    # 1. Draw the Outer Container
    canvas.create_rectangle(
        x, y, x + w, y + h, 
        outline="#FFFFFF", 
        width=2,
        fill="#000000",
        tags=f"{skill}_bar_outline"
    )
    
    # Inner bar boundaries
    inner_x_start = x + padding
    inner_y_top = y + padding
    inner_y_bottom = y + h - padding
    usable_width = w - 2 * padding
    segment_unit_width = segment_width + gap_width
    num_total_units = usable_width // segment_unit_width
    num_segments_to_fill = int(num_total_units * progress)
    
    # 2. Draw the Segmented Progress Fill
    for i in range(num_total_units):
        start_x = inner_x_start + (i * segment_unit_width)
        end_x = start_x + segment_width
        
        if i < num_segments_to_fill:
            fill_color = color
        else:
            fill_color = "#333333" 
            if i % 2 == 0:
                 fill_color = "#444444" 
        
        canvas.create_rectangle(
            start_x, inner_y_top, end_x, inner_y_bottom, 
            outline="",
            fill=fill_color,
            tags=f"{skill}_bar_segment_{i}"
        )

    # 3. Draw the Percentage Text 
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


# ---------------------------------------------------------
# ANIMATION & BINDING FUNCTIONS
# ---------------------------------------------------------
def pulse(tag):
    """Animates the size of a button image."""
    try:
        canvas_ref = STATE.current_canvas
        if not canvas_ref or not canvas_ref.winfo_exists(): return
    except: return

    data = STATE.button_data.get(tag)
    if not data: return
    
    STEP = 0.002
    MIN_SCALE = 1.00 # Base size
    MAX_SCALE = 1.05 # Maximum size (5% larger than base)

    target_scale = MAX_SCALE if data["hover"] else MIN_SCALE
    
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
            # Cancel the animation job once it returns to base size and no longer hovered
            STATE.root.after_cancel(data["job"])
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
    
    data["job"] = STATE.root.after(15, lambda: pulse(tag))

def on_enter(event, tag):
    """Handles hover-in event for pulse animation."""
    if tag == "next_btn" and STATE.selected_gender is None:
        STATE.root.config(cursor="arrow")
        return
    STATE.root.config(cursor="hand2")
    data = STATE.button_data.get(tag)
    if data:
        data["hover"] = True
        if data["job"] is None:
            data["growing"] = True 
            pulse(tag)

def on_leave(event, tag):
    """Handles hover-out event to stop pulse animation."""
    STATE.root.config(cursor="")
    data = STATE.button_data.get(tag)
    if data:
        data["hover"] = False

def create_pulsing_button(canvas, tag, filename, dims, coords, click_handler):
    """Creates a button, sets up state, and binds all events (enter, leave, click)."""
    pil_base = load_pil_image(filename, *dims, mode='RGBA')
    photo = ImageTk.PhotoImage(pil_base)
    
    canvas.create_image(*coords, image=photo, anchor="center", tags=tag)
    
    STATE.button_data[tag] = { "base_img": pil_base, "scale": 1.0, "growing": True, 
                                "hover": False, "job": None, "current_photo": photo }
    
    setattr(canvas, f"{tag}_img_ref", photo) 
    
    canvas.tag_bind(tag, "<Enter>", lambda e: on_enter(e, tag))
    canvas.tag_bind(tag, "<Leave>", lambda e: on_leave(e, tag))
    canvas.tag_bind(tag, "<Button-1>", click_handler)

# ---------------------------------------------------------
# AUDIO CONTROL FUNCTIONS & SLIDER CREATION
# ---------------------------------------------------------
def set_volume(value):
    """Updates pygame music volume based on slider value (0.0 to 1.0)."""
    try:
        volume = float(value) / 100.0
        pygame.mixer.music.set_volume(volume)
        STATE.initial_volume = float(value) 
    except pygame.error:
        pass
        
def start_music(music_file_path):
    """Initializes pygame mixer, loads, and plays background music in a loop."""
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(music_file_path)
        pygame.mixer.music.set_volume(STATE.initial_volume / 100.0) 
        pygame.mixer.music.play(-1)
        STATE.initial_volume = pygame.mixer.music.get_volume() * 100
    except pygame.error as e:
        pass
    except Exception as e:
        pass

def create_volume_slider(parent_window, is_portrait):
    """Creates, styles, and places the volume slider and icon."""
    
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

    current_slider = getattr(STATE, slider_attr)
    if current_slider: current_slider.destroy()
    current_label = getattr(STATE, icon_label_attr)
    if current_label and current_label.winfo_exists(): current_label.destroy()
    setattr(STATE, icon_label_attr, None)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure("TScale", background=parent_window['bg'], troughcolor="#444444")
    
    slider = ttk.Scale(
        parent_window, from_=0, to=100, orient='horizontal', 
        command=set_volume, style="TScale"
    )
    slider.set(STATE.initial_volume)
    setattr(STATE, slider_attr, slider)

    icon_pil = load_pil_image("sound.png", icon_size, icon_size, mode='RGBA')
    icon_photo = ImageTk.PhotoImage(icon_pil)
    setattr(STATE, icon_ref_attr, icon_photo) 

    if is_portrait:
        total_width = slider_width + 10 + icon_size
        start_x = (WINDOW_WIDTH - total_width) // 2
        slider_y_offset = (25 - icon_size) // 2 
    else:
        start_x = LANDSCAPE_SLIDER_X 
        slider_y_offset = (25 - icon_size) // 2 

    icon_label = tk.Label(parent_window, image=icon_photo, bg=parent_window['bg'], bd=0)
    setattr(STATE, icon_label_attr, icon_label)
    
    icon_label.place(x=start_x, y=y_position + slider_y_offset)

    slider.place(x=start_x + icon_size + 10, y=y_position, width=slider_width)
    
    if parent_window.winfo_class() != "Tk": 
        parent_window.after(10, slider.lift)
        parent_window.after(10, icon_label.lift)
    else: 
        STATE.root.after(10, slider.lift)
        STATE.root.after(10, icon_label.lift)


# ---------------------------------------------------------
# FRAME LOGIC
# ---------------------------------------------------------
def clear_current_frame():
    """
    Destroys the current canvas and associated dialog window.
    Cancels all pending pulse animation jobs.
    """
    for data in STATE.button_data.values():
        if data.get("job"):
            try:
                STATE.root.after_cancel(data["job"])
            except ValueError:
                pass
            data["job"] = None
    STATE.button_data.clear() 
    
    if STATE.current_canvas: STATE.current_canvas.destroy()
    STATE.current_canvas = None
    STATE.bg_ref = None 
    STATE.banner_char_ref = None 
    STATE.skill_bar_refs = [] 

def create_main_menu():
    clear_current_frame()
    
    # Ensure root window is visible when returning to main menu
    STATE.root.deiconify() 
    
    canvas = tk.Canvas(STATE.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, 
                       highlightthickness=0, bg=STATE.root['bg'])
    canvas.pack(fill="both", expand=True)
    STATE.current_canvas = canvas

    # --- DEBUGGING: Bind click event to log coordinates ---
    canvas.bind("<Button-1>", log_coordinates)
    
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
    clear_current_frame()
    
    STATE.root.deiconify() 
    if STATE.landscape_window:
        STATE.landscape_window.destroy()
        STATE.landscape_window = None

    STATE.selected_gender = None 
    STATE.user_name = None 

    canvas = tk.Canvas(STATE.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, 
                       highlightthickness=0, bg=STATE.root['bg'])
    canvas.pack(fill="both", expand=True)
    STATE.current_canvas = canvas

    # --- DEBUGGING: Bind click event to log coordinates ---
    canvas.bind("<Button-1>", log_coordinates)

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
    
    STATE.gender_label = tk.Label(canvas, text="", font=("Arial", 16, "bold"), 
                                  bg="#000000", fg="white", relief="flat")

    create_volume_slider(STATE.root, is_portrait=True)


def create_landscape_window(title, close_handler):
    """Initializes and configures a standard landscape Toplevel window."""
    clear_current_frame()
    STATE.root.withdraw() 

    if STATE.landscape_window:
        STATE.landscape_window.destroy()
        STATE.landscape_window = None
    
    win = tk.Toplevel(STATE.root)
    win.title(title)
    win.resizable(True, True) 
    win.configure(bg="#101030") 
    STATE.landscape_window = win
    
    center_x = (STATE.root.winfo_screenwidth() - LANDSCAPE_WIDTH) // 2
    center_y = (STATE.root.winfo_screenheight() - LANDSCAPE_HEIGHT) // 2
    win.geometry(f"{LANDSCAPE_WIDTH}x{LANDSCAPE_HEIGHT}+{center_x}+{center_y}")
    
    # Use the close_handler for the window's X button (top right)
    win.protocol("WM_DELETE_WINDOW", close_handler)

    canvas = tk.Canvas(win, width=LANDSCAPE_WIDTH, height=LANDSCAPE_HEIGHT, 
                       highlightthickness=0, bg=win['bg']) 
    canvas.pack(fill="both", expand=True)
    STATE.current_canvas = canvas 

    # --- DEBUGGING: Bind click event to log coordinates on landscape view ---
    canvas.bind("<Button-1>", log_coordinates)
    
    create_volume_slider(win, is_portrait=False) 
    
    return win, canvas

def show_third_frame():
    """Game View (Frame 3) - Dashboard with dynamic data from MySQL."""
    if STATE.user_name is None or STATE.selected_gender is None:
        messagebox.showwarning("Error", "Missing user data. Please complete user selection or creation.")
        create_main_menu()
        return

    STATE.db_progress_data = get_user_progress(STATE.user_name)

    # Handler for the Toplevel window's close button (X)
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu()
        
    win, canvas = create_landscape_window(f"Hasa Leveling - Dashboard: {STATE.user_name}", close_handler)

    dashboard_image = load_pil_image("dashboard.png", LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
    dashboard_photo = ImageTk.PhotoImage(dashboard_image)
    canvas.create_image(0, 0, image=dashboard_photo, anchor="nw")
    STATE.bg_ref = dashboard_photo 
    
    # --- DYNAMIC BANNER CONTENT ---
    # Username Shadow Text - uses the new USERNAME_TEXT_X
    canvas.create_text(
        USERNAME_TEXT_X + 2, USER_NAME_TEXT_Y + 2, 
        text=STATE.user_name.upper(), font=("Arial Black", 93, "bold"), fill="#3399FF", anchor="center", tags="user_name_shadow"
    )
    # Main Username Text - uses the new USERNAME_TEXT_X
    canvas.create_text(
        USERNAME_TEXT_X, USER_NAME_TEXT_Y, 
        text=STATE.user_name.upper(), font=("Arial Black", 93, "bold"), fill="#FFFFFF", anchor="center", justify="center", tags="user_name_text"
    )
    
    char_filename = "maledashboard.png" if STATE.selected_gender == "Male" else "femaledashboard.png"
    dims = MALE_AVATAR_DIMS if STATE.selected_gender == "Male" else FEMALE_AVATAR_DIMS 
        
    char_pil = load_pil_image(char_filename, *dims, mode='RGBA')
    char_photo = ImageTk.PhotoImage(char_pil)
    STATE.banner_char_ref = char_photo 
    
    # Character Avatar - uses the new AVATAR_CENTER_X and AVATAR_CENTER_Y
    canvas.create_image(AVATAR_CENTER_X, AVATAR_CENTER_Y, image=char_photo, anchor="center", tags="character_avatar")
    
    # --- SKILL PROGRESS BARS (DATABASE-DRIVEN) ---
    for bar in BASE_SKILL_PROGRESS_BARS:
        progress_value = STATE.db_progress_data.get(bar["db_key"], 0.10)
        bar_data = bar.copy()
        bar_data["progress"] = progress_value
        draw_skill_progress_bar(canvas, bar_data)
        
    # --- NAVIGATION BAR ELEMENTS ---
    NAV_BAR_Y_CENTER = 730 

    NAV_BUTTONS = [
        {"tag": "homenav_btn", "path": "homenav.png", "dims": (52, 65), "coords": (371, NAV_BAR_Y_CENTER), "handler": lambda e: show_third_frame()},
        {"tag": "tutorialnav_btn", "path": "tutorialnav.png", "dims": (82, 60), "coords": (545, NAV_BAR_Y_CENTER), "handler": lambda e: show_fourth_frame()},
        {"tag": "problemsnav_btn", "path": "problemsnav.png", "dims": (84, 60), "coords": (761, NAV_BAR_Y_CENTER), "handler": lambda e: show_fifth_frame()},
        
        # The exit button triggers 'Sign Out' which returns to Frame 1
        {"tag": "exitnav_btn", "path": "exitnav.png", "dims": (73, 65), "coords": (961, NAV_BAR_Y_CENTER), "handler": lambda e: on_nav_exit_click(win)},
    ]

    for btn in NAV_BUTTONS:
        create_pulsing_button(canvas, btn["tag"], btn["path"], btn["dims"], btn["coords"], btn["handler"])
        
    # --- SKILL BUTTONS ---
    for btn in SKILL_BUTTONS:
        create_pulsing_button(canvas, btn["tag"], btn["path"], btn["dims"], btn["coords"], btn["handler"])


def show_fourth_frame():
    """Tutorials View (Frame 4)"""
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu() 
        
    win, canvas = create_landscape_window("Hasa Leveling - Tutorials", close_handler)
    
    tk.Label(canvas, 
             text="TUTORIALS VIEW (FRAME 4)\n\nThis is where the user learns game mechanics.",
             font=("Arial", 24, "bold"), fg="white", bg=canvas['bg']
            ).place(relx=0.5, rely=0.5, anchor="center")
            
    tk.Button(canvas, text="Return to Dashboard (Frame 3)", command=show_third_frame, font=("Arial", 12)).place(x=10, y=10)


def show_fifth_frame():
    """Problems/Quests View (Frame 5)"""
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu() 

    win, canvas = create_landscape_window("Hasa Leveling - Problems/Quests", close_handler)
    
    tk.Label(canvas, 
             text="PROBLEMS/QUESTS VIEW (FRAME 5)\n\nThis is where the user solves problems and completes quests.",
             font=("Arial", 24, "bold"), fg="white", bg=canvas['bg']
            ).place(relx=0.5, rely=0.5, anchor="center")
            
    tk.Button(canvas, text="Return to Dashboard (Frame 3)", command=show_third_frame, font=("Arial", 12)).place(x=10, y=10)


# ---------------------------------------------------------
# DIALOG & PROGRESSION FUNCTIONS
# ---------------------------------------------------------
def prompt_for_name():
    """Pops up a dialog box to ask the user for their name, validating and registering a NEW user."""
    
    if STATE.selected_gender is None:
        messagebox.showwarning("Selection Required", "Please select a gender (Male or Female) before proceeding.")
        return

    dialog = tk.Toplevel(STATE.root)
    dialog.title("Register Character Name")
    dialog.geometry("300x180")
    dialog.transient(STATE.root)
    dialog.grab_set()
    
    dialog_x = STATE.root.winfo_x() + (STATE.root.winfo_width() // 2) - 150
    dialog_y = STATE.root.winfo_y() + (STATE.root.winfo_height() // 2) - 90
    dialog.geometry(f'+{dialog_x}+{dialog_y}')

    tk.Label(dialog, text="Input NEW Character Name:", font=("Arial", 12, "bold")).pack(pady=5)
    tk.Label(dialog, text="(Min: 4 chars, Max: 9 chars)", font=("Arial", 9)).pack()
    name_entry = tk.Entry(dialog, width=30)
    name_entry.pack(pady=5)
    name_entry.focus_set()

    def register_and_proceed():
        name = name_entry.get().strip()
        
        if not name:
            messagebox.showwarning("Input Required", "Please enter a name to continue.")
        elif len(name) < 4:
            messagebox.showwarning("Invalid Name", "Name must be at least 4 characters long.")
        elif len(name) > 9:
            messagebox.showwarning("Invalid Name", "Name cannot exceed 9 characters.")
        else:
            if insert_new_user(name, STATE.selected_gender):
                STATE.user_name = name
                dialog.destroy()
                show_third_frame() 

    tk.Button(dialog, text="Confirm & Register", command=register_and_proceed, font=("Arial", 10)).pack(pady=10)
    dialog.bind('<Return>', lambda event: register_and_proceed())
    
    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
    STATE.root.wait_window(dialog)


def show_user_selection_dialog(user_data):
    """Pops up a dialog to allow the user to select an existing profile and offers delete/create options."""
    
    dialog = tk.Toplevel(STATE.root)
    dialog.title("Manage User Profiles")
    dialog.geometry("350x300")
    dialog.transient(STATE.root)
    dialog.grab_set()
    
    dialog_x = STATE.root.winfo_x() + (STATE.root.winfo_width() // 2) - 175
    dialog_y = STATE.root.winfo_y() + (STATE.root.winfo_height() // 2) - 150
    dialog.geometry(f'+{dialog_x}+{dialog_y}')
    
    has_users = bool(user_data)
    usernames = sorted(user_data.keys())
    
    selected_user_var = tk.StringVar(dialog)
    if has_users:
        selected_user_var.set(usernames[0]) 

    # --- Load User Section ---
    tk.Label(dialog, text="--- SELECT EXISTING USER ---", font=("Arial", 12, "bold")).pack(pady=5)
    
    if has_users:
        user_menu = ttk.Combobox(dialog, textvariable=selected_user_var, values=usernames, state="readonly", width=20)
        user_menu.pack(pady=5)
    else:
        tk.Label(dialog, text="No existing users found.", fg="red").pack(pady=10)
        
    def select_and_load():
        if has_users:
            username = selected_user_var.get()
            if username in user_data:
                STATE.user_name = username
                STATE.selected_gender = user_data[username]
                dialog.destroy()
                show_third_frame()
        else:
            messagebox.showwarning("Selection", "Please create a new user.")
            
    load_btn = tk.Button(dialog, text="Load Selected User", command=select_and_load, font=("Arial", 10, "bold"), 
                         bg="#3399FF", fg="white", state=tk.NORMAL if has_users else tk.DISABLED)
    load_btn.pack(pady=5)

    # --- Delete User Functionality ---
    def delete_selected_user():
        if not has_users:
            return

        username = selected_user_var.get()
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to permanently delete user '{username}' and all their progress?", parent=dialog)
        
        if confirm:
            if delete_user_progress(username):
                messagebox.showinfo("Success", f"User '{username}' has been deleted.", parent=dialog)
                dialog.destroy()
                
                # Re-run the main access flow to refresh the user list
                STATE.user_list = fetch_all_users()
                show_user_selection_dialog(STATE.user_list)
            
    delete_btn = tk.Button(dialog, text="Delete Selected User", command=delete_selected_user, font=("Arial", 10), 
                           bg="#FF3333", fg="white", state=tk.NORMAL if has_users else tk.DISABLED)
    delete_btn.pack(pady=5)

    tk.Frame(dialog, height=1, bg="gray").pack(fill='x', pady=10) 

    # --- Create New User Section ---
    tk.Label(dialog, text="--- OR ---", font=("Arial", 10)).pack()
    tk.Button(dialog, text="Create New User", command=lambda: [dialog.destroy(), show_second_frame()], font=("Arial", 10)).pack(pady=10)

    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
    STATE.root.wait_window(dialog)


def confirm_action(action, window_to_close):
    """
    Shows a final confirmation dialog for either Sign Out or Exit.
    Includes reliable Pygame mixer stop/quit on Exit.
    """
    if action == 'Sign Out':
        confirmation = messagebox.askyesno(
            "Confirm Sign Out", 
            "Are you sure you want to sign out and return to the main menu?"
        )
    else: # Exit
        confirmation = messagebox.askyesno(
            "Confirm Exit", 
            "Are you sure you want to exit the application?"
        )

    if confirmation:
        if action == 'Exit':
            # --- FIX: Ensure Pygame mixer is explicitly stopped and quit on EXIT ---
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit() 
            except Exception as e:
                print(f"Warning: Pygame mixer quit failed: {e}")
                pass 
            # ----------------------------------------------------------------------

            if window_to_close:
                window_to_close.destroy()
            STATE.root.destroy()
        
        elif action == 'Sign Out':
            # --- FIX: Ensure root window is visible when returning to main menu ---
            if window_to_close:
                window_to_close.destroy()
            
            # This is important if root was hidden by landscape window (.withdraw())
            STATE.root.deiconify() 
            create_main_menu()
            
def on_nav_exit_click(landscape_window):
    """
    Handles the exit button click on the dashboard by confirming sign out.
    """
    confirm_action('Sign Out', landscape_window)


# ---------------------------------------------------------
# CLICK HANDLERS
# ---------------------------------------------------------
def on_access_game_click(event):
    """Fetches user list and opens selection dialog."""
    STATE.user_list = fetch_all_users()
    show_user_selection_dialog(STATE.user_list)

def on_exit_click(event=None):
    """Handles the exit button click on the main menu (Frame 1)."""
    confirm_action('Exit', None)


def on_gender_click(gender):
    """Handles gender selection/deselection on Frame 2."""
    is_deselecting = (STATE.selected_gender == gender)
    STATE.selected_gender = None if is_deselecting else gender
    
    if STATE.selected_gender:
        STATE.gender_label.config(text=f"Gender Selected: {gender}")
        STATE.gender_label.place(relx=0.5, rely=0.42, anchor="center") 
        STATE.gender_label.lift()
    else:
        STATE.gender_label.config(text="")
        STATE.gender_label.place_forget() 

def on_next_char_click(event):
    """Proceeds from Frame 2 to register a new user name."""
    prompt_for_name()


# =============================
# RUN
# =============================
if __name__ == "__main__":
    
    # Root setup
    root = tk.Tk()
    root.title("Hasa Leveling")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    root.configure(bg="#000000") 
    root.resizable(False, False)
    STATE.root = root 

    # Set the application window icon
    try:
        icon_pil = load_pil_image("logoicon.png", APP_ICON_SIZE, APP_ICON_SIZE, mode='RGBA')
        icon_photo = ImageTk.PhotoImage(icon_pil)
        STATE.app_icon_ref = icon_photo 
        root.iconphoto(True, icon_photo)
    except Exception as e:
        pass

    # Music
    music_path = os.path.join(ASSETS_DIR, "bgmusic.mp3") 
    start_music(music_path)
    
    # Start app flow
    create_main_menu()
    
    root.mainloop()