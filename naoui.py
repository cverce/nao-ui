## NAOUI ##
# This code only works for python 2.7.18 due to naoqi limitations

#To add movements to the list: add movements description in function execute_movements (line 140). 
# then add the button to the interface (line 372).

import Tkinter as tk
from PIL import Image, ImageTk
import naoqi
import numpy as np
import cv2
import threading
import time
import random

# CONNECT TO NAO
robot_ip = "000.000.0.00"
port = 0000
video_proxy = naoqi.ALProxy("ALVideoDevice", robot_ip, port)

def enable_artificial_life():
    if artificial_life_enabled.get():
        try:
            # Enable tracking and head movement
            tracker = naoqi.ALProxy("ALTracker", robot_ip, port)
            tracker.registerTarget("Face", 0.0)
            tracker.setMode("Move")
            mov = naoqi.ALProxy("ALMotion", robot_ip, port)
            mov.setStiffnesses("Head", 1.0)
        except RuntimeError:
            print("Error: Could not initialize head movement.")
    else:
        try:
            # Disable head movement
            mov = naoqi.ALProxy("ALMotion", robot_ip, port)
            mov.setStiffnesses("Head", 0.0)
        except RuntimeError:
            print("Error: Could not disable head movement.")

def speak_and_perform_gesture(text, volume=None):
    try:
        # Initialization of ALTextToSpeech and ALMotion
        tts = naoqi.ALProxy("ALTextToSpeech", robot_ip, port)
        motion = naoqi.ALProxy("ALMotion", robot_ip, port)
        volume= get_current_volume()

        if volume is None:
            volume = 0.5  # Set default volume if None

        tts.setVolume(volume)

        # Function to perform gesture if enabled
        def perform_gesture():
            if gestures_enabled.get():  # If gestures are enabled
                # Randomly select arm (Right or Left)
                arm = random.choice(["R", "L"])
                
                if arm == "R":
                    names = ['RShoulderPitch', 'RShoulderRoll', 'RElbowYaw', 'RElbowRoll', 'RWristYaw', 'RHand']
                    angles = [0.7, -0.3, 1.5, 0.5, 1.7, 0]
                else:  # Left arm
                    names = ['LShoulderPitch', 'LShoulderRoll', 'LElbowYaw', 'LElbowRoll', 'LWristYaw', 'LHand']
                    angles = [0.7, 0.3, -1.5, -0.5, -1.7, 0]
                
                # Perform the arm movement
                max_speed = 0.4
                motion.setAngles(names, angles, max_speed)
                
                time.sleep(0.5)
                
                # Speak the text
                tts.say(text)
                
                # Reset arm to default position
                motion.setAngles(names[0], 0.7 if arm == "R" else 0.7, 0.2)  # Adjust shoulder pitch
                motion.setAngles(names[1], 0.0, 0.2)  # Reset shoulder roll
                motion.setAngles(names[2], 0.0, 0.2)  # Elbow yaw remains unchanged
                #motion.setAngles(names, [0.0] * len(angles), 0.2)
            else:
                # Speak directly if gestures are not enabled
                tts.say(text)

        # Start speech and gesture actions in separate thread
        gesture_thread = threading.Thread(target=perform_gesture)
        gesture_thread.start()

        # Wait for the gesture thread to finish 
        gesture_thread.join()

    except Exception as e:
        print("Error:", e)


# Funzione to manage button click
def on_speak_button_click():
    text = text_entry.get()  # Retrieve text to be spoken
    speak_and_perform_gesture(text)

# Function to get current volume
def get_current_volume():
    try:
        tts = naoqi.ALProxy("ALTextToSpeech", robot_ip, port)
        return tts.getVolume()
    except Exception as e:
        print("Error getting volume:", e)
        return 0.7  # default volume

# Function to set volume
def set_volume(*args):
    try:
        volume = float(volume_scale.get()) / 100
        tts = naoqi.ALProxy("ALTextToSpeech", robot_ip, port)
        tts.setVolume(volume)
    except Exception as e:
        print("Error setting volume:", e)

# Function to execute movements
def execute_movement(movement_name=None):
    if movement_name is None:
        movement_name = movement_var.get()
    try:
        motion = naoqi.ALProxy("ALMotion", robot_ip, port)
        posture = naoqi.ALProxy("ALRobotPosture", robot_ip, port)
        
        motion.wakeUp()

        if movement_name == "Wave":
            motion.setAngles("RShoulderPitch", 0.5, 0.2)
            motion.setAngles("RShoulderRoll", -0.3, 0.2)
            motion.setAngles("RElbowRoll", 1.5, 0.2)
            motion.setAngles("RWristYaw", 0.0, 0.2)
            motion.setAngles("RHand", 0.0, 0.2)
            
        elif movement_name == "Stand up":
            posture.goToPosture("Stand", 0.8)
            
        elif movement_name == "Sit down":
            posture.goToPosture("Sit", 0.8)

        ## ADD MOVEMENTS HERE ##
            
    except Exception as e:
        print("Error executing movement:", e)

