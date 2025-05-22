import mysql.connector
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QTableWidget, QTableWidgetItem, QFrame, QListWidget,
    QLineEdit, QCalendarWidget, QDialog, QFormLayout, QDialogButtonBox,
    QMessageBox
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import sys

# Database connection
def create_connection():
    return mysql.connector.connect(
        host="localhost",  # Change if your MySQL server is on a different host
        user="admin",  # Replace with your MySQL username
        password="12345",  # Replace with your MySQL password
        database="guidance"  # Replace with your database name
    )

# Registration Dialog
class RegistrationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Admin Account")
        self.setFixedSize(350, 250)
        self.setStyleSheet("""
            QDialog {
                background-color: #e8f5e9;  /* Hyena Green */
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;  /* Hyena Green */
                color: white;
                padding: 8px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QDialogButtonBox QPushButton {
                min-width: 80px;
            }
        """)

        layout = QVBoxLayout(self)

        title = QLabel("Register Admin Account")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.register_admin)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def register_admin(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute("INSERT INTO admin_accounts (admin_username, admin_password) VALUES (%s, %s)", (username, password))
                connection.commit()
                cursor.close()
                connection.close()
                QMessageBox.information(self, "Registration Successful", f"Admin account '{username}' has been registered successfully!")
                self.accept()
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Error", f"Error: {err}")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")

# Login Dialog
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(350, 200)
        self.setStyleSheet("""
            QDialog {
                background-color: #e8f5e9;  /* Hyena Green */
                border-radius: 10px;
            }
            QLabel {
                font-size: 14px;
            }
            QLineEdit {
                padding: 8px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;  /* Hyena Green */
                color: white;
                padding: 8px;
                font-size: 14px;
                border: none;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QDialogButtonBox QPushButton {
                min-width: 80px;
            }
        """)

        layout = QVBoxLayout(self)

        title = QLabel("Welcome to Guidance System")
        title.setFont(QFont("Arial", 16, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)

        layout.addLayout(form_layout)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.login)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # Add Register button
        register_button = QPushButton("Register Admin Account")
        register_button.clicked.connect(self.open_registration_dialog)
        layout.addWidget(register_button)

    def open_registration_dialog(self):
        registration_dialog = RegistrationDialog()
        registration_dialog.exec_()

    def get_credentials(self):
        return self.username_input.text(), self.password_input.text()  # Add this line

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if username and password:
            try:
                connection = create_connection()
                cursor = connection.cursor()
                cursor.execute("SELECT * FROM admin_accounts WHERE admin_username = %s AND admin_password = %s", (username, password))
                result = cursor.fetchone()
                cursor.close()
                connection.close()

                if result:
                    self.accept()
                else:
                    QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            except mysql.connector.Error as err:
                QMessageBox.critical(self, "Error", f"Error: {err}")
        else:
            QMessageBox.warning(self, "Input Error", "Please enter both username and password.")

# Form Dialog
class FormDialog(QDialog):
    def __init__(self, title):
        super().__init__()
        self.setWindowTitle(title)
        self.setFixedSize(400, 300)
        self.setStyleSheet("""
            QDialog {
                background-color: #e8f5e9;  /* Hyena Green */
                border-radius: 10px;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                margin: 10px;
            }
        """)
        layout = QVBoxLayout(self)
        label = QLabel(f"{title} Form")
        layout.addWidget(label)

