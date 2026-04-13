# Word Suggestion Bot (OCR-based - Created for Word Bomb)

A Python-based utility that automatically suggests words containing specific syllables by reading them directly from your screen using OCR. Designed for word games like BombParty.

## ✨ Features
- **Real-time OCR**: Uses `EasyOCR` to capture syllables from a specific screen area.
- **Movable & Resizable Box**: A red interactive frame allows you to define exactly where the script should look for text.
- **Smart Suggestions**: Suggests the longest available words first.
- **Fast Automation**: Quickly types suggestions using simulated keyboard input.
- **Multi-suggestion Support**: Provides up to 2 suggestions accessible via hotkeys.

## 🛠️ Requirements
- Python 3.8+
- Dependencies: `easyocr`, `mss`, `numpy`, `pyautogui`, `keyboard`, `tkinter`

Install dependencies using:
```bash
pip install easyocr mss numpy pyautogui keyboard
```

## 🚀 How to Use
1. **Prepare the Wordlist**: Ensure a `wordlist.txt` file exists in the project directory (one word per line).
2. **Launch the Script**:
   ```bash
   python script.py
   ```
3. **Position the Box**: A red frame will appear. Drag it over the area where the syllable is displayed on your screen. You can resize it by dragging the bottom-right corner.
4. **Suggestions**:
   - The script will print suggestions in the console as it detects new syllables.
   - Press **`0`** to automatically type the **first** suggestion.
   - Press **`9`** to automatically type the **second** suggestion.

## 🌍 Language Customization

### Changing OCR Language
By default, the script is set to **Italian**. To change the OCR language:
1. Open `script.py`.
2. Find the line:
   ```python
   reader = easyocr.Reader(['it'], gpu=True)
   ```
3. Change `['it']` to your desired language code (e.g., `['en']` for English, `['fr']` for French).

### Wordlists
- The **provided `wordlist.txt` is in Italian**.
- If you switch languages, you **must replace `wordlist.txt`** with a wordlist corresponding to that language.

## ⚠️ Important Notes
- **Admin Privileges**: The `keyboard` library may require administrator/sudo privileges on some systems to capture hotkeys globally.
- **OCR Accuracy**: Lighting, font size, and background colors can affect OCR performance. Adjust the red box for best results.
- **Simulation Speed**: The typing speed is randomized slightly to appear more human-like, but use it responsibly.

## 📜 License
This project is open-source and available under the MIT License.
