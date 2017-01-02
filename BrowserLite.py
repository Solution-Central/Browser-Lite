from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtWebEngineCore import *
from PyQt5.QtPrintSupport import *

import sys


class AboutDialog(QDialog):

    def __init__(self, *args, **kwargs):
        # Initializing Super Class
        super(AboutDialog, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()

        title = QLabel('Browser Lite')
        font = title.font()
        font.setPointSize(24)
        title.setFont(font)
        layout.addWidget(title)

        logo = QLabel()
        logo.setPixmap(QPixmap('Images/BrowserIcon.png'))
        layout.addWidget(logo)

        layout.addWidget(QLabel('Version 2.1.1.0'))
        layout.addWidget(QLabel('Copyright 2016 Browser Lite Org.'))

        for i in range(layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        self.setLayout(layout)
        self.setWindowTitle('About Browser Lite')
        self.setWindowIcon(QIcon('Images/Help.png'))


class MainWindow(QMainWindow):
    
    def __init__(self, *args, **kwargs):

        super(MainWindow, self).__init__(*args, **kwargs)
        
        # Tab Widget
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tabDoubleClick)
        self.tabs.currentChanged.connect(self.tabChanged)
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.closeTab)

        self.setCentralWidget(self.tabs)

        # Navigation Bar
        nav = QToolBar('Navigation Bar')
        nav.setIconSize(QSize(30, 30))
        self.addToolBar(nav)

        # Back Button
        backBtn = QAction(QIcon('Images/Back.png'), 'Back', self)
        backBtn.setStatusTip('Previous Page')
        backBtn.triggered.connect(lambda: self.tabs.currentWidget().back())
        nav.addAction(backBtn)

        # Next Button
        nextBtn = QAction(QIcon('Images/Forward.png'), 'Next', self)
        nextBtn.setStatusTip('Next Page')
        nextBtn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        nav.addAction(nextBtn)

        # Reload Button
        reloadBtn = QAction(QIcon('Images/Reload.png'), 'Reload', self)
        reloadBtn.setStatusTip('Refresh')
        reloadBtn.triggered.connect(lambda: self.tabs.currentWidget().reload())
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
        self.urlBar = QLineEdit('--------------- Enter URL ---------------')
        self.urlBar.returnPressed.connect(self.navigate)
        nav.addWidget(self.urlBar)

        nav.addSeparator()

        progressBar = QProgressBar()
        progressBar.setMaximumHeight(20)
        progressBar.setMaximumWidth(150)
        nav.addWidget(progressBar)
