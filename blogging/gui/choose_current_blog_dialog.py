from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class ChooseCurrentBlogDialog(QDialog):
    '''Modal dialog for selecting which blog is "current" by ID.'''
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Choose Current Blog")
        self.resize(360, 180)
        self._build_ui()

    def _build_ui(self):
        '''Build layout for entering a blog ID and confirming selection.'''
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Select a current blog by ID")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: 600;")

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.id_input = QLineEdit()
        self.id_input.setValidator(QIntValidator(0, 1_000_000))
        self.id_input.setPlaceholderText("e.g. 123")
        form.addRow("Blog ID:", self.id_input)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #b00020;")

        submit_btn = QPushButton("Set current blog")
        submit_btn.clicked.connect(self._handle_set_current)

        layout.addWidget(title)
        layout.addSpacing(6)
        layout.addLayout(form)
        layout.addSpacing(8)
        layout.addWidget(submit_btn, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(6)
        layout.addWidget(self.status_label)
        self.setLayout(layout)

    def _handle_set_current(self):
        '''Validate input and attempt to set the current blog via controller.'''
        self.status_label.setText("")
        id_text = self.id_input.text().strip()
        if not id_text:
            self.status_label.setText("Enter an ID.")
            return

        blog_id = int(id_text)
        try:
            self.controller.set_current_blog(blog_id)
        except IllegalAccessException:
            self.status_label.setText("You must login first.")
            return
        except IllegalOperationException as exc:
            self.status_label.setText(str(exc))
            return
        except Exception:
            self.status_label.setText("Unable to set current blog.")
            return

        self.accept()
