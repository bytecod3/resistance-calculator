import sys
import math
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

# For EIA-96 Resistors
MULTIPLIERS_DICTIONARY = {'Z': 0.001, 'Y': 0.01, 'R': 0.01, 'X': 0.1, 'S': 0.1, 'A': 1, 'B': 10, 'H': 10, 'C': 100, 'D': 1000, 'E': 10000, 'F': 100000}
SIGNIFICANT_FIGURES = {'01': 100, '02': 102, '03': 105, '04': 107, '05': 110, '06': 113, '07': 115, '08': 118,
                       '09': 121, '10': 124, '11': 127, '12': 130, '13': 133, '14': 137, '15': 140, '16': 143,
                       '17':147, '18': 150, '19': 154, '20': 158, '21': 162, '22': 165, '23': 169, '24': 174,
                       '25': 178, '26': 182, '27': 187, '28': 191, '29': 196, '30': 200, '31': 205, '32': 210,
                       '33': 215, '34': 221, '35': 226, '36': 232, '37':237, '38': 243, '39': 249, '40': 255,
                       '41': 261, '42': 267, '43':274, '44': 280, '45': 287, '46': 294, '47': 301, '48': 309,
                       '49':316, '50': 324, '51':332, '52':340, '53': 348, '54': 357, '55': 365, '56':374,
                       '57': 383, '58': 392, '59': 402, '60': 412, '61':422, '62': 432, '63':442, '64':453,
                       '65':464, '66':475, '67':487, '68':499, '69':511, '70':523, '71':536, '72':549,
                       '73':562, '74':576, '75':590, '76': 604, '77': 619, '78': 634, '79': 649, '80': 665,
                       '81': 681, '82': 698, '83': 715, '84':732, '85': 750, '86': 768, '87': 787, '88': 806,
                       '89': 825, '90': 845, '91':866, '92':887, '93': 909, '94': 931, '95': 953, '96': 976}


