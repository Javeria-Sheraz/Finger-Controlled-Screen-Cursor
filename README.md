# Finger-Controlled Screen Cursor 🎯🖐️

Control your computer's **mouse cursor, click**, and even **scroll** — just by using hand gestures in the air!
Built using **OpenCV**, **MediaPipe**, **Autopy**, and **PyAutoGUI** libraries, this project leverages computer vision to offer a touchless interface using finger tracking.

## ✨ Features/Instructions

* **Move Cursor**: Raise your index finger and thumb to move the cursor on the screen.
* **Click**: Bring thumb and index finger together for a click action.
* **Scroll**: Raise both index and middle fingers and bring them together to scroll.

---

### ▶️ How to Run


### 1. Open your IDE or terminal window.

### 2. Clone the repository:

   ```
   git clone https://github.com/Javeria-Sheraz/Finger-Controlled-Screen-Cursor.git
   ```

### 3. Change the directory:

   ```
   cd Finger-Controlled-Screen-Cursor
   ```

### 4. Create a virtual environment:

```
python -m venv venv
```
Ensure the venv folder is created in the cloned repo folder

### 5. Activate the environment (for CMD terminal):

```
venv\Scripts\activate
```

> ⚠️ If you're using PowerShell and encounter script permission errors:

```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 6. Ensure `required_libraries.txt` is in the same folder. Install the required libraries:

```
pip install -r required_libraries.txt
```
### 7. Run the main file:

```
python screenmouse.py
```

 **Use your webcam** to control the cursor, click, and scroll using your fingers!

---

## 📌 Notes

* Ensure your webcam is connected.
* Adjust `frameReduction` and `smoothen` values in the script for better performance on different screen sizes.
* The system is optimized for a single hand with distinct gestures.

---

**Javeria Sheraz**
[LinkedIn](https://www.linkedin.com/in/javeria-sheraz) • [GitHub](https://github.com/Javeria-Sheraz)


