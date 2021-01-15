
import sys

##################################################################################################
#                                        IMPORT PYQT5                                            #
##################################################################################################
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtGui import QIcon
from functools import partial


##################################################################################################
#                                     CALCULATOR WINDOW CLASS                                    #
##################################################################################################
# To create calculator's window along with a grid of buttons
class CalculatorWindow(QMainWindow):
    # initializer
    def __init__(self, parent=None):
        super().__init__(parent)

        # set window's attributes
        self.setWindowTitle("Calculator")
        self.setFixedSize(300, 300)

        # add and set central widget
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.calculator_layout = QVBoxLayout()
        self.central_widget.setLayout(self.calculator_layout)   # set layout for central widget of window

        self.set_display()         # create display box
        self.set_buttons()         # create button' grid
    # ***********************************************************************


    #to set display widget
    def set_display(self):
        self.display = QLineEdit()          # display area of calculator
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)      # display set to read only
        self.calculator_layout.addWidget(self.display)
    # ***********************************************************************


    #to set grid of buttons
    def set_buttons(self):
        # Dictionary of all buttons [key: (PosX, PosY)]
        buttons_list = {
            '7': (0, 0),
            '8': (0, 1),
            '9': (0, 2),
            '/': (0, 3),
            'C': (0, 4),

            '4': (1, 0),
            '5': (1, 1),
            '6': (1, 2),
            '*': (1, 3),
            '(': (1, 4),

            '1': (2, 0),
            '2': (2, 1),
            '3': (2, 2),
            '-': (2, 3),
            ')': (2, 4),

            '0': (3, 0),
            '00': (3, 1),
            '.': (3, 2),
            '+': (3, 3),
            '=': (3, 4),
        }

        # empty dictionary to hold calculator's buttons
        self.btns = {}

        btns_grid_layout = QGridLayout()    # grid layout for button list

        # set grid of buttons
        for btn_key, pos in buttons_list.items():
            self.btns[btn_key] = QPushButton(btn_key)       #create buttton
            self.btns[btn_key].setFixedSize(40, 40)         #set dimensions of button
            btns_grid_layout.addWidget((self.btns[btn_key]), pos[0], pos[1])    #set xy-pos of a button in grid

        # attach grid to the general layout
        self.calculator_layout.addLayout(btns_grid_layout)  #attach grid layout to calculator
    # ***********************************************************************


    # display widget is the area where the expression will be printed
    # to update display tex
    def update_display_text(self, text):
        self.display.setText(text)
        self.setFocus()
    # ***********************************************************************


    # to clear display text
    def clear_display_text(self):
        self.update_display_text("")
    # ***********************************************************************


    # to get text of display area i.e current expression
    def get_display_text(self):
        return self.display.text()
    # ***********************************************************************



##################################################################################################
#                                        CONTROLLER CLASS                                        #
##################################################################################################
# To connect events with corresponding operations/slots
# to make a bridge b/w gui and operational code
class Controller:
    def __init__(self, gui):
        self.gui = gui
        self.connect_events()
    # ***********************************************************************

    # calculate result of expression and output it on the display area
    def calculate_expression(self, exp):
        result = (update_expression(self.gui.get_display_text()))
        self.gui.update_display_text(result)

    #display error/result for displayed expression
    def display_expression(self, btn_key):
        if self.gui.get_display_text() == "Erorr!":
            self.gui.clear_display_text()

        self.gui.update_display_text(self.gui.get_display_text() + btn_key)
    # ***********************************************************************

    # perform operations corresponding to specific events
    def connect_events(self):
        for btn_key in self.gui.btns:
            if btn_key != '=' and btn_key != 'C':
                self.gui.btns[btn_key].clicked.connect(partial(self.display_expression, btn_key))

        self.gui.btns['='].clicked.connect(self.calculate_expression)
        self.gui.display.returnPressed.connect(self.calculate_expression)
        self.gui.btns['C'].clicked.connect(self.gui.clear_display_text)
    # ***********************************************************************


# update expression based on the input text
# return ERROR! if expression is invalid
# Otherwise, return result of current valid expression
def update_expression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = "Error!"
    return result
# ***********************************************************************



# driver function
def main():
    app = QApplication(sys.argv)
    window = CalculatorWindow()
    window.setWindowIcon(QIcon("images/calculator.ico"))      # set icon for window
    window.show()
    Controller(gui=window)
    sys.exit(app.exec())
# ***********************************************************************

main()