class Window(QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        grid = QGridLayout()
        grid.addWidget(self.four_band(), 0, 0)
        grid.addWidget(self.five_band(), 0, 1)
        grid.addWidget(self.three_digit_smd(), 0, 2)
        grid.addWidget(self.four_digit_smd(), 0, 3)
        grid.addWidget(self.EIA_96(), 0, 4)

        self.setLayout(grid)

        self.setWindowTitle("RESISTANCE_CALCULATOR")
        self.setFixedSize(800, 400)
        self.setStyleSheet("background-color: gray;")

        self.resize(400, 500)

    def three_digit_smd(self):
        """Set the layout of the three-digit SMD calculator window"""
        groupbox = QGroupBox("3-DIGIT")

        self.code_entry = QLineEdit()
        self.code_entry.setPlaceholderText("ENTER CODE...")
        self.code_entry.setStyleSheet("""QLineEdit{background-color: white; color: black; font: 16px bold;}""")
        self.code_entry.setMaxLength(3)
        calc = QPushButton("CALCULATE")
        calc.clicked.connect(self.three_digits)
        calc.setStyleSheet("background-color: darkseagreen;")
        self.show_code = QLineEdit()
        self.show_code.setReadOnly(True)
        self.show_code.setStyleSheet("""QLineEdit{background-color: black; color: red;}""")
        self.show_code.setFixedWidth(120)
        font = self.show_code.font()
        font.setPointSize(14)
        self.show_code.setFont(font)

        vbox = QVBoxLayout()
        vbox.addWidget(self.code_entry)
        vbox.addWidget(calc)
        vbox.addWidget(self.show_code)

        groupbox.setLayout(vbox)

        return groupbox

    def three_digits(self):
        """Calculate the resistance of an SMD calculator using the three-digit coding system"""
        entered = self.code_entry.text()
        splitted_code = list(entered)

        # if full code is not entered
        if len(splitted_code) < 3:
            QMessageBox.information(self, 'Error!', 'Resistor code required!', QMessageBox.Ok)
        elif splitted_code[0].isalpha() == True or splitted_code[2].isalpha() == True:
            QMessageBox.information(self, 'Error!', 'Invalid resistor code!', QMessageBox.Ok)

        elif entered[1] != "R":
            x = splitted_code[0] + splitted_code[1]
            x1 = int(x)
            y = x1 * (10 ** int(splitted_code[2]))
            if y <= 100:
                final_y = str(y) + " OHMS"
                self.show_code.setText(final_y)
            if 100 < y < 1000000:
                y = y / 1000
                final_y = str(y) + " K"
                self.show_code.setText(final_y)
            elif y >= 1000000:
                y = y / 1000000
                final_y = str(y) + " M"
                self.show_code.setText(final_y)
        else:
            x = entered
            y = x.replace('R', '.')
            final_y = y + ' OHMS'
            self.show_code.setText(final_y)

    def four_digit_smd(self):
        groupbox = QGroupBox("4-DIGIT")

        self.code_entry2 = QLineEdit()
        self.code_entry2.setPlaceholderText("ENTER CODE...")
        self.code_entry2.setStyleSheet("""QLineEdit{background-color: white; color: black; font: 16px bold;}""")
        self.code_entry2.setMaxLength(4)
        calcu = QPushButton("CALCULATE")
        calcu.clicked.connect(self.four_digits)
        calcu.setStyleSheet("background-color: darkseagreen;")
        self.show_code2 = QLineEdit()
        self.show_code2.setReadOnly(True)
        self.show_code2.setStyleSheet("""QLineEdit{background-color: black; color: red;}""")
        self.show_code2.setFixedWidth(120)
        font = self.show_code2.font()
        font.setPointSize(14)
        self.show_code2.setFont(font)

        vbox = QVBoxLayout()
        vbox.addWidget(self.code_entry2)
        vbox.addWidget(calcu)
        vbox.addWidget(self.show_code2)

        groupbox.setLayout(vbox)

        return groupbox

    def four_digits(self):
        """Calculates the resistance of an SMD resistor using the four-digit coding scheme"""
        entered2 = self.code_entry2.text()
        splitted_code2 = list(entered2)

        # if full code is not entered
        if len(splitted_code2) < 4:
            QMessageBox.information(self, 'Error!', 'Resistor code required!', QMessageBox.Ok)

        elif splitted_code2[0].isalpha()==True or splitted_code2[1].isalpha()== True or splitted_code2[3].isalpha() == True:
            QMessageBox.information(self, 'Error!', 'Resistor code required!', QMessageBox.Ok)

        elif splitted_code2[2] != 'R':
            a = splitted_code2[0] + splitted_code2[1] + splitted_code2[2]
            a1 = int(a)
            b = a1 * (10 ** int(splitted_code2[3]))
            if b < 1000:
                final_b = str(b) + ' OHMS'
                self.show_code2.setText(final_b)
            if 1000 < b < 1000000:
                b = b / 1000
                final_b = str(b) + " K"
                self.show_code2.setText(final_b)
            elif b >= 1000000:
                b = b / 1000000
                final_b = str(b) + " M"
                self.show_code2.setText(final_b)
        else:
            a = entered2
            b = a.replace('R', '.')
            final_b = b + ' OHMS'
            self.show_code2.setText(final_b)


    def EIA_96(self):
        """Sets the layout of the eia-96-coded resistor window"""
        groupbox = QGroupBox("EIA-96")

        self.code_entry3 = QLineEdit()
        self.code_entry3.setPlaceholderText("ENTER CODE...")
        self.code_entry3.setMaxLength(3)
        self.code_entry3.setStyleSheet("""QLineEdit{background-color: white; color: black; font: 16px bold;}""")
        calcul = QPushButton("CALCULATE")
        calcul.clicked.connect(self.EIA)
        calcul.setStyleSheet("background-color: darkseagreen;")
        self.show_code3 = QLineEdit()
        self.show_code3.setReadOnly(True)
        self.show_code3.setStyleSheet("""QLineEdit{background-color: black; color: red;}""")
        self.show_code3.setFixedWidth(130)
        font = self.show_code3.font()
        font.setPointSize(14)
        self.show_code3.setFont(font)

        vbox = QVBoxLayout()
        vbox.addWidget(self.code_entry3)
        vbox.addWidget(calcul)
        vbox.addWidget(self.show_code3)

        groupbox.setLayout(vbox)

        return groupbox

    def EIA(self):
        """This function calculates the resistance of high-precision resistors using the EIA-96 coding scheme
        The required dictionaries are defined at the top of this file """
        code_entered = self.code_entry3.text()
        identifiers = code_entered[:2]

        if len(code_entered) == 0:
            QMessageBox.information(self, 'Error!', 'Resistor code required!', QMessageBox.Ok)

        elif code_entered[2] not in MULTIPLIERS_DICTIONARY:
            QMessageBox.information(self, 'Error!', 'Invalid resistor code!', QMessageBox.Ok)

        elif len(code_entered) < 3 or code_entered[2].isnumeric():
            QMessageBox.information(self, 'Error!', 'Invalid resistor code!', QMessageBox.Ok)
        elif identifiers in SIGNIFICANT_FIGURES and code_entered[2].isalpha():
            full_value = SIGNIFICANT_FIGURES[identifiers]
            multiply_by = MULTIPLIERS_DICTIONARY[code_entered[2]]
            full_res_value = full_value * multiply_by

            if full_res_value < 1000:
                full_res_value = str(full_res_value)
                self.show_code3.setText(str(full_res_value[:4]) + " Ohms")
            elif 1000 <= full_res_value < 1000000:
                full_res_value /= 1000
                self.show_code3.setText(str(full_res_value) + " K")
            elif full_res_value >= 1000000:
                full_res_value /= 1000000
                self.show_code3.setText(str(full_res_value) + " M")
        else:
            QMessageBox.information(self, 'Error!', 'Invalid resistor code!', QMessageBox.Ok)

    def four_band(self):
        """This functions sets the layout for the four-band color coded resistance calculation part"""
        groupbox = QGroupBox("4-BAND")

        # Labels
        lbl_band1 = QLabel("BAND 1:")
        lbl_band2 = QLabel("BAND 2:")
        lbl_band3 = QLabel("BAND 3:")
        lbl_band4 = QLabel("BAND 4:")

        # Calculate button
        calculate_btn = QPushButton("CALCULATE")
        calculate_btn.setStyleSheet("margin-top: 42px;background-color: darkseagreen; padding-top: 2px; padding-bottom: 6px")

        calculate_btn.clicked.connect(self.compute_resistance)

        # Resistance display widget
        r_Label = QLabel("RESISTANCE:")
        #r_Label.setStyleSheet("margin-top: 10px")
        self.display = QLineEdit()
        self.display.setStyleSheet("""QLineEdit{background-color: black; color: red;}""")
        self.display.setFixedWidth(120)
        self.display.setReadOnly(True)
        font = self.display.font()
        font.setPointSize(16)
        self.display.setFont(font)

        # Tolerance display widget
        t_label = QLabel("TOLERANCE")
        # t_label.setStyleSheet("margin-top: 38px")
        self.tolerance = QLineEdit()
        self.tolerance.setStyleSheet("""QLineEdit{background-color: black; color: red;}""")
        self.tolerance.setFixedWidth(120)
        self.tolerance.setReadOnly(True)
        font = self.tolerance.font()
        font.setPointSize(16)
        self.tolerance.setFont(font)

        # CREATING COMBO BOXES AND ADDING ITEMS
        # Band 1
        self.combo1 = QComboBox()
        self.setObjectName("combo1")

        self.combo1.addItem("BLACK", 0)
        self.combo1.addItem("BROWN", 1)
        self.combo1.addItem("RED", 2)
        self.combo1.addItem("ORANGE", 3)
        self.combo1.addItem("YELLOW", 4)
        self.combo1.addItem("GREEN", 5)
        self.combo1.addItem("BLUE", 6)
        self.combo1.addItem("VIOLET", 7)
        self.combo1.addItem("GRAY", 8)
        self.combo1.addItem("WHITE", 9)
        self.combo1.currentIndexChanged.connect(self.sf_1)

        # Band 2
        self.combo2 = QComboBox()
        self.setObjectName("Combo2")
        self.combo2.addItem("BLACK", 0)
        self.combo2.addItem("BROWN", 1)
        self.combo2.addItem("RED", 2)
        self.combo2.addItem("ORANGE", 3)
        self.combo2.addItem("YELLOW", 4)
        self.combo2.addItem("GREEN", 5)
        self.combo2.addItem("BLUE", 6)
        self.combo2.addItem("VIOLET", 7)
        self.combo2.addItem("GRAY", 8)
        self.combo2.addItem("WHITE", 9)
        self.combo2.currentIndexChanged.connect(self.sf_2)

        # Band 3 (multiplier)
        self.combo3 = QComboBox()
        self.setObjectName("Combo3")
        self.combo3.addItem("BLACK", 0)
        self.combo3.addItem("BROWN", 1)
        self.combo3.addItem("RED", 2)
        self.combo3.addItem("ORANGE", 3)
        self.combo3.addItem("YELLOW", 4)
        self.combo3.addItem("GREEN", 5)
        self.combo3.addItem("BLUE", 6)
        self.combo3.addItem("VIOLET", 7)
        self.combo3.addItem("GRAY", 8)
        self.combo3.addItem("WHITE", 9)
        self.combo3.addItem("GOLD", 0.1)
        self.combo3.addItem("SILVER", 0.01)
        self.combo3.currentIndexChanged.connect(self.multiplier)

        # Band 4(Tolerance)
        self.combo4 = QComboBox()
        self.setObjectName("Combo4")
        self.combo4.addItem("SILVER", 10)
        self.combo4.addItem("RED", 2)
        self.combo4.addItem("BROWN", 1)
        self.combo4.addItem("GREEN", 0.5)
        self.combo4.addItem("BLUE", 0.25)
        self.combo4.addItem("VIOLET", 0.1)
        self.combo4.addItem("GRAY", 0.05)
        self.combo4.addItem("GOLD", 5)
        self.combo4.addItem("NONE", 20)
        self.combo4.currentIndexChanged.connect(self.p_tolerance)

        # Adding the widgets to the screen
        vbox = QVBoxLayout()
        vbox.addWidget(lbl_band1)
        vbox.addWidget(self.combo1)
        vbox.addWidget(lbl_band2)
        vbox.addWidget(self.combo2)
        vbox.addWidget(lbl_band3)
        vbox.addWidget(self.combo3)
        vbox.addWidget(lbl_band4)
        vbox.addWidget(self.combo4)
        vbox.addWidget(calculate_btn)
        vbox.addWidget(r_Label)
        vbox.addWidget(self.display)
        vbox.addWidget(t_label)
        vbox.addWidget(self.tolerance)
        vbox.addStretch(1)

        groupbox.setLayout(vbox)

        return groupbox

    # FUNCTIONS TO SET COLORS AND RESISTOR VALUE
    def sf_1(self, index):
        self.combo1.setStyleSheet("background-color: %s" % self.combo1.itemText(index))
        digit_1 = self.combo1.itemData(index)
        return digit_1

    def sf_2(self, index):
        self.combo2.setStyleSheet("background-color: %s" % self.combo2.itemText(index))
        digit_2 = self.combo2.itemText(index)
        return digit_2

    def multiplier(self, index):
        self.combo3.setStyleSheet("background-color: %s" % self.combo3.itemText(index))
        power = self.combo3.itemText(index)
        return power

    def p_tolerance(self, index):
        self.combo4.setStyleSheet("background-color: %s" % self.combo4.itemText(index))
        tolerance_value = self.combo4.itemText(index)
        return tolerance_value

    def compute_resistance(self):
        """This function calculates the resistance of four-band color coded resistor"""
        significant_digit1 = self.combo1.currentData()
        significant_digit2 = self.combo2.currentData()
        multiplier_value = self.combo3.currentData()
        tolerance_value = str(self.combo4.currentData()) + "%"

        raw_resistance = str(significant_digit1) + str(significant_digit2)
        total_resistor_value = int(raw_resistance) * (10 ** multiplier_value)

        # conversions
        if 0 < total_resistor_value < 1000:
            total_resistor_value = str(total_resistor_value) + " Ohms"

        elif 0 < total_resistor_value < 1000000:
            total_resistor_value = total_resistor_value / 1000
            total_resistor_value = str(total_resistor_value) + " K"

        elif total_resistor_value >= 1000000:
            total_resistor_value = total_resistor_value / 1000000
            total_resistor_value = str(total_resistor_value) + " M"

        self.display.setText(str(total_resistor_value))
        self.tolerance.setText(tolerance_value)

    # 5-BAND RESISTANCE
    def five_band(self):
        """This functions sets the layout for the five-band color coded resistance calculation part"""
        groupbox = QGroupBox("5-BAND")

        # Labels
        lbl_band_five1 = QLabel("BAND 1:")
        lbl_band_five2 = QLabel("BAND 2:")
        lbl_band_five3 = QLabel("BAND 3:")
        lbl_band_five4 = QLabel("BAND 4:")
        lbl_band_five5 = QLabel("BAND 5:")

        calculate = QPushButton("CALCULATE")
        calculate.setStyleSheet("background-color: darkseagreen;")
        calculate.clicked.connect(self.calculate_resistance)

        r_label5 = QLabel("RESISTANCE:")
        self.display5 = QLineEdit()
        self.display5.setStyleSheet("""QLineEdit{background-color: black; color: red;}""")
        self.display5.setFixedWidth(120)
        self.display5.setReadOnly(True)
        font = self.display5.font()
        font.setPointSize(16)
        self.display5.setFont(font)

        t_label5 = QLabel("TOLERANCE: ")
        self.tolerance5 = QLineEdit()
        self.tolerance5.setStyleSheet("""QLineEdit{background-color: black; color: red;}""")
        self.tolerance5.setFixedWidth(120)
        self.tolerance5.setReadOnly(True)
        font = self.tolerance5.font()
        font.setPointSize(16)
        self.tolerance5.setFont(font)

        # CREATING COMBO BOXES AND ADDING ITEMS
        # Band 1(digit 1)
        self.five1 = QComboBox()
        self.setObjectName("five1")
        self.five1.addItem("BLACK", 0)
        self.five1.addItem("BROWN", 1)
        self.five1.addItem("RED", 2)
        self.five1.addItem("ORANGE", 3)
        self.five1.addItem("YELLOW", 4)
        self.five1.addItem("GREEN", 5)
        self.five1.addItem("Blue", 6)
        self.five1.addItem("VIOLET", 7)
        self.five1.addItem("GRAY", 8)
        self.five1.addItem("WHITE", 9)
        self.five1.currentIndexChanged.connect(self.digit_five1)

        # Band 2(digit 2)
        self.five2 = QComboBox()
        self.setObjectName("five2")
        self.five2.addItem("BLACK", 0)
        self.five2.addItem("BROWN", 1)
        self.five2.addItem("RED", 2)
        self.five2.addItem("ORANGE", 3)
        self.five2.addItem("YELLOW", 4)
        self.five2.addItem("GREEN", 5)
        self.five2.addItem("BLUE", 6)
        self.five2.addItem("VIOLET", 7)
        self.five2.addItem("GRAY", 8)
        self.five2.addItem("WHITE", 9)
        self.five2.currentIndexChanged.connect(self.digit_five2)

        # Band 3(digit 3)
        self.five3 = QComboBox()
        self.setObjectName("five3")
        self.five3.addItem("BLACK", 0)
        self.five3.addItem("BROWN", 1)
        self.five3.addItem("RED", 2)
        self.five3.addItem("ORANGE", 3)
        self.five3.addItem("YELLOW", 4)
        self.five3.addItem("GREEN", 5)
        self.five3.addItem("BLUE", 6)
        self.five3.addItem("VIOLET", 7)
        self.five3.addItem("GRAY", 8)
        self.five3.addItem("WHITE", 9)
        self.five3.currentIndexChanged.connect(self.digit_five3)

        # Band 4(multiplier)
        self.five4 = QComboBox()
        self.setObjectName("five4")
        self.five4.addItem("BLACK", 0)
        self.five4.addItem("BROWN", 1)
        self.five4.addItem("RED", 2)
        self.five4.addItem("ORANGE", 3)
        self.five4.addItem("YELLOW", 4)
        self.five4.addItem("GREEN", 5)
        self.five4.addItem("BLUE", 6)
        self.five4.addItem("VIOLET", 7)
        self.five4.addItem("GRAY", 8)
        self.five4.addItem("WHITE", 9)
        self.five4.addItem("GOLD", 0.1)
        self.five4.addItem("SILVER", 0.01)
        self.five4.currentIndexChanged.connect(self.digit_multiplier)

        # Band 5(Tolerance)
        self.five5 = QComboBox()
        self.setObjectName("five5")
        self.five5.addItem("SILVER", 10)
        self.five5.addItem("YELLOW", 5)
        self.five5.addItem("RED", 2)
        self.five5.addItem("BROWN", 1)
        self.five5.addItem("GREEN", 0.5)
        self.five5.addItem("BLUE", 0.25)
        self.five5.addItem("VIOLET", 0.1)
        self.five5.addItem("GRAY", 0.05)
        self.five5.addItem("NONE", 20)
        self.five5.currentIndexChanged.connect(self.digit_tolerance)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_band_five1)
        vbox.addWidget(self.five1)
        vbox.addWidget(lbl_band_five2)
        vbox.addWidget(self.five2)
        vbox.addWidget(lbl_band_five3)
        vbox.addWidget(self.five3)
        vbox.addWidget(lbl_band_five4)
        vbox.addWidget(self.five4)
        vbox.addWidget(lbl_band_five5)
        vbox.addWidget(self.five5)
        vbox.addWidget(calculate)
        vbox.addWidget(r_label5)
        vbox.addWidget(self.display5)
        vbox.addWidget(t_label5)
        vbox.addWidget(self.tolerance5)

        vbox.addStretch(1)
        groupbox.setLayout(vbox)
        return groupbox

    # FUNCTIONS TO ADD COLORS
    def digit_five1(self, index):
        self.five1.setStyleSheet("background-color: %s" % self.five1.itemText(index))

    def digit_five2(self, index):
        self.five2.setStyleSheet("background-color: %s" % self.five2.itemText(index))

    def digit_five3(self, index):
        self.five3.setStyleSheet("background-color: %s" % self.five3.itemText(index))

    def digit_multiplier(self, index):
        self.five4.setStyleSheet("background-color: %s" % self.five4.itemText(index))

    def digit_tolerance(self, index):
        self.five5.setStyleSheet("background-color: %s" % self.five5.itemText(index))

    def calculate_resistance(self):
        """ Calculates the resistance of five-color band resistors """
        digit1 = self.five1.currentData()
        digit2 = self.five2.currentData()
        digit3 = self.five3.currentData()
        multiply = self.five4.currentData()
        toler = str(self.five5.currentData()) + "%"

        pre_resistance = str(digit1) + str(digit2) + str(digit3)
        total_value = int(pre_resistance) * (10 ** multiply)

        # conversions
        if 0 < total_value < 1000:
            total_value = str(total_value) + " Ohms"

        elif 0 < total_value < 1000000:
            total_value = total_value / 1000
            total_value = str(total_value) + " K"

        elif total_value >= 1000000:
            total_value = total_value / 1000000
            total_value = str(total_value) + " M"

        self.display5.setText(str(total_value))
        self.tolerance5.setText(str(toler))


def main():
    app = QApplication(sys.argv)
    screen = Window()
    screen.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
