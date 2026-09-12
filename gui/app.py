# app.py
import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    # 1. Create the QApplication instance
    app = QApplication(sys.argv)
    
    # Optional: Apply global app styling or themes here
    # app.setStyle("Fusion")

    # 2. Instantiate and display the main window
    window = MainWindow()
    window.show()

    # 3. Start the Qt event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()