import tkinter as tk
import mss
import easyocr
import numpy as np
import time
import pyautogui
import keyboard
import random

pyautogui.FAILSAFE = False

# --- Wordlist Loading ---
def load_wordlist(filename):
    """Loads a set of words from a text file, one word per line."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return set(line.strip().lower() for line in f if line.strip())
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return set()

# --- Interactive OCR Box ---
class MovableResizableBox(tk.Tk):
    def __init__(self, x=1233, y=235, w=89, h=40):
        super().__init__()

        self.overrideredirect(True)
        self.attributes("-topmost", True)
        self.attributes("-transparentcolor", "black")
        self.configure(bg="black")
        self.geometry(f"{w}x{h}+{x}+{y}")

        self.res_border = 12
        self.min_w = 30
        self.min_h = 20

        self.drag_mode = None

        self.start_mouse_x = 0
        self.start_mouse_y = 0
        self.start_win_x = 0
        self.start_win_y = 0
        self.start_w = 0
        self.start_h = 0

        self.canvas = tk.Canvas(self, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.rect = self.canvas.create_rectangle(
            2, 2, w - 2, h - 2,
            outline="red", width=2
        )

        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
        self.canvas.bind("<Motion>", self.on_mouse_motion)
        self.bind("<Configure>", self.on_configure)

    def get_box(self):
        geo = self.geometry()
        dims, pos = geo.split('+', 1)
        w, h = map(int, dims.split('x'))
        x, y = map(int, pos.split('+'))
        return {"left": x, "top": y, "width": w, "height": h}

    def on_mouse_down(self, event):
        self.start_mouse_x = event.x_root
        self.start_mouse_y = event.y_root
        self.start_win_x = self.winfo_x()
        self.start_win_y = self.winfo_y()
        self.start_w = self.winfo_width()
        self.start_h = self.winfo_height()

        if self.start_w - event.x < self.res_border and self.start_h - event.y < self.res_border:
            self.drag_mode = "resize"
        else:
            self.drag_mode = "move"

    def on_mouse_drag(self, event):
        dx = event.x_root - self.start_mouse_x
        dy = event.y_root - self.start_mouse_y

        if self.drag_mode == "move":
            self.geometry(f"{self.start_w}x{self.start_h}+{self.start_win_x + dx}+{self.start_win_y + dy}")
        elif self.drag_mode == "resize":
            self.geometry(
                f"{max(self.min_w, self.start_w + dx)}x{max(self.min_h, self.start_h + dy)}+"
                f"{self.start_win_x}+{self.start_win_y}"
            )

    def on_mouse_up(self, event):
        self.drag_mode = None

    def on_mouse_motion(self, event):
        if self.winfo_width() - event.x < self.res_border and self.winfo_height() - event.y < self.res_border:
            self.config(cursor="size_nw_se")
            self.canvas.config(cursor="size_nw_se")
        else:
            self.config(cursor="fleur")
            self.canvas.config(cursor="fleur")

    def on_configure(self, event):
        self.canvas.coords(self.rect, 2, 2, event.width - 2, event.height - 2)

# --- EasyOCR Setup ---
# CHANGE LANGUAGE HERE: e.g., ['en'] for English, ['it'] for Italian
reader = easyocr.Reader(['it'], gpu=True)

def read_ocr_from_box(box):
    """Captures the screen region defined by the box and performs OCR."""
    coords = box.get_box()
    with mss.mss() as sct:
        img = np.array(sct.grab(coords))
        results = reader.readtext(img)
        return results[0][1].strip().lower() if results else ""

# --- Word Suggestions ---
def suggest_words(wordlist, syllable, used_words, top=2):
    """Returns words containing the syllable that haven't been used yet, sorted by length."""
    words = [w for w in wordlist if syllable in w and w not in used_words]
    words.sort(key=len, reverse=True)
    return words[:top]

# --- Simulated Typing ---
def type_simulated_word(word):
    """Types the word with human-like delays."""
    for i, ch in enumerate(word):
        pyautogui.write(ch)
        time.sleep(0.01 if i + 1 < len(word) and word[i + 1] == ch else random.uniform(0.002, 0.005))
    pyautogui.press('enter')

# --- MAIN ---
def main():
    wordlist = load_wordlist("wordlist.txt")
    if not wordlist:
        return

    box = MovableResizableBox()
    box.update()

    used_words = set()
    ready_words = ["", ""]
    last_syllable = ""

    def type_first(event):
        nonlocal ready_words
        word = ready_words[0]
        if word:
            type_simulated_word(word)
            used_words.add(word)
            ready_words[0] = ""  # Prevent double submission
            print(f"✍️ First word used: {word}")

    def type_second(event):
        nonlocal ready_words
        word = ready_words[1]
        if word:
            type_simulated_word(word)
            used_words.add(word)
            ready_words[1] = ""
            print(f"✍️ Second word used: {word}")

    keyboard.on_press_key('0', type_first)
    keyboard.on_press_key('9', type_second)

    print("🚀 Script running! Place the red box over the syllable area.")
    print("Keys: '0' for the first suggestion, '9' for the second suggestion.")

    try:
        while True:
            syllable = read_ocr_from_box(box)
            if syllable and syllable != last_syllable:
                last_syllable = syllable
                words = suggest_words(wordlist, syllable, used_words)

                ready_words = ["", ""]
                if words:
                    ready_words[:len(words)] = words
                    print(f"\n🎯 Syllable: {syllable}")
                    for i, p in enumerate(words):
                        print(f"🔥 Option {i+1}: {p}")
                else:
                    print(f"💣 No words available for '{syllable}' (all used or none found)")

            time.sleep(0.4)
            box.update()

    except KeyboardInterrupt:
        print("\n👋 Exiting...")

if __name__ == "__main__":
    main()
