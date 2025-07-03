#--------------------------------------------------------------------------------------------------------------------------------#  

#                ANDROSOT - PSIS ROBOTEAM
 
#--------------------------------------------------------------------------------------------------------------------------------# 

import cv2
import numpy as np
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from tkinter import messagebox, ttk
import serial
import time
import serial.tools.list_ports

# Global variable for the VideoCapture object
cap = None
adjustable_delay = 0  # Default value for delay
adjustable_offset = 20  # Default value for offset
color_order = ["Red", "Blue", "Yellow"]  # Default color order
#--------------------------------------------------------------------------------------------------------------------------------#  


 
#--------------------------------------------------------------------------------------------------------------------------------# 
# Function to switch to the "Dribble & Attack" screen
def on_avoidance():
    menu_frame.pack_forget()  # Hide the menu frame
    create_avoidance_interface()  # Create the Dribble & Attack interface

# Function to switch to the "Dribble & Attack" screen
def on_goalfirst():
    menu_frame.pack_forget()  # Hide the menu frame
    create_goalfirst()  # Create the Dribble & Attack interface

# Function to switch to the "Dribble & Attack" screen
def on_keeper():
    menu_frame.pack_forget()  # Hide the menu frame
    create_keeper_interface()  # Create the Dribble & Attack interface

def on_ball_color():
    menu_frame.pack_forget()  # Hide the menu frame
    create_ball_color()  # Create the Ball Color interface
#--------------------------------------------------------------------------------------------------------------------------------#  


 
#--------------------------------------------------------------------------------------------------------------------------------# 
# Function to go back to the menu from any screen
def on_back_to_menu():
    # Hide any active frames
    if 'avoidance_frame' in globals() and avoidance_frame.winfo_ismapped():
        avoidance_frame.pack_forget()
    if 'goalfirst_frame' in globals() and goalfirst_frame.winfo_ismapped():
        goalfirst_frame.pack_forget()
    if 'keeper_frame' in globals() and keeper_frame.winfo_ismapped():
        keeper_frame.pack_forget()
    if 'ball_color_frame' in globals() and ball_color_frame.winfo_ismapped():
        ball_color_frame.pack_forget()
   # if 'freekick_frame' in globals() and freekick_frame.winfo_ismapped():
     ##   freekick_frame.pack_forget()
 #--------------------------------------------------------------------------------------------------------------------------------#  


 
#--------------------------------------------------------------------------------------------------------------------------------#        
    release_webcam()  # Release the webcam when going back to the menu
    menu_frame.pack(fill=tk.BOTH, expand=True)  # Show menu frame again

# Function to release the webcam capture
def release_webcam():
    global cap
    if cap is not None:
        cap.release()
        cap = None
#--------------------------------------------------------------------------------------------------------------------------------#  
ser = None

def initialize_serial(port, baudrate=115200):
    global ser
    try:
        ser = serial.Serial(port, baudrate, timeout=0)
        time.sleep(2)  # Allow ESP32 to initialize
        print(f"Serial port {port} initialized with baudrate {baudrate}")
    except Exception as e:
        print(f"Error initializing serial port: {e}")

def serial_send(cmd, dataH, dataL):
    global ser
    lowbyte = dataL
    highbyte = cmd
    
    try:
        if ser and ser.is_open:
            print(f"Sending Cmd: {cmd}, dataH: {dataH}, dataL: {dataL}")
            message = bytes([0xFF, 0x55, lowbyte, 255 - lowbyte, highbyte, 255 - highbyte])
            ser.write(message)
            
            # Read acknowledgment from ESP32
            response = ser.readline().decode().strip()
            if response:
                print(f"ESP32 Response: {response}")
        else:
            print("Serial port not initialized or not open.")
    except Exception as e:
        print(f"Error sending data: {e}")

def send_cmd(cmd, dataH, dataL):
    serial_send(cmd, dataH, dataL)
 #--------------------------------------------------------------------------------------------------------------------------------#  


 
#--------------------------------------------------------------------------------------------------------------------------------#  
def get_com_ports():
    """Function to fetch and return a list of available USB COM ports (Linux version)."""
    com_ports = []
    # Check for both ttyUSB* and ttyACM* devices which are common for USB serial devices
    for port in serial.tools.list_ports.comports():
        if 'USB' in port.description or 'ACM' in port.device:
            com_ports.append(port.device)
    return com_ports

def auto_search_com_ports(com_port_var):
    """Function to automatically search for USB COM ports and update the dropdown."""
    com_ports = get_com_ports()  # Get the latest list of available USB COM ports
    if com_ports:
        com_port_var.set(com_ports[0])  # Set the dropdown to the first available COM port
        # Show a success message box
        messagebox.showinfo("COM Port Found", f"COM port {com_ports[0]} found and selected.")
        # Try to connect to the selected COM port
        connect_serial(com_ports[0])
    else:
        # Show an error message box if no COM ports are found
        messagebox.showerror("No COM Port Found", "No USB COM ports were found. Please check your connections.")

def connect_serial(com_port):
    """Function to initialize the serial connection based on the selected COM port."""
    global ser
    if com_port:
        try:
            # Establish a serial connection
            ser = serial.Serial(com_port, 115200, timeout=0)
            print(f"Connected to {com_port}")
        except serial.SerialException as e:
            print(f"Error: {e}")
            messagebox.showerror("Connection Error", f"Failed to connect to {com_port}. {e}")
 
#--------------------------------------------------------------------------------------------------------------------------------# 
# ========================
# Create Main Interface
# ========================
#--------------------------------------------------------------------------------------------------------------------------------# 
def create_interface():
    global root, menu_frame

    root = tk.Tk()
    root.title("ROBOSOT - PSIS ROBOTEAM")
    root.geometry("900x680")

    

    deep_teal = "#257180"
    creamy_beige = "#F2E5BF"
    vibrant_orange = "#FD8B51"
    white = "#FFFFFF"
    black = "#000000"

    menu_frame = tk.Frame(root, bg=creamy_beige, width=800, height=400)
    menu_frame.pack(fill=tk.BOTH, expand=True)

    header_frame = tk.Frame(menu_frame, bg=white, height=70, bd=3, relief="solid")
    header_frame.pack(fill=tk.X)
    inner_header = tk.Frame(header_frame, bg=deep_teal, height=60)
    inner_header.pack(fill=tk.BOTH, padx=3, pady=3)

    header_label = tk.Label(inner_header, text="ROBOSOT NAVIGATION & MISSION CONTROL", font=("Agency FB", 27, "bold"), bg=deep_teal, fg=white)
    header_label.pack(pady=10)

    # Left Side Menu with White Outline and Full Height to the Left Side
    left_frame = tk.Frame(menu_frame, width=200, bg=deep_teal, bd=3, relief="solid", highlightbackground="white", highlightthickness=3)
    left_frame.pack(side=tk.LEFT, fill=tk.Y, pady=(0,3))  # Ensures full height below header


    # Buttons without Message Boxes
    tk.Button(left_frame, text="AVOIDANCE", height=2, width=20, 
              font=("Arial", 12, "bold"), bg=vibrant_orange, fg=black, 
              relief="solid", bd=3,  
              command=on_avoidance).pack(pady=5)

    tk.Button(left_frame, text="GOAL FIRST", height=2, width=20, 
              font=("Arial", 12, "bold"), bg=vibrant_orange, fg=black, 
              relief="solid", bd=3,  
              command=on_goalfirst).pack(pady=5)

    tk.Button(left_frame, text="KEEPER MODE", height=2, width=20, 
              font=("Arial", 12, "bold"), bg=vibrant_orange, fg=black, 
              relief="solid", bd=3,  
              command=on_keeper).pack(pady=5)
    
    tk.Button(left_frame, text="COLOR", height=2, width=20, 
              font=("Arial", 12, "bold"), bg=vibrant_orange, fg=black, 
              relief="solid", bd=3,  
              command=on_ball_color).pack(pady=5)
    


    
        # Middle Section for Bluetooth Pairing
    middle_frame = tk.Frame(menu_frame, bg=creamy_beige, width=400, height=400)
    middle_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add Resized Image
    try:
        # Load and resize the image
        image_path = r'C:\Users\psisr\Documents\ROBOSOT_NUA\logo.jpg'

  # Replace with your image path
        original_img = Image.open(image_path)
        resized_img = original_img.resize((300, 300))  # Resize to 300x300 pixels

        # Convert to PhotoImage
        img = ImageTk.PhotoImage(resized_img)

        # Create a Label to display the image
        image_label = tk.Label(middle_frame, image=img, bg=creamy_beige)
        image_label.image = img  # Keep a reference to avoid garbage collection
        image_label.pack(pady=5)  # Adjust padding as needed
    except Exception as e:
        print(f"Error loading image: {e}")

            # Box Frame for COM Ports
    box_frame = tk.Frame(middle_frame, bg=white, relief="solid", bd=2, padx=15, pady=15, highlightbackground=deep_teal, highlightthickness=2)
    box_frame.pack(pady=15, padx=10)

    # Title Label (Smaller)
    title_label = tk.Label(box_frame, text="COM Port Selector", font=("Arial", 12, "bold"), fg=deep_teal, bg=white)
    title_label.pack(pady=(0, 8))

    # Fetch available COM ports
    com_ports = get_com_ports()

    # COM Port Dropdown Label (Smaller)
    com_port_label = tk.Label(box_frame, text="Select COM Port:", font=("Arial", 10, "bold"), fg=black, bg=white)
    com_port_label.pack()

    # COM Port Dropdown (Smaller)
    com_port_var = tk.StringVar(value=com_ports[0] if com_ports else "")
    com_port_combobox = ttk.Combobox(box_frame, textvariable=com_port_var, values=com_ports, state="readonly", font=("Arial", 10), width=12)
    com_port_combobox.pack(pady=5)

    # Button Style (Compact)
    button_style = {
        "font": ("Arial", 10, "bold"),
        "fg": white,
        "bg": deep_teal,
        "relief": "flat",
        "padx": 8,
        "pady": 3,
        "bd": 3,
        "activebackground": vibrant_orange,
        "cursor": "hand2",
        "width": 20
    }

    # Auto Search Button (Smaller)
    auto_search_button = tk.Button(box_frame, text="🔍 Auto Search", command=lambda: auto_search_com_ports(com_port_var), **button_style)
    auto_search_button.pack(pady=5)

    # Send Command Button (Smaller)
    send_button = tk.Button(box_frame, text="🚀 Send Command", command=lambda: send_cmd(1, 0x12, 0x34), **button_style)
    send_button.pack(pady=5)
        





#--------------------------------------------------------------------------------------------------------------------------------#  


 
#--------------------------------------------------------------------------------------------------------------------------------# 
def on_save_dribble_attack():
    messagebox.showinfo("Save", "Settings saved successfully!")
#--------------------------------------------------------------------------------------------------------------------------------#  


 
#--------------------------------------------------------------------------------------------------------------------------------# 
def update_frame(cap, label):
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        # If frame capture fails, just skip updating the frame (no error message)
        return
    
    # Convert the frame from BGR to RGB (Tkinter uses RGB, not BGR)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the frame to an Image object
    img = Image.fromarray(frame)

    # Convert the Image object to a Tkinter PhotoImage object
    imgtk = ImageTk.PhotoImage(image=img)

    # Update the label to display the new frame
    label.imgtk = imgtk
    label.configure(image=imgtk)

    # Call the function again after 10 ms to keep updating the frame
    label.after(10, update_frame, cap, label)

def update_frame(cap, label):
    # Capture a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        # If frame capture fails, just skip updating the frame (no error message)
        return
    
    # Resize the frame to 340x240
    frame = cv2.resize(frame, (640, 480))
    
    # Convert the frame from BGR to RGB (Tkinter uses RGB, not BGR)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Convert the frame to an Image object
    img = Image.fromarray(frame)

    # Convert the Image object to a Tkinter PhotoImage object
    imgtk = ImageTk.PhotoImage(image=img)

    # Update the label to display the new frame
    label.imgtk = imgtk
    label.configure(image=imgtk)

    # Call the function again after 10 ms to keep updating the frame
    label.after(10, update_frame, cap, label)
#--------------------------------------------------------------------------------------------------------------------------------#  


 
#--------------------------------------------------------------------------------------------------------------------------------# 
import configparser
import os

goal_shape = []  # Initialize as an empty list or appropriate default value
color_ranges = {}  # Initialize as an empty dictionary
# Define configuration file paths
script_dir = os.path.dirname(os.path.abspath(__file__))
ball_config_file = os.path.join(script_dir, "ball_config.ini")
goal_config_file = os.path.join(script_dir, "goal_config.ini")
obstacle_config_file = os.path.join(script_dir, "obstacle_config.ini")

def _load_config(config_file, section):
    config = configparser.ConfigParser()
    if not os.path.exists(config_file):
        print(f"Config file not found: {config_file}")
        return None
    
    config.read(config_file)
    if not config.has_section(section):
        print(f"Section not found in config file: {section}")
        return None
    
    print(f"Loaded config for {section} from {config_file}")
    return config[section]

def load_ball_settings():
    """Load ball color settings with HSV values"""
    ball_settings = {}
    colors = ["Red Ball", "Yellow Ball", "Blue Ball"]
    for color in colors:
        config = _load_config(ball_config_file, color)
        if config:
            ball_settings[color] = {
                "Lower Hue": config.getint("Lower Hue", fallback=0),
                "Lower Saturation": config.getint("Lower Saturation", fallback=0),
                "Lower Value": config.getint("Lower Value", fallback=0),
                "Upper Hue": config.getint("Upper Hue", fallback=179),
                "Upper Saturation": config.getint("Upper Saturation", fallback=255),
                "Upper Value": config.getint("Upper Value", fallback=255)
            }
            print(f"Loaded settings for {color}: {ball_settings[color]}")
    return ball_settings

def load_goal_settings():
    """Load goal settings with shape data"""
    goal_settings = {}
    colors = ["Red Goal", "Yellow Goal", "Blue Goal"]
    for color in colors:
        config = _load_config(goal_config_file, color)
        if config:
            goal_settings[color] = {
                "Lower Hue": config.getint("Lower Hue", fallback=0),
                "Lower Saturation": config.getint("Lower Saturation", fallback=0),
                "Lower Value": config.getint("Lower Value", fallback=0),
                "Upper Hue": config.getint("Upper Hue", fallback=179),
                "Upper Saturation": config.getint("Upper Saturation", fallback=255),
                "Upper Value": config.getint("Upper Value", fallback=255),
                "Goal Shape": config.get("Goal Shape", fallback="")
            }
            print(f"Loaded settings for {color}: {goal_settings[color]}")
    return goal_settings

def load_obstacle_settings():
    """Load obstacle settings with HSV values for a single obstacle"""
    obstacle_settings = {}
    section = "Obstacle"  # Single section for obstacles
    config = _load_config(obstacle_config_file, section)
    if config:
        obstacle_settings[section] = {
            "Lower Hue": config.getint("Lower Hue", fallback=0),
            "Lower Saturation": config.getint("Lower Saturation", fallback=0),
            "Lower Value": config.getint("Lower Value", fallback=0),
            "Upper Hue": config.getint("Upper Hue", fallback=179),
            "Upper Saturation": config.getint("Upper Saturation", fallback=255),
            "Upper Value": config.getint("Upper Value", fallback=255)
        }
        print(f"Loaded settings for {section}: {obstacle_settings[section]}")
    return obstacle_settings


def set_slider_values(color_name):
    """Load and apply settings based on color category"""
    global goal_shape  # Access the global goal_shape variable

    if "Ball" in color_name:
        config_file = ball_config_file
        section = color_name  # Use the color_name as the section name
    elif "Goal" in color_name:
        config_file = goal_config_file
        section = color_name  # Use the color_name as the section name
    elif "Obstacle" in color_name:
        config_file = obstacle_config_file
        section = color_name  # Use the color_name as the section name
    else:
        print("Invalid category for loading settings")
        return

    config = _load_config(config_file, section)  # Load the specific section
    if not config:
        print(f"No settings found for {color_name}")
        return

    # Apply common HSV settings
    red_l_h.set(config.getint("Lower Hue", fallback=0))
    red_l_s.set(config.getint("Lower Saturation", fallback=0))
    red_l_v.set(config.getint("Lower Value", fallback=0))
    red_u_h.set(config.getint("Upper Hue", fallback=179))
    red_u_s.set(config.getint("Upper Saturation", fallback=255))
    red_u_v.set(config.getint("Upper Value", fallback=255))

    # Handle goal-specific settings
    if "Goal" in color_name:
        try:
            goal_shape = eval(config.get("Goal Shape", fallback="[]"))
        except:
            goal_shape = []

def calibrate_color_shape(current_color):
    """Save the current slider values to the appropriate configuration file."""
    global goal_shape  # Access the global goal_shape variable

    # Determine the configuration file and section based on the current_color
    if "Ball" in current_color:
        config_file = ball_config_file
        section = current_color  # Use the current_color as the section name
    elif "Goal" in current_color:
        config_file = goal_config_file
        section = current_color  # Use the current_color as the section name
    elif "Obstacle" in current_color:
        config_file = obstacle_config_file
        section = current_color  # Use the current_color as the section name
    else:
        print("Invalid category for saving settings")
        return

    config = configparser.ConfigParser()
    if os.path.exists(config_file):
        config.read(config_file)

    # Add or update the section for the current_color
    if not config.has_section(section):
        config.add_section(section)

    # Save HSV values
    config[section]["Lower Hue"] = str(red_l_h.get())
    config[section]["Lower Saturation"] = str(red_l_s.get())
    config[section]["Lower Value"] = str(red_l_v.get())
    config[section]["Upper Hue"] = str(red_u_h.get())
    config[section]["Upper Saturation"] = str(red_u_s.get())
    config[section]["Upper Value"] = str(red_u_v.get())

    # Save goal shape if applicable
    if "Goal" in current_color:
        config[section]["Goal Shape"] = str(goal_shape)

    # Write to the configuration file
    with open(config_file, "w") as f:
        config.write(f)

    print(f"Settings saved for {current_color} in {config_file}")


deep_teal = "#257180"
creamy_beige = "#F2E5BF"
vibrant_orange = "#FD8B51"
white = "#FFFFFF"
black = "#000000"

def create_ball_color():
    global ball_color_frame, cap, red_l_h, red_l_s, red_l_v, red_u_h, red_u_s, red_u_v
    global current_color, mask_label, result_label  # Make these global

    # Initialize current_color with a default value
    current_color = "Red Ball"

    ball_color_frame = tk.Frame(root, bg=creamy_beige)
    ball_color_frame.pack(fill=tk.BOTH, expand=True)

    back_button = tk.Button(
        ball_color_frame,
        text="Back",
        command=on_back_to_menu,
        bg=deep_teal,
        fg=white,
        font=("Anton", 12, "bold"),  # Increased font size
        padx=10,  # Added horizontal padding
        pady=5  # Added vertical padding
    )
    back_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    option_button = tk.Button(
        ball_color_frame,
        text="COLOR CALIBRATION",
        bg=deep_teal,
        fg=white,
        font=("Anton", 12, "bold"),  # Increased font size
        padx=10,  # Added horizontal padding
        pady=5  # Added vertical padding
    )
    option_button.grid(row=0, column=1, padx=10, pady=10)

    # Update this function to load and set slider values
    def load_and_set_color(color_name):
        set_slider_values(color_name)
        global current_color
        current_color = color_name  # Update current color for saving

    button_frame = tk.Frame(ball_color_frame, bg=creamy_beige)
    button_frame.grid(row=1, column=0, columnspan=3, pady=10)
    # Button setup with updated function to load saved settings
    buttons = [
        ("BALL: Red", lambda: load_and_set_color("Red Ball")),
        ("BALL: Yellow", lambda: load_and_set_color("Yellow Ball")),
        ("BALL: Blue", lambda: load_and_set_color("Blue Ball")),
        ("GOAL: Red", lambda: load_and_set_color("Red Goal")),
        ("GOAL: Yellow", lambda: load_and_set_color("Yellow Goal")),
        ("GOAL: Blue", lambda: load_and_set_color("Blue Goal")),
        ("OBSTACLE", lambda: load_and_set_color("Obstacle")),
        ("SOCCER", lambda: load_and_set_color("Soccer"))
    ]

    for i, (label, func) in enumerate(buttons):
        tk.Button(button_frame, text=label, command=func, bg=deep_teal, fg=white, font=("Anton", 10, "bold")) \
            .grid(row=0, column=i, padx=5, pady=5)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot access webcam")
        return

    mask_display_frame = tk.LabelFrame(ball_color_frame, text="Mask Display", bg=deep_teal, fg=white, width=340,
                                        height=240)
    mask_display_frame.grid(row=2, column=0, padx=10, pady=10)

    result_display_frame = tk.LabelFrame(ball_color_frame, text="Result Display", bg=deep_teal, fg=white, width=340,
                                          height=240)
    result_display_frame.grid(row=2, column=1, padx=10, pady=10)

    mask_label = tk.Label(mask_display_frame, bg=black, width=340, height=240)
    mask_label.pack(padx=5, pady=5)

    result_label = tk.Label(result_display_frame, bg=black, width=340, height=240)
    result_label.pack(padx=5, pady=5)

    slider_frame = tk.LabelFrame(ball_color_frame, text="Adjust Color Range", bg=creamy_beige, fg=black)
    slider_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10)

    red_l_h = tk.Scale(slider_frame, from_=0, to=179, label="Lower Hue", orient=tk.HORIZONTAL, bg=deep_teal,
                        fg=white)
    red_l_h.set(0)
    red_l_h.grid(row=0, column=0, padx=10, pady=5)

    red_l_s = tk.Scale(slider_frame, from_=0, to=255, label="Lower Saturation", orient=tk.HORIZONTAL, bg=deep_teal,
                        fg=white)
    red_l_s.set(0)
    red_l_s.grid(row=1, column=0, padx=10, pady=5)

    red_l_v = tk.Scale(slider_frame, from_=0, to=255, label="Lower Value", orient=tk.HORIZONTAL, bg=deep_teal,
                        fg=white)
    red_l_v.set(0)
    red_l_v.grid(row=2, column=0, padx=10, pady=5)

    red_u_h = tk.Scale(slider_frame, from_=0, to=179, label="Upper Hue", orient=tk.HORIZONTAL, bg=vibrant_orange,
                        fg=black)
    red_u_h.set(179)
    red_u_h.grid(row=0, column=1, padx=10, pady=5)

    red_u_s = tk.Scale(slider_frame, from_=0, to=255, label="Upper Saturation", orient=tk.HORIZONTAL,
                        bg=vibrant_orange, fg=black)
    red_u_s.set(255)
    red_u_s.grid(row=1, column=1, padx=10, pady=5)

    red_u_v = tk.Scale(slider_frame, from_=0, to=255, label="Upper Value", orient=tk.HORIZONTAL, bg=vibrant_orange,
                        fg=black)
    red_u_v.set(255)
    red_u_v.grid(row=2, column=1, padx=10, pady=5)

    load_ball_settings()
    load_goal_settings()
    load_obstacle_settings()

    save_button = tk.Button(
        ball_color_frame,
        text="SAVE SETTINGS",
        command=lambda: calibrate_color_shape(current_color),  # Pass current_color
        bg=deep_teal,
        fg=white,
        font=("Anton", 12, "bold"),
        padx=10,
        pady=5
    )
    save_button.grid(row=0, column=2, padx=10, pady=10)


    update_ball_color_frame(cap, mask_label, result_label)


