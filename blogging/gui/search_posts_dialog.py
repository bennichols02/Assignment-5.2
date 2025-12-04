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
    def __init__(self, controller, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Search Posts")
        self.resize(560, 400)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        title = QLabel("Search Posts in Current Blog")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

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

        done_button = QPushButton("Done")
        done_button.setAutoDefault(False)
        done_button.setMinimumWidth(120)
        done_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        done_button.clicked.connect(self.close)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #b00020;")

        self.results = QPlainTextEdit()
        self.results.setReadOnly(True)
        self.results.setPlaceholderText("Search results will appear here.")
        self.results.setMinimumHeight(240)

        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addLayout(input_row)
        layout.addSpacing(6)

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
        self.results.clear()
        if not posts:
            self.status_label.setText(empty_message)
            return

        lines = []
        for post in posts:
            lines.append(f"Code: {getattr(post, 'code', '')} | Title: {getattr(post, 'title', '')}")
            lines.append(getattr(post, 'text', ''))
            lines.append("-" * 50)
        self.results.setPlainText("\n".join(lines))
        self.status_label.setText("")
