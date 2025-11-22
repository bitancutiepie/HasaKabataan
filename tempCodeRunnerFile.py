import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk
import os
import pygame
import json
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

# --- TUTORIAL YOUTUBE LINKS ---
TUTORIAL_LINKS = {
    "Python": {
        1: "https://www.youtube.com/watch?v=python_link_1", 
        2: "https://www.youtube.com/watch?v=python_link_2",
        3: "https://www.youtube.com/watch?v=python_link_3",
        4: "https://www.youtube.com/watch?v=python_link_4",
        5: "https://www.youtube.com/watch?v=python_link_5"
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
        self.click_sound = None # NEW: Reference for the click sound
        self.dialog_result = None # Used for custom confirmation dialogs
        
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
    conn = get_db_connection()
    if not conn:
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
        placeholder = Image.new(mode, (width, height), color='red')
        from PIL import ImageDraw
        draw = ImageDraw.Draw(placeholder)
        draw.text((10, 10), filename, fill=(255, 255, 255))
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
            print(f"Warning: Could not play click sound: {e}")
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
    STATE.root.config(cursor="")
    data = STATE.button_data.get(tag)
    if data:
        data["hover"] = False

def create_pulsing_button(canvas, tag, filename, dims, coords, click_handler, is_active=False):
    w, h = dims
    pil_base = load_pil_image(filename, round(w), round(h), mode='RGBA') 
    photo = ImageTk.PhotoImage(pil_base)
    
    canvas.create_image(*coords, image=photo, anchor="center", tags=tag)
    
    STATE.button_data[tag] = { "base_img": pil_base, "scale": 1.0, "growing": True, 
                                "hover": False, "job": None, "current_photo": photo }
    
    setattr(canvas, f"{tag}_img_ref", photo) 
    
    if not is_active:
        canvas.tag_bind(tag, "<Enter>", lambda e: on_enter(e, tag))
        canvas.tag_bind(tag, "<Leave>", lambda e: on_leave(e, tag))
        
        # MODIFIED: Wrap the original handler to play sound first
        def wrapped_handler(event):
            play_click_sound()
            click_handler(event)
            
        canvas.tag_bind(tag, "<Button-1>", wrapped_handler)
    else:
        # For non-interactive buttons (like dashboard icons that navigate back)
        # We still want the hand cursor for visual feedback, but no pulse animation
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
        pass
    except Exception as e:
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

def on_tutorial_nav_click(event):
    if STATE.current_tutorial_skill:
        show_fourth_frame(STATE.current_tutorial_skill)
    else:
        messagebox.showwarning("Skill Selection Required", "Please click a skill button on the left side of the Dashboard (Python, Java, etc.) to view its tutorial.")

def create_nav_buttons(canvas, win):
    NAV_BAR_Y_CENTER = 730 
    NAV_BUTTONS = [
        {"tag": "homenav_btn", "path": "homenav.png", "dims": (52, 65), "coords": (371, NAV_BAR_Y_CENTER), "handler": lambda e: show_third_frame()},
        {"tag": "tutorialnav_btn", "path": "tutorialnav.png", "dims": (82, 60), "coords": (545, NAV_BAR_Y_CENTER), "handler": on_tutorial_nav_click}, 
        {"tag": "problemsnav_btn", "path": "problemsnav.png", "dims": (84, 60), "coords": (761, NAV_BAR_Y_CENTER), "handler": lambda e: show_fifth_frame()},
        {"tag": "exitnav_btn", "path": "exitnav.png", "dims": (73, 65), "coords": (961, NAV_BAR_Y_CENTER), "handler": lambda e: on_nav_exit_click(win)},
    ]
    for btn in NAV_BUTTONS:
        # Note: If is_active is True, the click handler is bound directly inside create_pulsing_button 
        # using the (play_click_sound(), click_handler(e)) tuple for simplicity and ensuring sound plays.
        create_pulsing_button(canvas, btn["tag"], btn["path"], btn["dims"], btn["coords"], btn["handler"], is_active=False)


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
    create_pulsing_button(canvas, "next_btn", "nextChar.png", NEXT_DIMS, (263, 850), on_next_char_click)
    
    STATE.gender_label = tk.Label(canvas, text="", font=("Arial", 16, "bold"), 
                                  bg="#000000", fg="white", relief="flat")
    create_volume_slider(STATE.root, is_portrait=True)


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
    return win, canvas

def show_third_frame():
    if STATE.user_name is None or STATE.selected_gender is None:
        messagebox.showwarning("Error", "Missing user data. Please complete user selection or creation.")
        create_main_menu()
        return

    STATE.db_progress_data = get_user_progress(STATE.user_name)

    def close_handler():
        # Use custom confirm action here
        STATE.dialog_result = None
        confirm_action_custom('Sign Out', STATE.landscape_window, close_on_back=True)
        
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
        # Use custom confirm action here
        STATE.dialog_result = None
        confirm_action_custom('Sign Out', STATE.landscape_window, close_on_back=True)
        
    win, canvas = create_landscape_window("Hasa Leveling - Tutorials", close_handler)
    
    tutorial_image = load_pil_image("tutorialbg.png", LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT, mode='RGB')
    tutorial_photo = ImageTk.PhotoImage(tutorial_image)
    canvas.create_image(0, 0, image=tutorial_photo, anchor="nw")
    STATE.bg_ref = tutorial_photo 
    
    if skill_name:
        skill_filename = f"tut{skill_name.lower().replace('+', '')}.png"
        # Now using create_pulsing_button for hover effect
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
        create_pulsing_button(canvas, btn["tag"], btn["path"], btn["dims"], btn["coords"], handler, is_active=False)
            
    create_nav_buttons(canvas, win)

# --- NEW FUNCTION: PROBLEM SOLVER PLACEHOLDER ---
def open_problem_solver(skill, problem_number):
    """
    Placeholder: This handles what happens when a folder is clicked.
    Example: Open a window showing 'Java Problem #1'
    """
    print(f"Opening {skill} Problem #{problem_number}...")
    messagebox.showinfo("Problem Selected", f"You opened {skill} Problem Folder #{problem_number}")
    # Later, you can add logic here to open a specific image or window.


# --- NEW FRAME: PROBLEM SELECTION ---
def show_problem_selection_frame(skill_name):
    """
    Frame 6: Problem Selection View (Folders)
    Displays the Skill Icon on the left and 5 Problem Folders on the right.
    """
    def close_handler():
        # Use custom confirm action here
        STATE.dialog_result = None
        confirm_action_custom('Sign Out', STATE.landscape_window, close_on_back=True)
    
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
        # Use custom confirm action here
        STATE.dialog_result = None
        confirm_action_custom('Sign Out', STATE.landscape_window, close_on_back=True)

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

    dialog = tk.Toplevel(STATE.root)
    dialog.title("Register Character Name")
    dialog.geometry("300x180")
    dialog.transient(STATE.root)
    dialog.grab_set()
    
    dialog_x = STATE.root.winfo_x() + (STATE.root.winfo_width() // 2) - 150
    dialog_y = STATE.root.winfo_y() + (STATE.root.winfo_height() // 2) - 90
    dialog.geometry(f'+{dialog_x}+{dialog_y}')

    # --- CUSTOM DIALOG SETUP ---
    # Since you provided a custom image for this dialog too (image_866684.png), 
    # using a simple Toplevel is inefficient. We'll use the image provided, 
    # but resize it to fit the standard prompt dialog size (300x180 is too small for the image)
    
    # Determine the size of the custom dialog based on image aspect ratio for clarity.
    CUSTOM_DIALOG_WIDTH = 450
    CUSTOM_DIALOG_HEIGHT = 300
    
    dialog.geometry(f"{CUSTOM_DIALOG_WIDTH}x{CUSTOM_DIALOG_HEIGHT}")
    dialog_x = STATE.root.winfo_x() + (STATE.root.winfo_width() // 2) - (CUSTOM_DIALOG_WIDTH // 2)
    dialog_y = STATE.root.winfo_y() + (STATE.root.winfo_height() // 2) - (CUSTOM_DIALOG_HEIGHT // 2)
    dialog.geometry(f'+{dialog_x}+{dialog_y}')

    canvas = tk.Canvas(dialog, width=CUSTOM_DIALOG_WIDTH, height=CUSTOM_DIALOG_HEIGHT, highlightthickness=0, bg="#222222")
    canvas.pack(fill="both", expand=True)

    # Load and place custom background image (image_866684.png)
    bg_pil = load_pil_image("image_866684.png", CUSTOM_DIALOG_WIDTH, CUSTOM_DIALOG_HEIGHT, mode='RGB')
    bg_photo = ImageTk.PhotoImage(bg_pil)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    canvas.bg_ref = bg_photo # Keep reference

    # Entry Box (Repositioned to the white box in the image)
    name_entry = tk.Entry(dialog, width=20, font=("Arial", 14), justify='center', bd=0, relief="flat")
    canvas.create_window(CUSTOM_DIALOG_WIDTH//2, 195, window=name_entry)
    name_entry.focus_set()

    # --- Button Handlers ---
    def register_and_proceed():
        play_click_sound()
        name = name_entry.get().strip()
        if not name:
            messagebox.showwarning("Input Required", "Please enter a name to continue.", parent=dialog)
        elif len(name) < 4:
            messagebox.showwarning("Invalid Name", "Name must be at least 4 characters long.", parent=dialog)
        elif len(name) > 9:
            messagebox.showwarning("Invalid Name", "Name cannot exceed 9 characters.", parent=dialog)
        else:
            if insert_new_user(name, STATE.selected_gender):
                STATE.user_name = name
                dialog.destroy()
                show_third_frame() 

    # Create 'CONFIRM AND REGISTER' image button
    BTN_W, BTN_H = 200, 60 # Approximate button size from image
    btn_pil = load_pil_image("confirmregister.png", BTN_W, BTN_H, mode='RGBA') # Assuming a confirmregister.png file
    btn_photo = ImageTk.PhotoImage(btn_pil)
    canvas.btn_ref = btn_photo
    
    btn_id = canvas.create_image(CUSTOM_DIALOG_WIDTH//2, 260, image=btn_photo, anchor="center", tags="register_btn")
    
    # Wrap handler for pulsing effect and sound
    create_pulsing_button(canvas, "register_btn", "confirmregister.png", (BTN_W, BTN_H), (CUSTOM_DIALOG_WIDTH//2, 260), lambda e: register_and_proceed())

    # Replace the standard tk.Button with the image button logic (already done above)
    dialog.bind('<Return>', lambda event: register_and_proceed())
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
        
        # Bindings
        if has_users or tag == "create_btn":
            canvas.tag_bind(tag, "<Button-1>", wrapped_dialog_handler)
            canvas.tag_bind(tag, "<Enter>", lambda e: dialog.config(cursor="hand2"))
            canvas.tag_bind(tag, "<Leave>", lambda e: dialog.config(cursor=""))

    # --- Handlers ---
    def on_load_click(event):
        if not has_users: return
        username = selected_user_var.get()
        if username in user_data:
            STATE.user_name = username
            STATE.selected_gender = user_data[username]
            dialog.destroy()
            show_third_frame()
            
    def on_delete_click(event):
        if not has_users: return
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

# NEW FUNCTION: Custom Confirmation Dialog
# In HasaLeveling.py, starting around line 1125:

def confirm_action_custom(action, window_to_close, close_on_back=False):
    """
    Creates a custom confirmation dialog using the image provided by the user.
    Sets STATE.dialog_result to True/False for CONFIRM/BACK.
    """
    # --- CONFIGURATION ---
    DIALOG_WIDTH = 450
    DIALOG_HEIGHT = 300
    BTN_W, BTN_H = (180, 65) 
    
    # Determine the title and background image based on action
    if action == 'Sign Out':
        dialog_title = "Confirm Sign Out"
        bg_image_file = "image_86cec4.png" # The provided image
    else: # action == 'Exit'
        dialog_title = "Confirm Exit"
        bg_image_file = "confirmexit.png" # Assuming a similar custom image for exit
        
    dialog = tk.Toplevel(STATE.root)
    dialog.title(dialog_title)
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
    bg_pil = load_pil_image(bg_image_file, DIALOG_WIDTH, DIALOG_HEIGHT, mode='RGB')
    bg_photo = ImageTk.PhotoImage(bg_pil)
    canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    canvas.bg_ref = bg_photo  # Keep reference

    # --- Button Handlers ---
    def on_confirm_click(event):
        STATE.dialog_result = True
        dialog.destroy()
        perform_action(action, window_to_close)
        
    def on_back_click(event):
        STATE.dialog_result = False
        dialog.destroy()
        # If closing the main Toplevel window (like the Dashboard), destroy it on 'Back' click too
        if close_on_back and window_to_close:
            window_to_close.destroy()
            STATE.root.deiconify()
            create_main_menu()

    # --- 2. Place Custom Buttons ---
    
    # BACK Button (Left)
    # CORRECTED: Use coords=(x, y) instead of x=..., y=...
    create_pulsing_button(canvas, "back_btn", "back.png", (BTN_W, BTN_H), coords=(115, 240), click_handler=on_back_click)
    
    # CONFIRM Button (Right)
    # CORRECTED: Use coords=(x, y) instead of x=..., y=...
    create_pulsing_button(canvas, "confirm_btn", "confirm.png", (BTN_W, BTN_H), coords=(335, 240), click_handler=on_confirm_click)

    # Handle window close (X button) as 'Back'
    dialog.protocol("WM_DELETE_WINDOW", lambda: on_back_click(None))
    
    # Block the main window until the dialog is closed
    STATE.root.wait_window(dialog)


# MODIFIED: Renamed confirm_action to perform_action, 
# this function now executes the final action based on confirmation.
def perform_action(action, window_to_close):
    # This function is now only called AFTER the user confirms in the custom dialog.
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
    # REMOVED: play_click_sound(). Sound is handled by the button's wrapper.
    # The custom dialog handles the confirmation flow now.
    confirm_action_custom('Sign Out', landscape_window)


# ---------------------------------------------------------
# CLICK HANDLERS (Updated to ensure sound is played once via the wrapper function in create_pulsing_button)
# ---------------------------------------------------------
def on_access_game_click(event):
    STATE.user_list = fetch_all_users()
    show_user_selection_dialog(STATE.user_list)

def on_exit_click(event=None):
    # REMOVED: play_click_sound(). Sound is handled by the button's wrapper.
    # The custom dialog handles the confirmation flow now.
    confirm_action_custom('Exit', None)

def on_gender_click(gender):
    # REMOVED: play_click_sound(). Sound is handled by the button's wrapper.
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

    music_path = os.path.join(ASSETS_DIR, "bgmusic.mp3") 
    start_music(music_path)
    
    create_main_menu()
    root.mainloop()