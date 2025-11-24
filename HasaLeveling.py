import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import pygame
import mysql.connector
import webbrowser 

# --- GLOBAL CONSTANTS ---
ASSETS_DIR = "assets"

# NEW: Sound effect file path
CLICK_SOUND_PATH = os.path.join(ASSETS_DIR, "clicksoundeffect.wav")

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
AVATAR_CENTER_X = 1080  
AVATAR_CENTER_Y = 130 
USERNAME_TEXT_X = 450
USER_NAME_TEXT_Y = 125

# Avatar Dimensions for Individual Scaling
MALE_AVATAR_DIMS = (560, 315)
FEMALE_AVATAR_DIMS = (522, 273) 

# --- TUTORIAL FRAME ICON CONSTANTS ---
TUTORIAL_ICON_X = 240 
TUTORIAL_ICON_Y = 455 
TUTORIAL_ICON_DIMS = (160, 203)

# --- PROBLEM SOLVER BUTTON CONSTANTS ---
REVEAL_ANSWER_DIMS = (240, 130)
REVEAL_ANSWER_COORDS = (740, 530)

BACK_PROBLEM_DIMS = (220, 110)
BACK_PROBLEM_COORDS = (160, 580)

# --- ANSWER FRAME BUTTON CONSTANTS (New) ---
ADDSKILL_BUTTON_DIMS = (220, 110)
ADDSKILL_BUTTON_COORDS = (1255, 625)

# --- QOL ADDITION: LANDSCAPE USERNAME DISPLAY ---
LANDSCAPE_USERNAME_X = LANDSCAPE_WIDTH - 50 # Near the right edge
LANDSCAPE_USERNAME_Y = 30 # Near the top
LANDSCAPE_USERNAME_FONT = ("Arial Black", 16, "bold")


# --- TUTORIAL YOUTUBE LINKS ---
TUTORIAL_LINKS = {
    "Python": {
        1: "https://www.youtube.com/watch?v=python_link_1", 
        2: "https://www.youtube.com/watch?v=python_link_2",
        3: "https://www.youtube.com/watch?v=python_link_3",
        4: "https://www.youtube.com/watch?v=python_link_4",
        5: "https://www.youtube.com/watch="
    },
    "Java": {
        1: "https://www.youtube.com/watch?v=java_link_1", 
        2: "https://www.youtube.com/watch?v=java_link_2",
        3: "https://www.youtube.com/watch?v=java_link_3",
        4: "https://www.youtube.com/watch?v=java_link_4",
        5: "https://www.youtube.com/watch?v=java_link_5"
    },
    "HTML": {
        1: "https://www.youtube.com/watch?v=html_link_1", 
        2: "https://www.youtube.com/watch?v=html_link_2",
        3: "https://www.youtube.com/watch?v=html_link_3",
        4: "https://www.youtube.com/watch?v=html_link_4",
        5: "https://www.youtube.com/watch?v=html_link_5"
    },
    "C++": {
        1: "https://www.youtube.com/watch?v=c_plus_plus_link_1", 
        2: "https://www.youtube.com/watch?v=c_plus_plus_link_2",
        3: "https://www.youtube.com/watch?v=c_plus_plus_link_3",
        4: "https://www.youtube.com/watch?v=c_plus_plus_link_4",
        5: "https://www.youtube.com/watch?v=c_plus_plus_link_5"
    },
    "MySQL": {
        1: "https://www.youtube.com/watch?v=mysql_link_1", 
        2: "https://www.youtube.com/watch?v=mysql_link_2",
        3: "https://www.youtube.com/watch?v=mysql_link_3",
        4: "https://www.youtube.com/watch?v=mysql_link_4",
        5: "https://www.youtube.com/watch?v=mysql_link_5"
    },
}

# --- TUTORIAL PLAY BUTTON CONFIGURATION ---
PLAY_BUTTONS_DIMS = (156.1, 47.3) 
PLAY_BUTTONS_CONFIG = [
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
    "password": "jayvee101", 
    "database": "hasaleveling_db"
}

# SKILL BUTTON CONFIGURATION (Left Side)
SKILL_BUTTONS = [
    {"tag": "pythonskill_btn", "path": "pythonskill.png", "dims": (219, 137), "coords": (137, 411), "handler": lambda e: on_skill_button_click("Python")},
    {"tag": "javaskill_btn", "path": "javaskill.png", "dims": (223, 139), "coords": (325, 408), "handler": lambda e: on_skill_button_click("Java")},
    {"tag": "htmlskill_btn", "path": "htmlskill.png", "dims": (219, 137), "coords": (137, 513), "handler": lambda e: on_skill_button_click("HTML")},
    {"tag": "c++skill_btn", "path": "c++skill.png", "dims": (223, 139), "coords": (327, 514), "handler": lambda e: on_skill_button_click("C++")},
    {"tag": "mysqlskill_btn", "path": "mysqlskill.png", "dims": (220, 137), "coords": (224, 614), "handler": lambda e: on_skill_button_click("MySQL")},
]

