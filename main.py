# General imports
import json, time, os, sys, subprocess
from tkinter import messagebox
from datetime import datetime
# Qt imports
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow
from PyQt5.QtGui import QStandardItemModel, QStandardItem,QBrush, QColor, QFont, QPixmap, QIcon
from PyQt5.QtCore import QDate, QTimer
from PyQt5 import uic, QtWidgets
# Local imports

def eliminar_esta_funcion():
    def reemplazar_palabra(archivo, palabra_a_buscar, palabra_a_reemplazar):

        with open(archivo, "r") as f:
            contenido = f.read()

        contenido_nuevo = contenido.replace(palabra_a_buscar, palabra_a_reemplazar)

        with open(archivo, "w") as f:
            f.write(contenido_nuevo)
    ruta_menu_GUI = "C:\\Users\\migue\\Documents\\GitHub\\MDWLauncher\\Beta_GUI\\menu_ui.py"
    ruta_config_GUI = "C:\\Users\\migue\\Documents\\GitHub\\MDWLauncher\\Beta_GUI\\configPane_ui.py"
    
    reemplazar_palabra(ruta_config_GUI, "Ui_Form", "Ui_ConfigPane")
    reemplazar_palabra(ruta_config_GUI, "retranslateUi", "retranslateUiSettings")
    reemplazar_palabra(ruta_config_GUI, "setupUi", "OpenSettings")
    reemplazar_palabra(ruta_menu_GUI, "retranslateUi", "retranslateUiMenu")
    reemplazar_palabra(ruta_menu_GUI, "setupUi", "OpenMenu")
    reemplazar_palabra(ruta_menu_GUI, "Ui_Form", "Ui_Menu")
    
eliminar_esta_funcion()

from Utilities.general import *
import Assets
from Beta_GUI.menu_ui import Ui_Menu
from Beta_GUI.configPane_ui import Ui_ConfigPane

class ConfigPane(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_ConfigPane()
        self.ui.OpenSettings(self)

class main_gui(QtWidgets.QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self.menuUi = Ui_Menu()
        self.configUi = ConfigPane()
        self.PreStart()
        
    def PreStart(self):
        self.menuUi.OpenMenu(self)
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
            self.configPath = f"{self.minecraft_directory}{os.sep}mdw_config.mdw"
            print(self.configPath, self.minecraft_directory)
            if not os.path.exists(self.minecraft_directory):
                os.makedirs(self.minecraft_directory)
        def javaCheck():
            try:
                # Check for Java in environment variables (more reliable)
                java_path = subprocess.check_output(["where", "java"]).decode("utf-8").splitlines()[0]  # Adjust for OS (Windows)
                print(f"Java found: {java_path}")
                return java_path  # Indicate successful Java detection
            except subprocess.CalledProcessError:
                # Handle Java not found scenario
                ErrorMsg('Java error', 'Make sure you have Java installed correctly. If the problem persists, specify the path in the configuration.')
                exit()  # Indicate failed Java detection
            except Exception as e:  # Catch other potential errors
                ErrorMsg(
                    'Unexpected error',
                    f'{e}'
                    )
                exit()  # Indicate unexpected failure
        pathCheck()
        if not os.path.exists(self.configPath):
            checkJava = True
            corrupt = False
        else:
            with open(self.configPath,  "r") as f:
                if "&&" not in f.read():
                    ErrorMsg(
                            'Error config file',
                            'Corrupt file, default values ​​will be set.'
                            )
                    corrupt = True
                else:
                    corrupt = False
                if not os.path.exists(f.read().split("&&")[1]):
                    checkJava = True
                else:
                    checkJava = False
        if checkJava:
            javaPath = javaCheck()
            if not os.path.exists(self.configPath) or corrupt:
                with open(self.configPath, "w") as f:
                    f.write(f"2&&{javaPath}")
            else:
                with open(self.configPath, "r") as f:
                    ram = f.read().split("&&")[0]
                with open(self.configPath, "w") as f:
                    f.write(f"{ram}&&{javaPath}")
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
        self.configUi.show()  # Mostrar la ventana de configuración
        self.configUi.setWindowTitle("MDW launcher settings")
        self.prepareWidgets(False)
        if os.path.exists(self.configPath):
            with open(self.configPath, "r") as f:
                data = f.read().split("&&")
            self.configUi.ui.ramBox.setValue(int(data[0]))
            self.configUi.ui.javaPathEntry.setText(str(data[1]))
        
    def exitconfig(self):
        if QstMsg('Config', 'Changes you made may not be saved. Are you sure you want to exit?'):
            self.configUi.destroy()
        
    def saveConfig(self):
        ram = self.configUi.ui.ramBox.value()
        javaPath = self.configUi.ui.javaPathEntry.text()
        if not os.path.exists(javaPath):
            ErrorMsg(
                'Invalid Java path',
                'Java not found, not saving, retry.'
                )
        elif ram < 1:
            ErrorMsg(
                'Insufficient RAM specified',
                'Please specify a value greater than zero.'
                )
        else:
            with open(self.configPath, "w") as f:
                f.write(f"{ram}&&{javaPath}")

    def prepareWidgets(self, main = True) -> None:
        def loadImages():
            if main:
                self.menuUi.blockImage.setPixmap(Assets.AssetImageLoader('commandBlock.png'))
            self.setWindowIcon(Assets.AssetImageLoader('commandBlock.png', True))
        def connectButtons():
            if main:
                self.menuUi.settingsButton.clicked.connect(self.configload)
                self.menuUi.exitButton.clicked.connect(self.exit_)
                self.menuUi.filesButton.clicked.connect(self.seeLocalFiles)
            else:
                self.configUi.ui.saveButton.clicked.connect(self.saveConfig)
                self.configUi.ui.GoBackButton.clicked.connect(self.exitconfig)
                self.configUi.ui.filesButton.clicked.connect(self.seeLocalFiles)
        loadImages()
        connectButtons()
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = main_gui()
    gui.show()
    sys.exit(app.exec_())
