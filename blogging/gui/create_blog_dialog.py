from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QDialog,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QSpacerItem,
    QSizePolicy,
    QVBoxLayout,
)


class CreateBlogDialog(QDialog):
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Blog Manager")
        self.resize(480, 320)
        self._build_ui()

    def _build_ui(self):
        outer = QVBoxLayout()
        outer.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Blog Manager")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 600;")

        form_card = QVBoxLayout()
        form_card.setContentsMargins(18, 14, 18, 14)
        form_card.setSpacing(12)

        form_grid = QGridLayout()
        form_grid.setVerticalSpacing(10)
        form_grid.setHorizontalSpacing(12)
        form_grid.setColumnStretch(1, 2)
        form_grid.setColumnStretch(2, 1)

        self.id_input = QLineEdit()
        self.id_input.setValidator(QIntValidator(0, 1_000_000))
        self.id_input.setPlaceholderText("e.g. 123")
        self.id_input.textChanged.connect(self._populate_existing)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Blog name")

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("owner@example.com")

        self.existing_name = QLabel("-")
        self.existing_url = QLabel("-")
        self.existing_email = QLabel("-")
        for lbl in (self.existing_name, self.existing_url, self.existing_email):
            lbl.setStyleSheet("color: #555;")
            lbl.setMinimumWidth(180)
            lbl.setMaximumWidth(200)
            lbl.setWordWrap(False)

        form_grid.addWidget(QLabel("Blog ID:"), 0, 0)
        form_grid.addWidget(self.id_input, 0, 1)
        form_grid.addWidget(QLabel("Name:"), 1, 0)
        form_grid.addWidget(self.name_input, 1, 1)
        form_grid.addWidget(self.existing_name, 1, 2)
        form_grid.addWidget(QLabel("URL:"), 2, 0)
        form_grid.addWidget(self.url_input, 2, 1)
        form_grid.addWidget(self.existing_url, 2, 2)
        form_grid.addWidget(QLabel("Email:"), 3, 0)
        form_grid.addWidget(self.email_input, 3, 1)
        form_grid.addWidget(self.existing_email, 3, 2)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #b00020;")

        button_row = QHBoxLayout()
        button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        done_btn = QPushButton("Done")
        done_btn.setAutoDefault(False)
        done_btn.clicked.connect(self.accept)
        create_btn = QPushButton("Create")
        create_btn.setDefault(False)
        create_btn.setAutoDefault(False)
        create_btn.clicked.connect(self._handle_create)
        update_btn = QPushButton("Update")
        update_btn.setAutoDefault(False)
        update_btn.clicked.connect(self._handle_update)
        delete_btn = QPushButton("Delete")
        delete_btn.setAutoDefault(False)
        delete_btn.clicked.connect(self._handle_delete)

        button_row.addWidget(done_btn)
        button_row.addSpacing(8)
        button_row.addWidget(create_btn)
        button_row.addSpacing(8)
        button_row.addWidget(update_btn)
        button_row.addSpacing(8)
        button_row.addWidget(delete_btn)

        form_card.addLayout(form_grid)
        form_card.addWidget(self.status_label)
        form_card.addLayout(button_row)

        outer.addWidget(title)
        outer.addSpacing(8)
        outer.addLayout(form_card)
        outer.addStretch()
        self.setLayout(outer)

    def _handle_create(self):
        self.status_label.setStyleSheet("color: #b00020;")
        self.status_label.setText("")

        id_text = self.id_input.text().strip()
        name = self.name_input.text().strip()
        url = self.url_input.text().strip()
        email = self.email_input.text().strip()

        if not id_text:
            self.status_label.setText("All fields are required.")
            return

        blog_id = int(id_text)
        try:
            existing = self.controller.search_blog(blog_id)
        except IllegalAccessException:
            self.status_label.setText("You must login before creating blogs.")
            return
        if existing:
            self.status_label.setText("A blog with that ID already exists.")
            return

        if not name or not url or not email:
            self.status_label.setText("All fields are required.")
            return

        try:
            self.controller.create_blog(blog_id, name, url, email)
        except IllegalAccessException:
            self.status_label.setText("You must login before creating blogs.")
            return
        except IllegalOperationException:
            self.status_label.setText("A blog with that ID already exists.")
            return

        self.status_label.setStyleSheet("color: #1b5e20;")
        self.status_label.setText("Blog created successfully.")
        self._clear_inputs()

    def _handle_update(self):
        self.status_label.setStyleSheet("color: #b00020;")
        self.status_label.setText("")

        id_text = self.id_input.text().strip()
        name = self.name_input.text().strip()
        url = self.url_input.text().strip()
        email = self.email_input.text().strip()

        if not id_text or not name or not url or not email:
            self.status_label.setText("All fields are required.")
            return

        blog_id = int(id_text)
        try:
            self.controller.update_blog(blog_id, blog_id, name, url, email)
        except IllegalAccessException:
            self.status_label.setText("You must login before updating blogs.")
            return
        except IllegalOperationException as exc:
            self.status_label.setText(str(exc))
            return

        self.status_label.setStyleSheet("color: #1b5e20;")
        self.status_label.setText("Blog updated successfully.")
        self._clear_inputs()

    def _handle_delete(self):
        self.status_label.setStyleSheet("color: #b00020;")
        self.status_label.setText("")

        id_text = self.id_input.text().strip()
        if not id_text:
            self.status_label.setText("Enter an ID to delete.")
            return

        blog_id = int(id_text)
        try:
            existing = self.controller.search_blog(blog_id)
        except IllegalAccessException:
            self.status_label.setText("You must login before deleting blogs.")
            return

        if not existing:
            self.status_label.setText("Blog not found.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete blog ID {blog_id}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            self.controller.delete_blog(blog_id)
        except IllegalAccessException:
            self.status_label.setText("You must login before deleting blogs.")
            return
        except IllegalOperationException as exc:
            self.status_label.setText(str(exc))
            return

        self.status_label.setStyleSheet("color: #1b5e20;")
        self.status_label.setText("Blog deleted.")
        self._clear_inputs()

    def _clear_inputs(self):
        self.id_input.clear()
        self.name_input.clear()
        self.url_input.clear()
        self.email_input.clear()
        self.id_input.setFocus()
        self._set_existing("-", "-", "-")

    def _populate_existing(self):
        id_text = self.id_input.text().strip()
        if not id_text:
            self._set_existing("-", "-", "-")
            return

        blog_id = int(id_text)
        try:
            blog = self.controller.search_blog(blog_id)
        except IllegalAccessException:
            self.status_label.setStyleSheet("color: #b00020;")
            self.status_label.setText("You must login to check existing blogs.")
            self._set_existing("-", "-", "-")
            return

        if not blog:
            self._set_existing("Not found", "Not found", "Not found")
            return

        self._set_existing(blog.name, blog.url, blog.email)

    def _set_existing(self, name, url, email):
        self.existing_name.setText(name)
        self.existing_url.setText(url)
        self.existing_email.setText(email)
