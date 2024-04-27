import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QToolBar, QAction, QTabWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class BrowserWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Simple Browser")
        self.setGeometry(100, 100, 800, 600)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.create_toolbar()

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

        new_tab_action = QAction(QIcon("icons/plus.png"), "New Tab", self)
        new_tab_action.triggered.connect(self.create_new_tab)
        toolbar.addAction(new_tab_action)

    def create_new_tab(self):
        new_tab = QWidget()
        layout = QVBoxLayout()

        # Browser
        browser = QWebEngineView()
        browser.setUrl(QUrl("https://www.google.com"))
        layout.addWidget(browser)

        new_tab.setLayout(layout)
        self.tabs.addTab(new_tab, "New Tab")
        self.tabs.setCurrentWidget(new_tab)

    def go_to_url(self, url_entry, browser):
        url = url_entry.text()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        browser.setUrl(QUrl(url))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BrowserWindow()
    sys.exit(app.exec_())
