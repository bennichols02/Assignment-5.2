from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.exception.no_current_blog_exception import NoCurrentBlogException
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QPlainTextEdit,
    QVBoxLayout,
)


class SearchPostsDialog(QDialog):
    '''Provides streamlined access to post search functionality with real-time
    results displayed in a formatted text area. Supports both targeted
    text-based searching and comprehensive post listing with detailed
    metadata presentation including creation and modification timestamps.'''
    def __init__(self, controller, parent=None):
        '''Initializes the post search dialog with controller integration.'''
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Search Posts")
        self.resize(560, 400)
        self._build_ui()

    def _build_ui(self):
        '''Organizes functionality into clear sections for search input,
        action execution, and results presentation. Features a responsive
        layout that adapts to different content volumes while maintaining
        clear visual hierarchy and user guidance.'''
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

    # Dialog title with prominent styling
        title = QLabel("Search Posts in Current Blog")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        # Search input row with integrated action buttons
        input_row = QHBoxLayout()
        input_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter text to search within posts")
        self.search_input.returnPressed.connect(self._handle_search)

        search_button = QPushButton("Search")
        search_button.setAutoDefault(False)
        search_button.setMinimumWidth(120)
        search_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        search_button.clicked.connect(self._handle_search)

        list_all_button = QPushButton("List all posts")
        list_all_button.setAutoDefault(False)
        list_all_button.setMinimumWidth(120)
        list_all_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        list_all_button.clicked.connect(self._handle_list_all)

        input_row.addWidget(self.search_input)
        input_row.addSpacing(8)
        input_row.addWidget(search_button)
        input_row.addSpacing(8)
        input_row.addWidget(list_all_button)

        # Dialog completion button

        done_button = QPushButton("Done")
        done_button.setAutoDefault(False)
        done_button.setMinimumWidth(120)
        done_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        done_button.clicked.connect(self.close)

        # Status display for operation feedback

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #b00020;")

        # Results display area configured as required by assignment

        self.results = QPlainTextEdit()
        self.results.setReadOnly(True)
        self.results.setPlaceholderText("Search results will appear here.")
        self.results.setMinimumHeight(240)

        # Assemble all interface components

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addLayout(input_row)
        layout.addSpacing(6)

        # Right-aligned done button for clear dialog completion

        done_row = QHBoxLayout()
        done_row.addStretch()
        done_row.addWidget(done_button)
        layout.addLayout(done_row)
        layout.addSpacing(6)
        layout.addWidget(self.status_label)
        layout.addSpacing(6)
        layout.addWidget(self.results)
        self.setLayout(layout)

    def _handle_search(self):
        '''Validates search term presence, checks blog context and user
        permissions, and queries the controller for posts matching the
        search criteria. Displays formatted results in the text area or
        shows appropriate error messages for:
        - Empty search terms
        - Missing current blog context
        - Authentication requirements
        - No matching posts found
        '''
        term = self.search_input.text().strip()
        if not term:
            self.status_label.setText("Enter text to search.")
            self.results.clear()
            return
        try:
            posts = self.controller.retrieve_posts(term)
        except (IllegalAccessException, NoCurrentBlogException) as exc:
            self.status_label.setText(str(exc))
            self.results.clear()
            return
        except Exception:
            self.status_label.setText("Unable to search posts.")
            self.results.clear()
            return

        self._populate_results(posts, empty_message="No posts contain that text.")

    def _handle_list_all(self):
        '''Retrieves and displays all posts in the current blog.
        
        Checks blog context and user permissions, requests the complete
        post list from the controller, and displays all posts with
        detailed metadata in the text area. Shows appropriate error
        messages for:
        - Missing current blog context
        - Authentication requirements
        - Empty blog with no posts'''
        try:
            posts = self.controller.list_posts()
        except (IllegalAccessException, NoCurrentBlogException) as exc:
            self.status_label.setText(str(exc))
            self.results.clear()
            return
        except Exception:
            self.status_label.setText("Unable to list posts.")
            self.results.clear()
            return

        self._populate_results(posts, empty_message="No posts in this blog.")

    def _populate_results(self, posts, empty_message):
        '''Converts each post object into a formatted text representation
        including post number, title, creation/modification timestamps,
        and content. Separates individual posts with visual dividers
        for clear distinction. Handles timestamp formatting for both
        string and datetime objects.'''
        self.results.clear()
        if not posts:
            self.status_label.setText(empty_message)
            return

        lines = []
        for post in posts:
            lines.append(f"Post: {getattr(post, 'code', '')} | Title: {getattr(post, 'title', '')}")
            created = getattr(post, 'creation_time', None)
            updated = getattr(post, 'update_time', None)
            created_txt = created if isinstance(created, str) else getattr(created, 'isoformat', lambda: str(created))()
            updated_txt = updated if isinstance(updated, str) else getattr(updated, 'isoformat', lambda: str(updated))()
            lines.append(f"Created - {created_txt}, Changed - {updated_txt}")
            lines.append(getattr(post, 'text', ''))
            lines.append("-" * 50)
        self.results.setPlainText("\n".join(lines))
        self.status_label.setText("")
