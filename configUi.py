# General imports
import json, time, os, sys, subprocess
from tkinter import messagebox
from datetime import datetime
# Qt imports
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QBrush, QColor, QFont, QPixmap, QIcon
from PyQt5.QtCore import QDate
from PyQt5 import uic, QtWidgets
# Local imports
from Utilities.general import *
import Assets
from Beta_GUI.configPane_ui import Ui_Form

class config_gui(QtWidgets.QMainWindow, Ui_Form):
    
    def __init__(self) -> None:
        super().__init__()
        self.PreStart()
        
    def PreStart(self):
        self.setupUi(self)
        self.prepareWidgets()
        self.loadVariable()
        self.setWindowTitle("MDW Launcher")
        
    def loadVariable(self) -> None:
        def pathCheck():
            if os.name == 'nt':  # Windows
                self.user_windows = os.environ.get('USERNAME', '')
                self.minecraft_directory = os.path.join(
                    f'C:{os.sep}', 'Users', self.user_windows, 'AppData', 'Roaming', '.mdwLauncher'
                )
            else:  # Linux u otros sistemas
                self.user_linux = os.environ.get('USER', '')
                self.minecraft_directory = os.path.join(
                    '/home', self.user_linux, '.mdwLauncher'
                )
            self.json_path = os.path.join(self.minecraft_directory, f"{os.sep}mdw_config.json")
            if not os.path.exists(self.minecraft_directory):
                os.makedirs(self.minecraft_directory)
        def javaCheck():
            try:
                # Check for Java in environment variables (more reliable)
                java_path = subprocess.check_output(["where", "java"]).decode("utf-8").splitlines()[0]  # Adjust for OS (Windows)
                print(f"Java found: {java_path}")
                return True  # Indicate successful Java detection
            except subprocess.CalledProcessError:
                # Handle Java not found scenario
                ErrorMsg('Java error', 'Make sure you have Java installed correctly. If the problem persists, specify the path in the configuration.')
                return False  # Indicate failed Java detection
            except Exception as e:  # Catch other potential errors
                ErrorMsg(
                    'Unexpected error',
                    f'{e}'
                    )
                return False  # Indicate unexpected failure
        pathCheck()
        javaCheck()
            
    def exit_(self) -> None:
        if QstMsg(
            'Exit',
            'Are you sure to exit the launcher?'
            ):
            exit()
            
    def seeLocalFiles(self) -> None:
        if os.name == 'nt':  # Windows
            os.startfile(self.minecraft_directory)
        elif os.name == 'posix':  # Linux o macOS
            try:
                subprocess.Popen(['xdg-open', self.minecraft_directory])
            except FileNotFoundError:
                ErrorMsg(
                         'Explorer error'
                         'Could not open file explorer. Check that xdg-open is installed.'
                        )
        else:
            ErrorMsg(
                    'System error',
                    f'Unknown operating system "{os.name}".'
                    )

    def configload(self):
        pass
        
    def prepareWidgets(self) -> None:
        def loadImages():
            self.setWindowIcon(Assets.AssetImageLoader('commandBlock.png', True))
        def connectButtons():
            self.exitButton.clicked.connect(self.exit_)
            self.filesButton.clicked.connect(self.seeLocalFiles)
        loadImages()
        connectButtons()
            
def run():
    app = QApplication(sys.argv)
    gui = config_gui()
    gui.show()
    sys.exit(app.exec_())