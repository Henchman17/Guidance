import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QMessageBox, QInputDialog, QTableWidget, QTableWidgetItem, QLineEdit
)
from PyQt5.QtCore import QPropertyAnimation, QRect, Qt, QEasingCurve

class GuidanceRecordManagementSystem(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Guidance Record Management System")
        self.setGeometry(100, 100, 600, 400)

        self.records = []

        self.initialize_ui()

    def initialize_ui(self):
        """Initialize the user interface components."""
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Guidance Record Management System")
        title_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title_label)

        # Button Layout
        button_layout = QHBoxLayout()

        # Add Record Button
        add_button = QPushButton("Add Record")
        add_button.clicked.connect(self.add_record)
        button_layout.addWidget(add_button)

        # View Records Button
        view_button = QPushButton("View Records")
        view_button.clicked.connect(self.view_records)
        button_layout.addWidget(view_button)

        # Delete Record Button
        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete_record)
        button_layout.addWidget(delete_button)

        # Search Bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search Records...")
        button_layout.addWidget(self.search_bar)

        # Search Button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_records)
        button_layout.addWidget(search_button)

        # Exit Button
        exit_button = QPushButton("Exit")
        exit_button.clicked.connect(self.close)
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

        # Table for displaying records
        self.table = QTableWidget()
        self.table.setColumnCount(1)
        self.table.setHorizontalHeaderLabels(["Guidance Records"])
        layout.addWidget(self.table)

        self.setLayout(layout)

    def add_record(self):
        """Add a new record to the list."""
        record, ok = QInputDialog.getText(self, "Input", "Enter the guidance record:")
        if ok and record:
            self.records.append(record)
            QMessageBox.information(self, "Success", "Record added successfully!")
            self.update_table()
            self.animate_table()
        else:
            QMessageBox.warning(self, "Warning", "No record entered.")

    def view_records(self):
        """Display all records in the table."""
        self.update_table()

    def update_table(self):
        """Update the table with the current records."""
        self.table.setRowCount(len(self.records))
        for row, record in enumerate(self.records):
            self.table.setItem(row, 0, QTableWidgetItem(record))

    def delete_record(self):
        """Delete a specified record from the list."""
        record, ok = QInputDialog.getText(self, "Input", "Enter the record to delete:")
        if ok and record in self.records:
            self.records.remove(record)
            QMessageBox.information(self, "Success", "Record deleted successfully!")
            self.update_table()
            self.animate_table()
        else:
            QMessageBox.critical(self, "Error", "Record not found.")

    def search_records(self):
        """Search for records that match the input in the search bar."""
        search_text = self.search_bar.text().lower()
        if search_text:
            filtered_records = [record for record in self.records if search_text in record.lower()]
            self.table.setRowCount(len(filtered_records))
            for row, record in enumerate(filtered_records):
                self.table.setItem(row, 0, QTableWidgetItem(record))
            if not filtered_records:
                QMessageBox.information(self, "Search Result", "No records found.")
        else:
            self.update_table()  # Show all records if search bar is empty

        self.search_bar.clear()  # Clear the search bar after searching

    def animate_table(self):
        """Animate the table when records are added or deleted."""
        animation = QPropertyAnimation(self.table, b"geometry")
        animation.setDuration(500)
        animation.setStartValue(QRect(self.table.x(), self.table.y(), self.table.width(), 0))
        animation.setEndValue(QRect(self.table.x(), self.table.y(), self.table.width(), self.table.rowHeight(0) * len(self.records)))
        animation.setEasingCurve(QEasingCurve.InOutCubic)
        animation.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GuidanceRecordManagementSystem()
    window.show()
    sys.exit(app.exec_())