def update_ball_color_frame(cap, mask_display, result_display):
    """
    Update the video feed with color detection (no shape detection).
    """
    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.resize(frame, (340, 240))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    l_h_r, l_s_r, l_v_r = red_l_h.get(), red_l_s.get(), red_l_v.get()
    u_h_r, u_s_r, u_v_r = red_u_h.get(), red_u_s.get(), red_u_v.get()

    lower_red = np.array([l_h_r, l_s_r, l_v_r])
    upper_red = np.array([u_h_r, u_s_r, u_v_r])
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    result_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # show original frame.

    mask_rgb = cv2.cvtColor(cv2.cvtColor(mask_red, cv2.COLOR_GRAY2BGR), cv2.COLOR_BGR2RGB)

    mask_tk = ImageTk.PhotoImage(image=Image.fromarray(mask_rgb))
    result_tk = ImageTk.PhotoImage(image=Image.fromarray(result_rgb))

    mask_display.imgtk = mask_tk
    mask_display.configure(image=mask_tk)

    result_display.imgtk = result_tk
    result_display.configure(image=result_tk)

    mask_display.after(10, update_ball_color_frame, cap, mask_display, result_display)

#--------------------------------------------------------------------------------------------------------------------------------#  
start_avoidance_active = False  # Initialize to False
start_goalfirst_active = False
start_keeper_active = False
history_size = 5  # Number of previous values to average for smoothing

# Assume these are calibrated values:
# Constants
CAMERA_FOV = 60  # Camera's horizontal field of view in degrees
#REAL_GOAL_WIDTH = 0.5  # Real-world width of the goal in meters (adjust as needed)


REAL_BALL_DIAMETER = 0.1  # meters (e.g., a standard soccer ball)
REAL_GOAL_WIDTH = 1.0       # meters (measure actual goal width)
AVOIDANCE_DISTANCE = 0.3   # meters (stop this far from the ball)
GOAL_APPROACH_DISTANCE = 0.9  # meters (stop this far from the goal)
grabbing_state = None
grabbing_start_time = None
ball_search_state = "BEGIN_SEARCH"  # or any other valid state
REAL_OBSTACLE_WIDTH = 0.2  # Example: if real obstacle width is 20 cm (adjust to your case!)
   
# Safe default values
obstacle_center_x = None
obstacle_distance = None

# State variables
obstacle_state = None
state_start_time = None
APPROACH_DISTANCE = 1.0 # Distance at which obstacle avoidance is triggered
AVOIDANCE_TURN_DURATION = 2.0  # How long to keep turning/avoiding
AVOIDANCE_FORWARD_DURATION = 1.0  # How long to move forward after turn

WAIT_AFTER_STOP_DURATION = 1.0
FORWARD_AFTER_STOP_DURATION = 3.0
WAIT_AFTER_GRAB_DURATION = 1.5


 # pixels (goal centering tolerance)
 # Add to your global constants
