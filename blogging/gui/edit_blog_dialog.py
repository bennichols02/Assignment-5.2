from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QDialog,
    QLabel,
    QGridLayout,
    QHBoxLayout,
    QPushButton,
    QVBoxLayout,
)
from blogging.gui.post_manager_dialog import PostManagerDialog


class EditBlogDialog(QDialog):
    '''Centralized post management interface for the current blog.
    
    Provides streamlined access to post-related operations through
    organized button groups. Functions as a launching point for more
    specialized post management and search dialogs, maintaining focus
    on the currently selected blog context throughout all operations.'''
    def __init__(self, controller, current_blog, parent=None):
        super().__init__(parent)
        self.controller = controller
        self.current_blog = current_blog
        self.setWindowTitle("Edit Current Blog")
        self.resize(480, 260)
        self._build_ui()

    def _build_ui(self):
        '''Constructs the dialog interface with blog information and action controls.
        
        Organizes functionality into a clear hierarchy with:
        - Prominent blog identification header
        - Visual separation of blog context information
        - Grid arrangement of post management actions
        - Clear action descriptions and tooltips
        '''
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Dialog title dynamically adjusted based on blog context
        title = QLabel(self._header_text())
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: 600;")

        # Current blog information display
        self.blog_label = QLabel(self._current_blog_text())
        self.blog_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.blog_label.setStyleSheet("color: #555;")

        # Grid layout for organized action button arrangement
        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(12)

        # Post management button - comprehensive post operations
        post_manager_btn = QPushButton("Post manager")
        post_manager_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        post_manager_btn.setMinimumWidth(170)
        post_manager_btn.setMinimumHeight(42)
        post_manager_btn.setToolTip("Create, update, retrieve, delete, and list posts for the current blog.")
        post_manager_btn.clicked.connect(self._open_post_manager)

        # Post search button - focused post discovery
        search_posts_btn = QPushButton("Search posts")
        search_posts_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        search_posts_btn.setMinimumWidth(170)
        search_posts_btn.setMinimumHeight(42)
        search_posts_btn.setToolTip("Search posts in the current blog.")
        search_posts_btn.clicked.connect(self._open_search_posts)

        # Dialog completion button - returns to main interface
        logout_btn = QPushButton("Finish editing blog")
        logout_btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        logout_btn.setMinimumWidth(170)
        logout_btn.setMinimumHeight(42)
        logout_btn.setToolTip("Close this window.")
        logout_btn.clicked.connect(self.close)

        # Arrange buttons in a 2x2 grid pattern
        grid.addWidget(post_manager_btn, 0, 0)
        grid.addWidget(search_posts_btn, 0, 1)
        grid.addWidget(logout_btn, 1, 0, 1, 2)

        # Center the button grid within available horizontal space
        grid_wrapper = QHBoxLayout()
        grid_wrapper.setAlignment(Qt.AlignmentFlag.AlignCenter)
        grid_wrapper.addStretch()
        grid_wrapper.addLayout(grid)
        grid_wrapper.addStretch()

        # Assemble all interface components
        layout.addWidget(title)
        layout.addSpacing(4)
        layout.addWidget(self.blog_label)
        layout.addSpacing(16)
        layout.addLayout(grid_wrapper)
        layout.addStretch()
        self.setLayout(layout)

    def _current_blog_text(self):
        '''Creates user-friendly identification text including blog name
        and ID for clear context establishment in the interface.'''
        if not self.current_blog:
            return "No current blog selected."
        return f"{self.current_blog.name} (ID: {self.current_blog.id})"

    def _header_text(self):
        '''Dynamically adjusts header text to reflect whether a blog is
        currently selected for editing operations.'''
        if not self.current_blog:
            return "Edit Blog"
        return f"Editing: {self.current_blog.name}"

    def _open_post_manager(self):
        ''' Creates and displays a PostManagerDialog instance configured
        for the current blog context. The dialog operates in non-modal
        mode, allowing simultaneous interaction with multiple post
        management interfaces if desired.'''
        self.post_manager_dialog = PostManagerDialog(self.controller, self)
        self.post_manager_dialog.show()

    def _open_search_posts(self):
        '''Creates and displays a SearchPostsDialog instance configured
        for the current blog context. The dialog operates in non-modal
        mode, supporting concurrent post search and management activities.'''
        from blogging.gui.search_posts_dialog import SearchPostsDialog

        self.search_posts_dialog = SearchPostsDialog(self.controller, self)
        self.search_posts_dialog.show()
