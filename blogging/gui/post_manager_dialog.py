from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException
from blogging.post import Post
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class PostManagerDialog(QDialog):
    '''Dialog for creating, updating, and deleting posts within the current blog.'''
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Post Manager")
        self.resize(520, 420)
        self._suppress_load = False
        self._build_ui()
        self._set_next_post_number()

    def _build_ui(self):
        '''Construct the form fields and action buttons.'''
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Manage Posts")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.post_number_input = QLineEdit()
        self.post_number_input.setValidator(QIntValidator(1, 1_000_000))
        self.post_number_input.textChanged.connect(self._load_post_from_number)

        self.post_title_input = QLineEdit()
        self.post_title_input.setPlaceholderText("Post title")

        self.post_text_input = QTextEdit()
        self.post_text_input.setPlaceholderText("Post content")
        self.post_text_input.setMinimumHeight(160)

        form.addRow("Post number:", self.post_number_input)
        form.addRow("Title:", self.post_title_input)
        form.addRow("Text:", self.post_text_input)

        button_row = QHBoxLayout()
        button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        done_btn = QPushButton("Done")
        done_btn.clicked.connect(self.close)

        self.create_btn = QPushButton("Create")
        self.create_btn.clicked.connect(self._handle_create)

        self.update_btn = QPushButton("Update")
        self.update_btn.clicked.connect(self._handle_update)

        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self._handle_delete)

        for btn in (done_btn, self.create_btn, self.update_btn, delete_btn):
            btn.setMinimumWidth(120)
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        button_row.addWidget(done_btn)
        button_row.addSpacing(8)
        button_row.addWidget(self.create_btn)
        button_row.addSpacing(8)
        button_row.addWidget(self.update_btn)
        button_row.addSpacing(8)
        button_row.addWidget(delete_btn)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #b00020;")

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addLayout(form)
        layout.addSpacing(12)
        layout.addLayout(button_row)
        layout.addSpacing(8)
        layout.addWidget(self.status_label)
        layout.addStretch()
        self.setLayout(layout)

    def _load_post_from_number(self):
        '''Load post data when a number is typed, or prep for creation if missing.'''
        if self._suppress_load:
            return
        number_text = self.post_number_input.text().strip()
        if not number_text:
            self._clear_fields()
            self.status_label.setText("")
            self._update_button_states()
            return

        post_code = int(number_text)
        blog = self._current_blog()
        if not blog:
            self.status_label.setText("Select a current blog first.")
            self._clear_fields()
            self._update_button_states()
            return

        post = blog.search_post(post_code)
        if not post:
            self.status_label.setText("No post with that number. You can create it.")
            self._clear_fields()
            self.post_number_input.setText(str(post_code))
            self._update_button_states()
            return

        self.post_title_input.setText(post.title)
        self.post_text_input.setText(post.text)
        self.status_label.setText("")
        self._update_button_states()

    def _handle_create(self):
        '''Create a new post at the chosen number if it does not already exist.'''
        self.status_label.setStyleSheet("color: #b00020;")
        self.status_label.setText("")

        number_text = self.post_number_input.text().strip()
        title = self.post_title_input.text().strip()
        text = self.post_text_input.toPlainText().strip()

        if not number_text or not title or not text:
            self.status_label.setText("Post number, title, and text are required.")
            return

        blog = self._current_blog()
        if not blog:
            self.status_label.setText("Select a current blog first.")
            return

        post_code = int(number_text)
        existing = blog.search_post(post_code)
        if existing:
            self.status_label.setText("A post with that number already exists.")
            self._update_button_states()
            return

        try:
            new_post = Post(post_code, title, text)
            blog.post_dao.create_post(new_post)
        except Exception:
            self.status_label.setText("Unable to create post.")
            return

        self.status_label.setStyleSheet("color: #1b5e20;")
        self.status_label.setText("Post created.")
        self._clear_fields()
        self._set_next_post_number()

    def _handle_update(self):
        '''Update an existing post's title/text.'''
        self.status_label.setStyleSheet("color: #b00020;")
        self.status_label.setText("")

        number_text = self.post_number_input.text().strip()
        title = self.post_title_input.text().strip()
        text = self.post_text_input.toPlainText().strip()

        if not number_text or not title or not text:
            self.status_label.setText("Post number, title, and text are required.")
            return

        post_code = int(number_text)
        blog = self._current_blog()
        if not blog:
            self.status_label.setText("Select a current blog first.")
            return

        if not blog.search_post(post_code):
            self.status_label.setText("Post not found.")
            return

        try:
            self.controller.update_post(post_code, title, text)
        except (IllegalAccessException, NoCurrentBlogException) as exc:
            self.status_label.setText(str(exc))
            return
        except Exception:
            self.status_label.setText("Unable to update post.")
            return

        self.status_label.setStyleSheet("color: #1b5e20;")
        self.status_label.setText("Post updated.")

    def _handle_delete(self):
        '''Delete the selected post after user confirmation.'''
        self.status_label.setStyleSheet("color: #b00020;")
        self.status_label.setText("")

        number_text = self.post_number_input.text().strip()
        if not number_text:
            self.status_label.setText("Enter a post number to delete.")
            return

        post_code = int(number_text)
        blog = self._current_blog()
        if not blog:
            self.status_label.setText("Select a current blog first.")
            return

        post = blog.search_post(post_code)
        if not post:
            self.status_label.setText("Post not found.")
            return

        confirm = QMessageBox.question(
            self,
            "Confirm deletion",
            f"Delete post {post_code}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        try:
            self.controller.delete_post(post_code)
        except (IllegalAccessException, NoCurrentBlogException) as exc:
            self.status_label.setText(str(exc))
            return
        except Exception:
            self.status_label.setText("Unable to delete post.")
            return

        self.status_label.setStyleSheet("color: #1b5e20;")
        self.status_label.setText("Post deleted.")
        self._clear_fields()
        self._set_next_post_number()

    def _current_blog(self):
        '''Return the current blog or None if unavailable.'''
        try:
            return self.controller.get_current_blog()
        except Exception:
            return None

    def _set_next_post_number(self):
        '''Pre-fill the next available post number for convenience.'''
        blog = self._current_blog()
        if not blog:
            self.post_number_input.clear()
            self._update_button_states()
            return
        try:
            posts = blog.list_posts()
        except Exception:
            posts = []
        if posts:
            max_code = max(p.code for p in posts)
            next_code = max_code + 1
        else:
            next_code = 1
        self._suppress_load = True
        self.post_number_input.setText(str(next_code))
        self._suppress_load = False
        self.post_number_input.selectAll()
        self._update_button_states()

    def _clear_fields(self):
        '''Blank out the title/text editors.'''
        self.post_title_input.clear()
        self.post_text_input.clear()

    def _update_button_states(self):
        """Enable/disable create and update based on chosen number and blog."""
        number_text = self.post_number_input.text().strip()
        blog = self._current_blog()
        if not self.create_btn or not self.update_btn:
            return

        if not number_text or not blog:
            self.create_btn.setEnabled(False)
            self.update_btn.setEnabled(False)
            return

        try:
            post_code = int(number_text)
        except ValueError:
            self.create_btn.setEnabled(False)
            self.update_btn.setEnabled(False)
            return

        exists = blog.search_post(post_code) if blog else None
        self.create_btn.setEnabled(exists is None)
        self.update_btn.setEnabled(exists is not None)