#--------------------------------------------------------------------------------------------------------------------------------# 
def create_avoidance_interface():
    global avoidance_frame, cap, color_ranges, yaw_value_label
    global CAMERA_FOV, REAL_BALL_DIAMETER, REAL_GOAL_WIDTH, AVOIDANCE_DISTANCE, GOAL_APPROACH_DISTANCE
    global PID_KP, PID_KI, PID_KD
    global YAW_TOLERANCE, MIN_TURN_SPEED, MAX_TURN_SPEED
    global BALL_YAW_TOLERANCE, CENTER_THRESHOLD, BASE_TURN_SPEED, FORWARD_SPEED, FORWARD_DURATION
    global GOAL_YAW_TOLERANCE, GOAL_CENTER_THRESHOLD, GOAL_BASE_TURN_SPEED, GOAL_FORWARD_SPEED, GOAL_FORWARD_DURATION




    cap = None

    ball_settings = load_ball_settings()
    goal_settings = load_goal_settings()
    obstacle_settings = load_obstacle_settings()

    color_ranges = {}
    for color, settings in ball_settings.items():
        color_ranges[color] = (
            (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"]),
            (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])
        )
    for color, settings in goal_settings.items():
        color_ranges[color] = (
            (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"]),
            (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])
        )

    print(f"Color ranges: {color_ranges}")

    # Add obstacle settings to color_ranges
    for color, settings in obstacle_settings.items():
        color_ranges[color] = (
            (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"]),
            (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])
        )

    print(f"Color ranges: {color_ranges}")


    avoidance_frame = tk.Frame(root, bg=creamy_beige, width=900, height=600)
    avoidance_frame.pack(fill=tk.BOTH, expand=True)

    video_display = tk.Label(avoidance_frame, bg="black", width=640, height=480)
    video_display.place(x=20, y=50)

    back_button = tk.Button(
        avoidance_frame, text="Back", command=on_back_to_menu, 
        bg=deep_teal, fg=white, font=("Anton", 12, "bold"), padx=10, pady=5
    )
    back_button.place(x=20, y=7)

    def reset_sequence():
        global start_avoidance_active, color_order
        start_avoidance_active = False
        color_order = []
        serial_send(1, 0, 0)
        print("System reset. Sending cmd: (4, 0, 0)")
        messagebox.showinfo("System Reset", "The system has been reset. Avoidance mode is stopped.")

    reset_button = tk.Button(
        avoidance_frame, text="Reset", command=reset_sequence,
        bg=deep_teal, fg=white, font=("Anton", 12, "bold"), padx=10, pady=5
    )
    reset_button.place(x=340, y=7)

    def start_avoidance():
        global start_avoidance_active
        start_avoidance_active = True
        print("START AVOIDANCE mode activated.")

    option1_button = tk.Button(
        avoidance_frame, text="START AVOIDANCE", command=start_avoidance,
        bg=vibrant_orange, fg=black, font=("Anton", 12, "bold"), padx=10, pady=5
    )
    option1_button.place(x=120, y=7)



    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "avoidance_config.ini")

    def load_avoidance_config():
        config = configparser.ConfigParser()
        if os.path.exists(config_file):
            config.read(config_file)
            if 'AvoidanceSettings' in config:
                return config['AvoidanceSettings']
        return None

    def save_avoidance_config():
        config = configparser.ConfigParser()
        if os.path.exists(config_file):
            config.read(config_file)
        if not config.has_section('AvoidanceSettings'):
            config.add_section('AvoidanceSettings')

        config['AvoidanceSettings']['CAMERA_FOV'] = str(fov_input.get())
        config['AvoidanceSettings']['REAL_BALL_DIAMETER'] = str(ball_dia_input.get())
        config['AvoidanceSettings']['REAL_GOAL_WIDTH'] = str(goal_width_input.get())
        config['AvoidanceSettings']['AVOIDANCE_DISTANCE'] = str(avoid_dist_input.get())
        config['AvoidanceSettings']['GOAL_APPROACH_DISTANCE'] = str(goal_approach_input.get())
        config['AvoidanceSettings']['PID_KP'] = str(pid_kp_input.get())
        config['AvoidanceSettings']['PID_KI'] = str(pid_ki_input.get())
        config['AvoidanceSettings']['PID_KD'] = str(pid_kd_input.get())
        config['AvoidanceSettings']['YAW_TOLERANCE'] = str(yaw_tol_input.get())
        config['AvoidanceSettings']['MIN_TURN_SPEED'] = str(min_turn_input.get())
        config['AvoidanceSettings']['MAX_TURN_SPEED'] = str(max_turn_input.get())
        config['AvoidanceSettings']['BALL_YAW_TOLERANCE'] = str(ball_yaw_tol_input.get())
        config['AvoidanceSettings']['CENTER_THRESHOLD'] = str(center_thresh_input.get())
        config['AvoidanceSettings']['BASE_TURN_SPEED'] = str(base_turn_input.get())
        config['AvoidanceSettings']['FORWARD_SPEED'] = str(forward_speed_input.get())
        config['AvoidanceSettings']['FORWARD_DURATION'] = str(forward_duration_input.get())
        config['AvoidanceSettings']['GOAL_YAW_TOLERANCE'] = str(goal_yaw_tol_input.get())
        config['AvoidanceSettings']['GOAL_CENTER_THRESHOLD'] = str(goal_center_thresh_input.get())
        config['AvoidanceSettings']['GOAL_BASE_TURN_SPEED'] = str(goal_base_turn_input.get())
        config['AvoidanceSettings']['GOAL_FORWARD_SPEED'] = str(goal_forward_speed_input.get())
        config['AvoidanceSettings']['GOAL_FORWARD_DURATION'] = str(goal_forward_duration_input.get())




        with open(config_file, 'w') as f:
            config.write(f)

        messagebox.showinfo("Success", "Configuration saved successfully!")

    config = load_avoidance_config()
    if config:
        CAMERA_FOV = config.getfloat('CAMERA_FOV', fallback=60)
        REAL_BALL_DIAMETER = config.getfloat('REAL_BALL_DIAMETER', fallback=0.1)
        REAL_GOAL_WIDTH = config.getfloat('REAL_GOAL_WIDTH', fallback=1.0)
        AVOIDANCE_DISTANCE = config.getfloat('AVOIDANCE_DISTANCE', fallback=0.3)
        GOAL_APPROACH_DISTANCE = config.getfloat('GOAL_APPROACH_DISTANCE', fallback=0.9)
        PID_KP = config.getfloat('PID_KP', fallback=1.0)
        PID_KI = config.getfloat('PID_KI', fallback=0.0)
        PID_KD = config.getfloat('PID_KD', fallback=0.1)
        YAW_TOLERANCE = config.getfloat('YAW_TOLERANCE', fallback=15.0)
        MIN_TURN_SPEED = config.getint('MIN_TURN_SPEED', fallback=20)
        MAX_TURN_SPEED = config.getint('MAX_TURN_SPEED', fallback=20)
        BALL_YAW_TOLERANCE = config.getfloat('BALL_YAW_TOLERANCE', fallback=15.0)
        CENTER_THRESHOLD = config.getint('CENTER_THRESHOLD', fallback=30)
        BASE_TURN_SPEED = config.getint('BASE_TURN_SPEED', fallback=20)
        FORWARD_SPEED = config.getint('FORWARD_SPEED', fallback=30)
        FORWARD_DURATION = config.getfloat('FORWARD_DURATION', fallback=5.0)
        GOAL_YAW_TOLERANCE = config.getfloat('GOAL_YAW_TOLERANCE', fallback=10.0)
        GOAL_CENTER_THRESHOLD = config.getint('GOAL_CENTER_THRESHOLD', fallback=30)
        GOAL_BASE_TURN_SPEED = config.getint('GOAL_BASE_TURN_SPEED', fallback=15)
        GOAL_FORWARD_SPEED = config.getint('GOAL_FORWARD_SPEED', fallback=30)
        GOAL_FORWARD_DURATION = config.getfloat('GOAL_FORWARD_DURATION', fallback=5.0)
    else:
        CAMERA_FOV = 60
        REAL_BALL_DIAMETER = 0.1
        REAL_GOAL_WIDTH = 1.0
        AVOIDANCE_DISTANCE = 0.3
        GOAL_APPROACH_DISTANCE = 0.9
        PID_KP = 1.0
        PID_KI = 0.0
        PID_KD = 0.1
        YAW_TOLERANCE = 15.0
        MIN_TURN_SPEED = 20
        MAX_TURN_SPEED = 20
        BALL_YAW_TOLERANCE = 15.0
        CENTER_THRESHOLD = 30
        BASE_TURN_SPEED = 20
        FORWARD_SPEED = 30
        FORWARD_DURATION = 5.0
        GOAL_YAW_TOLERANCE = 10.0
        GOAL_CENTER_THRESHOLD = 30
        GOAL_BASE_TURN_SPEED = 15
        GOAL_FORWARD_SPEED = 30
        GOAL_FORWARD_DURATION = 5.0

    config_title_bar = tk.Frame(
        avoidance_frame, bg=deep_teal, width=227, height=42,
        highlightbackground="black", highlightthickness=2
    )
    config_title_bar.place(x=668, y=50)

    config_title = tk.Label(
        config_title_bar, text="⚙️ Configuration",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    config_title.place(relx=0.5, rely=0.5, anchor="center")

    config_frame = tk.Frame(
        avoidance_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    config_frame.place(x=668, y=90, width=227, height=160)

    pid_frame = tk.Frame(
        avoidance_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    pid_frame.place(x=20, y=583, width=210, height=93)

    # Title for PID section
    pid_title_bar = tk.Frame(
        avoidance_frame, bg=deep_teal, width=210, height=42,
        highlightbackground="black", highlightthickness=2
    )
    pid_title_bar.place(x=20, y=543)

    pid_title = tk.Label(
        pid_title_bar, text="⚙️ Allignment",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    pid_title.place(relx=0.5, rely=0.5, anchor="center")

    # Frame for Yaw Control
    yaw_title_bar = tk.Frame(
        avoidance_frame, bg=deep_teal, width=210, height=42,
        highlightbackground="black", highlightthickness=2
    )
    yaw_title_bar.place(x=240, y=543)

    yaw_title = tk.Label(
        yaw_title_bar, text="↩️ Turn Control",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    yaw_title.place(relx=0.5, rely=0.5, anchor="center")

    yaw_frame = tk.Frame(
        avoidance_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    yaw_frame.place(x=240, y=583, width=210, height=93)

        # Ball Settings Frame
    ball_title_bar = tk.Frame(
        avoidance_frame, bg=deep_teal, width=227, height=42,
        highlightbackground="black", highlightthickness=2
    )
    ball_title_bar.place(x=668, y=274)

    ball_title = tk.Label(
        ball_title_bar, text="⚽ Ball Behavior",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    ball_title.place(relx=0.5, rely=0.5, anchor="center")

    ball_frame = tk.Frame(
        avoidance_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    ball_frame.place(x=668, y=314, width=227, height=150)

    # Goal Settings Frame
    goal_title_bar = tk.Frame(
        avoidance_frame, bg=deep_teal, width=227, height=42,
        highlightbackground="black", highlightthickness=2
    )
    goal_title_bar.place(x=668, y=487)

    goal_title = tk.Label(
        goal_title_bar, text="🥅 Goal Behavior",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    goal_title.place(relx=0.5, rely=0.5, anchor="center")

    goal_frame = tk.Frame(
        avoidance_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    goal_frame.place(x=668, y=527, width=227, height=150)







    def create_compact_entry(parent, row, emoji, label_text, default_val):
        tk.Label(parent, text=emoji, bg="white", font=("Segoe UI Emoji", 9)).grid(row=row, column=0, sticky="w", padx=4)
        tk.Label(parent, text=label_text, bg="white", fg="#444", font=("Segoe UI", 12), anchor="w").grid(row=row, column=1, sticky="w", padx=2)
        entry = tk.Entry(parent, font=("Segoe UI", 12), width=8, bd=1, relief="solid", bg="#f1f1f1", justify="center")
        entry.grid(row=row, column=2, padx=(5, 2), pady=2)
        entry.insert(0, str(default_val))
        return entry

    # Create all input fields including PID
    fov_input = create_compact_entry(config_frame, 0, "📷", "FOV", CAMERA_FOV)
    ball_dia_input = create_compact_entry(config_frame, 1, "⚽", "Ball Ø", REAL_BALL_DIAMETER)
    goal_width_input = create_compact_entry(config_frame, 2, "🥅", "Goal Width", REAL_GOAL_WIDTH)
    avoid_dist_input = create_compact_entry(config_frame, 3, "🎯", "To Ball, m", AVOIDANCE_DISTANCE)
    goal_approach_input = create_compact_entry(config_frame, 4, "🎯", "To Goal, m", GOAL_APPROACH_DISTANCE)

    # Create PID input fields in their own box
    pid_kp_input = create_compact_entry(pid_frame, 1, "⚙️", "Kp", PID_KP) 
    pid_ki_input = create_compact_entry(pid_frame, 2, "⚙️", "Ki", PID_KI)
    pid_kd_input = create_compact_entry(pid_frame, 3, "⚙️", "Kd", PID_KD)

    # Input fields for yaw control
    yaw_tol_input = create_compact_entry(yaw_frame, 0, "📐", "Yaw Tol.", YAW_TOLERANCE)
    min_turn_input = create_compact_entry(yaw_frame, 1, "🔄", "Min Turn", MIN_TURN_SPEED)
    max_turn_input = create_compact_entry(yaw_frame, 2, "🔁", "Max Turn", MAX_TURN_SPEED)

    # Ball settings input fields
    ball_yaw_tol_input = create_compact_entry(ball_frame, 0, "📐", "Yaw Tol.", BALL_YAW_TOLERANCE)
    center_thresh_input = create_compact_entry(ball_frame, 1, "🎯", "Center Thresh", CENTER_THRESHOLD)
    base_turn_input = create_compact_entry(ball_frame, 2, "🔄", "Turn Speed", BASE_TURN_SPEED)
    forward_speed_input = create_compact_entry(ball_frame, 3, "➡️", "Fwd Speed", FORWARD_SPEED)
    forward_duration_input = create_compact_entry(ball_frame, 4, "⏱️", "Fwd Duration", FORWARD_DURATION)

        # Goal settings input fields
    goal_yaw_tol_input = create_compact_entry(goal_frame, 0, "📐", "Yaw Tol.", GOAL_YAW_TOLERANCE)
    goal_center_thresh_input = create_compact_entry(goal_frame, 1, "🎯", "Center Thresh", GOAL_CENTER_THRESHOLD)
    goal_base_turn_input = create_compact_entry(goal_frame, 2, "🔄", "Turn Speed", GOAL_BASE_TURN_SPEED)
    goal_forward_speed_input = create_compact_entry(goal_frame, 3, "➡️", "Fwd Speed", GOAL_FORWARD_SPEED)
    goal_forward_duration_input = create_compact_entry(goal_frame, 4, "⏱️", "Fwd Duration", GOAL_FORWARD_DURATION)

    save_button = tk.Button(
    avoidance_frame, text="💾 Save", command=save_avoidance_config,
    bg=deep_teal, fg=white, font=("Anton", 12, "bold"), padx=10, pady=5
    )
    save_button.place(x=450, y=7)


    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot access webcam")
        return






    def update_frame():
        global cap, start_avoidance_active, ser
        global previous_yaw, current_yaw, centered_on_ball, centering_start_time
        global centered_on_goal, goal_centering_start_time, ball_sequence_completed, goal_sequence_completed
        global return_to_zero_active, target_yaw
        global goal_search_state, goal_search_start_time, last_rotation_direction
    
        # Add these initialization if they don't exist
        if 'return_to_zero_active' not in globals():
            return_to_zero_active = False
        if 'target_yaw' not in globals():
            target_yaw = 0.0  # Target is 0 degrees
        
        # Initialize variables if they don't exist
        if 'current_yaw' not in globals():
            current_yaw = "N/A"
        if 'centered_on_ball' not in globals():
            centered_on_ball = False
        if 'centering_start_time' not in globals():
            centering_start_time = None
        if 'centered_on_goal' not in globals():
            centered_on_goal = False
        if 'goal_centering_start_time' not in globals():
            goal_centering_start_time = None
        if 'ball_sequence_completed' not in globals():
            ball_sequence_completed = False
        if 'goal_sequence_completed' not in globals():
            goal_sequence_completed = False





        # Improved serial reading
        if ser and ser.in_waiting:
            try:
                # Read all available lines
                while ser.in_waiting:
                    line = ser.readline().decode('utf-8').strip()
                    if line.startswith("Yaw:"):
                        try:
                            # Extract just the numeric value
                            yaw_value = float(line.split(':')[1].split()[0])
                            current_yaw = f"{yaw_value:.2f}"
                        except (IndexError, ValueError):
                            pass  # Skip if parsing fails
            except UnicodeDecodeError:
                # Clear buffer if we get garbled data
                ser.reset_input_buffer()
            except Exception as e:
                print(f"Serial error: {str(e)}")

        if cap is None or not cap.isOpened():
            return

        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture frame from webcam")
            return

        # Display yaw value on the video frame
        yaw_text = f"Yaw: {current_yaw}"
        cv2.putText(frame, yaw_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Convert the frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        detected_balls = []  # List to store all detected balls
        closest_ball = None  # Track the closest ball (largest area)
        max_area = 0  # Track the maximum area of detected balls
        detected_goals = []  # List to store all detected goals
        closest_goal = None  # Track the closest goal (largest area)
        max_goal_area = 0  # Track the maximum area of detected goals
        detected_obstacles = []  # List to store all detected obstacles
        closest_obstacle = None
        max_obstacle_area = 0

        # Calculate focal length at the beginning
        IMAGE_WIDTH = frame.shape[1]  # Ensure IMAGE_WIDTH is set
        focal_length = (IMAGE_WIDTH / 2) / np.tan(np.radians(CAMERA_FOV / 2))

        # --- Ball Detection ---
        for color_name, settings in ball_settings.items():
            # Extract HSV values from settings
            lower = (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"])
            upper = (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])

            # Create a mask for the current ball color
            mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))

            # Apply morphological operations to clean up the mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Remove small noise
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Fill small holes

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Process the largest contour
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                contour_area = cv2.contourArea(largest_contour)

                # Skip small contours (noise)
                if contour_area < 500:  # Adjust this threshold as needed
                    continue

                # Calculate circularity
                perimeter = cv2.arcLength(largest_contour, True)
                circularity = 4 * np.pi * (contour_area / (perimeter ** 2)) if perimeter > 0 else 0

                # Classify as ball if circularity is high
                if circularity > 0.4:  # Ball (high circularity)
                    # Store the detected ball
                    detected_balls.append({
                        "color": color_name,
                        "contour": largest_contour,
                        "area": contour_area,
                        "circularity": circularity
                    })

                    # Track the closest ball (largest area)
                    if contour_area > max_area:
                        max_area = contour_area
                        closest_ball = {
                            "color": color_name,
                            "contour": largest_contour,
                            "area": contour_area,
                            "circularity": circularity
                        }



        # --- Goal Detection ---
        for color_name, settings in goal_settings.items():
            # Extract HSV values from settings
            lower = (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"])
            upper = (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])

            # Create a mask for the current goal color
            mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))

            # Apply morphological operations to clean up the mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Remove small noise
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Fill small holes

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Process the largest contour
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                contour_area = cv2.contourArea(largest_contour)

                # Skip small contours (noise)
                if contour_area < 1000:  # Adjust this threshold as needed
                    continue

                # Calculate aspect ratio
                x, y, w, h = cv2.boundingRect(largest_contour)
                aspect_ratio = float(w) / h

                # Classify as goal if aspect ratio is high or low
                if aspect_ratio > 1.5 or aspect_ratio < 0.7:  # Goal (high or low aspect ratio)
                    # Store the detected goal
                    detected_goals.append({
                        "color": color_name,
                        "contour": largest_contour,
                        "area": contour_area,
                        "aspect_ratio": aspect_ratio,
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h
                    })

                    # Track the closest goal (largest area)
                    if contour_area > max_goal_area:
                        max_goal_area = contour_area
                        closest_goal = {
                            "color": color_name,
                            "contour": largest_contour,
                            "area": contour_area,
                            "aspect_ratio": aspect_ratio,
                            "x": x,
                            "y": y,
                            "w": w,
                            "h": h
                        }
        # --- Obstacle Detection ---               
        for color_name, settings in obstacle_settings.items():
            # Extract HSV values from settings
            lower = (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"])
            upper = (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])

            # Create a mask for the current obstacle color
            mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))

            # Apply morphological operations
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                contour_area = cv2.contourArea(largest_contour)

                if contour_area < 800:  # You can adjust this threshold
                    continue

                # Bounding rectangle for display
                x, y, w, h = cv2.boundingRect(largest_contour)

                detected_obstacles.append({
                    "color": color_name,
                    "contour": largest_contour,
                    "area": contour_area,
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h
                })

                if contour_area > max_obstacle_area:
                    max_obstacle_area = contour_area
                    closest_obstacle = {
                        "color": color_name,
                        "contour": largest_contour,
                        "area": contour_area,
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h
                    }


        # --- Draw All Detected Balls ---
        for ball in detected_balls:
            (x, y), radius = cv2.minEnclosingCircle(ball["contour"])
            center = (int(x), int(y))
            radius = int(radius)

            # Use red circle for the closest ball, green for others
            if ball == closest_ball:
                circle_color = (0, 0, 255)  # Red for closest ball
                label = f"{ball['color']}(Closest)"
            else:
                circle_color = (0, 255, 0)  # Green for other balls
                label = f"{ball['color']}"

            # Draw the circle
            cv2.circle(frame, center, radius, circle_color, 3)

            # Add text label for the ball
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
            text_x = int(center[0] - text_size[0] / 2)
            text_y = int(center[1] - radius - 10)  # Position text above the circle
            cv2.putText(frame, label, (text_x, text_y), font, font_scale, circle_color, font_thickness)

        # --- Draw All Detected Goals ---
        for goal in detected_goals:
            # Draw a trapezoidal frame for the goal
            epsilon = 0.01 * cv2.arcLength(goal["contour"], True)
            approx = cv2.approxPolyDP(goal["contour"], epsilon, True)
            
            # Use blue for the closest goal, cyan for others
            if goal == closest_goal:
                goal_color = (255, 0, 0)  # Blue for closest goal
                label = f"{goal['color']}(Closest)"
            else:
                goal_color = (255, 255, 0)  # Cyan for other goals
                label = f"{goal['color']}"
                
            cv2.drawContours(frame, [approx], -1, goal_color, 3)

            # Add text label for the goal
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
            text_x = int(goal['x'] + goal['w'] / 2 - text_size[0] / 2)
            text_y = int(goal['y'] - 10)  # Position text above the polygon
            cv2.putText(frame, label, (text_x, text_y), font, font_scale, goal_color, font_thickness)

        # --- Draw All Detected Obstacles ---
        for obstacle in detected_obstacles:
            x, y, w, h = obstacle["x"], obstacle["y"], obstacle["w"], obstacle["h"]

            if obstacle == closest_obstacle:
                rect_color = (0, 0, 255)  # Red for closest obstacle
                label = f"{obstacle['color']}(Closest)"
            else:
                rect_color = (0, 165, 255)  # Orange for other obstacles
                label = f"{obstacle['color']}"

            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), rect_color, 3)

            # Add label
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
            text_x = int(x + w / 2 - text_size[0] / 2)
            text_y = y - 10
            cv2.putText(frame, label, (text_x, text_y), font, font_scale, rect_color, font_thickness)


        # --- Calculate Distance to Closest Ball ---
        if closest_ball:
            (x, y), radius = cv2.minEnclosingCircle(closest_ball["contour"])
            ball_diameter_pixels = 2 * radius  # Diameter of the ball in pixels
            ball_center_x = x  # Store the x-coordinate of the ball center

            # Calculate distance to the ball
            ball_distance = (REAL_BALL_DIAMETER * focal_length) / ball_diameter_pixels

            # Display the distance on the ball
            distance_text = f"{ball_distance:.2f} m"
            cv2.putText(frame, distance_text, (int(x), int(y) + int(radius) + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            radius = 0  # Default value to prevent UnboundLocalError
            ball_center_x = None

        # --- Calculate Distance to Closest Goal ---
        if closest_goal:
            goal_width_pixels = closest_goal['w']  # Width of the goal in pixels
            goal_distance = (REAL_GOAL_WIDTH * focal_length) / goal_width_pixels
            goal_center_x = closest_goal['x'] + closest_goal['w'] / 2  # Store the x-coordinate of the goal center

            # Display the distance on the goal
            distance_text = f"{goal_distance:.2f} m"
            cv2.putText(frame, distance_text, 
                    (int(closest_goal['x']), int(closest_goal['y'] + closest_goal['h'] + 20)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            goal_center_x = None

        # --- Calculate Distance to Closest Obstacle ---
        if closest_obstacle:
            obstacle_width_pixels = closest_obstacle['w']  # Width of the obstacle in pixels
            obstacle_distance = (REAL_OBSTACLE_WIDTH * focal_length) / obstacle_width_pixels
            obstacle_center_x = closest_obstacle['x'] + closest_obstacle['w'] / 2  # x-coordinate of obstacle center

            # Display the distance on the obstacle
            distance_text = f"{obstacle_distance:.2f} m"
            cv2.putText(frame, distance_text,
                        (int(closest_obstacle['x']), int(closest_obstacle['y'] + closest_obstacle['h'] + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            obstacle_center_x = None


        # --- Draw Lines from Robot to Ball and Goal ---
        # Set the robot's position to the bottom center of the frame
        robot_position = (frame.shape[1] // 2, frame.shape[0] - 10)  # Bottom center (x, y)

        # Draw line to the closest ball
        if closest_ball:
            (x, y), _ = cv2.minEnclosingCircle(closest_ball["contour"])
            ball_center = (int(x), int(y))
            cv2.line(frame, robot_position, ball_center, (0, 255, 0), 2)  # Green line to ball

        # Draw line to the closest goal
        if closest_goal:
            goal_center = (int(closest_goal['x'] + closest_goal['w'] / 2), 
                        int(closest_goal['y'] + closest_goal['h'] / 2))
            cv2.line(frame, robot_position, goal_center, (255, 0, 0), 2)  # Blue line to goal

        # Draw line to the closest obstacle
        if closest_obstacle:
            obstacle_center = (int(closest_obstacle['x'] + closest_obstacle['w'] / 2), 
                            int(closest_obstacle['y'] + closest_obstacle['h'] / 2))
            cv2.line(frame, robot_position, obstacle_center, (0, 0, 255), 2)  # Red line to obstacle


        def handle_ball_sequence(closest_ball, frame, focal_length):
            global centered_on_ball, centering_start_time, ball_sequence_completed
            global ball_search_state, ball_search_target_yaw, ball_search_start_time, current_yaw
            global return_to_zero_active, awaiting_zero_alignment_after_ball, target_yaw
            global grabbing_state, grabbing_start_time
            global YAW_TOLERANCE, CENTER_THRESHOLD, BASE_TURN_SPEED, FORWARD_DURATION, FORWARD_SPEED
            global avoiding_obstacle, obstacle_avoidance_start_time
            global obstacle_distance  # ✅ Now declared globally

            # Init flags if not already present
            if 'grabbing_state' not in globals():
                grabbing_state = None
                grabbing_start_time = None
            if 'avoiding_obstacle' not in globals():
                avoiding_obstacle = False
                obstacle_avoidance_start_time = None

            # Yaw parsing
            try:
                current_yaw_value = float(current_yaw) if str(current_yaw) != "N/A" else 0.0
            except (ValueError, TypeError):
                current_yaw_value = 0.0
                print("Warning: Invalid yaw value, defaulting to 0.0")

            def get_yaw_diff(target, current):
                return (target - current + 180) % 360 - 180

            status_text = "Ball Sequence Active"
            debug_text = ""

            # ----------------- GRABBING SEQUENCE ------------------
            if grabbing_state is not None:
                now = time.time()

                if grabbing_state == "PREPARE_STOP":
                    serial_send(1, 0, 0)
                    grabbing_start_time = now
                    grabbing_state = "WAIT_AFTER_STOP"

                elif grabbing_state == "WAIT_AFTER_STOP":
                    if now - grabbing_start_time >= WAIT_AFTER_STOP_DURATION:
                        serial_send(2, 0, FORWARD_SPEED)
                        grabbing_start_time = now
                        grabbing_state = "FORWARD_AFTER_STOP"

                elif grabbing_state == "FORWARD_AFTER_STOP":
                    if now - grabbing_start_time >= FORWARD_AFTER_STOP_DURATION:
                        serial_send(17, 0, 0)  # Grab
                        grabbing_start_time = now
                        grabbing_state = "WAIT_AFTER_GRAB"

                elif grabbing_state == "WAIT_AFTER_GRAB":
                    if now - grabbing_start_time >= WAIT_AFTER_GRAB_DURATION:
                        centered_on_ball = False
                        centering_start_time = None
                        ball_sequence_completed = True

                        try:
                            current_yaw_float = float(current_yaw) if current_yaw != "N/A" else 0.0
                            print(f"Reached Ball. Yaw: {current_yaw_float:.2f}, preparing to return to 0°.")
                        except ValueError:
                            print("Yaw parsing error")

                        serial_send(16, 0, 50)  # Your new custom action instead of returning to 0 degrees

                        grabbing_state = None

                status_text = "Grabbing Ball..."
                debug_text = ""


            # ----------------- SEARCHING / OBSTACLE AVOIDANCE ------------------
            elif not closest_ball:
                print(f"[DEBUG] closest_ball: {closest_ball}, closest_obstacle: {closest_obstacle}, avoiding_obstacle: {avoiding_obstacle}")

                # Compute obstacle distance if closest_obstacle is present
                if closest_obstacle:
                    try:
                        obstacle_width_pixels = closest_obstacle['w']
                        obstacle_distance = (REAL_OBSTACLE_WIDTH * focal_length) / obstacle_width_pixels
                        print(f"[DEBUG] Calculated obstacle_distance: {obstacle_distance:.2f}")
                    except Exception as e:
                        print(f"[ERROR] Failed to compute obstacle_distance: {e}")
                        obstacle_distance = None
                else:
                    obstacle_distance = None
                    print("[DEBUG] No closest_obstacle found, setting obstacle_distance to None")

                # Check for obstacle and start avoidance
                if closest_obstacle and not avoiding_obstacle:
                    print(f"[DEBUG] Checking obstacle condition: distance = {obstacle_distance}, threshold = {APPROACH_DISTANCE}")
                    if obstacle_distance is not None and obstacle_distance <= APPROACH_DISTANCE:
                        status_text = "Obstacle Detected - Starting Avoidance"
                        print(f"[DEBUG] {status_text}")

                        try:
                            obstacle_x = closest_obstacle['x']
                            frame_center_x = frame.shape[1] / 2

                            if obstacle_x > frame_center_x:
                                serial_send(14, 0, FORWARD_SPEED)  # Diagonal left
                                status_text += " (Right Side) → Diagonal Left"
                            else:
                                serial_send(15, 0, FORWARD_SPEED)  # Diagonal right
                                status_text += " (Left Side) → Diagonal Right"
                            print(f"[DEBUG] Obstacle X: {obstacle_x}, Frame Center: {frame_center_x}")
                        except Exception as e:
                            print(f"[ERROR] Obstacle direction error: {e}")
                            serial_send(15, 0, FORWARD_SPEED)

                        obstacle_avoidance_start_time = time.time()
                        avoiding_obstacle = True
                        return

                # Handle obstacle avoidance state
                if avoiding_obstacle:
                    elapsed = time.time() - obstacle_avoidance_start_time

                    if elapsed < AVOIDANCE_TURN_DURATION:
                        status_text = f"Avoiding Obstacle: {AVOIDANCE_TURN_DURATION - elapsed:.1f}s remaining"
                        print(f"[DEBUG] {status_text}")
                        return
                    elif elapsed < AVOIDANCE_TURN_DURATION + AVOIDANCE_FORWARD_DURATION:
                        status_text = f"Clearing Forward: {(AVOIDANCE_TURN_DURATION + AVOIDANCE_FORWARD_DURATION) - elapsed:.1f}s remaining"
                        serial_send(2, 0, FORWARD_SPEED)
                        print(f"[DEBUG] {status_text}")
                        return
                    else:
                        serial_send(1, 0, 0)
                        avoiding_obstacle = False
                        ball_search_state = "BEGIN_SEARCH"
                        status_text = "Resuming Ball Search"
                        print(f"[DEBUG] {status_text}")


                # --- Ball search pattern ---
                if ball_search_state == "BEGIN_SEARCH":
                    ball_search_state = "TURN_TO_ZERO"
                    ball_search_target_yaw = 0.0
                    serial_send(5 if get_yaw_diff(0, current_yaw_value) > 0 else 6, 0, BASE_TURN_SPEED)
                    status_text = "Aligning to 0°"

                elif ball_search_state == "TURN_TO_ZERO":
                    yaw_diff = get_yaw_diff(ball_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= YAW_TOLERANCE:
                        ball_search_state = "ROTATE_LEFT_90"
                        ball_search_target_yaw = (current_yaw_value + 180) % 360
                        serial_send(5, 0, BASE_TURN_SPEED)
                        status_text = f"Rotating Left to {ball_search_target_yaw:.1f}°"
                    else:
                        serial_send(5 if yaw_diff > 0 else 6, 0, BASE_TURN_SPEED)
                        status_text = f"Turning to 0°: {abs(yaw_diff):.1f}° remaining"

                elif ball_search_state == "ROTATE_LEFT_90":
                    yaw_diff = get_yaw_diff(ball_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= YAW_TOLERANCE:
                        ball_search_state = "ROTATE_RIGHT_180"
                        ball_search_target_yaw = (current_yaw_value - 0) % 360
                        serial_send(6, 0, BASE_TURN_SPEED)
                        status_text = f"Rotating Right to {ball_search_target_yaw:.1f}°"
                    else:
                        status_text = f"Turning Left: {abs(yaw_diff):.1f}° remaining"

                elif ball_search_state == "ROTATE_RIGHT_180":
                    yaw_diff = get_yaw_diff(ball_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= YAW_TOLERANCE:
                        ball_search_state = "RETURN_TO_ZERO"
                        ball_search_target_yaw = 0.0
                        serial_send(5, 0, BASE_TURN_SPEED)
                        status_text = "Returning to 0°"
                    else:
                        status_text = f"Turning Right: {abs(yaw_diff):.1f}° remaining"

                elif ball_search_state == "RETURN_TO_ZERO":
                    yaw_diff = get_yaw_diff(ball_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= YAW_TOLERANCE:
                        ball_search_state = "MOVE_FORWARD"
                        ball_search_start_time = time.time()
                        serial_send(2, 0, FORWARD_SPEED)
                        status_text = "Final: Moving Forward"
                    else:
                        status_text = f"Returning to 0°: {abs(yaw_diff):.1f}° remaining"

                elif ball_search_state == "MOVE_FORWARD":
                    if time.time() - ball_search_start_time >= FORWARD_DURATION:
                        ball_search_state = "BEGIN_SEARCH"
                        status_text = "Pattern Restarted"
                    else:
                        status_text = f"Moving: {FORWARD_DURATION - (time.time() - ball_search_start_time):.1f}s left"

                debug_text = f"Yaw: {current_yaw_value:.1f}° | Target: {ball_search_target_yaw:.1f}°"

            # ----------------- BALL CENTERING ------------------
            else:
                try:
                    (x, y), radius = cv2.minEnclosingCircle(closest_ball["contour"])
                    ball_diameter_pixels = 2 * radius
                    ball_distance = (REAL_BALL_DIAMETER * focal_length) / ball_diameter_pixels
                    frame_center_x = frame.shape[1] / 2

                    if not centered_on_ball:
                        if x > frame_center_x + CENTER_THRESHOLD:
                            status_text = "Turning Right to Center on Ball"
                            serial_send(6, 0, BASE_TURN_SPEED)
                        elif x < frame_center_x - CENTER_THRESHOLD:
                            status_text = "Turning Left to Center on Ball"
                            serial_send(5, 0, BASE_TURN_SPEED)
                        else:
                            status_text = "Centered on Ball"
                            centered_on_ball = True
                            centering_start_time = time.time()
                            serial_send(1, 0, 0)
                    else:
                        if time.time() - centering_start_time > 1.0:
                            if x > frame_center_x + CENTER_THRESHOLD:
                                status_text = "Ball Drifted Right - Re-centering"
                                serial_send(1, 0, 0)
                                serial_send(6, 0, BASE_TURN_SPEED)
                                centered_on_ball = False
                                centering_start_time = None
                            elif x < frame_center_x - CENTER_THRESHOLD:
                                status_text = "Ball Drifted Left - Re-centering"
                                serial_send(1, 0, 0)
                                serial_send(5, 0, BASE_TURN_SPEED)
                                centered_on_ball = False
                                centering_start_time = None
                            elif ball_distance >= AVOIDANCE_DISTANCE:
                                status_text = "Moving Towards Ball"
                                serial_send(2, 0, FORWARD_SPEED)
                            else:
                                status_text = "Ball Reached - Starting Grab Sequence"
                                grabbing_state = "PREPARE_STOP"
                                grabbing_start_time = time.time()
                        else:
                            status_text = "Centering on Ball"
                            serial_send(1, 0, 0)

                    debug_text = f"Ball X: {int(x)} | Distance: {ball_distance:.2f} m"

                except Exception as e:
                    status_text = "Ball Detection Error"
                    print(f"Ball tracking error: {e}")

            # Overlay status
            cv2.putText(frame, status_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, debug_text, (30, 90), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2, cv2.LINE_AA)







        def handle_goal_sequence(closest_goal, frame, focal_length):
            global centered_on_goal, goal_centering_start_time, goal_sequence_completed
            global goal_search_state, goal_search_target_yaw, goal_search_start_time, current_yaw
            global GOAL_BASE_TURN_SPEED, GOAL_APPROACH_DISTANCE, GOAL_CENTER_THRESHOLD, GOAL_FORWARD_DURATION, GOAL_FORWARD_SPEED, GOAL_YAW_TOLERANCE
            global avoiding_obstacle, obstacle_avoidance_start_time

            # Initialize all required variables
            if 'goal_search_state' not in globals():
                goal_search_state = "BEGIN_SEARCH"
                goal_search_target_yaw = None
                goal_search_start_time = time.time()
            if 'avoiding_obstacle' not in globals():
                avoiding_obstacle = False
                obstacle_avoidance_start_time = None
            # Safely get current yaw value
            try:
                current_yaw_value = float(current_yaw) if isinstance(current_yaw, (int, float, str)) and str(current_yaw) != "N/A" else 0.0
            except (ValueError, TypeError):
                current_yaw_value = 0.0
                print("Warning: Invalid yaw value, defaulting to 0.0")

            def get_yaw_diff(target, current):
                """Calculate shortest yaw difference with wrapping"""
                return (target - current + 180) % 360 - 180

            status_text = "Goal Sequence Active"
            debug_text = ""


            # Compute obstacle distance if closest_obstacle is present
            if closest_obstacle:
                try:
                    obstacle_width_pixels = closest_obstacle['w']
                    obstacle_distance = (REAL_OBSTACLE_WIDTH * focal_length) / obstacle_width_pixels
                    print(f"[DEBUG] Calculated obstacle_distance: {obstacle_distance:.2f}")
                except Exception as e:
                    print(f"[ERROR] Failed to compute obstacle_distance: {e}")
                    obstacle_distance = None
            else:
                obstacle_distance = None
                print("[DEBUG] No closest_obstacle found, setting obstacle_distance to None")

            # Check for obstacle and start avoidance
            if closest_obstacle and not avoiding_obstacle:
                print(f"[DEBUG] Checking obstacle condition: distance = {obstacle_distance}, threshold = {APPROACH_DISTANCE}")
                if obstacle_distance is not None and obstacle_distance <= APPROACH_DISTANCE:
                    status_text = "Obstacle Detected - Starting Avoidance"
                    print(f"[DEBUG] {status_text}")

                    try:
                        obstacle_x = closest_obstacle['x']
                        frame_center_x = frame.shape[1] / 2

                        if obstacle_x > frame_center_x:
                            serial_send(14, 0, FORWARD_SPEED)  # Diagonal left
                            status_text += " (Right Side) → Diagonal Left"
                        else:
                            serial_send(15, 0, FORWARD_SPEED)  # Diagonal right
                            status_text += " (Left Side) → Diagonal Right"
                        print(f"[DEBUG] Obstacle X: {obstacle_x}, Frame Center: {frame_center_x}")
                    except Exception as e:
                        print(f"[ERROR] Obstacle direction error: {e}")
                        serial_send(15, 0, FORWARD_SPEED)

                    obstacle_avoidance_start_time = time.time()
                    avoiding_obstacle = True
                    return

            # Handle obstacle avoidance state
            if avoiding_obstacle:
                elapsed = time.time() - obstacle_avoidance_start_time

                if elapsed < AVOIDANCE_TURN_DURATION:
                    status_text = f"Avoiding Obstacle: {AVOIDANCE_TURN_DURATION - elapsed:.1f}s remaining"
                    print(f"[DEBUG] {status_text}")
                    return
                elif elapsed < AVOIDANCE_TURN_DURATION + AVOIDANCE_FORWARD_DURATION:
                    status_text = f"Clearing Forward: {(AVOIDANCE_TURN_DURATION + AVOIDANCE_FORWARD_DURATION) - elapsed:.1f}s remaining"
                    serial_send(2, 0, FORWARD_SPEED)
                    print(f"[DEBUG] {status_text}")
                    return
                else:
                    serial_send(1, 0, 0)
                    avoiding_obstacle = False
                    goal_search_state = "BEGIN_SEARCH"
                    status_text = "Resuming Ball Search"
                    print(f"[DEBUG] {status_text}")

            # Goal search behavior (when no goal detected)
            if not closest_goal:


                if goal_search_state == "BEGIN_SEARCH":
                    goal_search_state = "TURN_TO_ZERO"
                    goal_search_target_yaw = 0.0
                    serial_send(5 if get_yaw_diff(0, current_yaw_value) > 0 else 6, 0, GOAL_BASE_TURN_SPEED)
                    status_text = "Aligning to 0°"

                elif goal_search_state == "TURN_TO_ZERO":
                    yaw_diff = get_yaw_diff(goal_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= GOAL_YAW_TOLERANCE:
                        goal_search_state = "ROTATE_LEFT_90"
                        goal_search_target_yaw = (current_yaw_value + 60) % 360
                        serial_send(5, 0, GOAL_BASE_TURN_SPEED)
                        status_text = f"Rotating Left to {goal_search_target_yaw:.1f}°"
                    else:
                        serial_send(5 if yaw_diff > 0 else 6, 0, GOAL_BASE_TURN_SPEED)
                        status_text = f"Turning to 0°: {abs(yaw_diff):.1f}° remaining"

                elif goal_search_state == "ROTATE_LEFT_90":
                    yaw_diff = get_yaw_diff(goal_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= GOAL_YAW_TOLERANCE:
                        goal_search_state = "ROTATE_RIGHT_180"
                        goal_search_target_yaw = (current_yaw_value -60) % 360
                        serial_send(6, 0, GOAL_BASE_TURN_SPEED)
                        status_text = f"Rotating Right to {goal_search_target_yaw:.1f}°"
                    else:
                        status_text = f"Turning Left: {abs(yaw_diff):.1f}° remaining"

                elif goal_search_state == "ROTATE_RIGHT_180":
                    yaw_diff = get_yaw_diff(goal_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= GOAL_YAW_TOLERANCE:
                        goal_search_state = "RETURN_TO_ZERO"
                        goal_search_target_yaw = 0.0
                        serial_send(5, 0, GOAL_BASE_TURN_SPEED)
                        status_text = "Returning to 0°"
                    else:
                        status_text = f"Turning Right: {abs(yaw_diff):.1f}° remaining"

                elif goal_search_state == "RETURN_TO_ZERO":
                    yaw_diff = get_yaw_diff(goal_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= GOAL_YAW_TOLERANCE:
                        goal_search_state = "MOVE_FORWARD"
                        goal_search_start_time = time.time()
                        serial_send(2, 0, GOAL_FORWARD_SPEED)
                        status_text = "Final: Moving Forward"
                    else:
                        status_text = f"Returning to 0°: {abs(yaw_diff):.1f}° remaining"

                elif goal_search_state == "MOVE_FORWARD":
                    if time.time() - goal_search_start_time >= GOAL_FORWARD_DURATION:
                        goal_search_state = "BEGIN_SEARCH"
                        status_text = "Pattern Restarted"
                    else:
                        status_text = f"Moving: {GOAL_FORWARD_DURATION - (time.time() - goal_search_start_time):.1f}s left"

                debug_text = f"Yaw: {current_yaw_value:.1f}° | Target: {goal_search_target_yaw:.1f}°"

            # Normal goal handling (when goal is detected)
            else:
                goal_center_x = closest_goal['x'] + closest_goal['w'] / 2
                frame_center_x = frame.shape[1] / 2
                goal_width_pixels = closest_goal['w']
                goal_distance = (REAL_GOAL_WIDTH * focal_length) / goal_width_pixels

                if not centered_on_goal:
                    # Get the center of the goal (center of the bounding box)
                    # Check if the goal is outside the center threshold and move to adjust
                    if goal_center_x > frame_center_x + GOAL_CENTER_THRESHOLD:
                        status_text = "Turning Right to Center on Goal"
                        serial_send(6, 0, GOAL_BASE_TURN_SPEED)
                    elif goal_center_x < frame_center_x - GOAL_CENTER_THRESHOLD:
                        status_text = "Turning Left to Center on Goal"
                        serial_send(5, 0, GOAL_BASE_TURN_SPEED)
                    else:
                        status_text = "Centered on Goal"
                        centered_on_goal = True
                        goal_centering_start_time = time.time()
                        serial_send(1, 0, 0)  # Stop

                else:
                    # After centering, check if the goal has drifted and re-center if necessary
                    if time.time() - goal_centering_start_time > 1.0:
                        goal_center_x = closest_goal['x'] + closest_goal['w'] / 2
                        frame_center_x = frame.shape[1] / 2
                        
                        # If goal drifted right, move right to re-center
                        if goal_center_x > frame_center_x + GOAL_CENTER_THRESHOLD:
                            status_text = "Goal Drifted Right - Re-centering"
                            serial_send(1, 0, 0)
                            serial_send(6, 0, GOAL_BASE_TURN_SPEED)
                            centered_on_goal = False
                            goal_centering_start_time = None
                        
                        # If goal drifted left, move left to re-center
                        elif goal_center_x < frame_center_x - GOAL_CENTER_THRESHOLD:
                            status_text = "Goal Drifted Left - Re-centering"
                            serial_send(1, 0, 0)
                            serial_send(5, 0, GOAL_BASE_TURN_SPEED)
                            centered_on_goal = False
                            goal_centering_start_time = None

                    # If goal is centered, handle the approach or shooting action
                    else:
                        if goal_distance > GOAL_APPROACH_DISTANCE:
                            status_text = "Approaching Goal"
                            serial_send(2, 0, GOAL_FORWARD_SPEED)
                        else:
                            status_text = "Releasing and Shooting"
                            serial_send(1, 0, 0)  # Stop before action
                            serial_send(18, 0, 0)  # Open grabber to release ball
                            time.sleep(0.8)  # Optional delay to ensure ball drops
                            serial_send(9, 0, 0)  # Kick the ball
                            goal_sequence_completed = True

                debug_text = f"Distance: {goal_distance:.2f}m | GoalX: {int(goal_center_x)}"

            # Display status
            cv2.putText(frame, status_text, (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(frame, debug_text, (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)


        # --- Reset Sequences --- 
        def reset_sequences():
            global ball_sequence_completed, centered_on_ball, centering_start_time, closest_ball
            global goal_sequence_completed, centered_on_goal, goal_centering_start_time, closest_goal

            if ball_sequence_completed:
                print("DEBUG: Resetting Ball Sequence")
                ball_sequence_completed = False
                centered_on_ball = False
                centering_start_time = None
                closest_ball = None
                time.sleep(0.5)
            if goal_sequence_completed:
                print("DEBUG: Resetting Goal Sequence")
                goal_sequence_completed = False
                centered_on_goal = False
                goal_centering_start_time = None
                closest_goal = None
                time.sleep(0.5)

       
        # --- Main Processing Logic ---
        if start_avoidance_active:
            print("DEBUG: Avoidance Active")

            # Proceed directly with the sequences based on current completion state
            if not ball_sequence_completed:
                print("DEBUG: Executing Ball Sequence")
                handle_ball_sequence(closest_ball, frame, focal_length)

            elif ball_sequence_completed and not goal_sequence_completed:
                print("DEBUG: Executing Goal Sequence")
                handle_goal_sequence(closest_goal, frame, focal_length)

            elif ball_sequence_completed and goal_sequence_completed:
                print("DEBUG: Resetting Sequences After Goal")
                reset_sequences()




        # Convert the frame to RGB for displaying in the Tkinter label
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the video_display label with the new frame
        video_display.imgtk = imgtk
        video_display.configure(image=imgtk)

        # Repeat the process after 30 milliseconds
        video_display.after(10, update_frame)

    update_frame()






#--------------------------------------------------------------------------------------------------------------------------------#  


 
#--------------------------------------------------------------------------------------------------------------------------------# 
def create_goalfirst():
    global goalfirst_frame, cap, color_ranges, yaw_value_label
    global CAMERA_FOV, REAL_BALL_DIAMETER, REAL_GOAL_WIDTH, AVOIDANCE_DISTANCE, GOAL_APPROACH_DISTANCE
    global PID_KP, PID_KI, PID_KD
    global YAW_TOLERANCE, MIN_TURN_SPEED, MAX_TURN_SPEED
    global BALL_YAW_TOLERANCE, CENTER_THRESHOLD, BASE_TURN_SPEED, FORWARD_SPEED, FORWARD_DURATION
    global GOAL_YAW_TOLERANCE, GOAL_CENTER_THRESHOLD, GOAL_BASE_TURN_SPEED, GOAL_FORWARD_SPEED, GOAL_FORWARD_DURATION




    cap = None

    ball_settings = load_ball_settings()
    goal_settings = load_goal_settings()
    obstacle_settings = load_obstacle_settings()

    color_ranges = {}
    for color, settings in ball_settings.items():
        color_ranges[color] = (
            (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"]),
            (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])
        )
    for color, settings in goal_settings.items():
        color_ranges[color] = (
            (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"]),
            (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])
        )

    print(f"Color ranges: {color_ranges}")

    # Add obstacle settings to color_ranges
    for color, settings in obstacle_settings.items():
        color_ranges[color] = (
            (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"]),
            (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])
        )

    print(f"Color ranges: {color_ranges}")


    goalfirst_frame = tk.Frame(root, bg=creamy_beige, width=900, height=600)
    goalfirst_frame.pack(fill=tk.BOTH, expand=True)

    video_display = tk.Label(goalfirst_frame, bg="black", width=640, height=480)
    video_display.place(x=20, y=50)

    back_button = tk.Button(
        goalfirst_frame, text="Back", command=on_back_to_menu, 
        bg=deep_teal, fg=white, font=("Anton", 12, "bold"), padx=10, pady=5
    )
    back_button.place(x=20, y=7)

    def reset_sequence():
        global start_goalfirst_active, color_order
        start_goalfirst_active = False
        color_order = []
        serial_send(1, 0, 0)
        print("System reset. Sending cmd: (4, 0, 0)")
        messagebox.showinfo("System Reset", "The system has been reset. Avoidance mode is stopped.")

    reset_button = tk.Button(
        goalfirst_frame, text="Reset", command=reset_sequence,
        bg=deep_teal, fg=white, font=("Anton", 12, "bold"), padx=10, pady=5
    )
    reset_button.place(x=340, y=7)

    def start_goalfirst():
        global start_goalfirst_active
        start_goalfirst_active = True
        print("START move to the goal mode activated.")

    option1_button = tk.Button(
        goalfirst_frame, text="START TO GOAL", command=start_goalfirst,
        bg=vibrant_orange, fg=black, font=("Anton", 12, "bold"), padx=10, pady=5
    )
    option1_button.place(x=120, y=7)



    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "goalfirst_config.ini")

    def load_goalfirst_config():
        config = configparser.ConfigParser()
        if os.path.exists(config_file):
            config.read(config_file)
            if 'goalfirstSettings' in config:
                return config['goalfirstSettings']
        return None

    def save_goalfirst_config():
        config = configparser.ConfigParser()
        if os.path.exists(config_file):
            config.read(config_file)
        if not config.has_section('goalfirstSettings'):
            config.add_section('goalfirstSettings')

        config['goalfirstSettings']['CAMERA_FOV'] = str(fov_input.get())
        config['goalfirstSettings']['REAL_BALL_DIAMETER'] = str(ball_dia_input.get())
        config['goalfirstSettings']['REAL_GOAL_WIDTH'] = str(goal_width_input.get())
        config['goalfirstSettings']['AVOIDANCE_DISTANCE'] = str(avoid_dist_input.get())
        config['goalfirstSettings']['GOAL_APPROACH_DISTANCE'] = str(goal_approach_input.get())
        config['goalfirstSettings']['PID_KP'] = str(pid_kp_input.get())
        config['goalfirstSettings']['PID_KI'] = str(pid_ki_input.get())
        config['goalfirstSettings']['PID_KD'] = str(pid_kd_input.get())
        config['goalfirstSettings']['YAW_TOLERANCE'] = str(yaw_tol_input.get())
        config['goalfirstSettings']['MIN_TURN_SPEED'] = str(min_turn_input.get())
        config['goalfirstSettings']['MAX_TURN_SPEED'] = str(max_turn_input.get())
        config['goalfirstSettings']['BALL_YAW_TOLERANCE'] = str(ball_yaw_tol_input.get())
        config['goalfirstSettings']['CENTER_THRESHOLD'] = str(center_thresh_input.get())
        config['goalfirstSettings']['BASE_TURN_SPEED'] = str(base_turn_input.get())
        config['goalfirstSettings']['FORWARD_SPEED'] = str(forward_speed_input.get())
        config['goalfirstSettings']['FORWARD_DURATION'] = str(forward_duration_input.get())
        config['goalfirstSettings']['GOAL_YAW_TOLERANCE'] = str(goal_yaw_tol_input.get())
        config['goalfirstSettings']['GOAL_CENTER_THRESHOLD'] = str(goal_center_thresh_input.get())
        config['goalfirstSettings']['GOAL_BASE_TURN_SPEED'] = str(goal_base_turn_input.get())
        config['goalfirstSettings']['GOAL_FORWARD_SPEED'] = str(goal_forward_speed_input.get())
        config['goalfirstSettings']['GOAL_FORWARD_DURATION'] = str(goal_forward_duration_input.get())




        with open(config_file, 'w') as f:
            config.write(f)

        messagebox.showinfo("Success", "Configuration saved successfully!")

    config = load_goalfirst_config()
    if config:
        CAMERA_FOV = config.getfloat('CAMERA_FOV', fallback=60)
        REAL_BALL_DIAMETER = config.getfloat('REAL_BALL_DIAMETER', fallback=0.1)
        REAL_GOAL_WIDTH = config.getfloat('REAL_GOAL_WIDTH', fallback=1.0)
        AVOIDANCE_DISTANCE = config.getfloat('AVOIDANCE_DISTANCE', fallback=0.3)
        GOAL_APPROACH_DISTANCE = config.getfloat('GOAL_APPROACH_DISTANCE', fallback=0.9)
        PID_KP = config.getfloat('PID_KP', fallback=1.0)
        PID_KI = config.getfloat('PID_KI', fallback=0.0)
        PID_KD = config.getfloat('PID_KD', fallback=0.1)
        YAW_TOLERANCE = config.getfloat('YAW_TOLERANCE', fallback=15.0)
        MIN_TURN_SPEED = config.getint('MIN_TURN_SPEED', fallback=20)
        MAX_TURN_SPEED = config.getint('MAX_TURN_SPEED', fallback=20)
        BALL_YAW_TOLERANCE = config.getfloat('BALL_YAW_TOLERANCE', fallback=15.0)
        CENTER_THRESHOLD = config.getint('CENTER_THRESHOLD', fallback=30)
        BASE_TURN_SPEED = config.getint('BASE_TURN_SPEED', fallback=20)
        FORWARD_SPEED = config.getint('FORWARD_SPEED', fallback=30)
        FORWARD_DURATION = config.getfloat('FORWARD_DURATION', fallback=5.0)
        GOAL_YAW_TOLERANCE = config.getfloat('GOAL_YAW_TOLERANCE', fallback=10.0)
        GOAL_CENTER_THRESHOLD = config.getint('GOAL_CENTER_THRESHOLD', fallback=30)
        GOAL_BASE_TURN_SPEED = config.getint('GOAL_BASE_TURN_SPEED', fallback=15)
        GOAL_FORWARD_SPEED = config.getint('GOAL_FORWARD_SPEED', fallback=30)
        GOAL_FORWARD_DURATION = config.getfloat('GOAL_FORWARD_DURATION', fallback=5.0)
    else:
        CAMERA_FOV = 60
        REAL_BALL_DIAMETER = 0.1
        REAL_GOAL_WIDTH = 1.0
        AVOIDANCE_DISTANCE = 0.3
        GOAL_APPROACH_DISTANCE = 0.9
        PID_KP = 1.0
        PID_KI = 0.0
        PID_KD = 0.1
        YAW_TOLERANCE = 15.0
        MIN_TURN_SPEED = 20
        MAX_TURN_SPEED = 20
        BALL_YAW_TOLERANCE = 15.0
        CENTER_THRESHOLD = 30
        BASE_TURN_SPEED = 20
        FORWARD_SPEED = 30
        FORWARD_DURATION = 5.0
        GOAL_YAW_TOLERANCE = 10.0
        GOAL_CENTER_THRESHOLD = 30
        GOAL_BASE_TURN_SPEED = 15
        GOAL_FORWARD_SPEED = 30
        GOAL_FORWARD_DURATION = 5.0

    config_title_bar = tk.Frame(
        goalfirst_frame, bg=deep_teal, width=227, height=42,
        highlightbackground="black", highlightthickness=2
    )
    config_title_bar.place(x=668, y=50)

    config_title = tk.Label(
        config_title_bar, text="⚙️ Configuration",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    config_title.place(relx=0.5, rely=0.5, anchor="center")

    config_frame = tk.Frame(
        goalfirst_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    config_frame.place(x=668, y=90, width=227, height=160)

    pid_frame = tk.Frame(
        goalfirst_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    pid_frame.place(x=20, y=583, width=210, height=93)

    # Title for PID section
    pid_title_bar = tk.Frame(
        goalfirst_frame, bg=deep_teal, width=210, height=42,
        highlightbackground="black", highlightthickness=2
    )
    pid_title_bar.place(x=20, y=543)

    pid_title = tk.Label(
        pid_title_bar, text="⚙️ Allignment",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    pid_title.place(relx=0.5, rely=0.5, anchor="center")

    # Frame for Yaw Control
    yaw_title_bar = tk.Frame(
        goalfirst_frame, bg=deep_teal, width=210, height=42,
        highlightbackground="black", highlightthickness=2
    )
    yaw_title_bar.place(x=240, y=543)

    yaw_title = tk.Label(
        yaw_title_bar, text="↩️ Turn Control",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    yaw_title.place(relx=0.5, rely=0.5, anchor="center")

    yaw_frame = tk.Frame(
        goalfirst_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    yaw_frame.place(x=240, y=583, width=210, height=93)

        # Ball Settings Frame
    ball_title_bar = tk.Frame(
        goalfirst_frame, bg=deep_teal, width=227, height=42,
        highlightbackground="black", highlightthickness=2
    )
    ball_title_bar.place(x=668, y=274)

    ball_title = tk.Label(
        ball_title_bar, text="⚽ Ball Behavior",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    ball_title.place(relx=0.5, rely=0.5, anchor="center")

    ball_frame = tk.Frame(
        goalfirst_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    ball_frame.place(x=668, y=314, width=227, height=150)

    # Goal Settings Frame
    goal_title_bar = tk.Frame(
        goalfirst_frame, bg=deep_teal, width=227, height=42,
        highlightbackground="black", highlightthickness=2
    )
    goal_title_bar.place(x=668, y=487)

    goal_title = tk.Label(
        goal_title_bar, text="🥅 Goal Behavior",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    goal_title.place(relx=0.5, rely=0.5, anchor="center")

    goal_frame = tk.Frame(
        goalfirst_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    goal_frame.place(x=668, y=527, width=227, height=150)







    def create_compact_entry(parent, row, emoji, label_text, default_val):
        tk.Label(parent, text=emoji, bg="white", font=("Segoe UI Emoji", 9)).grid(row=row, column=0, sticky="w", padx=4)
        tk.Label(parent, text=label_text, bg="white", fg="#444", font=("Segoe UI", 12), anchor="w").grid(row=row, column=1, sticky="w", padx=2)
        entry = tk.Entry(parent, font=("Segoe UI", 12), width=8, bd=1, relief="solid", bg="#f1f1f1", justify="center")
        entry.grid(row=row, column=2, padx=(5, 2), pady=2)
        entry.insert(0, str(default_val))
        return entry

    # Create all input fields including PID
    fov_input = create_compact_entry(config_frame, 0, "📷", "FOV", CAMERA_FOV)
    ball_dia_input = create_compact_entry(config_frame, 1, "⚽", "Ball Ø", REAL_BALL_DIAMETER)
    goal_width_input = create_compact_entry(config_frame, 2, "🥅", "Goal Width", REAL_GOAL_WIDTH)
    avoid_dist_input = create_compact_entry(config_frame, 3, "🎯", "To Ball, m", AVOIDANCE_DISTANCE)
    goal_approach_input = create_compact_entry(config_frame, 4, "🎯", "To Goal, m", GOAL_APPROACH_DISTANCE)

    # Create PID input fields in their own box
    pid_kp_input = create_compact_entry(pid_frame, 1, "⚙️", "Kp", PID_KP) 
    pid_ki_input = create_compact_entry(pid_frame, 2, "⚙️", "Ki", PID_KI)
    pid_kd_input = create_compact_entry(pid_frame, 3, "⚙️", "Kd", PID_KD)

    # Input fields for yaw control
    yaw_tol_input = create_compact_entry(yaw_frame, 0, "📐", "Yaw Tol.", YAW_TOLERANCE)
    min_turn_input = create_compact_entry(yaw_frame, 1, "🔄", "Min Turn", MIN_TURN_SPEED)
    max_turn_input = create_compact_entry(yaw_frame, 2, "🔁", "Max Turn", MAX_TURN_SPEED)

    # Ball settings input fields
    ball_yaw_tol_input = create_compact_entry(ball_frame, 0, "📐", "Yaw Tol.", BALL_YAW_TOLERANCE)
    center_thresh_input = create_compact_entry(ball_frame, 1, "🎯", "Center Thresh", CENTER_THRESHOLD)
    base_turn_input = create_compact_entry(ball_frame, 2, "🔄", "Turn Speed", BASE_TURN_SPEED)
    forward_speed_input = create_compact_entry(ball_frame, 3, "➡️", "Fwd Speed", FORWARD_SPEED)
    forward_duration_input = create_compact_entry(ball_frame, 4, "⏱️", "Fwd Duration", FORWARD_DURATION)

        # Goal settings input fields
    goal_yaw_tol_input = create_compact_entry(goal_frame, 0, "📐", "Yaw Tol.", GOAL_YAW_TOLERANCE)
    goal_center_thresh_input = create_compact_entry(goal_frame, 1, "🎯", "Center Thresh", GOAL_CENTER_THRESHOLD)
    goal_base_turn_input = create_compact_entry(goal_frame, 2, "🔄", "Turn Speed", GOAL_BASE_TURN_SPEED)
    goal_forward_speed_input = create_compact_entry(goal_frame, 3, "➡️", "Fwd Speed", GOAL_FORWARD_SPEED)
    goal_forward_duration_input = create_compact_entry(goal_frame, 4, "⏱️", "Fwd Duration", GOAL_FORWARD_DURATION)

    save_button = tk.Button(
    goalfirst_frame, text="💾 Save", command=save_goalfirst_config,
    bg=deep_teal, fg=white, font=("Anton", 12, "bold"), padx=10, pady=5
    )
    save_button.place(x=450, y=7)


    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot access webcam")
        return






    def update_frame():
        global cap, start_goalfirst_active, ser
        global previous_yaw, current_yaw, centered_on_ball, centering_start_time
        global centered_on_goal, goal_centering_start_time, ball_sequence_completed, goal_sequence_completed
        global return_to_zero_active, target_yaw
        global goal_search_state, goal_search_start_time, last_rotation_direction
    
        # Add these initialization if they don't exist
        if 'return_to_zero_active' not in globals():
            return_to_zero_active = False
        if 'target_yaw' not in globals():
            target_yaw = 0.0  # Target is 0 degrees
        
        # Initialize variables if they don't exist
        if 'current_yaw' not in globals():
            current_yaw = "N/A"
        if 'centered_on_ball' not in globals():
            centered_on_ball = False
        if 'centering_start_time' not in globals():
            centering_start_time = None
        if 'centered_on_goal' not in globals():
            centered_on_goal = False
        if 'goal_centering_start_time' not in globals():
            goal_centering_start_time = None
        if 'ball_sequence_completed' not in globals():
            ball_sequence_completed = False
        if 'goal_sequence_completed' not in globals():
            goal_sequence_completed = False





        # Improved serial reading
        if ser and ser.in_waiting:
            try:
                # Read all available lines
                while ser.in_waiting:
                    line = ser.readline().decode('utf-8').strip()
                    if line.startswith("Yaw:"):
                        try:
                            # Extract just the numeric value
                            yaw_value = float(line.split(':')[1].split()[0])
                            current_yaw = f"{yaw_value:.2f}"
                        except (IndexError, ValueError):
                            pass  # Skip if parsing fails
            except UnicodeDecodeError:
                # Clear buffer if we get garbled data
                ser.reset_input_buffer()
            except Exception as e:
                print(f"Serial error: {str(e)}")

        if cap is None or not cap.isOpened():
            return

        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture frame from webcam")
            return

        # Display yaw value on the video frame
        yaw_text = f"Yaw: {current_yaw}"
        cv2.putText(frame, yaw_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Convert the frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        detected_balls = []  # List to store all detected balls
        closest_ball = None  # Track the closest ball (largest area)
        max_area = 0  # Track the maximum area of detected balls
        detected_goals = []  # List to store all detected goals
        closest_goal = None  # Track the closest goal (largest area)
        max_goal_area = 0  # Track the maximum area of detected goals
        detected_obstacles = []  # List to store all detected obstacles
        closest_obstacle = None
        max_obstacle_area = 0

        # Calculate focal length at the beginning
        IMAGE_WIDTH = frame.shape[1]  # Ensure IMAGE_WIDTH is set
        focal_length = (IMAGE_WIDTH / 2) / np.tan(np.radians(CAMERA_FOV / 2))

        # --- Ball Detection ---
        for color_name, settings in ball_settings.items():
            # Extract HSV values from settings
            lower = (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"])
            upper = (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])

            # Create a mask for the current ball color
            mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))

            # Apply morphological operations to clean up the mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Remove small noise
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Fill small holes

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Process the largest contour
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                contour_area = cv2.contourArea(largest_contour)

                # Skip small contours (noise)
                if contour_area < 500:  # Adjust this threshold as needed
                    continue

                # Calculate circularity
                perimeter = cv2.arcLength(largest_contour, True)
                circularity = 4 * np.pi * (contour_area / (perimeter ** 2)) if perimeter > 0 else 0

                # Classify as ball if circularity is high
                if circularity > 0.4:  # Ball (high circularity)
                    # Store the detected ball
                    detected_balls.append({
                        "color": color_name,
                        "contour": largest_contour,
                        "area": contour_area,
                        "circularity": circularity
                    })

                    # Track the closest ball (largest area)
                    if contour_area > max_area:
                        max_area = contour_area
                        closest_ball = {
                            "color": color_name,
                            "contour": largest_contour,
                            "area": contour_area,
                            "circularity": circularity
                        }



        # --- Goal Detection ---
        for color_name, settings in goal_settings.items():
            # Extract HSV values from settings
            lower = (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"])
            upper = (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])

            # Create a mask for the current goal color
            mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))

            # Apply morphological operations to clean up the mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Remove small noise
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Fill small holes

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Process the largest contour
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                contour_area = cv2.contourArea(largest_contour)

                # Skip small contours (noise)
                if contour_area < 1000:  # Adjust this threshold as needed
                    continue

                # Calculate aspect ratio
                x, y, w, h = cv2.boundingRect(largest_contour)
                aspect_ratio = float(w) / h

                # Classify as goal if aspect ratio is high or low
                if aspect_ratio > 1.5 or aspect_ratio < 0.7:  # Goal (high or low aspect ratio)
                    # Store the detected goal
                    detected_goals.append({
                        "color": color_name,
                        "contour": largest_contour,
                        "area": contour_area,
                        "aspect_ratio": aspect_ratio,
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h
                    })

                    # Track the closest goal (largest area)
                    if contour_area > max_goal_area:
                        max_goal_area = contour_area
                        closest_goal = {
                            "color": color_name,
                            "contour": largest_contour,
                            "area": contour_area,
                            "aspect_ratio": aspect_ratio,
                            "x": x,
                            "y": y,
                            "w": w,
                            "h": h
                        }
        # --- Obstacle Detection ---               
        for color_name, settings in obstacle_settings.items():
            # Extract HSV values from settings
            lower = (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"])
            upper = (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])

            # Create a mask for the current obstacle color
            mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))

            # Apply morphological operations
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                contour_area = cv2.contourArea(largest_contour)

                if contour_area < 800:  # You can adjust this threshold
                    continue

                # Bounding rectangle for display
                x, y, w, h = cv2.boundingRect(largest_contour)

                detected_obstacles.append({
                    "color": color_name,
                    "contour": largest_contour,
                    "area": contour_area,
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h
                })

                if contour_area > max_obstacle_area:
                    max_obstacle_area = contour_area
                    closest_obstacle = {
                        "color": color_name,
                        "contour": largest_contour,
                        "area": contour_area,
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h
                    }


        # --- Draw All Detected Balls ---
        for ball in detected_balls:
            (x, y), radius = cv2.minEnclosingCircle(ball["contour"])
            center = (int(x), int(y))
            radius = int(radius)

            # Use red circle for the closest ball, green for others
            if ball == closest_ball:
                circle_color = (0, 0, 255)  # Red for closest ball
                label = f"{ball['color']}(Closest)"
            else:
                circle_color = (0, 255, 0)  # Green for other balls
                label = f"{ball['color']}"

            # Draw the circle
            cv2.circle(frame, center, radius, circle_color, 3)

            # Add text label for the ball
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
            text_x = int(center[0] - text_size[0] / 2)
            text_y = int(center[1] - radius - 10)  # Position text above the circle
            cv2.putText(frame, label, (text_x, text_y), font, font_scale, circle_color, font_thickness)

        # --- Draw All Detected Goals ---
        for goal in detected_goals:
            # Draw a trapezoidal frame for the goal
            epsilon = 0.01 * cv2.arcLength(goal["contour"], True)
            approx = cv2.approxPolyDP(goal["contour"], epsilon, True)
            
            # Use blue for the closest goal, cyan for others
            if goal == closest_goal:
                goal_color = (255, 0, 0)  # Blue for closest goal
                label = f"{goal['color']}(Closest)"
            else:
                goal_color = (255, 255, 0)  # Cyan for other goals
                label = f"{goal['color']}"
                
            cv2.drawContours(frame, [approx], -1, goal_color, 3)

            # Add text label for the goal
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
            text_x = int(goal['x'] + goal['w'] / 2 - text_size[0] / 2)
            text_y = int(goal['y'] - 10)  # Position text above the polygon
            cv2.putText(frame, label, (text_x, text_y), font, font_scale, goal_color, font_thickness)

        # --- Draw All Detected Obstacles ---
        for obstacle in detected_obstacles:
            x, y, w, h = obstacle["x"], obstacle["y"], obstacle["w"], obstacle["h"]

            if obstacle == closest_obstacle:
                rect_color = (0, 0, 255)  # Red for closest obstacle
                label = f"{obstacle['color']}(Closest)"
            else:
                rect_color = (0, 165, 255)  # Orange for other obstacles
                label = f"{obstacle['color']}"

            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), rect_color, 3)

            # Add label
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
            text_x = int(x + w / 2 - text_size[0] / 2)
            text_y = y - 10
            cv2.putText(frame, label, (text_x, text_y), font, font_scale, rect_color, font_thickness)


        # --- Calculate Distance to Closest Ball ---
        if closest_ball:
            (x, y), radius = cv2.minEnclosingCircle(closest_ball["contour"])
            ball_diameter_pixels = 2 * radius  # Diameter of the ball in pixels
            ball_center_x = x  # Store the x-coordinate of the ball center

            # Calculate distance to the ball
            ball_distance = (REAL_BALL_DIAMETER * focal_length) / ball_diameter_pixels

            # Display the distance on the ball
            distance_text = f"{ball_distance:.2f} m"
            cv2.putText(frame, distance_text, (int(x), int(y) + int(radius) + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            radius = 0  # Default value to prevent UnboundLocalError
            ball_center_x = None

        # --- Calculate Distance to Closest Goal ---
        if closest_goal:
            goal_width_pixels = closest_goal['w']  # Width of the goal in pixels
            goal_distance = (REAL_GOAL_WIDTH * focal_length) / goal_width_pixels
            goal_center_x = closest_goal['x'] + closest_goal['w'] / 2  # Store the x-coordinate of the goal center

            # Display the distance on the goal
            distance_text = f"{goal_distance:.2f} m"
            cv2.putText(frame, distance_text, 
                    (int(closest_goal['x']), int(closest_goal['y'] + closest_goal['h'] + 20)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            goal_center_x = None

        # --- Calculate Distance to Closest Obstacle ---
        if closest_obstacle:
            obstacle_width_pixels = closest_obstacle['w']  # Width of the obstacle in pixels
            obstacle_distance = (REAL_OBSTACLE_WIDTH * focal_length) / obstacle_width_pixels
            obstacle_center_x = closest_obstacle['x'] + closest_obstacle['w'] / 2  # x-coordinate of obstacle center

            # Display the distance on the obstacle
            distance_text = f"{obstacle_distance:.2f} m"
            cv2.putText(frame, distance_text,
                        (int(closest_obstacle['x']), int(closest_obstacle['y'] + closest_obstacle['h'] + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            obstacle_center_x = None


        # --- Draw Lines from Robot to Ball and Goal ---
        # Set the robot's position to the bottom center of the frame
        robot_position = (frame.shape[1] // 2, frame.shape[0] - 10)  # Bottom center (x, y)

        # Draw line to the closest ball
        if closest_ball:
            (x, y), _ = cv2.minEnclosingCircle(closest_ball["contour"])
            ball_center = (int(x), int(y))
            cv2.line(frame, robot_position, ball_center, (0, 255, 0), 2)  # Green line to ball

        # Draw line to the closest goal
        if closest_goal:
            goal_center = (int(closest_goal['x'] + closest_goal['w'] / 2), 
                        int(closest_goal['y'] + closest_goal['h'] / 2))
            cv2.line(frame, robot_position, goal_center, (255, 0, 0), 2)  # Blue line to goal

        # Draw line to the closest obstacle
        if closest_obstacle:
            obstacle_center = (int(closest_obstacle['x'] + closest_obstacle['w'] / 2), 
                            int(closest_obstacle['y'] + closest_obstacle['h'] / 2))
            cv2.line(frame, robot_position, obstacle_center, (0, 0, 255), 2)  # Red line to obstacle


        def handle_ball_sequence(closest_ball, frame, focal_length):
            global centered_on_ball, centering_start_time, ball_sequence_completed
            global ball_search_state, ball_search_target_yaw, ball_search_start_time, current_yaw
            global return_to_zero_active, awaiting_zero_alignment_after_ball, target_yaw
            global grabbing_state, grabbing_start_time
            global YAW_TOLERANCE, CENTER_THRESHOLD, BASE_TURN_SPEED, FORWARD_DURATION, FORWARD_SPEED
            global avoiding_obstacle, obstacle_avoidance_start_time
            global obstacle_distance  # ✅ Now declared globally

            # Init flags if not already present
            if 'grabbing_state' not in globals():
                grabbing_state = None
                grabbing_start_time = None
            if 'avoiding_obstacle' not in globals():
                avoiding_obstacle = False
                obstacle_avoidance_start_time = None

            # Yaw parsing
            try:
                current_yaw_value = float(current_yaw) if str(current_yaw) != "N/A" else 0.0
            except (ValueError, TypeError):
                current_yaw_value = 0.0
                print("Warning: Invalid yaw value, defaulting to 0.0")

            def get_yaw_diff(target, current):
                return (target - current + 180) % 360 - 180

            status_text = "Ball Sequence Active"
            debug_text = ""

            # ----------------- GRABBING SEQUENCE ------------------
            if grabbing_state is not None:
                now = time.time()

                if grabbing_state == "PREPARE_STOP":
                    serial_send(1, 0, 0)
                    grabbing_start_time = now
                    grabbing_state = "WAIT_AFTER_STOP"

                elif grabbing_state == "WAIT_AFTER_STOP":
                    if now - grabbing_start_time >= WAIT_AFTER_STOP_DURATION:
                        serial_send(2, 0, FORWARD_SPEED)
                        grabbing_start_time = now
                        grabbing_state = "FORWARD_AFTER_STOP"

                elif grabbing_state == "FORWARD_AFTER_STOP":
                    if now - grabbing_start_time >= FORWARD_AFTER_STOP_DURATION:
                        serial_send(17, 0, 0)  # Grab
                        grabbing_start_time = now
                        grabbing_state = "WAIT_AFTER_GRAB"

                elif grabbing_state == "WAIT_AFTER_GRAB":
                    if now - grabbing_start_time >= WAIT_AFTER_GRAB_DURATION:
                        centered_on_ball = False
                        centering_start_time = None
                        ball_sequence_completed = True

                        try:
                            current_yaw_float = float(current_yaw) if current_yaw != "N/A" else 0.0
                            print(f"Reached Ball. Yaw: {current_yaw_float:.2f}, preparing to return to 0°.")
                        except ValueError:
                            print("Yaw parsing error")

                        serial_send(16, 0, 50)  # Your new custom action instead of returning to 0 degrees

                        grabbing_state = None

                status_text = "Grabbing Ball..."
                debug_text = ""


            # ----------------- SEARCHING / OBSTACLE AVOIDANCE ------------------
            elif not closest_ball:
                print(f"[DEBUG] closest_ball: {closest_ball}, closest_obstacle: {closest_obstacle}, avoiding_obstacle: {avoiding_obstacle}")

                # Compute obstacle distance if closest_obstacle is present
                if closest_obstacle:
                    try:
                        obstacle_width_pixels = closest_obstacle['w']
                        obstacle_distance = (REAL_OBSTACLE_WIDTH * focal_length) / obstacle_width_pixels
                        print(f"[DEBUG] Calculated obstacle_distance: {obstacle_distance:.2f}")
                    except Exception as e:
                        print(f"[ERROR] Failed to compute obstacle_distance: {e}")
                        obstacle_distance = None
                else:
                    obstacle_distance = None
                    print("[DEBUG] No closest_obstacle found, setting obstacle_distance to None")

                # Check for obstacle and start avoidance
                if closest_obstacle and not avoiding_obstacle:
                    print(f"[DEBUG] Checking obstacle condition: distance = {obstacle_distance}, threshold = {APPROACH_DISTANCE}")
                    if obstacle_distance is not None and obstacle_distance <= APPROACH_DISTANCE:
                        status_text = "Obstacle Detected - Starting Avoidance"
                        print(f"[DEBUG] {status_text}")

                        try:
                            obstacle_x = closest_obstacle['x']
                            frame_center_x = frame.shape[1] / 2

                            if obstacle_x > frame_center_x:
                                serial_send(14, 0, FORWARD_SPEED)  # Diagonal left
                                status_text += " (Right Side) → Diagonal Left"
                            else:
                                serial_send(15, 0, FORWARD_SPEED)  # Diagonal right
                                status_text += " (Left Side) → Diagonal Right"
                            print(f"[DEBUG] Obstacle X: {obstacle_x}, Frame Center: {frame_center_x}")
                        except Exception as e:
                            print(f"[ERROR] Obstacle direction error: {e}")
                            serial_send(15, 0, FORWARD_SPEED)

                        obstacle_avoidance_start_time = time.time()
                        avoiding_obstacle = True
                        return

                # Handle obstacle avoidance state
                if avoiding_obstacle:
                    elapsed = time.time() - obstacle_avoidance_start_time

                    if elapsed < AVOIDANCE_TURN_DURATION:
                        status_text = f"Avoiding Obstacle: {AVOIDANCE_TURN_DURATION - elapsed:.1f}s remaining"
                        print(f"[DEBUG] {status_text}")
                        return
                    elif elapsed < AVOIDANCE_TURN_DURATION + AVOIDANCE_FORWARD_DURATION:
                        status_text = f"Clearing Forward: {(AVOIDANCE_TURN_DURATION + AVOIDANCE_FORWARD_DURATION) - elapsed:.1f}s remaining"
                        serial_send(2, 0, FORWARD_SPEED)
                        print(f"[DEBUG] {status_text}")
                        return
                    else:
                        serial_send(1, 0, 0)
                        avoiding_obstacle = False
                        ball_search_state = "BEGIN_SEARCH"
                        status_text = "Resuming Ball Search"
                        print(f"[DEBUG] {status_text}")


                # --- Ball search pattern ---
                if ball_search_state == "BEGIN_SEARCH":
                    ball_search_state = "TURN_TO_ZERO"
                    ball_search_target_yaw = 0.0
                    serial_send(5 if get_yaw_diff(0, current_yaw_value) > 0 else 6, 0, BASE_TURN_SPEED)
                    status_text = "Aligning to 0°"

                elif ball_search_state == "TURN_TO_ZERO":
                    yaw_diff = get_yaw_diff(ball_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= YAW_TOLERANCE:
                        ball_search_state = "ROTATE_LEFT_90"
                        ball_search_target_yaw = (current_yaw_value + 180) % 360
                        serial_send(5, 0, BASE_TURN_SPEED)
                        status_text = f"Rotating Left to {ball_search_target_yaw:.1f}°"
                    else:
                        serial_send(5 if yaw_diff > 0 else 6, 0, BASE_TURN_SPEED)
                        status_text = f"Turning to 0°: {abs(yaw_diff):.1f}° remaining"

                elif ball_search_state == "ROTATE_LEFT_90":
                    yaw_diff = get_yaw_diff(ball_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= YAW_TOLERANCE:
                        ball_search_state = "ROTATE_RIGHT_180"
                        ball_search_target_yaw = (current_yaw_value - 0) % 360
                        serial_send(6, 0, BASE_TURN_SPEED)
                        status_text = f"Rotating Right to {ball_search_target_yaw:.1f}°"
                    else:
                        status_text = f"Turning Left: {abs(yaw_diff):.1f}° remaining"

                elif ball_search_state == "ROTATE_RIGHT_180":
                    yaw_diff = get_yaw_diff(ball_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= YAW_TOLERANCE:
                        ball_search_state = "RETURN_TO_ZERO"
                        ball_search_target_yaw = 0.0
                        serial_send(5, 0, BASE_TURN_SPEED)
                        status_text = "Returning to 0°"
                    else:
                        status_text = f"Turning Right: {abs(yaw_diff):.1f}° remaining"

                elif ball_search_state == "RETURN_TO_ZERO":
                    yaw_diff = get_yaw_diff(ball_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= YAW_TOLERANCE:
                        ball_search_state = "MOVE_FORWARD"
                        ball_search_start_time = time.time()
                        serial_send(2, 0, FORWARD_SPEED)
                        status_text = "Final: Moving Forward"
                    else:
                        status_text = f"Returning to 0°: {abs(yaw_diff):.1f}° remaining"

                elif ball_search_state == "MOVE_FORWARD":
                    if time.time() - ball_search_start_time >= FORWARD_DURATION:
                        ball_search_state = "BEGIN_SEARCH"
                        status_text = "Pattern Restarted"
                    else:
                        status_text = f"Moving: {FORWARD_DURATION - (time.time() - ball_search_start_time):.1f}s left"

                debug_text = f"Yaw: {current_yaw_value:.1f}° | Target: {ball_search_target_yaw:.1f}°"

            # ----------------- BALL CENTERING ------------------
            else:
                try:
                    (x, y), radius = cv2.minEnclosingCircle(closest_ball["contour"])
                    ball_diameter_pixels = 2 * radius
                    ball_distance = (REAL_BALL_DIAMETER * focal_length) / ball_diameter_pixels
                    frame_center_x = frame.shape[1] / 2

                    if not centered_on_ball:
                        if x > frame_center_x + CENTER_THRESHOLD:
                            status_text = "Turning Right to Center on Ball"
                            serial_send(6, 0, BASE_TURN_SPEED)
                        elif x < frame_center_x - CENTER_THRESHOLD:
                            status_text = "Turning Left to Center on Ball"
                            serial_send(5, 0, BASE_TURN_SPEED)
                        else:
                            status_text = "Centered on Ball"
                            centered_on_ball = True
                            centering_start_time = time.time()
                            serial_send(1, 0, 0)
                    else:
                        if time.time() - centering_start_time > 1.0:
                            if x > frame_center_x + CENTER_THRESHOLD:
                                status_text = "Ball Drifted Right - Re-centering"
                                serial_send(1, 0, 0)
                                serial_send(6, 0, BASE_TURN_SPEED)
                                centered_on_ball = False
                                centering_start_time = None
                            elif x < frame_center_x - CENTER_THRESHOLD:
                                status_text = "Ball Drifted Left - Re-centering"
                                serial_send(1, 0, 0)
                                serial_send(5, 0, BASE_TURN_SPEED)
                                centered_on_ball = False
                                centering_start_time = None
                            elif ball_distance >= AVOIDANCE_DISTANCE:
                                status_text = "Moving Towards Ball"
                                serial_send(2, 0, FORWARD_SPEED)
                            else:
                                status_text = "Ball Reached - Starting Grab Sequence"
                                grabbing_state = "PREPARE_STOP"
                                grabbing_start_time = time.time()
                        else:
                            status_text = "Centering on Ball"
                            serial_send(1, 0, 0)

                    debug_text = f"Ball X: {int(x)} | Distance: {ball_distance:.2f} m"

                except Exception as e:
                    status_text = "Ball Detection Error"
                    print(f"Ball tracking error: {e}")

            # Overlay status
            cv2.putText(frame, status_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, debug_text, (30, 90), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2, cv2.LINE_AA)







        def handle_goal_sequence(closest_goal, frame, focal_length):
            global centered_on_goal, goal_centering_start_time, goal_sequence_completed
            global goal_search_state, goal_search_target_yaw, goal_search_start_time, current_yaw
            global GOAL_BASE_TURN_SPEED, GOAL_APPROACH_DISTANCE, GOAL_CENTER_THRESHOLD, GOAL_FORWARD_DURATION, GOAL_FORWARD_SPEED, GOAL_YAW_TOLERANCE
            global avoiding_obstacle, obstacle_avoidance_start_time
            

            # Initialize all required variables
            if 'goal_search_state' not in globals():
                goal_search_state = "BEGIN_SEARCH"
                goal_search_target_yaw = None
                goal_search_start_time = time.time()
            if 'avoiding_obstacle' not in globals():
                avoiding_obstacle = False
                obstacle_avoidance_start_time = None
            # Safely get current yaw value
            try:
                current_yaw_value = float(current_yaw) if isinstance(current_yaw, (int, float, str)) and str(current_yaw) != "N/A" else 0.0
            except (ValueError, TypeError):
                current_yaw_value = 0.0
                print("Warning: Invalid yaw value, defaulting to 0.0")

            def get_yaw_diff(target, current):
                """Calculate shortest yaw difference with wrapping"""
                return (target - current + 180) % 360 - 180

            status_text = "Goal Sequence Active"
            debug_text = ""


            # Compute obstacle distance if closest_obstacle is present
            if closest_obstacle:
                try:
                    obstacle_width_pixels = closest_obstacle['w']
                    obstacle_distance = (REAL_OBSTACLE_WIDTH * focal_length) / obstacle_width_pixels
                    print(f"[DEBUG] Calculated obstacle_distance: {obstacle_distance:.2f}")
                except Exception as e:
                    print(f"[ERROR] Failed to compute obstacle_distance: {e}")
                    obstacle_distance = None
            else:
                obstacle_distance = None
                print("[DEBUG] No closest_obstacle found, setting obstacle_distance to None")

            # Check for obstacle and start avoidance
            if closest_obstacle and not avoiding_obstacle:
                print(f"[DEBUG] Checking obstacle condition: distance = {obstacle_distance}, threshold = {APPROACH_DISTANCE}")
                if obstacle_distance is not None and obstacle_distance <= APPROACH_DISTANCE:
                    status_text = "Obstacle Detected - Starting Avoidance"
                    print(f"[DEBUG] {status_text}")

                    try:
                        obstacle_x = closest_obstacle['x']
                        frame_center_x = frame.shape[1] / 2

                        if obstacle_x > frame_center_x:
                            serial_send(14, 0, FORWARD_SPEED)  # Diagonal left
                            status_text += " (Right Side) → Diagonal Left"
                        else:
                            serial_send(15, 0, FORWARD_SPEED)  # Diagonal right
                            status_text += " (Left Side) → Diagonal Right"
                        print(f"[DEBUG] Obstacle X: {obstacle_x}, Frame Center: {frame_center_x}")
                    except Exception as e:
                        print(f"[ERROR] Obstacle direction error: {e}")
                        serial_send(15, 0, FORWARD_SPEED)

                    obstacle_avoidance_start_time = time.time()
                    avoiding_obstacle = True
                    return

            # Handle obstacle avoidance state
            if avoiding_obstacle:
                elapsed = time.time() - obstacle_avoidance_start_time

                if elapsed < AVOIDANCE_TURN_DURATION:
                    status_text = f"Avoiding Obstacle: {AVOIDANCE_TURN_DURATION - elapsed:.1f}s remaining"
                    print(f"[DEBUG] {status_text}")
                    return
                elif elapsed < AVOIDANCE_TURN_DURATION + AVOIDANCE_FORWARD_DURATION:
                    status_text = f"Clearing Forward: {(AVOIDANCE_TURN_DURATION + AVOIDANCE_FORWARD_DURATION) - elapsed:.1f}s remaining"
                    serial_send(2, 0, FORWARD_SPEED)
                    print(f"[DEBUG] {status_text}")
                    return
                else:
                    serial_send(1, 0, 0)
                    avoiding_obstacle = False
                    goal_search_state = "BEGIN_SEARCH"
                    status_text = "Resuming Ball Search"
                    print(f"[DEBUG] {status_text}")

            # Goal search behavior (when no goal detected)
            if not closest_goal:


                if goal_search_state == "BEGIN_SEARCH":
                    serial_send(17, 0, 0)  # Grab
                    goal_search_state = "TURN_TO_ZERO"
                    goal_search_target_yaw = 0.0
                    serial_send(5 if get_yaw_diff(0, current_yaw_value) > 0 else 6, 0, GOAL_BASE_TURN_SPEED)
                    status_text = "Aligning to 0°"


                elif goal_search_state == "TURN_TO_ZERO":
                    yaw_diff = get_yaw_diff(goal_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= GOAL_YAW_TOLERANCE:
                        goal_search_state = "ROTATE_LEFT_90"
                        goal_search_target_yaw = (current_yaw_value + 60) % 360
                        serial_send(5, 0, GOAL_BASE_TURN_SPEED)
                        status_text = f"Rotating Left to {goal_search_target_yaw:.1f}°"
                    else:
                        serial_send(5 if yaw_diff > 0 else 6, 0, GOAL_BASE_TURN_SPEED)
                        status_text = f"Turning to 0°: {abs(yaw_diff):.1f}° remaining"

                elif goal_search_state == "ROTATE_LEFT_90":
                    yaw_diff = get_yaw_diff(goal_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= GOAL_YAW_TOLERANCE:
                        goal_search_state = "ROTATE_RIGHT_180"
                        goal_search_target_yaw = (current_yaw_value -60) % 360
                        serial_send(6, 0, GOAL_BASE_TURN_SPEED)
                        status_text = f"Rotating Right to {goal_search_target_yaw:.1f}°"
                    else:
                        status_text = f"Turning Left: {abs(yaw_diff):.1f}° remaining"

                elif goal_search_state == "ROTATE_RIGHT_180":
                    yaw_diff = get_yaw_diff(goal_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= GOAL_YAW_TOLERANCE:
                        goal_search_state = "RETURN_TO_ZERO"
                        goal_search_target_yaw = 0.0
                        serial_send(5, 0, GOAL_BASE_TURN_SPEED)
                        status_text = "Returning to 0°"
                    else:
                        status_text = f"Turning Right: {abs(yaw_diff):.1f}° remaining"

                elif goal_search_state == "RETURN_TO_ZERO":
                    yaw_diff = get_yaw_diff(goal_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= GOAL_YAW_TOLERANCE:
                        goal_search_state = "MOVE_FORWARD"
                        goal_search_start_time = time.time()
                        serial_send(2, 0, GOAL_FORWARD_SPEED)
                        status_text = "Final: Moving Forward"
                    else:
                        status_text = f"Returning to 0°: {abs(yaw_diff):.1f}° remaining"

                elif goal_search_state == "MOVE_FORWARD":
                    if time.time() - goal_search_start_time >= GOAL_FORWARD_DURATION:
                        goal_search_state = "BEGIN_SEARCH"
                        status_text = "Pattern Restarted"
                    else:
                        status_text = f"Moving: {GOAL_FORWARD_DURATION - (time.time() - goal_search_start_time):.1f}s left"

                debug_text = f"Yaw: {current_yaw_value:.1f}° | Target: {goal_search_target_yaw:.1f}°"

            # Normal goal handling (when goal is detected)
            else:
                goal_center_x = closest_goal['x'] + closest_goal['w'] / 2
                frame_center_x = frame.shape[1] / 2
                goal_width_pixels = closest_goal['w']
                goal_distance = (REAL_GOAL_WIDTH * focal_length) / goal_width_pixels

                if not centered_on_goal:
                    # Get the center of the goal (center of the bounding box)
                    # Check if the goal is outside the center threshold and move to adjust
                    if goal_center_x > frame_center_x + GOAL_CENTER_THRESHOLD:
                        status_text = "Turning Right to Center on Goal"
                        serial_send(6, 0, GOAL_BASE_TURN_SPEED)
                    elif goal_center_x < frame_center_x - GOAL_CENTER_THRESHOLD:
                        status_text = "Turning Left to Center on Goal"
                        serial_send(5, 0, GOAL_BASE_TURN_SPEED)
                    else:
                        status_text = "Centered on Goal"
                        centered_on_goal = True
                        goal_centering_start_time = time.time()
                        serial_send(1, 0, 0)  # Stop

                else:
                    # After centering, check if the goal has drifted and re-center if necessary
                    if time.time() - goal_centering_start_time > 1.0:
                        goal_center_x = closest_goal['x'] + closest_goal['w'] / 2
                        frame_center_x = frame.shape[1] / 2
                        
                        # If goal drifted right, move right to re-center
                        if goal_center_x > frame_center_x + GOAL_CENTER_THRESHOLD:
                            status_text = "Goal Drifted Right - Re-centering"
                            serial_send(1, 0, 0)
                            serial_send(6, 0, GOAL_BASE_TURN_SPEED)
                            centered_on_goal = False
                            goal_centering_start_time = None
                        
                        # If goal drifted left, move left to re-center
                        elif goal_center_x < frame_center_x - GOAL_CENTER_THRESHOLD:
                            status_text = "Goal Drifted Left - Re-centering"
                            serial_send(1, 0, 0)
                            serial_send(5, 0, GOAL_BASE_TURN_SPEED)
                            centered_on_goal = False
                            goal_centering_start_time = None

                    # If goal is centered, handle the approach or shooting action
                    else:
                        if goal_distance > GOAL_APPROACH_DISTANCE:
                            status_text = "Approaching Goal"
                            serial_send(2, 0, GOAL_FORWARD_SPEED)
                        else:
                            status_text = "Releasing and Shooting"
                            serial_send(1, 0, 0)  # Stop before action
                            serial_send(18, 0, 0)  # Open grabber to release ball
                            time.sleep(0.8)  # Optional delay to ensure ball drops
                            serial_send(9, 0, 0)  # Kick the ball
                            goal_sequence_completed = True

                debug_text = f"Distance: {goal_distance:.2f}m | GoalX: {int(goal_center_x)}"

            # Display status
            cv2.putText(frame, status_text, (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(frame, debug_text, (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)


        # --- Reset Sequences --- 
        def reset_sequences():
            global ball_sequence_completed, centered_on_ball, centering_start_time, closest_ball
            global goal_sequence_completed, centered_on_goal, goal_centering_start_time, closest_goal

            if ball_sequence_completed:
                print("DEBUG: Resetting Ball Sequence")
                ball_sequence_completed = False
                centered_on_ball = False
                centering_start_time = None
                closest_ball = None
                time.sleep(0.5)
            if goal_sequence_completed:
                print("DEBUG: Resetting Goal Sequence")
                goal_sequence_completed = False
                centered_on_goal = False
                goal_centering_start_time = None
                closest_goal = None
                time.sleep(0.5)

       
        if start_goalfirst_active:
            print("DEBUG: GOAL FIRST Active")

            # Goal-first sequence logic
            if not goal_sequence_completed:
                print("DEBUG: Executing Goal Sequence")
                handle_goal_sequence(closest_goal, frame, focal_length)

            elif goal_sequence_completed and not ball_sequence_completed:
                print("DEBUG: Executing Ball Sequence")
                handle_ball_sequence(closest_ball, frame, focal_length)

            elif goal_sequence_completed and ball_sequence_completed:
                print("DEBUG: Resetting Sequences After Ball")
                reset_sequences()




        # Convert the frame to RGB for displaying in the Tkinter label
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the video_display label with the new frame
        video_display.imgtk = imgtk
        video_display.configure(image=imgtk)

        # Repeat the process after 30 milliseconds
        video_display.after(10, update_frame)

    update_frame()
#--------------------------------------------------------------------------------------------------------------------------------#  


 
#--------------------------------------------------------------------------------------------------------------------------------# 

#--------------------------------------------------------------------------------------------------------------------------------# 
def create_keeper_interface():
    global keeper_frame, cap, color_ranges, yaw_value_label
    global CAMERA_FOV, REAL_BALL_DIAMETER, REAL_GOAL_WIDTH, AVOIDANCE_DISTANCE, GOAL_APPROACH_DISTANCE
    global PID_KP, PID_KI, PID_KD
    global YAW_TOLERANCE, MIN_TURN_SPEED, MAX_TURN_SPEED
    global BALL_YAW_TOLERANCE, CENTER_THRESHOLD, BASE_TURN_SPEED, FORWARD_SPEED, FORWARD_DURATION
    global GOAL_YAW_TOLERANCE, GOAL_CENTER_THRESHOLD, GOAL_BASE_TURN_SPEED, GOAL_FORWARD_SPEED, GOAL_FORWARD_DURATION




    cap = None

    ball_settings = load_ball_settings()
    goal_settings = load_goal_settings()
    obstacle_settings = load_obstacle_settings()

    color_ranges = {}
    for color, settings in ball_settings.items():
        color_ranges[color] = (
            (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"]),
            (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])
        )
    for color, settings in goal_settings.items():
        color_ranges[color] = (
            (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"]),
            (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])
        )

    print(f"Color ranges: {color_ranges}")

    # Add obstacle settings to color_ranges
    for color, settings in obstacle_settings.items():
        color_ranges[color] = (
            (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"]),
            (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])
        )

    print(f"Color ranges: {color_ranges}")


    keeper_frame = tk.Frame(root, bg=creamy_beige, width=900, height=600)
    keeper_frame.pack(fill=tk.BOTH, expand=True)

    video_display = tk.Label(keeper_frame, bg="black", width=640, height=480)
    video_display.place(x=20, y=50)

    back_button = tk.Button(
        keeper_frame, text="Back", command=on_back_to_menu, 
        bg=deep_teal, fg=white, font=("Anton", 12, "bold"), padx=10, pady=5
    )
    back_button.place(x=20, y=7)

    def reset_sequence():
        global start_keeper_active, color_order
        start_keeper_active = False
        color_order = []
        serial_send(1, 0, 0)
        print("System reset. Sending cmd: (4, 0, 0)")
        messagebox.showinfo("System Reset", "The system has been reset. Avoidance mode is stopped.")

    reset_button = tk.Button(
        keeper_frame, text="Reset", command=reset_sequence,
        bg=deep_teal, fg=white, font=("Anton", 12, "bold"), padx=10, pady=5
    )
    reset_button.place(x=340, y=7)

    def start_keeper():
        global start_keeper_active
        start_keeper_active = True
        print("START KEEPER mode activated.")

    option1_button = tk.Button(
        keeper_frame, text="START KEEPER", command=start_keeper,
        bg=vibrant_orange, fg=black, font=("Anton", 12, "bold"), padx=10, pady=5
    )
    option1_button.place(x=120, y=7)



    config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "keeper_config.ini")

    def load_keeper_config():
        config = configparser.ConfigParser()
        if os.path.exists(config_file):
            config.read(config_file)
            if 'keeperSettings' in config:
                return config['keeperSettings']
        return None

    def save_keeper_config():
        config = configparser.ConfigParser()
        if os.path.exists(config_file):
            config.read(config_file)
        if not config.has_section('keeperSettings'):
            config.add_section('keeperSettings')

        config['keeperSettings']['CAMERA_FOV'] = str(fov_input.get())
        config['keeperSettings']['REAL_BALL_DIAMETER'] = str(ball_dia_input.get())
        config['keeperSettings']['REAL_GOAL_WIDTH'] = str(goal_width_input.get())
        config['keeperSettings']['AVOIDANCE_DISTANCE'] = str(avoid_dist_input.get())
        config['keeperSettings']['GOAL_APPROACH_DISTANCE'] = str(goal_approach_input.get())
        config['keeperSettings']['PID_KP'] = str(pid_kp_input.get())
        config['keeperSettings']['PID_KI'] = str(pid_ki_input.get())
        config['keeperSettings']['PID_KD'] = str(pid_kd_input.get())
        config['keeperSettings']['YAW_TOLERANCE'] = str(yaw_tol_input.get())
        config['keeperSettings']['MIN_TURN_SPEED'] = str(min_turn_input.get())
        config['keeperSettings']['MAX_TURN_SPEED'] = str(max_turn_input.get())
        config['keeperSettings']['BALL_YAW_TOLERANCE'] = str(ball_yaw_tol_input.get())
        config['keeperSettings']['CENTER_THRESHOLD'] = str(center_thresh_input.get())
        config['keeperSettings']['BASE_TURN_SPEED'] = str(base_turn_input.get())
        config['keeperSettings']['FORWARD_SPEED'] = str(forward_speed_input.get())
        config['keeperSettings']['FORWARD_DURATION'] = str(forward_duration_input.get())
        config['keeperSettings']['GOAL_YAW_TOLERANCE'] = str(goal_yaw_tol_input.get())
        config['keeperSettings']['GOAL_CENTER_THRESHOLD'] = str(goal_center_thresh_input.get())
        config['keeperSettings']['GOAL_BASE_TURN_SPEED'] = str(goal_base_turn_input.get())
        config['keeperSettings']['GOAL_FORWARD_SPEED'] = str(goal_forward_speed_input.get())
        config['keeperSettings']['GOAL_FORWARD_DURATION'] = str(goal_forward_duration_input.get())




        with open(config_file, 'w') as f:
            config.write(f)

        messagebox.showinfo("Success", "Configuration saved successfully!")

    config = load_keeper_config()
    if config:
        CAMERA_FOV = config.getfloat('CAMERA_FOV', fallback=60)
        REAL_BALL_DIAMETER = config.getfloat('REAL_BALL_DIAMETER', fallback=0.1)
        REAL_GOAL_WIDTH = config.getfloat('REAL_GOAL_WIDTH', fallback=1.0)
        AVOIDANCE_DISTANCE = config.getfloat('AVOIDANCE_DISTANCE', fallback=0.3)
        GOAL_APPROACH_DISTANCE = config.getfloat('GOAL_APPROACH_DISTANCE', fallback=0.9)
        PID_KP = config.getfloat('PID_KP', fallback=1.0)
        PID_KI = config.getfloat('PID_KI', fallback=0.0)
        PID_KD = config.getfloat('PID_KD', fallback=0.1)
        YAW_TOLERANCE = config.getfloat('YAW_TOLERANCE', fallback=15.0)
        MIN_TURN_SPEED = config.getint('MIN_TURN_SPEED', fallback=20)
        MAX_TURN_SPEED = config.getint('MAX_TURN_SPEED', fallback=20)
        BALL_YAW_TOLERANCE = config.getfloat('BALL_YAW_TOLERANCE', fallback=15.0)
        CENTER_THRESHOLD = config.getint('CENTER_THRESHOLD', fallback=30)
        BASE_TURN_SPEED = config.getint('BASE_TURN_SPEED', fallback=20)
        FORWARD_SPEED = config.getint('FORWARD_SPEED', fallback=30)
        FORWARD_DURATION = config.getfloat('FORWARD_DURATION', fallback=5.0)
        GOAL_YAW_TOLERANCE = config.getfloat('GOAL_YAW_TOLERANCE', fallback=10.0)
        GOAL_CENTER_THRESHOLD = config.getint('GOAL_CENTER_THRESHOLD', fallback=30)
        GOAL_BASE_TURN_SPEED = config.getint('GOAL_BASE_TURN_SPEED', fallback=15)
        GOAL_FORWARD_SPEED = config.getint('GOAL_FORWARD_SPEED', fallback=30)
        GOAL_FORWARD_DURATION = config.getfloat('GOAL_FORWARD_DURATION', fallback=5.0)
    else:
        CAMERA_FOV = 60
        REAL_BALL_DIAMETER = 0.1
        REAL_GOAL_WIDTH = 1.0
        AVOIDANCE_DISTANCE = 0.3
        GOAL_APPROACH_DISTANCE = 0.9
        PID_KP = 1.0
        PID_KI = 0.0
        PID_KD = 0.1
        YAW_TOLERANCE = 15.0
        MIN_TURN_SPEED = 20
        MAX_TURN_SPEED = 20
        BALL_YAW_TOLERANCE = 15.0
        CENTER_THRESHOLD = 30
        BASE_TURN_SPEED = 20
        FORWARD_SPEED = 30
        FORWARD_DURATION = 5.0
        GOAL_YAW_TOLERANCE = 10.0
        GOAL_CENTER_THRESHOLD = 30
        GOAL_BASE_TURN_SPEED = 15
        GOAL_FORWARD_SPEED = 30
        GOAL_FORWARD_DURATION = 5.0

    config_title_bar = tk.Frame(
        keeper_frame, bg=deep_teal, width=227, height=42,
        highlightbackground="black", highlightthickness=2
    )
    config_title_bar.place(x=668, y=50)

    config_title = tk.Label(
        config_title_bar, text="⚙️ Configuration",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    config_title.place(relx=0.5, rely=0.5, anchor="center")

    config_frame = tk.Frame(
        keeper_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    config_frame.place(x=668, y=90, width=227, height=160)

    pid_frame = tk.Frame(
        keeper_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    pid_frame.place(x=20, y=583, width=210, height=93)

    # Title for PID section
    pid_title_bar = tk.Frame(
        keeper_frame, bg=deep_teal, width=210, height=42,
        highlightbackground="black", highlightthickness=2
    )
    pid_title_bar.place(x=20, y=543)

    pid_title = tk.Label(
        pid_title_bar, text="⚙️ Allignment",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    pid_title.place(relx=0.5, rely=0.5, anchor="center")

    # Frame for Yaw Control
    yaw_title_bar = tk.Frame(
        keeper_frame, bg=deep_teal, width=210, height=42,
        highlightbackground="black", highlightthickness=2
    )
    yaw_title_bar.place(x=240, y=543)

    yaw_title = tk.Label(
        yaw_title_bar, text="↩️ Turn Control",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    yaw_title.place(relx=0.5, rely=0.5, anchor="center")

    yaw_frame = tk.Frame(
        keeper_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    yaw_frame.place(x=240, y=583, width=210, height=93)

        # Ball Settings Frame
    ball_title_bar = tk.Frame(
        keeper_frame, bg=deep_teal, width=227, height=42,
        highlightbackground="black", highlightthickness=2
    )
    ball_title_bar.place(x=668, y=274)

    ball_title = tk.Label(
        ball_title_bar, text="⚽ Ball Behavior",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    ball_title.place(relx=0.5, rely=0.5, anchor="center")

    ball_frame = tk.Frame(
        keeper_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    ball_frame.place(x=668, y=314, width=227, height=150)

    # Goal Settings Frame
    goal_title_bar = tk.Frame(
        keeper_frame, bg=deep_teal, width=227, height=42,
        highlightbackground="black", highlightthickness=2
    )
    goal_title_bar.place(x=668, y=487)

    goal_title = tk.Label(
        goal_title_bar, text="🥅 Goal Behavior",
        font=("Segoe UI", 12, "bold"), bg=deep_teal, fg="white"
    )
    goal_title.place(relx=0.5, rely=0.5, anchor="center")

    goal_frame = tk.Frame(
        keeper_frame, bg="white", bd=1, relief="flat",
        highlightbackground="black", highlightthickness=2
    )
    goal_frame.place(x=668, y=527, width=227, height=150)







    def create_compact_entry(parent, row, emoji, label_text, default_val):
        tk.Label(parent, text=emoji, bg="white", font=("Segoe UI Emoji", 9)).grid(row=row, column=0, sticky="w", padx=4)
        tk.Label(parent, text=label_text, bg="white", fg="#444", font=("Segoe UI", 12), anchor="w").grid(row=row, column=1, sticky="w", padx=2)
        entry = tk.Entry(parent, font=("Segoe UI", 12), width=8, bd=1, relief="solid", bg="#f1f1f1", justify="center")
        entry.grid(row=row, column=2, padx=(5, 2), pady=2)
        entry.insert(0, str(default_val))
        return entry

    # Create all input fields including PID
    fov_input = create_compact_entry(config_frame, 0, "📷", "FOV", CAMERA_FOV)
    ball_dia_input = create_compact_entry(config_frame, 1, "⚽", "Ball Ø", REAL_BALL_DIAMETER)
    goal_width_input = create_compact_entry(config_frame, 2, "🥅", "Goal Width", REAL_GOAL_WIDTH)
    avoid_dist_input = create_compact_entry(config_frame, 3, "🎯", "To Ball, m", AVOIDANCE_DISTANCE)
    goal_approach_input = create_compact_entry(config_frame, 4, "🎯", "To Goal, m", GOAL_APPROACH_DISTANCE)

    # Create PID input fields in their own box
    pid_kp_input = create_compact_entry(pid_frame, 1, "⚙️", "Kp", PID_KP) 
    pid_ki_input = create_compact_entry(pid_frame, 2, "⚙️", "Ki", PID_KI)
    pid_kd_input = create_compact_entry(pid_frame, 3, "⚙️", "Kd", PID_KD)

    # Input fields for yaw control
    yaw_tol_input = create_compact_entry(yaw_frame, 0, "📐", "Yaw Tol.", YAW_TOLERANCE)
    min_turn_input = create_compact_entry(yaw_frame, 1, "🔄", "Min Turn", MIN_TURN_SPEED)
    max_turn_input = create_compact_entry(yaw_frame, 2, "🔁", "Max Turn", MAX_TURN_SPEED)

    # Ball settings input fields
    ball_yaw_tol_input = create_compact_entry(ball_frame, 0, "📐", "Yaw Tol.", BALL_YAW_TOLERANCE)
    center_thresh_input = create_compact_entry(ball_frame, 1, "🎯", "Center Thresh", CENTER_THRESHOLD)
    base_turn_input = create_compact_entry(ball_frame, 2, "🔄", "Turn Speed", BASE_TURN_SPEED)
    forward_speed_input = create_compact_entry(ball_frame, 3, "➡️", "Fwd Speed", FORWARD_SPEED)
    forward_duration_input = create_compact_entry(ball_frame, 4, "⏱️", "Fwd Duration", FORWARD_DURATION)

        # Goal settings input fields
    goal_yaw_tol_input = create_compact_entry(goal_frame, 0, "📐", "Yaw Tol.", GOAL_YAW_TOLERANCE)
    goal_center_thresh_input = create_compact_entry(goal_frame, 1, "🎯", "Center Thresh", GOAL_CENTER_THRESHOLD)
    goal_base_turn_input = create_compact_entry(goal_frame, 2, "🔄", "Turn Speed", GOAL_BASE_TURN_SPEED)
    goal_forward_speed_input = create_compact_entry(goal_frame, 3, "➡️", "Fwd Speed", GOAL_FORWARD_SPEED)
    goal_forward_duration_input = create_compact_entry(goal_frame, 4, "⏱️", "Fwd Duration", GOAL_FORWARD_DURATION)

    save_button = tk.Button(
    keeper_frame, text="💾 Save", command=save_keeper_config,
    bg=deep_teal, fg=white, font=("Anton", 12, "bold"), padx=10, pady=5
    )
    save_button.place(x=450, y=7)


    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        messagebox.showerror("Error", "Cannot access webcam")
        return






    def update_frame():
        global cap, start_keeper_active, ser
        global previous_yaw, current_yaw, centered_on_ball, centering_start_time
        global centered_on_goal, goal_centering_start_time, ball_sequence_completed, goal_sequence_completed
        global return_to_zero_active, target_yaw
        global goal_search_state, goal_search_start_time, last_rotation_direction
    
        # Add these initialization if they don't exist
        if 'return_to_zero_active' not in globals():
            return_to_zero_active = False
        if 'target_yaw' not in globals():
            target_yaw = 0.0  # Target is 0 degrees
        
        # Initialize variables if they don't exist
        if 'current_yaw' not in globals():
            current_yaw = "N/A"
        if 'centered_on_ball' not in globals():
            centered_on_ball = False
        if 'centering_start_time' not in globals():
            centering_start_time = None
        if 'centered_on_goal' not in globals():
            centered_on_goal = False
        if 'goal_centering_start_time' not in globals():
            goal_centering_start_time = None
        if 'ball_sequence_completed' not in globals():
            ball_sequence_completed = False
        if 'goal_sequence_completed' not in globals():
            goal_sequence_completed = False





        # Improved serial reading
        if ser and ser.in_waiting:
            try:
                # Read all available lines
                while ser.in_waiting:
                    line = ser.readline().decode('utf-8').strip()
                    if line.startswith("Yaw:"):
                        try:
                            # Extract just the numeric value
                            yaw_value = float(line.split(':')[1].split()[0])
                            current_yaw = f"{yaw_value:.2f}"
                        except (IndexError, ValueError):
                            pass  # Skip if parsing fails
            except UnicodeDecodeError:
                # Clear buffer if we get garbled data
                ser.reset_input_buffer()
            except Exception as e:
                print(f"Serial error: {str(e)}")

        if cap is None or not cap.isOpened():
            return

        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Error", "Failed to capture frame from webcam")
            return

        # Display yaw value on the video frame
        yaw_text = f"Yaw: {current_yaw}"
        cv2.putText(frame, yaw_text, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                    0.7, (255, 255, 255), 2, cv2.LINE_AA)
        
        # Convert the frame to HSV color space
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        detected_balls = []  # List to store all detected balls
        closest_ball = None  # Track the closest ball (largest area)
        max_area = 0  # Track the maximum area of detected balls
        detected_goals = []  # List to store all detected goals
        closest_goal = None  # Track the closest goal (largest area)
        max_goal_area = 0  # Track the maximum area of detected goals
        detected_obstacles = []  # List to store all detected obstacles
        closest_obstacle = None
        max_obstacle_area = 0

        # Calculate focal length at the beginning
        IMAGE_WIDTH = frame.shape[1]  # Ensure IMAGE_WIDTH is set
        focal_length = (IMAGE_WIDTH / 2) / np.tan(np.radians(CAMERA_FOV / 2))

        # --- Ball Detection ---
        for color_name, settings in ball_settings.items():
            # Extract HSV values from settings
            lower = (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"])
            upper = (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])

            # Create a mask for the current ball color
            mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))

            # Apply morphological operations to clean up the mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Remove small noise
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Fill small holes

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Process the largest contour
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                contour_area = cv2.contourArea(largest_contour)

                # Skip small contours (noise)
                if contour_area < 500:  # Adjust this threshold as needed
                    continue

                # Calculate circularity
                perimeter = cv2.arcLength(largest_contour, True)
                circularity = 4 * np.pi * (contour_area / (perimeter ** 2)) if perimeter > 0 else 0

                # Classify as ball if circularity is high
                if circularity > 0.4:  # Ball (high circularity)
                    # Store the detected ball
                    detected_balls.append({
                        "color": color_name,
                        "contour": largest_contour,
                        "area": contour_area,
                        "circularity": circularity
                    })

                    # Track the closest ball (largest area)
                    if contour_area > max_area:
                        max_area = contour_area
                        closest_ball = {
                            "color": color_name,
                            "contour": largest_contour,
                            "area": contour_area,
                            "circularity": circularity
                        }



        # --- Goal Detection ---
        for color_name, settings in goal_settings.items():
            # Extract HSV values from settings
            lower = (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"])
            upper = (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])

            # Create a mask for the current goal color
            mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))

            # Apply morphological operations to clean up the mask
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)  # Remove small noise
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)  # Fill small holes

            # Find contours in the mask
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # Process the largest contour
            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                contour_area = cv2.contourArea(largest_contour)

                # Skip small contours (noise)
                if contour_area < 1000:  # Adjust this threshold as needed
                    continue

                # Calculate aspect ratio
                x, y, w, h = cv2.boundingRect(largest_contour)
                aspect_ratio = float(w) / h

                # Classify as goal if aspect ratio is high or low
                if aspect_ratio > 1.5 or aspect_ratio < 0.7:  # Goal (high or low aspect ratio)
                    # Store the detected goal
                    detected_goals.append({
                        "color": color_name,
                        "contour": largest_contour,
                        "area": contour_area,
                        "aspect_ratio": aspect_ratio,
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h
                    })

                    # Track the closest goal (largest area)
                    if contour_area > max_goal_area:
                        max_goal_area = contour_area
                        closest_goal = {
                            "color": color_name,
                            "contour": largest_contour,
                            "area": contour_area,
                            "aspect_ratio": aspect_ratio,
                            "x": x,
                            "y": y,
                            "w": w,
                            "h": h
                        }
        # --- Obstacle Detection ---               
        for color_name, settings in obstacle_settings.items():
            # Extract HSV values from settings
            lower = (settings["Lower Hue"], settings["Lower Saturation"], settings["Lower Value"])
            upper = (settings["Upper Hue"], settings["Upper Saturation"], settings["Upper Value"])

            # Create a mask for the current obstacle color
            mask = cv2.inRange(hsv_frame, np.array(lower), np.array(upper))

            # Apply morphological operations
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
            mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

            # Find contours
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                largest_contour = max(contours, key=cv2.contourArea)
                contour_area = cv2.contourArea(largest_contour)

                if contour_area < 800:  # You can adjust this threshold
                    continue

                # Bounding rectangle for display
                x, y, w, h = cv2.boundingRect(largest_contour)

                detected_obstacles.append({
                    "color": color_name,
                    "contour": largest_contour,
                    "area": contour_area,
                    "x": x,
                    "y": y,
                    "w": w,
                    "h": h
                })

                if contour_area > max_obstacle_area:
                    max_obstacle_area = contour_area
                    closest_obstacle = {
                        "color": color_name,
                        "contour": largest_contour,
                        "area": contour_area,
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h
                    }


        # --- Draw All Detected Balls ---
        for ball in detected_balls:
            (x, y), radius = cv2.minEnclosingCircle(ball["contour"])
            center = (int(x), int(y))
            radius = int(radius)

            # Use red circle for the closest ball, green for others
            if ball == closest_ball:
                circle_color = (0, 0, 255)  # Red for closest ball
                label = f"{ball['color']}(Closest)"
            else:
                circle_color = (0, 255, 0)  # Green for other balls
                label = f"{ball['color']}"

            # Draw the circle
            cv2.circle(frame, center, radius, circle_color, 3)

            # Add text label for the ball
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
            text_x = int(center[0] - text_size[0] / 2)
            text_y = int(center[1] - radius - 10)  # Position text above the circle
            cv2.putText(frame, label, (text_x, text_y), font, font_scale, circle_color, font_thickness)

        # --- Draw All Detected Goals ---
        for goal in detected_goals:
            # Draw a trapezoidal frame for the goal
            epsilon = 0.01 * cv2.arcLength(goal["contour"], True)
            approx = cv2.approxPolyDP(goal["contour"], epsilon, True)
            
            # Use blue for the closest goal, cyan for others
            if goal == closest_goal:
                goal_color = (255, 0, 0)  # Blue for closest goal
                label = f"{goal['color']}(Closest)"
            else:
                goal_color = (255, 255, 0)  # Cyan for other goals
                label = f"{goal['color']}"
                
            cv2.drawContours(frame, [approx], -1, goal_color, 3)

            # Add text label for the goal
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
            text_x = int(goal['x'] + goal['w'] / 2 - text_size[0] / 2)
            text_y = int(goal['y'] - 10)  # Position text above the polygon
            cv2.putText(frame, label, (text_x, text_y), font, font_scale, goal_color, font_thickness)

        # --- Draw All Detected Obstacles ---
        for obstacle in detected_obstacles:
            x, y, w, h = obstacle["x"], obstacle["y"], obstacle["w"], obstacle["h"]

            if obstacle == closest_obstacle:
                rect_color = (0, 0, 255)  # Red for closest obstacle
                label = f"{obstacle['color']}(Closest)"
            else:
                rect_color = (0, 165, 255)  # Orange for other obstacles
                label = f"{obstacle['color']}"

            # Draw rectangle
            cv2.rectangle(frame, (x, y), (x + w, y + h), rect_color, 3)

            # Add label
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 1
            font_thickness = 2
            text_size = cv2.getTextSize(label, font, font_scale, font_thickness)[0]
            text_x = int(x + w / 2 - text_size[0] / 2)
            text_y = y - 10
            cv2.putText(frame, label, (text_x, text_y), font, font_scale, rect_color, font_thickness)


        # --- Calculate Distance to Closest Ball ---
        if closest_ball:
            (x, y), radius = cv2.minEnclosingCircle(closest_ball["contour"])
            ball_diameter_pixels = 2 * radius  # Diameter of the ball in pixels
            ball_center_x = x  # Store the x-coordinate of the ball center

            # Calculate distance to the ball
            ball_distance = (REAL_BALL_DIAMETER * focal_length) / ball_diameter_pixels

            # Display the distance on the ball
            distance_text = f"{ball_distance:.2f} m"
            cv2.putText(frame, distance_text, (int(x), int(y) + int(radius) + 20), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            radius = 0  # Default value to prevent UnboundLocalError
            ball_center_x = None

        # --- Calculate Distance to Closest Goal ---
        if closest_goal:
            goal_width_pixels = closest_goal['w']  # Width of the goal in pixels
            goal_distance = (REAL_GOAL_WIDTH * focal_length) / goal_width_pixels
            goal_center_x = closest_goal['x'] + closest_goal['w'] / 2  # Store the x-coordinate of the goal center

            # Display the distance on the goal
            distance_text = f"{goal_distance:.2f} m"
            cv2.putText(frame, distance_text, 
                    (int(closest_goal['x']), int(closest_goal['y'] + closest_goal['h'] + 20)), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            goal_center_x = None

        # --- Calculate Distance to Closest Obstacle ---
        if closest_obstacle:
            obstacle_width_pixels = closest_obstacle['w']  # Width of the obstacle in pixels
            obstacle_distance = (REAL_OBSTACLE_WIDTH * focal_length) / obstacle_width_pixels
            obstacle_center_x = closest_obstacle['x'] + closest_obstacle['w'] / 2  # x-coordinate of obstacle center

            # Display the distance on the obstacle
            distance_text = f"{obstacle_distance:.2f} m"
            cv2.putText(frame, distance_text,
                        (int(closest_obstacle['x']), int(closest_obstacle['y'] + closest_obstacle['h'] + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            obstacle_center_x = None


        # --- Draw Lines from Robot to Ball and Goal ---
        # Set the robot's position to the bottom center of the frame
        robot_position = (frame.shape[1] // 2, frame.shape[0] - 10)  # Bottom center (x, y)

        # Draw line to the closest ball
        if closest_ball:
            (x, y), _ = cv2.minEnclosingCircle(closest_ball["contour"])
            ball_center = (int(x), int(y))
            cv2.line(frame, robot_position, ball_center, (0, 255, 0), 2)  # Green line to ball

        # Draw line to the closest goal
        if closest_goal:
            goal_center = (int(closest_goal['x'] + closest_goal['w'] / 2), 
                        int(closest_goal['y'] + closest_goal['h'] / 2))
            cv2.line(frame, robot_position, goal_center, (255, 0, 0), 2)  # Blue line to goal

        # Draw line to the closest obstacle
        if closest_obstacle:
            obstacle_center = (int(closest_obstacle['x'] + closest_obstacle['w'] / 2), 
                            int(closest_obstacle['y'] + closest_obstacle['h'] / 2))
            cv2.line(frame, robot_position, obstacle_center, (0, 0, 255), 2)  # Red line to obstacle


        def handle_ball_sequence(closest_ball, frame, focal_length):
            global centered_on_ball, centering_start_time, ball_sequence_completed
            global ball_search_state, ball_search_target_yaw, ball_search_start_time, current_yaw
            global return_to_zero_active, awaiting_zero_alignment_after_ball, target_yaw
            global grabbing_state, grabbing_start_time
            global YAW_TOLERANCE, CENTER_THRESHOLD, BASE_TURN_SPEED, FORWARD_DURATION, FORWARD_SPEED
            global avoiding_obstacle, obstacle_avoidance_start_time
            global obstacle_distance  # ✅ Now declared globally 

            # Init flags if not already present
            if 'grabbing_state' not in globals():
                grabbing_state = None
                grabbing_start_time = None
            if 'avoiding_obstacle' not in globals():
                avoiding_obstacle = False
                obstacle_avoidance_start_time = None

            # Yaw parsing
            try:
                current_yaw_value = float(current_yaw) if str(current_yaw) != "N/A" else 0.0
            except (ValueError, TypeError):
                current_yaw_value = 0.0
                print("Warning: Invalid yaw value, defaulting to 0.0")

            def get_yaw_diff(target, current):
                return (target - current + 180) % 360 - 180

            status_text = "Ball Sequence Active"
            debug_text = ""

            # ----------------- GRABBING SEQUENCE ------------------
            if grabbing_state is not None:
                now = time.time()

                if grabbing_state == "PREPARE_STOP":
                    serial_send(1, 0, 0)
                    grabbing_start_time = now
                    grabbing_state = "WAIT_AFTER_STOP"

                elif grabbing_state == "WAIT_AFTER_STOP":
                    if now - grabbing_start_time >= WAIT_AFTER_STOP_DURATION:
                        serial_send(2, 0, FORWARD_SPEED)
                        grabbing_start_time = now
                        grabbing_state = "FORWARD_AFTER_STOP"

                elif grabbing_state == "FORWARD_AFTER_STOP":
                    if now - grabbing_start_time >= FORWARD_AFTER_STOP_DURATION:
                        serial_send(17, 0, 0)  # Grab
                        grabbing_start_time = now
                        grabbing_state = "WAIT_AFTER_GRAB"

                elif grabbing_state == "WAIT_AFTER_GRAB":
                    if now - grabbing_start_time >= WAIT_AFTER_GRAB_DURATION:
                        centered_on_ball = False
                        centering_start_time = None
                        ball_sequence_completed = True

                        try:
                            current_yaw_float = float(current_yaw) if current_yaw != "N/A" else 0.0
                            print(f"Reached Ball. Yaw: {current_yaw_float:.2f}, preparing to return to 0°.")
                        except ValueError:
                            print("Yaw parsing error")

                        serial_send(16, 0, 50)  # Your new custom action instead of returning to 0 degrees

                        grabbing_state = None

                status_text = "Grabbing Ball..."
                debug_text = ""


            # ----------------- SEARCHING / OBSTACLE AVOIDANCE ------------------
            elif not closest_ball:
                print(f"[DEBUG] closest_ball: {closest_ball}, closest_obstacle: {closest_obstacle}, avoiding_obstacle: {avoiding_obstacle}")

                # Compute obstacle distance if closest_obstacle is present
                if closest_obstacle:
                    try:
                        obstacle_width_pixels = closest_obstacle['w']
                        obstacle_distance = (REAL_OBSTACLE_WIDTH * focal_length) / obstacle_width_pixels
                        print(f"[DEBUG] Calculated obstacle_distance: {obstacle_distance:.2f}")
                    except Exception as e:
                        print(f"[ERROR] Failed to compute obstacle_distance: {e}")
                        obstacle_distance = None
                else:
                    obstacle_distance = None
                    print("[DEBUG] No closest_obstacle found, setting obstacle_distance to None")

                # Check for obstacle and start avoidance
                if closest_obstacle and not avoiding_obstacle:
                    print(f"[DEBUG] Checking obstacle condition: distance = {obstacle_distance}, threshold = {APPROACH_DISTANCE}")
                    if obstacle_distance is not None and obstacle_distance <= APPROACH_DISTANCE:
                        status_text = "Obstacle Detected - Starting Avoidance"
                        print(f"[DEBUG] {status_text}")

                        try:
                            obstacle_x = closest_obstacle['x']
                            frame_center_x = frame.shape[1] / 2

                            if obstacle_x > frame_center_x:
                                serial_send(14, 0, FORWARD_SPEED)  # Diagonal left
                                status_text += " (Right Side) → Diagonal Left"
                            else:
                                serial_send(15, 0, FORWARD_SPEED)  # Diagonal right
                                status_text += " (Left Side) → Diagonal Right"
                            print(f"[DEBUG] Obstacle X: {obstacle_x}, Frame Center: {frame_center_x}")
                        except Exception as e:
                            print(f"[ERROR] Obstacle direction error: {e}")
                            serial_send(15, 0, FORWARD_SPEED)

                        obstacle_avoidance_start_time = time.time()
                        avoiding_obstacle = True
                        return

                # Handle obstacle avoidance state
                if avoiding_obstacle:
                    elapsed = time.time() - obstacle_avoidance_start_time

                    if elapsed < AVOIDANCE_TURN_DURATION:
                        status_text = f"Avoiding Obstacle: {AVOIDANCE_TURN_DURATION - elapsed:.1f}s remaining"
                        print(f"[DEBUG] {status_text}")
                        return
                    elif elapsed < AVOIDANCE_TURN_DURATION + AVOIDANCE_FORWARD_DURATION:
                        status_text = f"Clearing Forward: {(AVOIDANCE_TURN_DURATION + AVOIDANCE_FORWARD_DURATION) - elapsed:.1f}s remaining"
                        serial_send(2, 0, FORWARD_SPEED)
                        print(f"[DEBUG] {status_text}")
                        return
                    else:
                        serial_send(1, 0, 0)
                        avoiding_obstacle = False
                        ball_search_state = "BEGIN_SEARCH"
                        status_text = "Resuming Ball Search"
                        print(f"[DEBUG] {status_text}")


                    # --- Ball search pattern ---
                    if ball_search_state == "BEGIN_SEARCH":
                        ball_search_state = "TURN_TO_ZERO"
                        ball_search_target_yaw = 0.0
                        serial_send(3 if get_yaw_diff(0, current_yaw_value) > 0 else 4, 0, BASE_TURN_SPEED)
                        status_text = "Aligning to 0°"

                    elif ball_search_state == "TURN_TO_ZERO":
                        yaw_diff = get_yaw_diff(ball_search_target_yaw, current_yaw_value)
                        if abs(yaw_diff) <= YAW_TOLERANCE:
                            ball_search_state = "ROTATE_LEFT_90"
                            ball_search_target_yaw = (current_yaw_value + 180) % 360
                            serial_send(3, 0, BASE_TURN_SPEED)
                            status_text = f"Rotating Left to {ball_search_target_yaw:.1f}°"
                        else:
                            serial_send(3 if yaw_diff > 0 else 4, 0, BASE_TURN_SPEED)
                            status_text = f"Turning to 0°: {abs(yaw_diff):.1f}° remaining"

                    elif ball_search_state == "ROTATE_LEFT_90":
                        yaw_diff = get_yaw_diff(ball_search_target_yaw, current_yaw_value)
                        if abs(yaw_diff) <= YAW_TOLERANCE:
                            ball_search_state = "ROTATE_RIGHT_180"
                            ball_search_target_yaw = (current_yaw_value - 0) % 360
                            serial_send(4, 0, BASE_TURN_SPEED)
                            status_text = f"Rotating Right to {ball_search_target_yaw:.1f}°"
                        else:
                            status_text = f"Turning Left: {abs(yaw_diff):.1f}° remaining"

                    elif ball_search_state == "ROTATE_RIGHT_180":
                        yaw_diff = get_yaw_diff(ball_search_target_yaw, current_yaw_value)
                        if abs(yaw_diff) <= YAW_TOLERANCE:
                            ball_search_state = "RETURN_TO_ZERO"
                            ball_search_target_yaw = 0.0
                            serial_send(3, 0, BASE_TURN_SPEED)
                            status_text = "Returning to 0°"
                        else:
                            status_text = f"Turning Right: {abs(yaw_diff):.1f}° remaining"

                    elif ball_search_state == "RETURN_TO_ZERO":
                        yaw_diff = get_yaw_diff(ball_search_target_yaw, current_yaw_value)
                        if abs(yaw_diff) <= YAW_TOLERANCE:
                            ball_search_state = "MOVE_FORWARD"
                            ball_search_start_time = time.time()
                            #serial_send(2, 0, FORWARD_SPEED)
                            status_text = "Final: Moving Forward"
                        else:
                            status_text = f"Returning to 0°: {abs(yaw_diff):.1f}° remaining"

            # ----------------- BALL CENTERING ------------------
            else:
                try:
                    (x, y), radius = cv2.minEnclosingCircle(closest_ball["contour"])
                    ball_diameter_pixels = 2 * radius
                    ball_distance = (REAL_BALL_DIAMETER * focal_length) / ball_diameter_pixels
                    frame_center_x = frame.shape[1] / 2

                    if not centered_on_ball:
                        if x > frame_center_x + CENTER_THRESHOLD:
                            status_text = "Turning Right to Center on Ball"
                            serial_send(4, 0, BASE_TURN_SPEED)
                        elif x < frame_center_x - CENTER_THRESHOLD:
                            status_text = "Turning Left to Center on Ball"
                            serial_send(3, 0, BASE_TURN_SPEED)
                        else:
                            status_text = "Centered on Ball"
                            centered_on_ball = True
                            centering_start_time = time.time()
                            serial_send(1, 0, 0)
                    else:
                        if time.time() - centering_start_time > 1.0:
                            if x > frame_center_x + CENTER_THRESHOLD:
                                status_text = "Ball Drifted Right - Re-centering"
                                serial_send(1, 0, 0)
                                serial_send(4, 0, BASE_TURN_SPEED)
                                centered_on_ball = False
                                centering_start_time = None
                            elif x < frame_center_x - CENTER_THRESHOLD:
                                status_text = "Ball Drifted Left - Re-centering"
                                serial_send(1, 0, 0)
                                serial_send(3, 0, BASE_TURN_SPEED)
                                centered_on_ball = False
                                centering_start_time = None
                            elif ball_distance >= AVOIDANCE_DISTANCE:
                                status_text = "Moving Towards Ball"
                                serial_send(2, 0, FORWARD_SPEED)
                            else:
                                status_text = "Ball Reached - Starting Grab Sequence"
                                grabbing_state = "PREPARE_STOP"
                                grabbing_start_time = time.time()
                        else:
                            status_text = "Centering on Ball"
                            serial_send(1, 0, 0)


                    debug_text = f"Ball X: {int(x)} | Distance: {ball_distance:.2f} m"

                except Exception as e:
                    status_text = "Ball Detection Error"
                    print(f"Ball tracking error: {e}")

            # Overlay status
            cv2.putText(frame, status_text, (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (255, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, debug_text, (30, 90), cv2.FONT_HERSHEY_SIMPLEX,
                        0.7, (0, 255, 0), 2, cv2.LINE_AA)







        def handle_goal_sequence(closest_goal, frame, focal_length):
            global centered_on_goal, goal_centering_start_time, goal_sequence_completed
            global goal_search_state, goal_search_target_yaw, goal_search_start_time, current_yaw
            global GOAL_BASE_TURN_SPEED, GOAL_APPROACH_DISTANCE, GOAL_CENTER_THRESHOLD, GOAL_FORWARD_DURATION, GOAL_FORWARD_SPEED, GOAL_YAW_TOLERANCE
            global avoiding_obstacle, obstacle_avoidance_start_time

            # Initialize all required variables
            if 'goal_search_state' not in globals():
                goal_search_state = "BEGIN_SEARCH"
                goal_search_target_yaw = None
                goal_search_start_time = time.time()
            if 'avoiding_obstacle' not in globals():
                avoiding_obstacle = False
                obstacle_avoidance_start_time = None
            # Safely get current yaw value
            try:
                current_yaw_value = float(current_yaw) if isinstance(current_yaw, (int, float, str)) and str(current_yaw) != "N/A" else 0.0
            except (ValueError, TypeError):
                current_yaw_value = 0.0
                print("Warning: Invalid yaw value, defaulting to 0.0")

            def get_yaw_diff(target, current):
                """Calculate shortest yaw difference with wrapping"""
                return (target - current + 180) % 360 - 180

            status_text = "Goal Sequence Active"
            debug_text = ""


            # Compute obstacle distance if closest_obstacle is present
            if closest_obstacle:
                try:
                    obstacle_width_pixels = closest_obstacle['w']
                    obstacle_distance = (REAL_OBSTACLE_WIDTH * focal_length) / obstacle_width_pixels
                    print(f"[DEBUG] Calculated obstacle_distance: {obstacle_distance:.2f}")
                except Exception as e:
                    print(f"[ERROR] Failed to compute obstacle_distance: {e}")
                    obstacle_distance = None
            else:
                obstacle_distance = None
                print("[DEBUG] No closest_obstacle found, setting obstacle_distance to None")

            # Check for obstacle and start avoidance
            if closest_obstacle and not avoiding_obstacle:
                print(f"[DEBUG] Checking obstacle condition: distance = {obstacle_distance}, threshold = {APPROACH_DISTANCE}")
                if obstacle_distance is not None and obstacle_distance <= APPROACH_DISTANCE:
                    status_text = "Obstacle Detected - Starting Avoidance"
                    print(f"[DEBUG] {status_text}")

                    try:
                        obstacle_x = closest_obstacle['x']
                        frame_center_x = frame.shape[1] / 2

                        if obstacle_x > frame_center_x:
                            serial_send(14, 0, FORWARD_SPEED)  # Diagonal left
                            status_text += " (Right Side) → Diagonal Left"
                        else:
                            serial_send(15, 0, FORWARD_SPEED)  # Diagonal right
                            status_text += " (Left Side) → Diagonal Right"
                        print(f"[DEBUG] Obstacle X: {obstacle_x}, Frame Center: {frame_center_x}")
                    except Exception as e:
                        print(f"[ERROR] Obstacle direction error: {e}")
                        serial_send(15, 0, FORWARD_SPEED)

                    obstacle_avoidance_start_time = time.time()
                    avoiding_obstacle = True
                    return

            # Handle obstacle avoidance state
            if avoiding_obstacle:
                elapsed = time.time() - obstacle_avoidance_start_time

                if elapsed < AVOIDANCE_TURN_DURATION:
                    status_text = f"Avoiding Obstacle: {AVOIDANCE_TURN_DURATION - elapsed:.1f}s remaining"
                    print(f"[DEBUG] {status_text}")
                    return
                elif elapsed < AVOIDANCE_TURN_DURATION + AVOIDANCE_FORWARD_DURATION:
                    status_text = f"Clearing Forward: {(AVOIDANCE_TURN_DURATION + AVOIDANCE_FORWARD_DURATION) - elapsed:.1f}s remaining"
                    serial_send(2, 0, FORWARD_SPEED)
                    print(f"[DEBUG] {status_text}")
                    return
                else:
                    serial_send(1, 0, 0)
                    avoiding_obstacle = False
                    goal_search_state = "BEGIN_SEARCH"
                    status_text = "Resuming Ball Search"
                    print(f"[DEBUG] {status_text}")

            # Goal search behavior (when no goal detected)
            if not closest_goal:


                if goal_search_state == "BEGIN_SEARCH":
                    goal_search_state = "TURN_TO_ZERO"
                    goal_search_target_yaw = 0.0
                    serial_send(5 if get_yaw_diff(0, current_yaw_value) > 0 else 6, 0, GOAL_BASE_TURN_SPEED)
                    status_text = "Aligning to 0°"

                elif goal_search_state == "TURN_TO_ZERO":
                    yaw_diff = get_yaw_diff(goal_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= GOAL_YAW_TOLERANCE:
                        goal_search_state = "ROTATE_LEFT_90"
                        goal_search_target_yaw = (current_yaw_value + 60) % 360
                        serial_send(5, 0, GOAL_BASE_TURN_SPEED)
                        status_text = f"Rotating Left to {goal_search_target_yaw:.1f}°"
                    else:
                        serial_send(5 if yaw_diff > 0 else 6, 0, GOAL_BASE_TURN_SPEED)
                        status_text = f"Turning to 0°: {abs(yaw_diff):.1f}° remaining"

                elif goal_search_state == "ROTATE_LEFT_90":
                    yaw_diff = get_yaw_diff(goal_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= GOAL_YAW_TOLERANCE:
                        goal_search_state = "ROTATE_RIGHT_180"
                        goal_search_target_yaw = (current_yaw_value -60) % 360
                        serial_send(6, 0, GOAL_BASE_TURN_SPEED)
                        status_text = f"Rotating Right to {goal_search_target_yaw:.1f}°"
                    else:
                        status_text = f"Turning Left: {abs(yaw_diff):.1f}° remaining"

                elif goal_search_state == "ROTATE_RIGHT_180":
                    yaw_diff = get_yaw_diff(goal_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= GOAL_YAW_TOLERANCE:
                        goal_search_state = "RETURN_TO_ZERO"
                        goal_search_target_yaw = 0.0
                        serial_send(5, 0, GOAL_BASE_TURN_SPEED)
                        status_text = "Returning to 0°"
                    else:
                        status_text = f"Turning Right: {abs(yaw_diff):.1f}° remaining"

                elif goal_search_state == "RETURN_TO_ZERO":
                    yaw_diff = get_yaw_diff(goal_search_target_yaw, current_yaw_value)
                    if abs(yaw_diff) <= GOAL_YAW_TOLERANCE:
                        goal_search_state = "MOVE_FORWARD"
                        goal_search_start_time = time.time()
                        serial_send(2, 0, GOAL_FORWARD_SPEED)
                        status_text = "Final: Moving Forward"
                    else:
                        status_text = f"Returning to 0°: {abs(yaw_diff):.1f}° remaining"

                elif goal_search_state == "MOVE_FORWARD":
                    if time.time() - goal_search_start_time >= GOAL_FORWARD_DURATION:
                        goal_search_state = "BEGIN_SEARCH"
                        status_text = "Pattern Restarted"
                    else:
                        status_text = f"Moving: {GOAL_FORWARD_DURATION - (time.time() - goal_search_start_time):.1f}s left"

                debug_text = f"Yaw: {current_yaw_value:.1f}° | Target: {goal_search_target_yaw:.1f}°"

            # Normal goal handling (when goal is detected)
            else:
                goal_center_x = closest_goal['x'] + closest_goal['w'] / 2
                frame_center_x = frame.shape[1] / 2
                goal_width_pixels = closest_goal['w']
                goal_distance = (REAL_GOAL_WIDTH * focal_length) / goal_width_pixels

                if not centered_on_goal:
                    # Get the center of the goal (center of the bounding box)
                    # Check if the goal is outside the center threshold and move to adjust
                    if goal_center_x > frame_center_x + GOAL_CENTER_THRESHOLD:
                        status_text = "Turning Right to Center on Goal"
                        serial_send(6, 0, GOAL_BASE_TURN_SPEED)
                    elif goal_center_x < frame_center_x - GOAL_CENTER_THRESHOLD:
                        status_text = "Turning Left to Center on Goal"
                        serial_send(5, 0, GOAL_BASE_TURN_SPEED)
                    else:
                        status_text = "Centered on Goal"
                        centered_on_goal = True
                        goal_centering_start_time = time.time()
                        serial_send(1, 0, 0)  # Stop

                else:
                    # After centering, check if the goal has drifted and re-center if necessary
                    if time.time() - goal_centering_start_time > 1.0:
                        goal_center_x = closest_goal['x'] + closest_goal['w'] / 2
                        frame_center_x = frame.shape[1] / 2
                        
                        # If goal drifted right, move right to re-center
                        if goal_center_x > frame_center_x + GOAL_CENTER_THRESHOLD:
                            status_text = "Goal Drifted Right - Re-centering"
                            serial_send(1, 0, 0)
                            serial_send(6, 0, GOAL_BASE_TURN_SPEED)
                            centered_on_goal = False
                            goal_centering_start_time = None
                        
                        # If goal drifted left, move left to re-center
                        elif goal_center_x < frame_center_x - GOAL_CENTER_THRESHOLD:
                            status_text = "Goal Drifted Left - Re-centering"
                            serial_send(1, 0, 0)
                            serial_send(5, 0, GOAL_BASE_TURN_SPEED)
                            centered_on_goal = False
                            goal_centering_start_time = None

                    # If goal is centered, handle the approach or shooting action
                    else:
                        if goal_distance > GOAL_APPROACH_DISTANCE:
                            status_text = "Approaching Goal"
                            serial_send(2, 0, GOAL_FORWARD_SPEED)
                        else:
                            status_text = "Releasing and Shooting"
                            serial_send(1, 0, 0)  # Stop before action
                            serial_send(18, 0, 0)  # Open grabber to release ball
                            time.sleep(0.8)  # Optional delay to ensure ball drops
                            serial_send(9, 0, 0)  # Kick the ball
                            goal_sequence_completed = True

                debug_text = f"Distance: {goal_distance:.2f}m | GoalX: {int(goal_center_x)}"

            # Display status
            cv2.putText(frame, status_text, (30, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
            cv2.putText(frame, debug_text, (30, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)


        # --- Reset Sequences --- 
        def reset_sequences():
            global ball_sequence_completed, centered_on_ball, centering_start_time, closest_ball
            global goal_sequence_completed, centered_on_goal, goal_centering_start_time, closest_goal

            if ball_sequence_completed:
                print("DEBUG: Resetting Ball Sequence")
                ball_sequence_completed = False
                centered_on_ball = False
                centering_start_time = None
                closest_ball = None
                time.sleep(0.5)
            if goal_sequence_completed:
                print("DEBUG: Resetting Goal Sequence")
                goal_sequence_completed = False
                centered_on_goal = False
                goal_centering_start_time = None
                closest_goal = None
                time.sleep(0.5)

       
        # --- Main Processing Logic ---
        if start_keeper_active:
            print("DEBUG: Keeper Active")

            if not ball_sequence_completed:
                print("DEBUG: Executing Ball Sequence")
                handle_ball_sequence(closest_ball, frame, focal_length)

            else:
                print("DEBUG: Ball Sequence Completed — Resetting")
                reset_sequences()




        # Convert the frame to RGB for displaying in the Tkinter label
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        # Update the video_display label with the new frame
        video_display.imgtk = imgtk
        video_display.configure(image=imgtk)

        # Repeat the process after 30 milliseconds
        video_display.after(10, update_frame)

    update_frame()




# Initialize the interface
create_interface()
root.mainloop()