# Main Dashboard
class Dashboard(QMainWindow):
    def __init__(self, username):
        super().__init__()
        self.username = username

        self.setWindowTitle("School Guidance Record Management Dashboard")
        self.setGeometry(100, 100, 1200, 700)

        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QVBoxLayout()
        container.setLayout(main_layout)

        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)

        content_layout = QHBoxLayout()
        main_layout.addLayout(content_layout)

        sidebar = self.create_sidebar()
        content_layout.addWidget(sidebar)

        self.content_layout = QVBoxLayout()
        content_layout.addLayout(self.content_layout)

        self.showMaximized()
        self.build_dashboard()

    def create_top_bar(self):
        top_frame = QFrame()
        top_frame.setFixedHeight(50)
        top_frame.setStyleSheet("background-color: #4CAF50;")  # Hyena Green

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)

        welcome = QLabel(f"👋 Welcome, {self.username}")
        welcome.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        welcome.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layout.addWidget(welcome)
        layout.addStretch()

        # Notification bell button
        notification_bell = QPushButton("🔔")
        notification_bell.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                color: white;
                font-size: 20px;
                border: none;
            }
            QPushButton:hover {
                color: #c1e1c1;
            }
        """)
        notification_bell.setCursor(Qt.PointingHandCursor)
        notification_bell.clicked.connect(self.show_notifications)
        layout.addWidget(notification_bell)

        profile_pic = QLabel()
        pixmap = QPixmap(40, 40)
        pixmap.fill(Qt.gray)
        profile_pic.setPixmap(pixmap)
        profile_pic.setFixedSize(40, 40)
        layout.addWidget(profile_pic)

        sign_out_button = QPushButton("Sign Out")
        sign_out_button.setStyleSheet("background-color: #e74c3c; color: white;")
        sign_out_button.clicked.connect(self.sign_out)
        layout.addWidget(sign_out_button)

        top_frame.setLayout(layout)
        return top_frame

    def show_notifications(self):
        # Placeholder for notification messages
        QMessageBox.information(self, "Notifications", "You have 3 new notifications.")

    def create_sidebar(self):
        sidebar = QListWidget()
        sidebar.setFixedWidth(200)
        sidebar.addItems([
            "📊 Dashboard",
            "🧑‍🎓 Student Records",
            "📝 Counseling Sessions",
            "📌 Forms",
            "📅 Calendar",
            "📈 Reports",
            "⚙️ Settings"
        ])
        sidebar.currentItemChanged.connect(self.switch_view)
        return sidebar

    def build_dashboard(self):
        self.clear_layout(self.content_layout)

        header = QLabel("Dashboard")
        header.setFont(QFont("Arial", 20))
        self.content_layout.addWidget(header)

        search_layout = QHBoxLayout()
        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Search student...")
        self.search_box.textChanged.connect(self.filter_table)
        search_layout.addWidget(self.search_box)
        self.content_layout.addLayout(search_layout)

        overview = self.create_overview_cards()
        self.content_layout.addLayout(overview)

        self.table = self.create_sessions_table()
        self.content_layout.addWidget(self.table)

    def show_forms(self):
        self.clear_layout(self.content_layout)
        header = QLabel("Forms")
        header.setFont(QFont("Arial", 20))
        self.content_layout.addWidget(header)

        form_layout = QHBoxLayout()
        form_names = [
            "Good Moral and Re-Admission",
            "Student Cumulative",
            "Routine Interview",
            "Psychological Exam",
            "Exit Interview"
        ]
        for form_name in form_names:
            card = self.create_form_card(form_name)
            form_layout.addWidget(card)

        self.content_layout.addLayout(form_layout)

    def create_form_card(self, title):
        button = QPushButton(title)
        button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;  /* Hyena Green */
                color: white;
                font-size: 16px;
                border: none;
                border-radius: 5px;
                padding: 10px;
                margin: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        button.clicked.connect(lambda: self.open_form_dialog(title))
        return button

    def open_form_dialog(self, title):
        form_dialog = FormDialog(title)
        form_dialog.exec_()

    def show_calendar(self):
        self.clear_layout(self.content_layout)
        label = QLabel("📅 Session Calendar")
        label.setFont(QFont("Arial", 18))
        self.content_layout.addWidget(label)

        calendar = QCalendarWidget()
        self.content_layout.addWidget(calendar)

    def show_charts(self):
        self.clear_layout(self.content_layout)
        label = QLabel("📈 Counseling Statistics")
        label.setFont(QFont("Arial", 18))
        self.content_layout.addWidget(label)

        chart_widget = self.create_chart()
        self.content_layout.addWidget(chart_widget)

    def switch_view(self, current, _):
        if not current:
            return
        view = current.text()
        if "Dashboard" in view:
            self.build_dashboard()
        elif "Forms" in view:
            self.show_forms()
        elif "Calendar" in view:
            self.show_calendar()
        elif "Reports" in view or "Charts" in view:
            self.show_charts()
        elif "Student Records" in view:
            self.display_message("Student Records - Coming Soon")
        elif "Counseling Sessions" in view:
            self.display_message("Counseling Sessions - Coming Soon")
        elif "Settings" in view:
            self.display_message("Settings - Coming Soon")

    def create_overview_cards(self):
        layout = QHBoxLayout()
        cards = [
            ("🧑‍🎓 Total Students", "525"),
            ("🧠 Active Cases", "42"),
            ("📅 Upcoming Sessions", "12")
        ]
        for title, count in cards:
            card = self.create_card(title, count)
            layout.addWidget(card)
        return layout

    def create_card(self, title, count):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setFixedSize(200, 80)

        vbox = QVBoxLayout()
        label_title = QLabel(title)
        label_count = QLabel(count)
        label_count.setFont(QFont("Arial", 18, QFont.Bold))
        label_title.setStyleSheet("color: gray")

        vbox.addWidget(label_title)
        vbox.addWidget(label_count)
        frame.setLayout(vbox)
        return frame

    def create_sessions_table(self):
        table = QTableWidget()
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Student", "Date", "Counselor", "Topic", "Status"])
        self.sessions = [
            ("John Doe", "2025-04-15", "Ms. Carter", "Academic Stress", "Completed"),
            ("Jane Smith", "2025-04-16", "Mr. Reyes", "Peer Conflict", "Scheduled"),
            ("Mark Yoon", "2025-04-14", "Ms. Carter", "Family Issue", "Follow-up"),
        ]
        table.setRowCount(len(self.sessions))

        for row, session in enumerate(self.sessions):
            for col, item in enumerate(session):
                table.setItem(row, col, QTableWidgetItem(item))

        table.resizeColumnsToContents()
        return table

    def filter_table(self):
        query = self.search_box.text().lower()
        for row in range(self.table.rowCount()):
            student_name = self.table.item(row, 0).text().lower()
            self.table.setRowHidden(row, query not in student_name)

    def create_chart(self):
        figure = Figure(figsize=(5, 3))
        canvas = FigureCanvas(figure)
        ax = figure.add_subplot(111)

        labels = ['Academic Stress', 'Peer Conflict', 'Family Issue']
        sizes = [12, 5, 7]
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')

        return canvas
    
    def display_message(self, message):
        self.clear_layout(self.content_layout)
        label = QLabel(message)
        label.setFont(QFont("Arial", 18))
        self.content_layout.addWidget(label)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def sign_out(self):
        reply = QMessageBox.question(self, 'Confirm Sign Out', 
                                    "Are you sure you want to sign out?", 
                                    QMessageBox.Yes | QMessageBox.No, 
                                    QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.close()  # Close the dashboard
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_F11:
            if self.isFullScreen():
                self.showNormal()  # Exit full-screen
            else:
                self.showFullScreen()  # Enter full-screen

def main():
    app = QApplication(sys.argv)
    while True:
        login = LoginDialog()
        if login.exec_() == QDialog.Accepted:
            username, password = login.get_credentials()
            if username and password:  # Ensure credentials are provided
                try:
                    connection = create_connection()
                    cursor = connection.cursor()
                    cursor.execute("SELECT * FROM admin_accounts WHERE admin_username = %s AND admin_password = %s", (username, password))
                    result = cursor.fetchone()
                    cursor.close()
                    connection.close()

                    if result:
                        dashboard = Dashboard(username)  # Pass username
                        dashboard.show()
                        sys.exit(app.exec_())
                    else:
                        QMessageBox.warning(login, "Invalid Credentials", "The username or password you entered is incorrect. Please try again.")
                except mysql.connector.Error as err:
                    QMessageBox.critical(login, "Database Error", f"Error: {err}")
            else:
                QMessageBox.warning(login, "Input Error", "Please enter both username and password.")
        else:
            sys.exit()

if __name__ == '__main__':
    main()