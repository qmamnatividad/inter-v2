import sys
import requests
from PyQt5.QtWidgets import QInputDialog, QApplication, QMainWindow, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon, QIntValidator, QPixmap, QPalette, QBrush
from PyQt5.QtCore import Qt
from PyQt5 import QtCore
import re
import timer
from datetime import datetime
import os

def resource_path(relative_path):
    """ Get the absolute path to the resource, works for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

api_url = "https://script.google.com/macros/s/AKfycbxTvN_1fd5a7uzsKpD0wOxvK3JBGrq35c-LLJE0Wvwo3gfGjEjhN5akBg5AkbC7bLSU/exec"

def insert_user(email, student_number, date, time):
    current_time = datetime.now()
    date = current_time.strftime("%Y-%m-%d")  # Separate date
    time = current_time.strftime("%I:%M:%S %p")  # Separate time in 12-hour format

    try:
        headers = {'Content-Type': 'application/json'}
        data = {
            'email': email,
            'student_number': student_number,
            'date': date,  
            'time': time  
        }
        response = requests.post(api_url, json=data, headers=headers)  # Add headers for JSON
        if response.status_code == 200 and response.json().get("status") == "success":
            return True
        else:
            return False
    except Exception as e:
        return False


def on_submit():
    email = name_input.text()
    student_number = student_number_input.text()

    current_time = datetime.now()
    date = current_time.strftime("%Y-%m-%d")  # Separate date
    time = current_time.strftime("%I:%M:%S %p")  # Separate time in 12-hour format

    # Perform validation for email and student number
    if not re.match(r'^[\w\.-]+@tip\.edu\.ph$', email):
        QMessageBox.warning(win, "Email Error", "Please enter a valid TIP email.")
        return

    if len(student_number) != 7:
        QMessageBox.warning(win, "Student Number Error", "Please enter a valid Student Number.")
        return

    # Call insert_user with separate date and time
    success = insert_user(email, student_number, date, time)

    if success:
        # Clear input fields and hide the window
        name_input.clear()
        student_number_input.clear()
        win.hide()

        global timer_window
        timer_window = timer.start_timer(email, student_number)
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

        self.set_background("login.png")

        window_width = self.width()
        window_height = self.height()
        input_width = 300
        input_height = 40
        button_width = 150
        button_height = 40
        x_center = (window_width - input_width) // 2
        y_center = (window_height // 2) - 30  

        global name_input
        name_input = QLineEdit(self)
        name_input.setPlaceholderText("Enter your TIP Email")
        name_input.setGeometry(x_center, y_center, input_width, input_height)
        name_input.setStyleSheet("""
            border: 1px solid #C0C0C0;
            border-radius: 15px;
            padding: 5px;
            font-size: 14px;
            background: #FFFFFF;  /* Solid white background */
        """)

        global student_number_input
        student_number_input = QLineEdit(self)
        student_number_input.setPlaceholderText("Enter your Student Number")
        student_number_input.setGeometry(x_center, y_center + 60, input_width, input_height)
        student_number_input.setStyleSheet("""
            border: 1px solid #C0C0C0;
            border-radius: 15px;
            padding: 5px;
            font-size: 14px;
            background: #FFFFFF;  /* Solid white background */
        """)
        
        int_validator = QIntValidator(0, 9999999)
        student_number_input.setValidator(int_validator)

        login_button = QPushButton("Start Session", self)
        login_button.setGeometry((window_width - button_width) // 2, y_center + 130, button_width, button_height)
        login_button.setStyleSheet("""
            QPushButton {
                border: 2px solid #333;
                border-radius: 20px;
                background-color: #333; /* Black color */
                color: #FFF; /* White text color */
                font-size: 16px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #444; /* Slightly lighter black on hover */
            }
        """)
        login_button.clicked.connect(on_submit)
    
    def set_background(self, image_path):
        """Set background image of the window."""
        image_path = resource_path(image_path)  
        background = QPixmap(image_path)
        background = background.scaled(self.size(), QtCore.Qt.KeepAspectRatioByExpanding, QtCore.Qt.SmoothTransformation)
        palette = self.palette()
        palette.setBrush(QPalette.Window, QBrush(background))
        self.setPalette(palette)

    def closeEvent(self, event):
        """Override the closeEvent to require a password before closing."""
        password, ok = QInputDialog.getText(self, 'Admin Password', 'Enter password to close:', QLineEdit.Password)

        if ok and password == "123":  # Change this to the default password
            event.accept()  # Close the application if the password is correct
        else:
            QMessageBox.warning(self, "Incorrect Password", "The password you entered is incorrect.")
            event.ignore()  # Prevent closing if the password is incorrect

def window():
    app = QApplication(sys.argv)
    global win
    win = MainWindow()
    win.setWindowFlags(QtCore.Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
    win.show()
    sys.exit(app.exec_())

window()
