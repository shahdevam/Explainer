import tkinter as tk
from tkinter import ttk, font
import pyperclip
import requests
import keyboard

# Settings
HOTKEY = 'ctrl+alt+e'
API_KEY = 'AIzaSyB9m_qJ3Pphm_HPCADIfelA01v0AmhW0Zw'  # Replace with your actual Gemini key
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

# UI Configuration
BG_COLOR = "#F0F0F0"
TEXT_COLOR = "#333333"
BUTTON_COLOR = "#4CAF50"  # Green
FONT_NAME = "Segoe UI"
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 300

def get_explanation(text):
    try:
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "contents": [{
                "parts": [{"text": f"Explain this in simple terms for a non-technical user: {text}"}]
            }]
        }
        response = requests.post(
            f"{GEMINI_URL}?key={API_KEY}",
            headers=headers,
            json=data
        )
        response.raise_for_status()  # Raise an error for bad status codes
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"Error getting explanation: {str(e)}"

def show_bubble(explanation):
    root = tk.Tk()
    root.title("Smart Explanation")
    root.configure(bg=BG_COLOR)
    
    # Center window
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - WINDOW_WIDTH) // 2
    y = (screen_height - WINDOW_HEIGHT) // 2
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
    
    # Custom font
    custom_font = font.Font(family=FONT_NAME, size=10)
    title_font = font.Font(family=FONT_NAME, size=12, weight="bold")
    
    # Main frame
    main_frame = ttk.Frame(root, padding=15)
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    # Title
    title_label = ttk.Label(main_frame, text="Explanation", font=title_font, 
                           foreground="#2C3E50", background=BG_COLOR)
    title_label.pack(pady=(0, 10))
    
    # Text area with scrollbar
    text_frame = ttk.Frame(main_frame)
    text_frame.pack(fill=tk.BOTH, expand=True)
    
    text_area = tk.Text(text_frame, wrap=tk.WORD, font=custom_font, 
                       bg="white", fg=TEXT_COLOR, padx=10, pady=10,
                       relief="flat", highlightthickness=2,
                       highlightbackground="#D0D0D0")
    text_area.insert(tk.END, explanation)
    text_area.config(state=tk.DISABLED)
    
    scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_area.yview)
    text_area.configure(yscrollcommand=scrollbar.set)
    
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    # Close button
    close_button = ttk.Button(main_frame, text="Close", command=root.destroy,
                             style="Custom.TButton")
    close_button.pack(pady=10)
    
    # Style configuration
    style = ttk.Style()
    style.configure("Custom.TButton", font=(FONT_NAME, 10, "bold"),
                    foreground="white", background=BUTTON_COLOR,
                    bordercolor=BUTTON_COLOR, focuscolor=BG_COLOR)
    
    root.mainloop()

def main():
    print(f"Program running! Press {HOTKEY} to get explanations")
    keyboard.add_hotkey(HOTKEY, lambda: show_bubble(
        get_explanation(pyperclip.paste())
    ))
    keyboard.wait()

if __name__ == "__main__":
    main()