##        self.tabs.currentWidget().loadStarted.connect(progressBar.reset)
             
        nav.addSeparator()

        # Stop Button
        stopBtn = QAction(QIcon('Images/Stop.png'), 'Stop', self)
        stopBtn.setStatusTip('Stop')
        stopBtn.triggered.connect(lambda: self.tabs.currentWidget().stop())
        nav.addAction(stopBtn)

        self.menuBar().setNativeMenuBar(False)

        # Menu Bar
        fileMenu = self.menuBar().addMenu('&File')
        editMenu = self.menuBar().addMenu('&Edit')
        viewMenu = self.menuBar().addMenu('&View')
        windowMenu = self.menuBar().addMenu('&Window')
        helpMenu = self.menuBar().addMenu('&Help')
        
        # Help Menu
        aboutHelp = QAction(QIcon('Images/Help.png'), 'About', self)
        aboutHelp.setStatusTip('About Browser')
        aboutHelp.triggered.connect(self.about)
        helpMenu.addAction(aboutHelp)
        helpMenu.addSeparator()

        pythonHelp = QAction(QIcon('Images/Python.png'), 'Python Org', self)
        pythonHelp.setStatusTip('Python Organisation')
        pythonHelp.triggered.connect(self.navigatePythonOrg)
        helpMenu.addAction(pythonHelp)
        helpMenu.addSeparator()
        
        qtHelp = QAction(QIcon('Images/Qt.png'), 'Qt Docs', self)
        qtHelp.setStatusTip('Qt Documentation')
        qtHelp.triggered.connect(self.navigateQt)
        helpMenu.addAction(qtHelp)
        helpMenu.addSeparator()
        # Help Menu Ends

        # File Menu
        openFile = QAction(QIcon('Images/Open-File.png'), 'Open File', self)
        openFile.setStatusTip('Open File From')
        openFile.triggered.connect(self.openAction)
        fileMenu.addAction(openFile)
        fileMenu.addSeparator()

        saveFile = QAction(QIcon('Images/Save.png'), 'Save File', self)
        saveFile.setStatusTip('Save File')
        saveFile.triggered.connect(self.saveAction)
        fileMenu.addAction(saveFile)
        fileMenu.addSeparator()

        printAction = QAction(QIcon('Images/Print-File.png'), 'Print', self)
        printAction.setStatusTip('Print Current Page')
        printAction.triggered.connect(self.printPage)
        fileMenu.addAction(printAction)
        fileMenu.addSeparator()

        newTabAction = QAction(QIcon('Images/Add-Tab.png'), 'New Tab', self)
        newTabAction.setStatusTip('Add New Tab')
        newTabAction.triggered.connect(self.newTab)
        fileMenu.addAction(newTabAction)
        fileMenu.addSeparator()
        #File Menu Ends
        
        self.newTab(QUrl('https://www.google.com'), 'Google')
        
        self.tabs.currentChanged.connect(lambda x:
        self.tabs.currentWidget().loadProgress.connect(progressBar.setValue))
        self.tabs.tabBarClicked.connect(lambda x:
        self.tabs.currentWidget().loadProgress.connect(progressBar.setValue))

        self.show()

        self.setWindowTitle('Browser Lite')
        self.setGeometry(5, 30, 1355, 730)
        self.setWindowIcon(QIcon('Images/BrowserIcon.png'))


    def newTab(self, qurl = None, label = 'Blank'):
        
        if (qurl is None) or (qurl is False):
            qurl = QUrl('')
        
        browser = QWebEngineView()
        browser.setUrl(qurl)
        t = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(t)
        
        browser.urlChanged.connect(lambda qurl, browser = browser:
                                   self.updateUrl(qurl, browser))

        browser.loadFinished.connect(lambda _, t=t, browser=browser:
                        self.tabs.setTabText(t, browser.page().title()))
        

    def tabDoubleClick(self, i):

        # No Tab Under Click
        if i == -1:
            self.newTab()


    def tabChanged(self, i):
        qurl = self.tabs.currentWidget().url()
        self.updateUrl(qurl, self.tabs.currentWidget())


    def closeTab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)


    def navigateQt(self):
        self.tabs.currentWidget().setUrl(QUrl('http://doc.qt.io/qt-5/'))


    def navigatePythonOrg(self):
        self.tabs.currentWidget().setUrl(QUrl('https://www.python.org'))
        
    
    def about(self):
        dlg = AboutDialog()
        dlg.exec()


    def openAction(self):
        fileName, _ = QFileDialog.getOpenFileName(self, 'Open File', '',
                                               'Hypertext Markup Language (*.htm, *html);;'
                                               'All Files (*.*)')
        if fileName:
            with open(fileName, 'r', encoding = 'UTF-8') as f:
                html = f.read()
            
            self.tabs.currentWidget().setHtml(html)
            self.tabs.currentWidget().setUrl(QUrl(fileName))
            

    def saveAction(self):
        global name
        fileName, _ = QFileDialog.getSaveFileName(self, 'Save Page As', '',
                                                  'HTML Page (*.html *.htm);;'
                                                  'All Files (*.*)')

        if fileName:
            name = fileName
            html = self.tabs.currentWidget().page()
            html.toHtml(self.saveHtml)


    def saveHtml(self, save):
        with open(name, 'w', encoding = 'UTF-8') as f:
            f.write(save)
        

    def printPage(self):
        printer = QPrinter(QPrinter.HighResolution)
        printer.setOutputFormat(QPrinter.NativeFormat)
        printer.setOrientation(QPrinter.Portrait)
        printer.setPaperSize(QPrinter.A4)
        printer.setFullPage(True)

##        self.tabs.currentWidget().render(printer)

##        printWid = QPrintPreviewWidget(printer, self.tabs.currentWidget())
##        printDiag = QPrintPreviewDialog(printer, printWid)
##        print(printWid.pageCount())
##        printDiag.setGeometry(180, 100, 1000, 500)
##        printDiag.paintRequested.connect(printWid.print)
##
##        printDiag.exec_()


    def navigateToHome(self):

        self.tabs.currentWidget().setUrl(QUrl('https://www.google.com'))


    def navigate(self): # URL not recieved

        q = QUrl(self.urlBar.text())
        
        if q.scheme() == '':    # If Scheme not set then, return '' blank string
            q.setScheme('http')
        self.tabs.currentWidget().setUrl(q)



    def updateUrl(self, q, browser):
        
        # If the signal is not from the current widget, then Ignore.
        if browser != self.tabs.currentWidget():
            return

        if q.scheme() == 'https':
            # Secure
            self.http.setPixmap(QPixmap('Images/Https.png').scaled(25,25))
        else:
            # Insecure
            self.http.setPixmap(QPixmap('Images/Http.png').scaled(30,30))
        
        self.urlBar.setText(q.toString())

        # To show the URL from starting
        self.urlBar.setCursorPosition(0)
        

name = ''
app = QApplication(sys.argv)
app.setApplicationName('Browser Lite')
app.setOrganizationName('Lite Softwares')
app.setOrganizationDomain('litesoftwares.com')

win = MainWindow()
win.show()
app.exec_()