def toggle_help():
    # Toggle visibility of the help text
    if help_label.winfo_ismapped():
        help_label.pack_forget()
        mix_frame.config(width=300)  # Restore original width
    else:
        help_label.pack(pady=5, padx=10, fill="x")
        mix_frame.config(width=500)  # Expand width to accommodate help text


# Function to add action to mix
def add_to_mix():
    action_type = mix_type_var.get()
    if action_type == "Movement":
        action = movement_var.get()
    else:  # Speech
        action = text_entry.get()
        if not action:
            return
        
        if gestures_enabled.get():
            action = "{} (Gestures Enabled)".format(action)
    
    mix_listbox.insert(tk.END, "%s: %s" % (action_type, action))
    
# Function to remove selected action from mix
def remove_from_mix():
    try:
        selection = mix_listbox.curselection()
        if selection:
            mix_listbox.delete(selection)
    except:
        pass

# Function to execute mix
def execute_mix():
    def execute_actions():
        actions = mix_listbox.get(0, tk.END)
        try: 
            volume_value = volume_scale.get()
        except:
             volume_value = 50  # Default value in case it's None
            
        volume = float(volume_value) / 100

        for action in actions:
            action = action.strip()  # Remove extra white spaces
            
            if ": " not in action:
                continue  

            action_type, value = action.split(": ", 1)
            gestures_state = "Enabled" if "(Gestures Enabled)" in value else "Disabled"
            
            if action_type == "Movement":
                execute_movement(value)
            else:  # Speech
                value = value.replace(" (Gestures Enabled)", "")
                speak_and_perform_gesture(value, volume=volume)
            
            time.sleep(0.2)  # Small delay between actions
        
        # Re-enable the button after execution
        execute_mix_button.config(state=tk.NORMAL)
    
    # Disable the button during execution
    execute_mix_button.config(state=tk.DISABLED)
    
    # Start execution in a separate thread
    thread = threading.Thread(target=execute_actions)
    thread.start()

# Function to update the image in the GUI
def update_image():
    if camera_active:
        try:
            video_data = video_proxy.getImageRemote(video_client)
            
            if video_data is not None:
                width = video_data[0]
                height = video_data[1]
                raw_data = video_data[6]
                
                image = np.frombuffer(raw_data, dtype=np.uint8).reshape((height, width, 3))
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                
                img = Image.fromarray(image_rgb)
                aspect_ratio = img.width / img.height
                new_height = 400
                new_width = int(new_height * aspect_ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)
                
                img_tk = ImageTk.PhotoImage(image=img)
                label.config(image=img_tk)
                label.image = img_tk
            else:
                print("Image not available")
        except Exception as e:
            print("Error acquiring image:", e)

    root.after(100, update_image)

# Function for the button that makes NAO speak
def on_speak_button_click():
    text = text_entry.get()
    if text:
        speak_and_perform_gesture(text)
    else:
        speak_and_perform_gesture("Please enter a message!")

# Function to toggle the camera
def toggle_camera():
    global video_client
    global camera_active
    
    if camera_active:
        video_proxy.unsubscribe(video_client)
        camera_active = False
        camera_button.config(text="Start Camera")
    else:
        video_client = video_proxy.subscribeCamera("test_video", 0, video_resolution, color_space, fps)
        camera_active = True
        camera_button.config(text="Stop Camera")

# Function to move up the selected action in the list
def move_up():
    selected = mix_listbox.curselection()
    if selected:
        index = selected[0]
        if index > 0:
            # Get the selected item and its position
            item = mix_listbox.get(index)
            mix_listbox.delete(index)
            mix_listbox.insert(index - 1, item)
            mix_listbox.select_set(index - 1)

# Function to move down the selected action in the list
def move_down():
    selected = mix_listbox.curselection()
    if selected:
        index = selected[0]
        if index < mix_listbox.size() - 1:
            # Get the selected item and its position
            item = mix_listbox.get(index)
            mix_listbox.delete(index)
            mix_listbox.insert(index + 1, item)
            mix_listbox.select_set(index + 1)



# Camera settings
video_resolution = 2
color_space = 11
fps = 15
camera_active = False

# Setup the main window
root = tk.Tk()
root.title("NAO Control Interface")

# Main container with grid layout
main_container = tk.Frame(root)
main_container.pack(padx=10, pady=10, fill="both", expand=True)

# Configure columns
for i in range(3):  # Now we have 3 columns
    main_container.grid_columnconfigure(i, weight=1)


## CAMERA SECTION (Left Column) ##
camera_frame = tk.Frame(main_container)
camera_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

camera_title = tk.Label(camera_frame, text="Camera", font=("Helvetica", 16, "bold"))
camera_title.pack(pady=5)

label = tk.Label(camera_frame)
label.pack()

camera_button = tk.Button(camera_frame, text="Start Camera", command=toggle_camera)
camera_button.pack(pady=5)

## CONTROLS SECTION (Middle Column) ##
controls_frame = tk.Frame(main_container)
controls_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

# Volume Control Section
volume_frame = tk.LabelFrame(controls_frame, text="Volume Control", font=("Helvetica", 12, "bold"))
volume_frame.pack(padx=5, pady=5, fill="x")

