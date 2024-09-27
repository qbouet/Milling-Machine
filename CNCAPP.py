"""
CC2511 - Assignment 2
CNC App Software
John Edmer Ortiz, Thomas Mehes, Quentin Bouet
"""
import sys
import serial
from PyQt5 import QtCore, QtWidgets

conn = serial.Serial("COM14", baudrate=115200, timeout=1)

# motor manual control delay (milliseconds)
MTR_DELAY = 1

# signals read by pico
Y_UP = "1"
X_LEFT = "2"
Y_DOWN = "3"
X_RIGHT = "4"
Z_RAISE = "5"
Z_LOWER = "6"
TOGGLE_SPINDLE = "7"
INC_PWM = "8"
DEC_PWM = "9"
DRAW = "0"
STOP_SPINDLE = "Q"

SCALE = 7  # multiply commands to pico by SCALE
Z_CLEARANCE = 300  # number of steps in Z direction when raising spindle during drawing process
X_LIMIT = 700
Y_LIMIT = 700
FILE_NAME = "matrix.txt"

class Ui_MainWindow(object):

    # start with spindle off
    spindle_status = False

    # get and format matrix from txt. file into MATRIX (list of lists format)
    MATRIX = []
    with open(FILE_NAME, "r") as in_file:
        for line in in_file:
            MATRIX.append(list(line.strip(", \n").split(",")))

    # convert strings to ints
    index_y = 0
    for row in MATRIX:
        index_x = 0
        for value in row:
            MATRIX[index_y][index_x] = int(value)
            index_x += 1
        index_y += 1

    def setupUi(self, MainWindow):
        """Creates, sets dimensions and positions of UI buttons"""
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 410)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.inc_pwm_button = QtWidgets.QPushButton(self.centralwidget)
        self.inc_pwm_button.setGeometry(QtCore.QRect(200, 340, 80, 50))
        self.inc_pwm_button.setObjectName("inc_pwm_button")
        self.inc_pwm_button.clicked.connect(self.inc_pwm)

        self.dec_pwm_button = QtWidgets.QPushButton(self.centralwidget)
        self.dec_pwm_button.setGeometry(QtCore.QRect(20, 340, 80, 50))
        self.dec_pwm_button.setObjectName("dec_pwm_button")
        self.dec_pwm_button.clicked.connect(self.dec_pwm)

        self.draw_button = QtWidgets.QPushButton(self.centralwidget)
        self.draw_button.setGeometry(QtCore.QRect(125, 145, 50, 50))
        self.draw_button.setObjectName("draw_button")
        self.draw_button.clicked.connect(self.start_drawing)

        self.spindle_button = QtWidgets.QPushButton(self.centralwidget)
        self.spindle_button.setGeometry(QtCore.QRect(100, 340, 100, 50))
        self.spindle_button.setObjectName("spindle_button")
        self.spindle_button.clicked.connect(self.toggle_spindle)

        self.y_up_button = QtWidgets.QPushButton(self.centralwidget)
        self.y_up_button.setGeometry(QtCore.QRect(110, 10, 81, 91))
        self.y_up_button.setObjectName("y_up_button")
        self.y_up_button.pressed.connect(self.start_moving_up)
        self.y_up_button.released.connect(self.stop_moving_up)

        self.x_left_button = QtWidgets.QPushButton(self.centralwidget)
        self.x_left_button.setGeometry(QtCore.QRect(10, 120, 81, 91))
        self.x_left_button.setObjectName("x_left_button")
        self.x_left_button.pressed.connect(self.start_moving_left)
        self.x_left_button.released.connect(self.stop_moving_left)

        self.y_down_button = QtWidgets.QPushButton(self.centralwidget)
        self.y_down_button.setGeometry(QtCore.QRect(110, 230, 81, 91))
        self.y_down_button.setObjectName("y_down_button")
        self.y_down_button.pressed.connect(self.start_moving_down)
        self.y_down_button.released.connect(self.stop_moving_down)

        self.x_right_button = QtWidgets.QPushButton(self.centralwidget)
        self.x_right_button.setGeometry(QtCore.QRect(210, 120, 81, 91))
        self.x_right_button.setObjectName("x_right_button")
        self.x_right_button.pressed.connect(self.start_moving_right)
        self.x_right_button.released.connect(self.stop_moving_right)

        self.z_raise_button = QtWidgets.QPushButton(self.centralwidget)
        self.z_raise_button.setGeometry(QtCore.QRect(310, 60, 81, 91))
        self.z_raise_button.setObjectName("z_raise_button")
        self.z_raise_button.pressed.connect(self.start_moving_raise)
        self.z_raise_button.released.connect(self.stop_moving_raise)

        self.z_lower_button = QtWidgets.QPushButton(self.centralwidget)
        self.z_lower_button.setGeometry(QtCore.QRect(310, 180, 81, 91))
        self.z_lower_button.setObjectName("z_lower_button")
        self.z_lower_button.pressed.connect(self.start_moving_lower)
        self.z_lower_button.released.connect(self.stop_moving_lower)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 421, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        """Sets UI widget initial properties"""
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.draw_button.setText(_translate("MainWindow", "DRAW"))
        self.y_up_button.setText(_translate("MainWindow", "Y_UP"))
        self.x_left_button.setText(_translate("MainWindow", "X_LEFT"))
        self.y_down_button.setText(_translate("MainWindow", "Y_DOWN"))
        self.x_right_button.setText(_translate("MainWindow", "X_RIGHT"))
        self.z_raise_button.setText(_translate("MainWindow", "Z_RAISE"))
        self.z_lower_button.setText(_translate("MainWindow", "Z_LOWER"))
        self.spindle_button.setText(_translate("MainWindow", "TOGGLE_SPINDLE"))
        self.inc_pwm_button.setText(_translate("MainWindow", "INC_PWM"))
        self.dec_pwm_button.setText(_translate("MainWindow", "DEC_PWM"))
        self.inc_pwm_button.setEnabled(False)
        self.dec_pwm_button.setEnabled(False)

    ####################################################################################################

    def dec_pwm(self):
        """sends "Decrease PWM" signal"""
        conn.write(DEC_PWM.encode())

    ####################################################################################################

    def inc_pwm(self):
        """sends "Increase PWM" signal"""
        conn.write(INC_PWM.encode())

    ####################################################################################################

    def toggle_spindle(self):
        """sends "toggle spindle" signal"""
        self.spindle_status = not self.spindle_status
        if self.spindle_status:
            self.inc_pwm_button.setEnabled(True)
            self.dec_pwm_button.setEnabled(True)
        else:
            self.inc_pwm_button.setEnabled(False)
            self.dec_pwm_button.setEnabled(False)
        conn.write(TOGGLE_SPINDLE.encode())

    ####################################################################################################

    def start_drawing(self):
        """draw image efficiently from matrix using algorithm (Q code)"""
        # send draw signal to pico
        conn.write(DRAW.encode())

        # set reference position (origin) to same as corner of matrix
        position = [0, 0]

        # raise spindle from desired position (indicated by user)
        print("RAISING")
        for i in range(Z_CLEARANCE):
            conn.write(Z_RAISE.encode())

        # start by scanning right side first
        scan_right = True
        # reset limit flag
        stop_drawing = False
        # while there is still "1"s in the matrix and the x and y limits haven't been reached yet
        while self.check(self.MATRIX) and not stop_drawing:

            # find first "1" in matrix
            position, x, y = self.find_first_one(position)

            # go to next surrounding "1"
            while not stop_drawing:

                # scan right side of current position
                if scan_right:
                    print("SCANNING RIGHT...")

                    # 0  0  0
                    # 0 "1" 1
                    # 0  0  0  => right
                    if self.MATRIX[y][x + 1] == 1:
                        x += 1

                    # 0  0  0
                    # 0 "1" 0
                    # 0  1  0  => bottom
                    elif self.MATRIX[y + 1][x] == 1:
                        y += 1

                    # 0  1  0
                    # 0 "1" 0
                    # 0  0  0  => top
                    elif self.MATRIX[y - 1][x] == 1:
                        y += -1

                    # 0  0  1
                    # 0 "1" 0
                    # 0  0  0  => top right
                    elif self.MATRIX[y - 1][x + 1] == 1:
                        y += -1
                        x += 1

                    # 0  0  0
                    # 0 "1" 0
                    # 0  0  1  => bottom right
                    elif self.MATRIX[y + 1][x + 1] == 1:
                        y += 1
                        x += 1

                    else:
                        # scan left next time before exiting loop
                        scan_right = False
                        break

                # scan left side of current position
                else:
                    print("SCANNING LEFT...")

                    # 0  0  0
                    # 1 "1" 0
                    # 0  0  0  => left
                    if self.MATRIX[y][x - 1] == 1:
                        x += -1

                    # 0  0  0
                    # 0 "1" 0
                    # 0  1  0  => bottom
                    elif self.MATRIX[y + 1][x] == 1:
                        y += 1

                    # 0  1  0
                    # 0 "1" 0
                    # 0  0  0  => top
                    elif self.MATRIX[y - 1][x] == 1:
                        y += -1

                    # 1  0  0
                    # 0 "1" 0
                    # 0  0  0  => top left
                    elif self.MATRIX[y - 1][x - 1] == 1:
                        y += -1
                        x += -1

                    # 0  0  0
                    # 0 "1" 0
                    # 1  0  0  => bottom left
                    elif self.MATRIX[y + 1][x - 1] == 1:
                        y += 1
                        x += -1

                    else:
                        # scan right next time before exiting loop
                        scan_right = True
                        break

                self.give_instructions(position, x, y)
                position = [x + 1, y + 1]
                print(position)

                # stop drawing (exit all loops) if x or y limit is reached
                stop_drawing = self.check_limits(stop_drawing, x, y)

                # replace "1" with "2" to avoid repetition
                self.MATRIX[y][x] = 2

            # raise spindle when there are no more surrounding "1"
            print("RAISING")
            for i in range(Z_CLEARANCE):
                conn.write(Z_RAISE.encode())

        # stop spindle after drawing process
        conn.write(STOP_SPINDLE.encode())

        # UNCOMMENT for debugging
        # for row in self.MATRIX:
        #     print(row)

    def check_limits(self, stop_drawing, x, y):
        """check x and y limits if reached"""
        if x > X_LIMIT or y > Y_LIMIT:
            stop_drawing = True
            print("REACHED BOUNDARY LIMIT")
        return stop_drawing

    def find_first_one(self, position):
        """find first "1" in matrix"""
        # set x and y to -1 because 0 is already a point in the matrix
        x = -1
        y = -1
        exit_loop = 0
        # scan entire matrix from top left of matrix till a "1" is found
        for row in self.MATRIX:
            y += 1
            x = -1  # restart x counter
            for value in row:
                x += 1
                if value == 1:
                    self.give_instructions(position, x, y)
                    position = [x + 1, y + 1]
                    print(position)
                    # lower spindle to the position of the first "1"
                    print("LOWERING")
                    for i in range(Z_CLEARANCE):
                        conn.write(Z_LOWER.encode())

                    # replace "1" with "2" to avoid repetition
                    self.MATRIX[y][x] = 2
                    exit_loop = 1
                    break
            if exit_loop == 1:
                break
        return position, x, y

    ####################################################################################################

    def check(self, matrix):
        """Check if matrix contains "1" """
        for row in matrix:
            for value in row:
                if value == 1:
                    return True
        return False

    ####################################################################################################

    def give_instructions(self, position, x, y):
        """Send instructions to pico (x and y directions) by comparing old and new position"""
        while position[0] > x + 1:
            for i in range(SCALE):
                print("MOVE LEFT")
                conn.write(X_LEFT.encode())
            position[0] += -1
        while position[0] < x + 1:
            for i in range(SCALE):
                conn.write(X_RIGHT.encode())
            position[0] += 1
        while position[1] > y + 1:
            for i in range(SCALE):
                print("MOVE UP")
                conn.write(Y_UP.encode())
            position[1] += -1
        while position[1] < y + 1:
            for i in range(SCALE):
                print("MOVE DOWN")
                conn.write(Y_DOWN.encode())
            position[1] += 1

        # UNCOMMENT for debugging
        # print(position)

    ####################################################################################################

    # Manual control for upward movement of Y motor

    def move_up(self):
        """Sends "move up" signal"""
        print("MOTOR IS MOVING UP")

        conn.write(Y_UP.encode())

    def start_moving_up(self):
        """Calls function move_up every MTR_DELAY intervals"""
        self.move_up_timer = QtCore.QTimer()
        self.move_up_timer.timeout.connect(self.move_up)
        self.move_up_timer.start(MTR_DELAY)

    def stop_moving_up(self):
        """Stops call loop when Y_UP button is released"""
        self.move_up_timer.stop()

    ####################################################################################################

    # Manual control for left movement of X motor

    def move_left(self):
        """Sends "move left" signal"""
        print("MOTOR IS MOVING LEFT")

        conn.write(X_LEFT.encode())

    def start_moving_left(self):
        """Calls function move_left every MTR_DELAY intervals"""
        self.move_left_timer = QtCore.QTimer()
        self.move_left_timer.timeout.connect(self.move_left)
        self.move_left_timer.start(MTR_DELAY)  # adjust interval as necessary

    def stop_moving_left(self):
        """Stops call loop when X_LEFT button is released"""
        self.move_left_timer.stop()

    ####################################################################################################

    # Manual control for downward movement of Y motor

    def move_down(self):
        """Sends "move down" signal"""
        print("MOTOR IS MOVING DOWN")

        conn.write(Y_DOWN.encode())

    def start_moving_down(self):
        """Calls function move_down every MTR_DELAY intervals"""
        self.move_down_timer = QtCore.QTimer()
        self.move_down_timer.timeout.connect(self.move_down)
        self.move_down_timer.start(MTR_DELAY)  # adjust interval as necessary

    def stop_moving_down(self):
        """Stops call loop when Y_DOWN button is released"""
        self.move_down_timer.stop()

    ####################################################################################################

    # Manual control for right movement of X motor

    def move_right(self):
        """Sends "move right" signal"""
        print("MOTOR IS MOVING RIGHT")

        conn.write(X_RIGHT.encode())

    def start_moving_right(self):
        """Calls function move_right every MTR_DELAY intervals"""
        self.move_right_timer = QtCore.QTimer()
        self.move_right_timer.timeout.connect(self.move_right)
        self.move_right_timer.start(MTR_DELAY)  # adjust interval as necessary

    def stop_moving_right(self):
        """Stops call loop when X_RIGHT button is released"""
        self.move_right_timer.stop()

    ####################################################################################################

    # Manual control for raise movement of Z motor

    def move_raise(self):
        """Sends "raise" signal"""
        print("MOTOR IS RISING")

        conn.write(Z_RAISE.encode())

    def start_moving_raise(self):
        """Calls function move_raise every MTR_DELAY intervals"""
        self.move_raise_timer = QtCore.QTimer()
        self.move_raise_timer.timeout.connect(self.move_raise)
        self.move_raise_timer.start(MTR_DELAY)  # adjust interval as necessary

    def stop_moving_raise(self):
        """Stops call loop when Z_RAISE button is released"""
        self.move_raise_timer.stop()

    ####################################################################################################

    # Manual control for lower movement of Z motor

    def move_lower(self):
        """Sends "lower" signal"""
        print("MOTOR IS LOWERING")

        conn.write(Z_LOWER.encode())

    def start_moving_lower(self):
        """Calls function move_lower every MTR_DELAY intervals"""
        self.move_lower_timer = QtCore.QTimer()
        self.move_lower_timer.timeout.connect(self.move_lower)
        self.move_lower_timer.start(MTR_DELAY)  # adjust interval as necessary

    def stop_moving_lower(self):
        """Stops call loop when Z_LOWER button is released"""
        self.move_lower_timer.stop()

    ####################################################################################################


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())
