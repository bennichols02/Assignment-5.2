import sys
from blogging.configuration import Configuration
from blogging.controller import Controller
from blogging.exception.invalid_login_exception import InvalidLoginException
from blogging.exception.duplicate_login_exception import DuplicateLoginException
from blogging.exception.invalid_logout_exception import InvalidLogoutException
from blogging.exception.illegal_operation_exception import IllegalOperationException
from blogging.exception.illegal_access_exception import IllegalAccessException
from blogging.gui.search_blog_dialog import SearchBlogDialog
from blogging.gui.create_blog_dialog import CreateBlogDialog
from blogging.gui.edit_blog_dialog import EditBlogDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import (
    QApplication,
    QFormLayout,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class BloggingGUI(QMainWindow):
    '''
    Primary window of the blogging system GUI application.
    Manages the transition between login screen and main application interface
    using a stacked widget layout. Coordinates user interactions with the
    underlying controller for all blogging operations.
    '''
    def __init__(self):
        """ 
        Initializes the main application window with default settings.
        Sets up persistence configuration, controller instance, and prepares
        the user interface components.
        """
        super().__init__()
        # set autosave to True to ensure persistence is working
        self.configuration = Configuration()
        self.configuration.__class__.autosave = True
        self.controller = Controller()

        self.setWindowTitle("Blogging System")
        self.resize(500, 200)

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)

        self.login_page = LoginPage(self.handle_login)
        self.home_page = HomePage(
            self.controller,
            self.handle_logout,
            self.open_search_dialog,
            self.open_create_dialog,
            self.open_edit_dialog,
        )
        self.stacked.addWidget(self.login_page)
        self.stacked.addWidget(self.home_page)
        self.stacked.setCurrentWidget(self.login_page)

    def handle_login(self, username: str, password: str):
        '''Processes user login attempt using provided credentials.
        Validates credentials through the controller and switches to home
        page on successful authentication. Displays appropriate error messages
        for invalid credentials or duplicate login attempts.'''
        self.login_page.set_status("")
        if not username or not password:
            self.login_page.set_status("Enter a username and password.")
            return

        try:
            self.controller.login(username, password)
        except DuplicateLoginException:
            self.login_page.set_status("A user is already logged in.")
            return
        except InvalidLoginException:
            self.login_page.set_status("Login failed. Check credentials.")
            return

        self.home_page.set_username(username)
        self.home_page.update_current_blog(None)
        self.login_page.clear_password()
        self.stacked.setCurrentWidget(self.home_page)

    def handle_logout(self):
        '''Terminates the current user session and returns to login screen.
        Clears user-specific data from the controller and resets the
        interface to its initial state.'''
        try:
            self.controller.logout()
        except InvalidLogoutException:
            # Should not happen via the UI, but keep UI state safe.
            self.home_page.set_status("No active user session.")
            return

        self.home_page.set_status("")
        self.stacked.setCurrentWidget(self.login_page)
        self.login_page.set_status("Logged out.")

    def open_search_dialog(self):
        '''Opens the blog search dialog for finding and viewing blogs.
        The dialog operates in non-modal mode, allowing users to interact
        with other parts of the application simultaneously.'''
        # Keep a reference when using non-blocking show
        self.search_dialog = SearchBlogDialog(self.controller, self)
        self.search_dialog.show()

    def open_create_dialog(self):
        '''Opens the blog management dialog for creating, updating, and
        deleting blogs. Provides comprehensive blog administration
        functionality in a dedicated interface..'''
        # Keep a reference when using non-blocking show
        self.create_dialog = CreateBlogDialog(self.controller, self)
        self.create_dialog.show()

    def open_edit_dialog(self):
        '''Opens the blog editing interface for the currently selected blog.
        Only available when a blog has been set as the current working blog.
        Provides access to post management and search functionality.'''
        try:
            current = self.controller.get_current_blog()
        except Exception:
            current = None

        # keep reference for non-blocking show
        self.edit_dialog = EditBlogDialog(self.controller, current, self)
        self.edit_dialog.show()