current_volume = int(get_current_volume() * 100)
volume_scale = tk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                       command=set_volume, label="Volume %")
current_volume = float(get_current_volume() * 100)
volume_scale.set(current_volume)
volume_scale.pack(pady=5, padx=5, fill="x")


# Artificial Life Control Section
artificial_life_frame = tk.LabelFrame(controls_frame, text="Artificial Life", font=("Helvetica", 12, "bold"))
artificial_life_frame.pack(padx=5, pady=5, fill="x")

artificial_life_enabled = tk.BooleanVar(value=True)
artificial_life_checkbox = tk.Checkbutton(artificial_life_frame, text="Enable Head Movement", 
                                          variable=artificial_life_enabled, command=enable_artificial_life)
artificial_life_checkbox.pack(pady=5, padx=5, fill="x")


# Speech Section
gestures_enabled = tk.BooleanVar(value=True) 
speech_frame = tk.LabelFrame(controls_frame, text="Speech", font=("Helvetica", 12, "bold"))
speech_frame.pack(padx=5, pady=5, fill="x")

text_entry = tk.Entry(speech_frame, width=30)
text_entry.pack(pady=5, padx=5, fill="x")

speak_button = tk.Button(speech_frame, text="Make NAO Speak", command=on_speak_button_click)
speak_button.pack(pady=5)

gesture_checkbox = tk.Checkbutton(speech_frame, text="Enable gestures", variable=gestures_enabled)
gesture_checkbox.pack(pady=5)

# Movement Section
movement_frame = tk.LabelFrame(controls_frame, text="Movement", font=("Helvetica", 12, "bold"))
movement_frame.pack(padx=5, pady=5, fill="x")

movement_var = tk.StringVar(value="Wave")
movements = ["Wave", "Stand up", "Sit down"] ## ADD MOVEMENTS HERE ##
for movement in movements:
    rb = tk.Radiobutton(movement_frame, text=movement, variable=movement_var, value=movement)
    rb.pack(anchor="w", padx=5)

execute_button = tk.Button(movement_frame, text="Execute Movement", command=execute_movement)
execute_button.pack(pady=5)

# MIX SECTION (Right Column)
mix_frame = tk.Frame(main_container)
mix_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

# Frame for title and help button
title_frame = tk.Frame(mix_frame)
title_frame.pack(fill="x", pady=5)

# Title label
mix_title = tk.Label(title_frame, text="Create a Mix", font=("Helvetica", 16, "bold"))
mix_title.pack(side="left", padx=5)

# Help button
help_button = tk.Button(title_frame, text="?", command=toggle_help, font=("Helvetica", 12))
help_button.pack(side=tk.RIGHT, padx=5) 
# Help text label (initially hidden)
help_label = tk.Label(mix_frame, text="A Mix consists of speech and movement actions. First, set the parameters for the action in the adjacent column. Once you're satisfied with the settings, select the type of action and click 'Add to Mix' to add it to your list. You can then remove, reorder, or execute the list.", wraplength=400)


# Action type selection
mix_type_var = tk.StringVar(value="Speech")
mix_type_frame = tk.Frame(mix_frame)
mix_type_frame.pack(fill="x", pady=5)

tk.Radiobutton(mix_type_frame, text="Speech", variable=mix_type_var, 
               value="Speech").pack(side=tk.LEFT, padx=5)
tk.Radiobutton(mix_type_frame, text="Movement", variable=mix_type_var, 
               value="Movement").pack(side=tk.LEFT, padx=5)

# Add to Mix button
add_button = tk.Button(mix_frame, text="Add to Mix", command=add_to_mix, width=15)
add_button.pack(pady=5, anchor= 'w')

# Mix list
mix_listbox_frame = tk.Frame(mix_frame)
mix_listbox_frame.pack(fill="both", expand=True, pady=5)

mix_listbox = tk.Listbox(mix_listbox_frame, height=10, width=40)
mix_listbox.pack(side=tk.LEFT, pady=5, fill="both", expand=True)

# Buttons to the right of the listbox
button_frame = tk.Frame(mix_listbox_frame)
button_frame.pack(side=tk.LEFT, padx=10, pady=5)

remove_button = tk.Button(button_frame, text="Remove", command=remove_from_mix)
remove_button.pack(fill="x", pady=5)

move_up_button = tk.Button(button_frame, text="Move Up", command=move_up)
move_up_button.pack(fill="x", pady=5)

move_down_button = tk.Button(button_frame, text="Move Down", command=move_down)
move_down_button.pack(fill="x", pady=5)

# Execute Mix button
execute_mix_button = tk.Button(mix_frame, text="Execute Mix", command=execute_mix)
execute_mix_button.pack(pady=5)

# Warning Label
warning_label = tk.Label(mix_frame, text="Warning: Once you press 'Execute Mix', you cannot modify the mix.", 
                         fg="red", font=("Helvetica", 10, "italic"))
warning_label.pack(pady=10)


# Start the image update process
update_image()

# Start the GUI
root.mainloop()

# Release the camera at the end
if camera_active:
    video_proxy.unsubscribe(video_client)