from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtPrintSupport import *

import sys


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)


        # Making an object of QWebEngineView Class
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://www.google.com'))

        self.setCentralWidget(self.browser)

        # Navigation Bar
        nav = QToolBar('Navigation Bar')
        nav.setIconSize(QSize(30, 30))
        self.addToolBar(nav)

        # Back Button
        backBtn = QAction(QIcon('Images/Back.png'), 'Back', self)
        backBtn.setStatusTip('Previous Page')
        backBtn.triggered.connect(self.browser.back)
        nav.addAction(backBtn)

        # Next Button
        nextBtn = QAction(QIcon('Images/Forward.png'), 'Next', self)
        nextBtn.setStatusTip('Next Page')
        nextBtn.triggered.connect(self.browser.forward)
        nav.addAction(nextBtn)

        # Reload Button
        reloadBtn = QAction(QIcon('Images/Reload.png'), 'Reload', self)
        reloadBtn.setStatusTip('Refresh')
        reloadBtn.triggered.connect(self.browser.reload)
        nav.addAction(reloadBtn)

        nav.addSeparator()

        # Home Button
        homeBtn = QAction(QIcon('Images/Home.png'), 'Home', self)
        homeBtn.setStatusTip('Home')
        homeBtn.triggered.connect(self.navigateToHome)
        nav.addAction(homeBtn)

        nav.addSeparator()

        # Http(s) Symbol
        self.http = QLabel()   # Image
        self.http.setPixmap(QPixmap('Images/Http.png').scaled(30,30))
        nav.addWidget(self.http)

        # Url Bar
        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.navigate)
        nav.addWidget(self.urlBar)

        nav.addSeparator()

        # Stop Button
        stopBtn = QAction(QIcon('Images/Stop.png'), 'Stop', self)
        stopBtn.setStatusTip('Stop')
        stopBtn.triggered.connect(self.browser.stop)
        nav.addAction(stopBtn)

        self.browser.urlChanged.connect(self.updateUrl)

        self.menuBar().setNativeMenuBar(False)

        # Menu Bar
        fileMenu = self.menuBar().addMenu('&File')
        editMenu = self.menuBar().addMenu('&Edit')
        viewMenu = self.menuBar().addMenu('&View')
        windowMenu = self.menuBar().addMenu('&Window')
        helpMenu = self.menuBar().addMenu('&Help')

        printAction = QAction(QIcon(), 'Print', self)
        printAction.setStatusTip('Print Current Page')
        printAction.triggered.connect(self.printPage)
        fileMenu.addAction(printAction)
        

        self.show()

        self.setWindowTitle('Browser Lite')
        self.setGeometry(5, 30, 1355, 730)
        self.setWindowIcon(QIcon('Images/BrowserIcon.png'))


    def printPage(self):
##        print('Printing...')
        diag = QPrintPreviewDialog()
        diag.setGeometry(100, 100, 1100, 600)
        page = self.browser.page()
        print('Done')
##        page.printToPdf()
##        diag.paintRequested.connect(page.printToPdf)
        print('Exec')

        diag.exec_()
##        print('Exit')


    def navigateToHome(self):

        self.browser.setUrl(QUrl('https://www.google.com'))


    def navigate(self): # URL not recieved

        q = QUrl(self.urlBar.text())
        if q.scheme() == '':    # If Scheme not set then, return '' blank string
            q.setScheme('http')
        self.browser.setUrl(q)



    def updateUrl(self, q):

        if q.scheme() == 'https':
            # Secure
            self.http.setPixmap(QPixmap('Images/Https.png').scaled(25,25))
        else:
            # Insecure
            self.http.setPixmap(QPixmap('Images/Http.png').scaled(30,30))
            
        
        self.urlBar.setText(q.toString())

        # To show the URL from starting
        self.urlBar.setCursorPosition(0)
        



app = QApplication(sys.argv)
app.setApplicationName('Browser Lite')
app.setOrganizationName('Lite Softwares')
app.setOrganizationDomain('litesoftwares.com')

win = MainWindow()
win.show()
app.exec_()
