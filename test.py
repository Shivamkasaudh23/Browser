import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QToolBar, QAction, QTabWidget, QShortcut, QMenu
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Shivam's Browser")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_toolbar()

        # Initial tab
        self.create_new_tab()

        self.show()

    def create_toolbar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        url_entry = QLineEdit()
        url_entry.returnPressed.connect(lambda: self.go_to_url(url_entry, self.tabs.currentWidget()))
        toolbar.addWidget(url_entry)

        back_button = QPushButton(QIcon("icons/back.png"), "")
        back_button.clicked.connect(lambda: self.tabs.currentWidget().back())
        toolbar.addWidget(back_button)

        forward_button = QPushButton(QIcon("icons/forward.png"), "")
        forward_button.clicked.connect(lambda: self.tabs.currentWidget().forward())
        toolbar.addWidget(forward_button)

        refresh_button = QPushButton(QIcon("icons/refresh.png"), "")
        refresh_button.clicked.connect(lambda: self.tabs.currentWidget().reload())
        toolbar.addWidget(refresh_button)

        new_tab_button = QPushButton(QIcon("icons/plus.png"), "")
        new_tab_button.clicked.connect(self.create_new_tab)
        toolbar.addWidget(new_tab_button)

        incognito_tab_button = QPushButton(QIcon("icons/incognito.png"), "")
        incognito_tab_button.clicked.connect(lambda: self.create_new_tab(incognito=True))
        toolbar.addWidget(incognito_tab_button)

        # Add keyboard shortcuts
        new_tab_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_T), self)
        new_tab_shortcut.activated.connect(self.create_new_tab)

        close_tab_shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_W), self)
        close_tab_shortcut.activated.connect(self.close_current_tab)

    def create_new_tab(self, incognito=False):
        new_tab = QWidget()
        layout = QVBoxLayout()

        # Browser
        browser = QWebEngineView()
        layout.addWidget(browser)

        new_tab.setLayout(layout)
        self.tabs.addTab(new_tab, "")  # Set an empty string as the initial header
        self.tabs.setCurrentWidget(new_tab)

        # Load Google on the new tab
        if incognito:
            browser.setUrl(QUrl("https://www.duckduckgo.com"))
        else:
            browser.setUrl(QUrl("https://www.google.com"))

        # Store the browser instance as an attribute of the new_tab widget
        new_tab.browser = browser

        # Connect the titleChanged signal to update the tab header
        browser.titleChanged.connect(lambda title: self.update_tab_header(new_tab, title))

    def close_current_tab(self):
        index = self.tabs.currentIndex()
        if index != -1:
            self.tabs.removeTab(index)

    def update_tab_header(self, tab, title):
        # Set the title of the tab based on the webpage title
        index = self.tabs.indexOf(tab)
        if index != -1:
            self.tabs.setTabText(index, title)

    def go_to_url(self, url_entry, tab):
        url = url_entry.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        # Access the browser instance from the tab widget
        tab.browser.setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    sys.exit(app.exec_())