# BASE SKILL PROGRESS BAR CONFIGURATION
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
        self.volume_slider_root = None
        self.volume_slider_landscape = None
        self.app_icon_ref = None 
        self.icon_ref_portrait = None
        self.icon_label_portrait = None
        self.icon_ref_landscape = None
        self.icon_label_landscape = None
        self.button_data = {}
        self.selected_gender = None
        self.user_name = None
        self.bg_ref = None 
        self.initial_volume = 50.0
        self.banner_char_ref = None 
        self.skill_bar_refs = [] 
        self.db_progress_data = {} 
        self.user_list = {}
        self.tutorial_icon_ref = None
        self.current_tutorial_skill = None 
        self.click_sound = None 
        self.current_problem_number = None 
        
STATE = AppState()

# =============================
# Database Functions
# =============================

def get_db_connection():
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
    conn = get_db_connection()
    if not conn:
        return {}
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
    conn = get_db_connection()
    if not conn:
        # NOTE: This fallback is good, but it's important to use the same logic 
        # as the default values for a new user if the DB is down.
        # Returning 0.10 for consistency with new user insert fallback.
        return {
            "html_progress": 0.10, "cplusplus_progress": 0.10, 
            "mysql_progress": 0.10, "python_progress": 0.10, 
            "java_progress": 0.10, "status": "default_used"
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
        
        # Fallback for existing user not found (shouldn't happen if called correctly)
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
    conn = get_db_connection()
    if not conn:
        return False
    
    # Map the display skill name to the database column name (db_key)
    # The original function signature takes the display name, but the internal logic uses db_key
    # The 'db_key' in the original implementation was the display name (e.g., "Python").
    # For this function to work correctly, we map the display name to the column name.
    skill_map = {
        "HTML": "html_progress",
        "C++": "cplusplus_progress",
        "MySQL": "mysql_progress",
        "Python": "python_progress",
        "Java": "java_progress"
    }
    column_name = skill_map.get(db_key) # db_key here is actually the skill_name (e.g., "Python")
    if not column_name:
        print(f"Error: Invalid skill name provided: {db_key}")
        return False
        
    try:
        cursor = conn.cursor()
        # Ensure progress doesn't exceed 1.0 (100%)
        # This SQL statement gets the current value, adds the increment, and then caps it at 1.0
        update_query = f"""
        UPDATE user_progress 
        SET {column_name} = LEAST({column_name} + %s, 1.0) 
        WHERE username = %s
        """
        cursor.execute(update_query, (increment, username.upper()))
        conn.commit()
        return cursor.rowcount > 0
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Failed to update progress for {db_key}: {err}")
        return False
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def insert_new_user(username, gender):
    conn = get_db_connection()
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        # Start new users with 0.10 (10%) progress as per your default/fallback values
        insert_query = """
        INSERT INTO user_progress (username, gender, html_progress, cplusplus_progress, mysql_progress, python_progress, java_progress)
        VALUES (%s, %s, 0.10, 0.10, 0.10, 0.10, 0.10)
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
    print(f"Clicked Coordinates (X, Y): {event.x}, {event.y}")

def load_pil_image(filename, width, height, mode='RGBA'):
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
    return img.resize((width, height), Image.Resampling.LANCZOS) 

def draw_skill_progress_bar(canvas, bar_data):
    x, y, w, h = bar_data["x"], bar_data["y"], bar_data["w"], bar_data["h"]
    progress = bar_data["progress"]
    color = bar_data["color"]
    skill = bar_data["skill"]
    
    padding = 2             
    segment_width = 4       
    gap_width = 1           
    
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
    num_total_units = usable_width // segment_unit_width
    num_segments_to_fill = int(num_total_units * progress)
    
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
    """Plays a short click sound effect."""
    if STATE.click_sound:
        try:
            STATE.click_sound.play()
        except pygame.error as e:
            # Handle cases where mixer might be busy or sound object is invalid
            # print(f"Warning: Could not play click sound: {e}")
            pass
    else:
        # Load the sound if it hasn't been loaded yet
        try:
            STATE.click_sound = pygame.mixer.Sound(CLICK_SOUND_PATH)
            STATE.click_sound.play()
        except pygame.error as e:
            print(f"Error loading or playing click sound: {e}")
        except FileNotFoundError:
            print(f"Error: Click sound file not found at {CLICK_SOUND_PATH}")

# ---------------------------------------------------------
# ANIMATION & BINDING FUNCTIONS
# ---------------------------------------------------------
def pulse(tag):
    try:
        canvas_ref = STATE.current_canvas
        if not canvas_ref or not canvas_ref.winfo_exists(): return
    except: return

    data = STATE.button_data.get(tag)
    if not data: return
    
    STEP = 0.002
    MIN_SCALE = 1.00 
    MAX_SCALE = 1.05 

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
    # REMOVED: check for next_btn and STATE.selected_gender here to allow pulse
    STATE.root.config(cursor="hand2")
    data = STATE.button_data.get(tag)
    if data:
        data["hover"] = True
        if data["job"] is None:
            data["growing"] = True 
            pulse(tag)

def on_leave(event, tag):
    STATE.root.config(cursor="")
    data = STATE.button_data.get(tag)
    if data:
        data["hover"] = False

def create_pulsing_button(canvas, tag, filename, dims, coords, click_handler, disable_pulse=False):
    """
    Creates an image button that pulses on hover unless disable_pulse is True.
    """
    w, h = dims
    pil_base = load_pil_image(filename, round(w), round(h), mode='RGBA') 
    photo = ImageTk.PhotoImage(pil_base)
    
    canvas.create_image(*coords, image=photo, anchor="center", tags=tag)
    
    # Check if a reference for this photo is already stored (from a previous frame)
    # If not, create the ref to prevent garbage collection
    if not hasattr(canvas, f"{tag}_img_ref"):
        setattr(canvas, f"{tag}_img_ref", photo) 

    if not disable_pulse:
        STATE.button_data[tag] = { "base_img": pil_base, "scale": 1.0, "growing": True, 
                                    "hover": False, "job": None, "current_photo": photo }
    else:
        # Still need to initialize data to allow the basic cursor change logic to work
        STATE.button_data[tag] = { "base_img": pil_base, "scale": 1.0, "growing": False, 
                                    "hover": False, "job": None, "current_photo": photo }

    
    if not disable_pulse:
        canvas.tag_bind(tag, "<Enter>", lambda e: on_enter(e, tag))
        canvas.tag_bind(tag, "<Leave>", lambda e: on_leave(e, tag))
        
        # MODIFIED: Wrap the original handler to play sound first
        def wrapped_handler(event):
            play_click_sound()
            click_handler(event)
            
        canvas.tag_bind(tag, "<Button-1>", wrapped_handler)
    else:
        # For non-interactive buttons (like dashboard icons that navigate back) 
        # that should not pulse, but still need the hand cursor.
        canvas.tag_bind(tag, "<Enter>", lambda e: STATE.root.config(cursor="hand2"))
        canvas.tag_bind(tag, "<Leave>", lambda e: STATE.root.config(cursor=""))
        canvas.tag_bind(tag, "<Button-1>", lambda e: (play_click_sound(), click_handler(e)))


# ---------------------------------------------------------
# AUDIO CONTROL FUNCTIONS & SLIDER CREATION
# ---------------------------------------------------------
def set_volume(value):
    try:
        volume = float(value) / 100.0
        pygame.mixer.music.set_volume(volume)
        STATE.initial_volume = float(value) 
    except pygame.error:
        pass
        
def start_music(music_file_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(music_file_path)
        pygame.mixer.music.set_volume(STATE.initial_volume / 100.0) 
        pygame.mixer.music.play(-1)
        STATE.initial_volume = pygame.mixer.music.get_volume() * 100
    except pygame.error as e:
        # print(f"Warning: Pygame music error: {e}")
        pass
    except Exception as e:
        # print(f"Warning: Unexpected music error: {e}")
        pass

def create_volume_slider(parent_window, is_portrait):
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
    STATE.tutorial_icon_ref = None 
    STATE.current_problem_number = None 

def on_tutorial_nav_click(event):
    if STATE.current_tutorial_skill:
        show_fourth_frame(STATE.current_tutorial_skill)
    else:
        messagebox.showwarning("Skill Selection Required", "Please click a skill button on the left side of the Dashboard (Python, Java, etc.) to view its tutorial.")

def create_nav_buttons(canvas, win):
    NAV_BAR_Y_CENTER = 730 
    
    # MODIFIED COORDINATES FOR BETTER SPACING: (343, 563, 783, 1003)
    NAV_BUTTONS = [
        {"tag": "homenav_btn", "path": "homenav.png", "dims": (52, 65), "coords": (343, NAV_BAR_Y_CENTER), "handler": lambda e: show_third_frame()},
        {"tag": "tutorialnav_btn", "path": "tutorialnav.png", "dims": (82, 60), "coords": (563, NAV_BAR_Y_CENTER), "handler": on_tutorial_nav_click}, 
        {"tag": "problemsnav_btn", "path": "problemsnav.png", "dims": (84, 60), "coords": (783, NAV_BAR_Y_CENTER), "handler": lambda e: show_fifth_frame()},
        {"tag": "exitnav_btn", "path": "exitnav.png", "dims": (73, 65), "coords": (1003, NAV_BAR_Y_CENTER), "handler": lambda e: on_nav_exit_click(win)},
    ]
    for btn in NAV_BUTTONS:
        # disable_pulse is False by default, enabling the pulse animation for navigation buttons
        create_pulsing_button(canvas, btn["tag"], btn["path"], btn["dims"], btn["coords"], btn["handler"], disable_pulse=False)


def create_main_menu():
    clear_current_frame()
    STATE.root.deiconify() 
    
    canvas = tk.Canvas(STATE.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, 
                       highlightthickness=0, bg=STATE.root['bg'])
    canvas.pack(fill="both", expand=True)
    STATE.current_canvas = canvas
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
    # Ensure next_btn also uses the pulsing feature
    create_pulsing_button(canvas, "next_btn", "nextChar.png", NEXT_DIMS, (263, 850), on_next_char_click)
    
    STATE.gender_label = tk.Label(canvas, text="", font=("Arial", 16, "bold"), 
                                  bg="#000000", fg="white", relief="flat")
    create_volume_slider(STATE.root, is_portrait=True)


# MODIFIED: Added user_name display
def create_landscape_window(title, close_handler):
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
    
    win.protocol("WM_DELETE_WINDOW", close_handler)

    canvas = tk.Canvas(win, width=LANDSCAPE_WIDTH, height=LANDSCAPE_HEIGHT, 
                       highlightthickness=0, bg=win['bg']) 
    canvas.pack(fill="both", expand=True)
    STATE.current_canvas = canvas 
    canvas.bind("<Button-1>", log_coordinates)
    create_volume_slider(win, is_portrait=False) 

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
    if STATE.user_name is None or STATE.selected_gender is None:
        messagebox.showwarning("Error", "Missing user data. Please complete user selection or creation.")
        create_main_menu()
        return

    STATE.db_progress_data = get_user_progress(STATE.user_name)

    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu()
        
    win, canvas = create_landscape_window(f"Hasa Leveling - Dashboard: {STATE.user_name}", close_handler)

    dashboard_image = load_pil_image("dashboard.png", LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
    dashboard_photo = ImageTk.PhotoImage(dashboard_image)
    canvas.create_image(0, 0, image=dashboard_photo, anchor="nw")
    STATE.bg_ref = dashboard_photo 
    
    canvas.create_text(
        USERNAME_TEXT_X + 2, USER_NAME_TEXT_Y + 2, 
        text=STATE.user_name.upper(), font=("Arial Black", 93, "bold"), fill="#3399FF", anchor="center", tags="user_name_shadow"
    )
    canvas.create_text(
        USERNAME_TEXT_X, USER_NAME_TEXT_Y, 
        text=STATE.user_name.upper(), font=("Arial Black", 93, "bold"), fill="#FFFFFF", anchor="center", justify="center", tags="user_name_text"
    )
    
    char_filename = "maledashboard.png" if STATE.selected_gender == "Male" else "femaledashboard.png"
    dims = MALE_AVATAR_DIMS if STATE.selected_gender == "Male" else FEMALE_AVATAR_DIMS 
        
    char_pil = load_pil_image(char_filename, *dims, mode='RGBA')
    char_photo = ImageTk.PhotoImage(char_pil)
    STATE.banner_char_ref = char_photo 
    canvas.create_image(AVATAR_CENTER_X, AVATAR_CENTER_Y, image=char_photo, anchor="center", tags="character_avatar")
    
    for bar in BASE_SKILL_PROGRESS_BARS:
        progress_value = STATE.db_progress_data.get(bar["db_key"], 0.10)
        bar_data = bar.copy()
        bar_data["progress"] = progress_value
        draw_skill_progress_bar(canvas, bar_data)
        
    create_nav_buttons(canvas, win)
    for btn in SKILL_BUTTONS:
        create_pulsing_button(canvas, btn["tag"], btn["path"], btn["dims"], btn["coords"], btn["handler"])

def on_skill_button_click(skill_name):
    STATE.current_tutorial_skill = skill_name 
    show_fourth_frame(skill_name)

def open_tutorial_link(button_num):
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
            webbrowser.open_new_tab(link)
        except Exception as e:
            messagebox.showerror("System Error", f"Failed to open link. Please ensure you have a web browser installed. Error: {e}")
    else:
        messagebox.showwarning("Link Missing", f"Link for {skill} Tutorial {button_num} is not set or invalid in TUTORIAL_LINKS.")

def on_tutorial_icon_click(event):
    show_third_frame()

def show_fourth_frame(skill_name=None):
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu() 
        
    win, canvas = create_landscape_window("Hasa Leveling - Tutorials", close_handler)
    
    tutorial_image = load_pil_image("tutorialbg.png", LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
    tutorial_photo = ImageTk.PhotoImage(tutorial_image)
    canvas.create_image(0, 0, image=tutorial_photo, anchor="nw")
    STATE.bg_ref = tutorial_photo 
    
    if skill_name:
        skill_filename = f"tut{skill_name.lower().replace('+', '')}.png"
        # Now using create_pulsing_button for hover effect
        # Set disable_pulse=True here if you don't want the skill icon to pulse
        create_pulsing_button(
            canvas, 
            "tutorial_skill_icon", 
            skill_filename, 
            TUTORIAL_ICON_DIMS, 
            (TUTORIAL_ICON_X, TUTORIAL_ICON_Y), 
            on_tutorial_icon_click
        )

    for btn in PLAY_BUTTONS_CONFIG:
        handler = lambda e, num=btn["button_num"]: open_tutorial_link(num)
        # Ensure play buttons use the pulsing feature
        create_pulsing_button(canvas, btn["tag"], btn["path"], btn["dims"], btn["coords"], handler, disable_pulse=False)
            
    create_nav_buttons(canvas, win)


# --- MODIFIED FUNCTION: ADDSKILL CLICK HANDLER ---
def on_add_skill_click(skill_name, problem_number):
    """
    Updates user progress by adding 20% (0.20) to the specified skill
    and navigates back to the Dashboard to show the new progress.
    """
    increment = 0.20 # 20%
    if STATE.user_name and skill_name:
        if update_user_progress(STATE.user_name, skill_name, increment):
            messagebox.showinfo(
                "Skill Added!", 
                f"Congratulations! **{skill_name}** progress updated by 20% for completing Problem #{problem_number}!"
            )
            # After successful update, go back to the Dashboard (Frame 3) to refresh progress bars
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
    """Handles the Reveal Answer button click by showing the answer frame."""
    show_answer_frame(skill, problem_number)


def open_problem_solver(skill, problem_number):
    """
    This handles what happens when a folder is clicked.
    Routes to the specific problem frame.
    """
    STATE.current_problem_number = problem_number
    
    # MODIFIED: Route all skills to the solver frame for easier development
    show_problem_solver_frame(skill, problem_number)


# --- NEW FRAME: ANSWER SOLVER VIEW (Frame 8) ---
def show_answer_frame(skill_name, problem_number):
    """
    Frame 8: Answer View (The answer image is displayed here)
    """
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu() 
    
    # Create Window
    title = f"Hasa Leveling - {skill_name} Answer {problem_number}"
    win, canvas = create_landscape_window(title, close_handler)
    
    # --- Background Image Logic (answercX.png) ---
    skill_abbr_map = {
        "C++": "c", "Python": "python", "Java": "java", "HTML": "html", "MySQL": "mysql"
    }
    
    skill_abbr = skill_abbr_map.get(skill_name, "c") 
    
    # File naming convention: answerc1.png, answerj1.png, etc.
    bg_filename = f"answer{skill_abbr}{problem_number}.png"
    
    try:
        bg_image = load_pil_image(bg_filename, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
    except Exception:
        # Fallback
        bg_filename = "problemsbg.png" 
        bg_image = load_pil_image(bg_filename, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
        messagebox.showwarning("Image Missing", f"Could not load specific answer background: {bg_filename}. Using generic problem background.")
        
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    STATE.bg_ref = bg_photo 
    
    # ---------------------------------------------------------
    # 1. Back Button (Same dimensions/place as question frame's back button)
    # ---------------------------------------------------------
    create_pulsing_button(
        canvas, 
        "back_answer_btn", 
        "problemback.png", 
        BACK_PROBLEM_DIMS, 
        BACK_PROBLEM_COORDS, 
        # Back button returns to the question frame
        lambda e: show_problem_solver_frame(skill_name, problem_number)
    )

    # ---------------------------------------------------------
    # 2. Add Skill Button (New)
    # ---------------------------------------------------------
    # QoL Improvement: Only allow adding skill if progress is < 1.0 (100%)
    current_progress = STATE.db_progress_data.get(skill_name.lower().replace('+', '') + "_progress", 0.0)
    
    if current_progress < 1.0:
        create_pulsing_button(
            canvas, 
            "add_skill_btn", 
            "addskill.png", 
            ADDSKILL_BUTTON_DIMS, 
            ADDSKILL_BUTTON_COORDS, 
            lambda e: on_add_skill_click(skill_name, problem_number)
        )
    else:
        # QoL: Show a disabled/different button or just text if skill is maxed
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
    Frame 7: Problem Solving View (The actual question is displayed here)
    """
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu() 
    
    # Create Window
    title = f"Hasa Leveling - {skill_name} Problem {problem_number}"
    win, canvas = create_landscape_window(title, close_handler)
    
    # --- Background Image Logic (REFINED) ---
    # Map skill name to filename abbreviation
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
        # Fallback in case the specific image is missing
        bg_filename = "problemsbg.png" 
        bg_image = load_pil_image(bg_filename, LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
        messagebox.showwarning("Image Missing", f"Could not load specific background: {bg_filename}. Using generic problem background.")
        
    bg_photo = ImageTk.PhotoImage(bg_image)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    STATE.bg_ref = bg_photo 
    
    # ---------------------------------------------------------
    # 1. Reveal Answer Button (FILE NAME CORRECTED)
    # ---------------------------------------------------------
    create_pulsing_button(
        canvas, 
        "reveal_answer_btn", 
        "revealbutton.png", # CORRECTED FILENAME
        REVEAL_ANSWER_DIMS, 
        REVEAL_ANSWER_COORDS, 
        # Calls the updated handler
        lambda e: on_reveal_answer_click(skill_name, problem_number)
    )

    # ---------------------------------------------------------
    # 2. Back Button
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
    Frame 6: Problem Selection View (Folders)
    Displays the Skill Icon on the left and 5 Problem Folders on the right.
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
    # 1. LEFT SIDE: SKILL ICON (Same as Tutorial Frame)
    # ---------------------------------------------------------
    # Map skill name to filename (e.g., "Java" -> "tutjava.png")
    skill_filename = f"tut{skill_name.lower().replace('+', '')}.png"
    
    # Now using create_pulsing_button for hover effect
    create_pulsing_button(
        canvas, 
        "problem_skill_icon", 
        skill_filename, 
        TUTORIAL_ICON_DIMS, 
        (TUTORIAL_ICON_X, TUTORIAL_ICON_Y), 
        lambda e: show_fifth_frame()
    )

    # QoL Addition: Explicitly state the skill name under the icon
    canvas.create_text(
        TUTORIAL_ICON_X, TUTORIAL_ICON_Y + TUTORIAL_ICON_DIMS[1] // 2 + 20, 
        text=f"{skill_name} Problems", 
        font=("Arial Black", 18, "bold"), 
        fill="#FFD700",
        anchor="center"
    )
    
    # ---------------------------------------------------------
    # 2. RIGHT SIDE: FOLDER BUTTONS (Same positions as Play Buttons)
    # ---------------------------------------------------------
    
    # IMPORTANT: Set this to the actual size of your problem folder pngs
    FOLDER_DIMS = (150, 110) 
    
    # Offset to move folders up vertically
    FOLDER_Y_OFFSET = 50 

    # We reuse the coordinates from PLAY_BUTTONS_CONFIG but shift Y
    for i, config in enumerate(PLAY_BUTTONS_CONFIG):
        prob_num = i + 1
        folder_tag = f"folder_{prob_num}_btn"
        folder_path = f"problem{prob_num}.png" # problem1.png, problem2.png, etc.
        
        original_x, original_y = config["coords"]
        folder_coords = (original_x, original_y - FOLDER_Y_OFFSET)
        
        # Handler: Open the specific problem
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
    """Problems/Quests Menu (Frame 5)"""
    def close_handler():
        STATE.landscape_window.destroy()
        create_main_menu() 

    win, canvas = create_landscape_window("Hasa Leveling - Problems/Quests", close_handler)
    
    problems_bg_image = load_pil_image("problemsbg.png", LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
    problems_bg_photo = ImageTk.PhotoImage(problems_bg_image)
    canvas.create_image(0, 0, image=problems_bg_photo, anchor="nw")
    STATE.bg_ref = problems_bg_photo 
    
    # --- PROBLEM CATEGORY BUTTONS ---
    # IMPORTANT: Update this to your actual image dimensions if they differ
    PROBLEM_BTN_DIMS = (160, 203) 

    # Centered horizontally and lowered
    PROBLEM_BUTTONS = [
        {"tag": "prob_java",   "path": "tutjava.png",   "coords": (243, 500),    "skill": "Java"},
        {"tag": "prob_html",   "path": "tuthtml.png",   "coords": (463, 500),    "skill": "HTML"},
        {"tag": "prob_c",      "path": "tutc.png",      "coords": (683, 500),    "skill": "C++"}, 
        {"tag": "prob_mysql",  "path": "tutmysql.png",  "coords": (903, 500),    "skill": "MySQL"},
        {"tag": "prob_python", "path": "tutpython.png", "coords": (1123, 500),   "skill": "Python"} 
    ]

    for btn in PROBLEM_BUTTONS:
        # Link to the new folder selection frame
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
# DIALOG & PROGRESSION FUNCTIONS
# ---------------------------------------------------------
def prompt_for_name():
    if STATE.selected_gender is None:
        messagebox.showwarning("Selection Required", "Please select a gender (Male or Female) before proceeding.")
        return

    # --- CONFIGURATION FOR NAME INPUT DIALOG ---
    DIALOG_WIDTH = 350 
    DIALOG_HEIGHT = 300 
    
    # Coordinates relative to the dialog canvas
    ENTRY_Y = 175 
    BUTTON_Y = 245 
    BUTTON_DIMS = (180, 65) 
    # -------------------------------------------

    dialog = tk.Toplevel(STATE.root)
    dialog.title("Register Character Name")
    dialog.geometry(f"{DIALOG_WIDTH}x{DIALOG_HEIGHT}")
    dialog.transient(STATE.root)
    dialog.grab_set()
    
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
    canvas.dialog_button_data = {}

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

    # --- Entry Field ---
    name_entry = tk.Entry(dialog, width=25, font=("Arial", 14)) 
    canvas.create_window(DIALOG_WIDTH // 2, ENTRY_Y, window=name_entry)
    name_entry.focus_set()

    def register_and_proceed():
        play_click_sound() 
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
    Customized User Selection Dialog with userForm.png background
    and image-based buttons for Load, Delete, and Create.
    """
    # --- CONFIGURATION (ADJUST THESE TO MATCH YOUR IMAGES) ---
    DIALOG_WIDTH = 450
    DIALOG_HEIGHT = 450
    
    # Button Dimensions (Width, Height)
    BTN_W, BTN_H = (180, 65) 
    
    # Combobox configuration
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
    
    # Create Canvas for Background and Custom Buttons
    canvas = tk.Canvas(dialog, width=DIALOG_WIDTH, height=DIALOG_HEIGHT, highlightthickness=0, bg="#222222")
    canvas.pack(fill="both", expand=True)

    # --- 1. Load Background Image ---
    bg_pil = load_pil_image("userForm.png", DIALOG_WIDTH, DIALOG_HEIGHT, mode='RGB')
    bg_photo = ImageTk.PhotoImage(bg_pil)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    canvas.bg_ref = bg_photo  # Keep reference
    
    # --- Custom Pulse Logic for Dialog ---
    canvas.dialog_button_data = {}

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


    # --- Data Setup ---
    has_users = bool(user_data)
    usernames = sorted(user_data.keys())
    selected_user_var = tk.StringVar(dialog)
    if has_users:
        selected_user_var.set(usernames[0])

    # --- 2. Dropdown (Combobox) ---
    DROPDOWN_X = DIALOG_WIDTH // 2
    DROPDOWN_Y = 195 
    
    # --- Apply custom style for height ---
    style = ttk.Style()
    # Define a custom style with the larger font size
    style.configure("Custom.TCombobox", font=("Arial", COMBOBOX_FONT_SIZE))
    # ----------------------------------------

    if has_users:
        # Use the custom style to increase the height
        user_menu = ttk.Combobox(dialog, 
                                 textvariable=selected_user_var, 
                                 values=usernames, 
                                 state="readonly", 
                                 width=COMBOBOX_WIDTH,
                                 style="Custom.TCombobox" # Apply the new style
                                )
        canvas.create_window(DROPDOWN_X, DROPDOWN_Y, window=user_menu)
    else:
        # If no users, show text on canvas
        canvas.create_text(DROPDOWN_X, DROPDOWN_Y, text="No users found.", fill="red", font=("Arial", 12, "bold"))

    # --- Button Helpers ---
    def create_dialog_img_button(tag, filename, x, y, handler):
        """Helper to create a simple clickable image button on the dialog canvas."""
        # Use the new BTN_W and BTN_H
        img_pil = load_pil_image(filename, BTN_W, BTN_H, mode='RGBA')
        img_photo = ImageTk.PhotoImage(img_pil)
        
        # Create image on canvas
        item_id = canvas.create_image(x, y, image=img_photo, anchor="center", tags=tag)
        
        # Store ref
        setattr(canvas, f"{tag}_ref", img_photo)
        
        # Wrapped handler for the dialog image buttons
        def wrapped_dialog_handler(event):
            play_click_sound() # Play sound before action
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

    # --- Handlers ---
    def on_load_click(event):
        if not has_users: 
            messagebox.showwarning("No Users", "Please create a user profile first.")
            return
        username = selected_user_var.get()
        if username in user_data:
            STATE.user_name = username
            STATE.selected_gender = user_data[username]
            dialog.destroy()
            show_third_frame()
            
    def on_delete_click(event):
        if not has_users:
            messagebox.showwarning("No Users", "There are no users to delete.") 
            return
        username = selected_user_var.get()
        # Note: messagebox calls don't need the click sound played before them, 
        # as the sound will be played when the user clicks the "Delete" image button.
        confirm = messagebox.askyesno("Confirm Delete", f"Delete user '{username}'?", parent=dialog)
        if confirm:
            if delete_user_progress(username):
                dialog.destroy()
                # Refresh by calling the function again with fresh data
                STATE.user_list = fetch_all_users()
                show_user_selection_dialog(STATE.user_list)

    def on_create_click(event):
        dialog.destroy()
        show_second_frame()

    # --- 3. Place Custom Buttons ---
    
    # Load User Button (Left/Center)
    create_dialog_img_button("load_btn", "loaduser.png", x=115, y=295, handler=on_load_click)
    
    # Delete User Button (Right/Center)
    create_dialog_img_button("delete_btn", "deleteuser.png", x=335, y=295, handler=on_delete_click)
    
    # Create User Button (Bottom)
    create_dialog_img_button("create_btn", "createuser.png", x=DIALOG_WIDTH//2, y=385, handler=on_create_click)

    # Standard window close protocol
    dialog.protocol("WM_DELETE_WINDOW", dialog.destroy)
    STATE.root.wait_window(dialog)


def confirm_action(action, window_to_close):
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
        # Play sound before action that closes window
        play_click_sound() 
        if action == 'Exit':
            try:
                pygame.mixer.music.stop()
                pygame.mixer.quit() 
            except Exception as e:
                print(f"Warning: Pygame mixer quit failed: {e}")
                pass 
            if window_to_close:
                window_to_close.destroy()
            STATE.root.destroy()
        elif action == 'Sign Out':
            if window_to_close:
                window_to_close.destroy()
            STATE.root.deiconify() 
            create_main_menu()
            
def on_nav_exit_click(landscape_window):
    # Play sound when confirming navigation exit
    play_click_sound()
    confirm_action('Sign Out', landscape_window)


# ---------------------------------------------------------
# CLICK HANDLERS
# ---------------------------------------------------------
def on_access_game_click(event):
    STATE.user_list = fetch_all_users()
    show_user_selection_dialog(STATE.user_list)

def on_exit_click(event=None):
    # Play sound when confirming exit
    play_click_sound()
    confirm_action('Exit', None)

def on_gender_click(gender):
    play_click_sound() 
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
    # Move the gender check from on_enter to here to allow the pulse animation
    if STATE.selected_gender is None:
        messagebox.showwarning("Selection Required", "Please select a gender (Male or Female) before proceeding.")
        return
    prompt_for_name()

# QoL Addition: Check for assets directory before running
def check_assets_dir():
    if not os.path.isdir(ASSETS_DIR):
        messagebox.showerror(
            "Fatal Error: Assets Missing", 
            f"The required assets folder '{ASSETS_DIR}' was not found.\n\nPlease ensure this folder is in the same directory as the script."
        )
        return False
    return True

# =============================
# RUN
# =============================
if __name__ == "__main__":
    
    if not check_assets_dir():
        # Exit if assets are missing
        import sys
        sys.exit() 
        
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

    music_path = os.path.join(ASSETS_DIR, "bgmusic.mp3") 
    start_music(music_path)
    
    create_main_menu()
    root.mainloop()