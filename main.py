import sys
from ctypes import windll, wintypes

import win32api
import win32gui
from win32con import *
from consts import *
# noinspection PyPackageRequirements
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget

user32 = windll.user32


class MainWindow(QMainWindow):
    msgNotify: int
    hwnd: int
    bootstrapped: bool = False

    def __init__(self):
        super().__init__()
        uic.loadUi("GUI.ui", self)

    def showEvent(self, a0: QtGui.QShowEvent) -> None:
        self.hwnd = self.winId().__int__()
        self.setHooks()
        self.bootstrapped = True

    def nativeEvent(self, eventType, message):
        if not self.bootstrapped:
            return super().nativeEvent(eventType, message)
        if eventType == b'windows_generic_MSG':
            msg = wintypes.MSG.from_address(message.__int__())
            if msg.message == self.msgNotify:
                # print("------------")
                # print(msg.wParam)
                # print(msg.lParam)
                if msg.wParam == HSHELL_WINDOWCREATED:
                    print('Created', msg.lParam)
                elif msg.wParam == HSHELL_WINDOWACTIVATED:
                    print('Activated')
                elif msg.wParam == HSHELL_WINDOWDESTROYED:
                    print('Destroyed', msg.lParam)
                elif msg.wParam == HSHELL_GETMINRECT:
                    print('GetMinRect')
                elif msg.wParam == HSHELL_WINDOWFULLSCREEN:
                    print('Fullscreen')
                elif msg.wParam == HSHELL_WINDOWNORMAL:
                    print('Normal')
                elif msg.wParam == HSHELL_REDRAW:
                    print('Redraw')
                elif msg.wParam == HSHELL_FLASH:
                    print('Flash')
        return super().nativeEvent(eventType, message)

    def setHooks(self):
        self.msgNotify = win32api.RegisterWindowMessage("SHELLHOOK")
        user32.RegisterShellHookWindow(self.hwnd)
        user32.SetShellWindow(self.hwnd)
        user32.SetTaskmanWindow(self.hwnd)

    def onWinIdChange(self):
        self.hwnd = self.winId().__int__()
        self.setHooks()


app = QApplication(sys.argv)
window = MainWindow()


def onBtnClick():
    print()


list: QListWidget = window.listWidget
button: QPushButton = window.pushButton

button.clicked.connect(onBtnClick)

window.show()
code = app.exec_()
sys.exit(code)
