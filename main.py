#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

from PySide.QtCore import QUrl, Qt
from PySide.QtGui import QApplication
from PySide.QtDeclarative import QDeclarativeView
from backend.chat_manager import ChatManager

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("AIKON")

    view = QDeclarativeView()
    view.setWindowTitle("AIKON")
    view.setResizeMode(QDeclarativeView.SizeRootObjectToView)

    # N9 portrait
    if hasattr(Qt, "WA_LockPortraitOrientation"):
        view.setAttribute(Qt.WA_LockPortraitOrientation, True)

    chat_mgr = ChatManager()
    context = view.rootContext()
    context.setContextProperty("pyChatManager", chat_mgr)

    qml_file = os.path.join(BASE_DIR, "qml", "main.qml")
    view.setSource(QUrl.fromLocalFile(qml_file))

    errors = view.errors()
    if errors:
        for e in errors:
            print("QML Error:", e.toString())

    view.setGeometry(0, 0, 480, 854)
    view.showFullScreen()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