class LoginPage(QWidget):
    '''Authentication interface for user login.
    Presents a simple form for username and password entry with validation
    and error feedback. Provides access to system exit functionality.'''
    def __init__(self, on_login):
        '''Initializes the login page with authentication callback.'''
        super().__init__()
        self.on_login = on_login
        self._build_ui()

    def _build_ui(self):
        '''Constructs the login interface layout with all visual components.
        Arranges form elements, buttons, and status display in a centered,
        vertically organized layout.'''
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Application title and description
        title = QLabel("Blogging System")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 600;")

        subtitle = QLabel("Log in to manage blogs and posts")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("color: #555;")

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self._emit_login)
        
        # Form layout for credential input
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)

        button_row = QHBoxLayout()
        button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        login_button = QPushButton("Log in")
        login_button.clicked.connect(self._emit_login)
        button_row.addWidget(login_button)

        # Action buttons for login and application exit
        quit_button = QPushButton("Quit")
        quit_button.clicked.connect(QApplication.instance().quit)
        button_row.addWidget(quit_button)

        # Status display for authentication feedback
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #b00020;")

        
        # Assemble all components in the layout
        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addSpacing(10)
        layout.addLayout(form_layout)
        layout.addSpacing(10)
        layout.addLayout(button_row)
        layout.addSpacing(10)
        layout.addWidget(self.status_label)
        layout.addStretch()     

        # Container for centered presentation
        container = QWidget()
        container.setLayout(layout)
        outer = QVBoxLayout()
        outer.addStretch()
        outer.addWidget(container)
        outer.addStretch()
        self.setLayout(outer)

    def _emit_login(self):
        '''Collects entered credentials and forwards them to the login handler.
        Triggered by login button click or Enter key press in password field.'''
        username = self.username_input.text().strip()
        password = self.password_input.text()
        self.on_login(username, password)

    def set_status(self, message: str):
        self.status_label.setText(message)

    def clear_password(self):
        self.password_input.clear()


