#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

@author: Derek Wiseman
"""


import sys
from PyQt5 import QtWidgets, QtWebEngineWidgets

"""A GUI that will be the parent for the folium map."""
class GUI:
    def __init__(self):
        self._app = QtWidgets.QApplication([])
    
    """Display the folium map"""
    def _display(self):
        sys.exit(self._app.exec_())
    
    """
    Set the window and call internal display method
    @param folium_map the folium object to display within the WebEngineView
    """
    def display_map(self, folium_map):
        # Create a main window for the application
        main_window = QtWidgets.QMainWindow()
        
        # Set a descriptive title for the window
        main_window.setWindowTitle("Network Map Visualizer")
        
        # Set an initial, larger size for the window
        main_window.resize(1024, 768) # A common resolution for better viewing

        browser = QtWebEngineWidgets.QWebEngineView()
        browser.setHtml(folium_map.get_root().render())
        # Set the web view as the central widget of the main window
        main_window.setCentralWidget(browser)
        
        # Optionally, add a status bar (can be used for messages like "Loading...")
        main_window.statusBar().showMessage("Map loaded successfully.")

        # Show the main window
        main_window.show()
        self._display()
        


