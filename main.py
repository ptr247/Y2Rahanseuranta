from gui import GUI

import sys
from PyQt5.QtWidgets import QApplication

def main():


    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    gui = GUI()



    sys.exit(app.exec_())



if __name__ == "__main__":
    main()