import sys
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import re
import timer
import requests

api_url = "https://script.google.com/macros/s/AKfycbwf7b9iX95GYqmeO5T0QfoXtBMrjyHbNuYITHpqLoG9OATzGEwEThZTKD9yYsING4c/exec"

def insert_user(email, student_number):
    """Function to insert email and student_number into Google Sheets via Google Apps Script."""
    try:
        data = {
            'email': email,
            'student_number': student_number
        }
        response = requests.post(api_url, json=data)
        if response.status_code == 200 and response.json().get("status") == "success":
            return True
        else:
            print(f"Error: {response.text}")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def on_submit():
    email = name_input.text()
    student_number = student_number_input.text()

    # Validate email format (must be a TIP email)
    if not re.match(r'^[\w\.-]+@tip\.edu\.ph$', email):
        QMessageBox.warning(win, "Email Error", "Please enter a valid TIP email.")
        return

    # Validate student number (must be 7 digits)
    if len(student_number) != 7:
        QMessageBox.warning(win, "Student Number Error", "Please enter a valid Student Number.")
        return

    # Attempt to insert the user data
    success = insert_user(email, student_number)

    if success:
        print(f"Inserted into Google Sheets: Email: {email}, Student Number: {student_number}")
        # Clear the input fields after submission
        name_input.clear()
        student_number_input.clear()

        # Hide the MainWindow
        win.hide()

        global timer_window
        # Pass the email and student number to the timer window and show it
        timer_window = timer.start_timer(email, student_number)
        # Connect the timer_closed signal to a function that will show the main window
        timer_window.timer_closed.connect(show_main_window)
    else:
        QMessageBox.critical(win, "Submission Error", "Failed to insert data into Google Sheets.")

def show_main_window():
    """Function to show the main window when the timer window is closed."""
    win.show()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(800, 300, 500, 500)
        self.setWindowTitle("Open Lab")
        self.setWindowIcon(QIcon("logo.png"))
        self.setToolTip("OpenLab")

        self.set_background("b1.png")  

        window_width = self.width()
        window_height = self.height()
        input_width = 200
        input_height = 30
        button_width = 100
        button_height = 30
        x_center = (window_width - input_width) // 2
        y_center = (window_height // 2) - 60

        global name_input
        name_input = QLineEdit(self)
        name_input.setPlaceholderText("Enter your Email")
        name_input.setGeometry(x_center, y_center, input_width, input_height)
        name_input.setStyleSheet("border: 2px solid gray; border-radius: 10px; padding: 5px;")

        global student_number_input
        student_number_input = QLineEdit(self)
        student_number_input.setPlaceholderText("Enter your Student Number")
        student_number_input.setGeometry(x_center, y_center + 50, input_width, input_height)
        student_number_input.setStyleSheet("border: 2px solid gray; border-radius: 10px; padding: 5px;")
        
        int_validator = QIntValidator(0, 9999999)
        student_number_input.setValidator(int_validator)

        login_button = QPushButton("Start Session", self)
        login_button.setGeometry((window_width - button_width) // 2, y_center + 100, button_width, button_height)
        login_button.setStyleSheet("""
            QPushButton {
                border: 2px solid gray;
                border-radius: 15px;
                background-color: #A3C1DA;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #BCD2E8;
            }
        """)
        login_button.clicked.connect(on_submit)
    
    def set_background(self, image_path):
        """Set background image of the window."""
        background = QPixmap(image_path)

        background = background.scaled(self.size(), QtCore.Qt.IgnoreAspectRatio)

        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(palette)

    def closeEvent(self, event):
        """Override the closeEvent to disable window closing."""
        reply = QMessageBox.question(self, 'Close Confirmation',
                                     "This application is required and must fill up",
                                     QMessageBox.Ok, QMessageBox.Ok)

        if reply == QMessageBox.Ok:
            event.accept()
        else:
            event.ignore()

def window():
    app = QApplication(sys.argv)
    global win
    win = MainWindow()
    win.setWindowFlags(QtCore.Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    win.show()
    sys.exit(app.exec_())

window()
