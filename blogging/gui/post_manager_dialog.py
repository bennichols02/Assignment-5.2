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
    '''Integrates creation, modification, and deletion functionality with
    intelligent post number handling and existing data detection. Features
    dynamic interface adaptation that automatically suggests available
    post numbers and adjusts button availability based on post existence.'''
    def __init__(self, controller, parent=None):
        '''Initializes the post management dialog with controller integration.'''
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Post Manager")
        self.resize(520, 420)
        self._suppress_load = False
        self._build_ui()
        self._set_next_post_number()

    def _build_ui(self):
        '''Organizes post attributes into a three-field form with appropriate
        input widgets for different data types. Provides four action buttons
        for dialog control and post operations with dynamic enable/disable
        states based on input validation and post existence.'''
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Dialog title with prominent styling
        title = QLabel("Manage Posts")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        # Form layout for organized field presentation
        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        # Post number input with numeric validation and change detection
        self.post_number_input = QLineEdit()
        self.post_number_input.setValidator(QIntValidator(1, 1_000_000))
        self.post_number_input.textChanged.connect(self._load_post_from_number)

        # Post title input with placeholder guidance
        self.post_title_input = QLineEdit()
        self.post_title_input.setPlaceholderText("Post title")
       
        # Post content input with multi-line support
        self.post_text_input = QTextEdit()
        self.post_text_input.setPlaceholderText("Post content")
        self.post_text_input.setMinimumHeight(160)

        form.addRow("Post number:", self.post_number_input)
        form.addRow("Title:", self.post_title_input)
        form.addRow("Text:", self.post_text_input)

        # Action buttons for dialog control and post operations
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


        # Standardize button appearance and behavior
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

        # Status display for operation feedback
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #b00020;")

        # Assemble all interface components
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
        '''Monitors changes to the post number input field and attempts to
        load existing post data when a valid number is detected. Updates
        the form fields with existing post content or prepares the
        interface for new post creation based on post existence.
        
        Automatically adjusts button availability to prevent invalid
        operations (e.g., updating non-existent posts).'''
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
        '''Validates all input fields for completeness, checks for duplicate
        post numbers within the current blog, verifies blog context and
        user permissions, and attempts to create the post through the
        controller. Provides visual feedback and resets the form on success.'''
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
        '''Processes modification of an existing post's content.
        
        Validates all input fields for completeness, verifies the post
        exists in the current blog, checks blog context and user permissions,
        and attempts to update the post through the controller. Provides
        visual feedback on operation success.'''
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
        '''Validates the post number is provided, verifies the post exists
        in the current blog, checks blog context and user permissions,
        presents a confirmation dialog, and attempts to delete the post
        through the controller. Provides visual feedback and resets the
        form on success.'''
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
        '''Safely accesses the controller's current blog property with
        exception handling for cases where no blog is selected or
        user authentication issues occur..'''
        try:
            return self.controller.get_current_blog()
        except Exception:
            return None

    def _set_next_post_number(self):
        '''Calculates the next sequential post number based on existing
        posts in the current blog. If no posts exist, suggests number 1.
        Pre-fills the post number input field with this suggestion and
        selects the text for easy replacement if desired.'''
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
        '''Clears post content fields while preserving the post number
        input to facilitate sequential post operations. Maintains
        clean interface state between operations.'''
        self.post_title_input.clear()
        self.post_text_input.clear()

    def _update_button_states(self):
        """  Evaluates the current input state and blog context to determine
        which operations are valid. Enables the Create button when the
        post number is available, and enables the Update button when
        the post number corresponds to an existing post."""
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
