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

# Registration Dialog
class RegistrationDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register Admin Account")
        self.setFixedSize(350, 250)
        self.setStyleSheet("""
            QDialog {
                background-color: #f2f4f7;
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
                background-color: #4CAF50;
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
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_credentials(self):
        return self.username_input.text(), self.password_input.text()


# Login Dialog
class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.setFixedSize(350, 200)
        self.setStyleSheet("""
            QDialog {
                background-color: #f2f4f7;
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
                background-color: #4CAF50;
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
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        # Add Register button
        register_button = QPushButton("Register Admin Account")
        register_button.clicked.connect(self.open_registration_dialog)
        layout.addWidget(register_button)

    def open_registration_dialog(self):
        registration_dialog = RegistrationDialog()
        if registration_dialog.exec_() == QDialog.Accepted:
            username, password = registration_dialog.get_credentials()
            # Here you would typically save the new admin account to a database or file
            # For demonstration, we will just show a message box
            QMessageBox.information(self , "Registration Successful", f"Admin account '{username}' has been registered successfully!")

    def get_credentials(self):
        return self.username_input.text(), self.password_input.text()




# Main Dashboard
class Dashboard(QMainWindow):
    def __init__(self, username):  # Accept username
        super().__init__()
        self.username = username  # Save it

        self.setWindowTitle("School Guidance Record Management Dashboard")
        self.setGeometry(100, 100, 1200, 700)

        container = QWidget()
        self.setCentralWidget(container)

        main_layout = QVBoxLayout()
        container.setLayout(main_layout)

        # Add top bar
        top_bar = self.create_top_bar()
        main_layout.addWidget(top_bar)

        # Horizontal content split (sidebar + content area)
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
        top_frame.setStyleSheet("background-color: #2c3e50;")

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 0, 10, 0)

        welcome = QLabel(f"👋 Welcome, {self.username}")
        welcome.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        welcome.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        layout.addWidget(welcome)
        layout.addStretch()

        # Profile Picture
        profile_pic = QLabel()
        pixmap = QPixmap(40, 40)  # Create a placeholder for the profile picture
        pixmap.fill(Qt.gray)  # Fill with gray color for placeholder
        profile_pic.setPixmap(pixmap)
        profile_pic.setFixedSize(40, 40)
        layout.addWidget(profile_pic)

        # Sign Out Button
        sign_out_button = QPushButton("Sign Out")
        sign_out_button.setStyleSheet("background-color: #e74c3c; color: white;")
        sign_out_button.clicked.connect(self.sign_out)
        layout.addWidget(sign_out_button)


        top_frame.setLayout(layout)
        return top_frame

    def create_sidebar(self):
        sidebar = QListWidget()
        sidebar.setFixedWidth(200)
        sidebar.addItems([
            "📊 Dashboard",
            "🧑‍🎓 Student Records",
            "📝 Counseling Sessions",
            "📌 Referrals",
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
        elif "Calendar" in view:
            self.show_calendar()
        elif "Reports" in view or "Charts" in view:
            self.show_charts()
        elif "Student Records" in view:
            self.display_message("Student Records - Coming Soon")
        elif "Counseling Sessions" in view:
            self.display_message("Counseling Sessions - Coming Soon")
        elif "Referrals" in view:
            self.display_message("Referrals - Coming Soon")
        elif "Settings" in view:
            self.display_message("Settings - Coming Soon")

    def create_overview_cards(self):
        layout = QHBoxLayout()
        cards = [
            ("🧑‍🎓 Total Students", "525"),
            ("🧠 Active Cases", "42"),
            ("📅 Upcoming Sessions", "12"),
            ("📈 Referrals Made", "18"),
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

        # Dummy data
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
                if username == "admin" and password == "password":
                    dashboard = Dashboard(username)  # Pass username
                    dashboard.show()
                    sys.exit(app.exec_())
                else:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setWindowTitle("Invalid Credentials")
                    msg.setText("The username or password you entered is incorrect. Please try again.")
                    msg.exec_()
            else:
                sys.exit()


if __name__ == '__main__':
    main()