class HomePage(QWidget):
    '''Main navigation interface displayed after successful authentication.
    Provides access to all blogging system functionality through organized
    button groups and displays current session information.'''
    def __init__(self, controller, on_logout, on_search_blog, on_create_blog, on_edit_blog):
        '''Initializes the home page with navigation callbacks.'''
        super().__init__()
        self.controller = controller
        self.on_logout = on_logout
        self.on_search_blog = on_search_blog
        self.on_create_blog = on_create_blog
        self.on_edit_blog = on_edit_blog
        self._build_ui()

    def _build_ui(self):
        '''Constructs the home page layout with user information display,
        current blog selection interface, and application navigation buttons.
        Organizes functionality into logical groups for intuitive user flow.'''
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # User welcome display
        self.welcome_label = QLabel()
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 18px; font-weight: 600;")
        
        # Current blog status display
        self.current_blog_label = QLabel("Current blog: None")
        self.current_blog_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.current_blog_label.setStyleSheet("color: #555;")

        # Blog selection interface
        header_row = QVBoxLayout()
        header_row.setAlignment(Qt.AlignmentFlag.AlignCenter)

        choose_button = QPushButton("Set current blog")
        choose_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        choose_button.setMinimumWidth(170)
        choose_button.setMinimumHeight(42)
        choose_button.clicked.connect(self._handle_set_current_blog)

        self.current_blog_input = QLineEdit()
        self.current_blog_input.setValidator(QIntValidator(0, 1_000_000))
        self.current_blog_input.setPlaceholderText("Blog ID")
        self.current_blog_input.setFixedWidth(170)
        self.current_blog_input.returnPressed.connect(self._handle_set_current_blog)

        header_row.addWidget(self.current_blog_label)
        header_row.addSpacing(6)
        header_row.addWidget(self.current_blog_input, alignment=Qt.AlignmentFlag.AlignCenter)
        header_row.addSpacing(6)
        header_row.addWidget(choose_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Main navigation buttons
        button_row = QVBoxLayout()
        button_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_row.setSpacing(12)

        create_button = QPushButton("Blog manager")
        create_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        create_button.clicked.connect(self.on_create_blog)
        create_button.setToolTip("Create, update, and delete blogs")
        create_button.setMinimumWidth(170)
        create_button.setMinimumHeight(42)

        search_button = QPushButton("Search blog")
        search_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        search_button.clicked.connect(self.on_search_blog)
        search_button.setToolTip("Search blogs by ID, name, or list all blogs")
        search_button.setMinimumWidth(170)
        search_button.setMinimumHeight(42)

        self.edit_button = QPushButton("Edit blog")
        self.edit_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.edit_button.setEnabled(False)
        self.edit_button.setToolTip("Select a current blog first.")
        self.edit_button.setMinimumWidth(170)
        self.edit_button.setMinimumHeight(42)
        self.edit_button.clicked.connect(self.on_edit_blog)

        logout_button = QPushButton("Log out")
        logout_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        logout_button.clicked.connect(self.on_logout)
        logout_button.setToolTip("End your session and return to login")
        logout_button.setMinimumWidth(170)
        logout_button.setMinimumHeight(42)
        
        # Grid layout for button organization
        grid = QGridLayout()
        grid.setHorizontalSpacing(16)
        grid.setVerticalSpacing(12)
        grid.addWidget(create_button, 0, 0)
        grid.addWidget(search_button, 0, 1)
        grid.addWidget(self.edit_button, 1, 0)
        grid.addWidget(logout_button, 1, 1)

        row_wrapper = QHBoxLayout()
        row_wrapper.setAlignment(Qt.AlignmentFlag.AlignCenter)
        row_wrapper.addStretch()
        row_wrapper.addLayout(grid)
        row_wrapper.addStretch()

        button_row.addLayout(row_wrapper)

        # Status display for operation feedback
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #b00020;")

        # Assemble all components
        layout.addWidget(self.welcome_label)
        layout.addSpacing(8)
        layout.addLayout(header_row)
        layout.addSpacing(14)
        layout.addLayout(button_row)
        layout.addSpacing(10)
        layout.addWidget(self.status_label)
        layout.addStretch()
        self.setLayout(layout)

    def set_username(self, username: str):
        '''Update welcome banner with the active username.'''
        self.welcome_label.setText(f"Welcome, {username}")

    def set_status(self, message: str):
        '''Updates the operation status message displayed to the user.'''
        self.status_label.setText(message)

    def update_current_blog(self, blog):
        '''Updates the interface to reflect the currently selected blog.
        Enables or disables the edit button based on blog selection
        and updates the current blog display label with relevant information.
        '''
        if not blog:
            self.current_blog_label.setText("Current blog selected: None")
            self.edit_button.setEnabled(False)
            self.edit_button.setToolTip("Select a current blog first.")
            return
        self.current_blog_label.setText(
            f"Current blog selected: {blog.name} - ID: {blog.id}"
        )
        self.edit_button.setEnabled(True)
        self.edit_button.setToolTip(
            "Create, update, retrieve, delete, and list all posts in the current blog."
        )

    def _handle_set_current_blog(self):
        '''Processes user request to set a blog as the current working blog.
        
        Validates the entered blog ID, attempts to set it as current through
        the controller, and updates the interface accordingly. Provides
        appropriate error feedback for invalid IDs or permission issues.'''
        self.status_label.setText("")
        id_text = self.current_blog_input.text().strip()
        if not id_text:
            self.status_label.setText("Enter a blog ID first.")
            return

        blog_id = int(id_text)
        try:
            self.controller.set_current_blog(blog_id)
            blog = self.controller.get_current_blog()
            self.update_current_blog(blog)
            self.status_label.setText("")
        except (IllegalOperationException, IllegalAccessException) as exc:
            self.status_label.setText(str(exc))
        except Exception:
            self.status_label.setText("Unable to set current blog.")
        finally:
            self.current_blog_input.clear()


def main():
    """
    Application entry point for GUI mode execution.
    
    Initializes the PyQt6 application framework, creates the main window,
    and starts the event loop for user interaction.
    """
    app = QApplication(sys.argv)
    window = BloggingGUI()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()
