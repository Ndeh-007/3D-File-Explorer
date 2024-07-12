import ctypes
import os
import sys


from PySide6.QtWidgets import QApplication

from views.explorer import FileExplorer

# define the application resources
from assets import resources

# define the environment settings
# os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=0"  # disable dark mode support

# initialize the window taskbar icon
myAppID = u'akumah.file.tree.0'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myAppID)
basedir = os.path.dirname(__file__)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileExplorer()
    window.show()
    sys.exit(app.exec())
