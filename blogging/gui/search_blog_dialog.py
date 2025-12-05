from blogging.exception.illegal_access_exception import IllegalAccessException
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIntValidator, QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import (
    QDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QTableView,
    QVBoxLayout,
)
'''Dialog interface for searching, retrieving, and displaying blog information.
Implements three distinct blog search methods as required by the assignment:
1. Exact match search by blog ID
2. Partial match search by blog name
3. Complete listing of all registered blogs

All search results are displayed in a QTableView widget to meet assignment
requirements for blog presentation.'''


class SearchBlogDialog(QDialog):
    ''' Interactive dialog for locating and viewing blogs in the system.
    
    Provides a unified interface for multiple search strategies with
    real-time results displayed in a tabular format. Each search method
    validates user input and provides appropriate feedback through
    status messages and visual results.'''
    def __init__(self, controller, parent=None):
        '''Initializes the blog search dialog with controller integration.'''
        super().__init__(parent)
        self.controller = controller
        self.setWindowTitle("Blogs")
        self.resize(620, 420)
        self._build_ui()

    def _build_ui(self):
        ''' Constructs the dialog interface with search controls and results display.
        
        Organizes functionality into three distinct search sections:
        - ID-based exact matching
        - Name-based partial matching
        - Complete blog listing'''
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Dialog title with styling

        title = QLabel("Search Blogs")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: 600;")

        # Section 1: Search by exact blog ID
        id_block = QVBoxLayout()
        id_block.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.id_input = QLineEdit()
        self.id_input.setPlaceholderText("Enter blog ID")
        self.id_input.setValidator(QIntValidator(0, 1_000_000))
        search_id_button = QPushButton("Search by ID")
        search_id_button.setAutoDefault(False)
        search_id_button.setMinimumWidth(110)
        self.id_input.returnPressed.connect(lambda: search_id_button.click())
        search_id_button.clicked.connect(self._handle_search_by_id)
        id_block.addWidget(self.id_input)
        id_block.addSpacing(6)
        id_block.addWidget(search_id_button)

        # Section 2: Search by partial name matching
        name_block = QVBoxLayout()
        name_block.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.phrase_input = QLineEdit()
        self.phrase_input.setPlaceholderText("Enter phrase to search blog name")
        search_phrase_button = QPushButton("Search by Name")
        search_phrase_button.setAutoDefault(False)
        search_phrase_button.setMinimumWidth(110)
        self.phrase_input.returnPressed.connect(lambda: search_phrase_button.click())
        search_phrase_button.clicked.connect(self._handle_search_by_phrase)
        name_block.addWidget(self.phrase_input)
        name_block.addSpacing(6)
        name_block.addWidget(search_phrase_button)

        # Section 3: Complete blog listing and dialog control
        list_block = QVBoxLayout()
        list_block.setAlignment(Qt.AlignmentFlag.AlignTop)
        list_block.setContentsMargins(0, 0, 0, 0)
        list_all_button = QPushButton("List all blogs")
        list_all_button.setAutoDefault(False)
        list_all_button.setMinimumWidth(110)
        list_all_button.clicked.connect(self._handle_list_all)
        done_button = QPushButton("Done")
        done_button.setAutoDefault(False)
        done_button.setMinimumWidth(110)
        done_button.clicked.connect(self.accept)
        list_block.addSpacing(0)
        list_block.addWidget(list_all_button)
        list_block.addSpacing(2)
        list_block.addWidget(done_button)

        # Horizontal arrangement of all search sections
        actions_row = QHBoxLayout()
        actions_row.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignHCenter)
        actions_row.addLayout(id_block)
        actions_row.addSpacing(12)
        actions_row.addLayout(name_block)
        actions_row.addSpacing(12)
        actions_row.addLayout(list_block)

        # Status display for search feedback and error messages
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #b00020;")

        # Results table configured as required by assignment
        self.table = QTableView()
        self.model = QStandardItemModel(0, 4, self)
        self.model.setHorizontalHeaderLabels(["ID", "Name", "URL", "Email"])
        self.table.setModel(self.model)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QTableView.EditTrigger.NoEditTriggers)

        # Assemble all interface components
        layout.addWidget(title)
        layout.addSpacing(8)
        layout.addLayout(actions_row)
        layout.addSpacing(6)
        layout.addWidget(self.status_label)
        layout.addSpacing(8)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def _handle_search_by_id(self):
        '''Executes exact match search for a blog by its numeric identifier.
        
        Validates input format, checks user authentication status, and
        queries the controller for the specified blog. Displays the result
        in the table or shows appropriate error messages for:
        - Empty input fields
        - Authentication requirements
        - Non-existent blog IDs
        '''
        self.status_label.setText("")
        self._clear_table()
        id_text = self.id_input.text().strip()
        if not id_text:
            self.status_label.setText("Enter a blog ID to search.")
            self._schedule_reset_input(self.id_input)
            return

        blog_id = int(id_text)
        try:
            blog = self.controller.search_blog(blog_id)
        except IllegalAccessException:
            self.status_label.setText("You must login before searching blogs.")
            self._schedule_reset_input(self.id_input)
            return

        if not blog:
            self.status_label.setText("No blog found with that ID.")
            self._schedule_reset_input(self.id_input)
            return

        self._show_results([blog])
        self.status_label.setText("")

        self._schedule_reset_input(self.id_input)

    def _handle_search_by_phrase(self):
        '''Executes partial match search for blogs containing text in their names.
        
        Validates input presence, checks user authentication, and queries
        the controller for blogs matching the search phrase. Displays all
        matching results in the table or shows appropriate error messages for:
        - Empty search phrases
        - Authentication requirements
        - No matching blogs found.'''
        self.status_label.setText("")
        self._clear_table()
        phrase = self.phrase_input.text().strip()
        if phrase == "":
            self.status_label.setText("Enter a search phrase.")
            self._schedule_reset_input(self.phrase_input)
            return

        try:
            blogs = self.controller.retrieve_blogs(phrase)
        except IllegalAccessException:
            self.status_label.setText("You must login before searching blogs.")
            self._schedule_reset_input(self.phrase_input)
            return

        if not blogs:
            self.status_label.setText("No blogs match that phrase.")
            self._schedule_reset_input(self.phrase_input)
            return

        self._show_results(blogs)
        self.status_label.setText("")
        self._schedule_reset_input(self.phrase_input)

    def _handle_list_all(self):
        '''Retrieves and displays all blogs currently registered in the system.
        
        Checks user authentication status and requests the complete blog
        list from the controller. Displays all blogs in the table or shows
        appropriate error messages for:
        - Authentication requirements
        - Empty blog registry'''
        self.status_label.setText("")
        self._clear_table()
        try:
            blogs = self.controller.list_blogs()
        except IllegalAccessException:
            self.status_label.setText("You must login before listing blogs.")
            self._schedule_reset_input()
            return

        if not blogs:
            self.status_label.setText("No blogs registered.")
            self._schedule_reset_input()
            return

        self._show_results(blogs)
        self.status_label.setText("")
        self._schedule_reset_input()

    def _show_results(self, blogs):
        '''Converts each blog object into a table row with four columns
        representing the blog's ID, Name, URL, and Email attributes.
        All table items are set as non-editable to maintain data integrity
        and prevent accidental modification through the search interface.'''
        self.model.setRowCount(0)
        for blog in blogs:
            row = [
                QStandardItem(str(blog.id)),
                QStandardItem(blog.name),
                QStandardItem(blog.url),
                QStandardItem(blog.email),
            ]
            for item in row:
                item.setEditable(False)
            self.model.appendRow(row)

    def _clear_table(self):
        ''' Removes all existing rows from the results table.
        
        Prepares the table for new search results by resetting its
        content while preserving the column structure and headers.
        Ensures clean presentation of each search operation's output.
        '''
        self.model.setRowCount(0)

    def _schedule_reset_input(self, target_input=None):
        ''' 
        Schedules asynchronous clearing of input fields.

        Uses QTimer to perform input clearing without blocking the UI thread.
        This provides smoother user experience by allowing immediate visual
        feedback before field reset occurs.'''
        QTimer.singleShot(0, lambda: self._reset_input(target_input))

    def _reset_input(self, target_input=None):
        ''' Resets both ID and phrase search fields to empty state. Optionally
        sets focus to a specified input widget to facilitate rapid sequential
        searches without manual field selection.
        '''
        self.id_input.clear()
        self.phrase_input.clear()
        if target_input is not None:
            target_input.setFocus()
