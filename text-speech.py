import pyttsx3
import customtkinter as ctk

# Initialize pyttsx3
engine = pyttsx3.init()

# Function to convert text to speech
def speak():
    text = text_entry.get("1.0", "end").strip()
    if text:
        engine.say(text)
        engine.runAndWait()

# Function to change voice
def change_voice(choice):
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id if choice == "Male" else voices[1].id)

# Function to change rate
def change_rate(value):
    engine.setProperty('rate', int(float(value)))

# Function to change volume
def change_volume(value):
    engine.setProperty('volume', float(value))

# Initialize CustomTkinter
ctk.set_appearance_mode("dark")  # Dark mode
ctk.set_default_color_theme("blue")

# GUI Setup
root = ctk.CTk()
root.title("Text-to-Speech")
root.geometry("400x450")

# Text Entry
text_entry = ctk.CTkTextbox(root, height=100, width=350)
text_entry.pack(pady=10)

# Speak Button
speak_button = ctk.CTkButton(root, text="Speak", command=speak)
speak_button.pack(pady=5)

# Voice Selection
ctk.CTkLabel(root, text="Voice:").pack()
voice_var = ctk.StringVar(value="Male")
voice_dropdown = ctk.CTkOptionMenu(root, variable=voice_var, values=["Male", "Female"], command=change_voice)
voice_dropdown.pack()

# Rate Slider
ctk.CTkLabel(root, text="Rate:").pack()
rate_slider = ctk.CTkSlider(root, from_=100, to=300, command=change_rate)
rate_slider.pack()
rate_slider.set(200)

# Volume Slider
ctk.CTkLabel(root, text="Volume:").pack()
volume_slider = ctk.CTkSlider(root, from_=0, to=1, command=change_volume)
volume_slider.pack()
volume_slider.set(1)

# Run the App
root.mainloop()
