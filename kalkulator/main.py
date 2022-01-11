from PyQt5.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QMessageBox
import sys

calc = 0
pd = 0
numb = ''


class Window(QWidget):
    def prov(self):
        global calc, pd, numb
        if pd == 0:
            calc += float(numb)
        elif pd == 1:
            calc += float(numb)
        elif pd == 2:
            calc -= float(numb)
        elif pd == 3:
            calc *= float(numb)
        elif pd == 4:
            try:
                calc /= float(numb)
            except:
                QMessageBox.about(self, "Error", "На ноль делить нельзя")
        numb = ''

    def __init__(self):
        super(Window, self).__init__()
        self.le = QLineEdit(self)
        self.set_ui()

    def set_ui(self):
        self.setGeometry(200, 200, 160, 200)
        self.setWindowTitle('Калькулятор')
        self.le.setGeometry(0, 0, 120, 40)

        for i in range(10):
            self.btn = QPushButton(str(i), self)
            if i == 0:
                self.btn.setGeometry(40, 160, 40, 40)
            elif i <= 3:
                self.btn.setGeometry(40 * (i - 1), 120, 40, 40)
            elif i <= 6:
                self.btn.setGeometry(40 * (i - 4), 80, 40, 40)
            elif i <= 9:
                self.btn.setGeometry(40 * (i - 7), 40, 40, 40)
            self.btn.clicked.connect(lambda checked=None, j=i: self.click_event(j))

        self.btne = QPushButton('=', self)
        self.btne.setGeometry(120, 160, 40, 40)
        self.btne.clicked.connect(self.click_event_e)

        self.btnp = QPushButton('+', self)
        self.btnp.setGeometry(120, 40, 40, 40)
        self.btnp.clicked.connect(self.click_event_p)

        self.btnm = QPushButton('-', self)
        self.btnm.setGeometry(120, 80, 40, 40)
        self.btnm.clicked.connect(self.click_event_m)

        self.btny = QPushButton('*', self)
        self.btny.setGeometry(0, 160, 40, 40)
        self.btny.clicked.connect(self.click_event_y)

        self.btnd = QPushButton('/', self)
        self.btnd.setGeometry(80, 160, 40, 40)
        self.btnd.clicked.connect(self.click_event_d)

        self.btnc = QPushButton('C', self)
        self.btnc.setGeometry(120, 0, 40, 40)
        self.btnc.clicked.connect(self.click_event_c)

        self.btnt = QPushButton('.', self)
        self.btnt.setGeometry(120, 120, 40, 40)
        self.btnt.clicked.connect(self.click_event_t)

        self.show()

    def click_event(self, j):
        global numb
        self.le.setText(self.le.text() + str(j))
        numb += str(j)

    def click_event_t(self):
        global numb
        self.le.setText(self.le.text() + '.')
        numb += '.'

    def click_event_e(self):
        global pd, numb, calc
        self.prov()
        self.le.setText(str(calc))
        pd = 0
        numb = str(calc)
        calc = 0

    def click_event_p(self):
        global pd
        self.prov()
        self.le.setText(self.le.text() + '+')
        pd = 1

    def click_event_m(self):
        global pd
        self.prov()
        self.le.setText(self.le.text() + '-')
        pd = 2

    def click_event_y(self):
        global pd
        self.prov()
        self.le.setText(self.le.text() + '*')
        pd = 3

    def click_event_d(self):
        global pd
        self.prov()
        self.le.setText(self.le.text() + '/')
        pd = 4

    def click_event_c(self):
        global pd, numb, calc
        self.le.setText('')
        calc = 0
        pd = 0
        numb = ''


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = Window()
    sys.exit(app.exec_())