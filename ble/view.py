from PyQt5 import QtCore, QtGui, QtWidgets
# from pyqtgraph import GraphicsLayoutWidget

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(779, 835)

        # Main Tab Widget
        self.mainTabWidget = QtWidgets.QTabWidget(Dialog)
        self.mainTabWidget.setGeometry(QtCore.QRect(10, 10, 761, 811))
        self.mainTabWidget.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.mainTabWidget.setObjectName("mainTabWidget")

        # Tab 1: Configuration Tab
        self.configTab = QtWidgets.QWidget()
        self.configTab.setObjectName("configTab")

        # Labels
        self.configButtonsLabel = self.create_label(self.configTab, "configButtonsLabel", 80, 70, 181, 31, "Botones de configuracion", "color: rgb(255, 255, 255);")
        self.availableEspLabel = self.create_label(self.configTab, "availableEspLabel", 140, 60, 141, 21, "Esp32 disponibles por bluetooth", "color: rgb(0, 0, 0);")
        self.accSamplingLabel = self.create_label(self.configTab, "accSamplingLabel", 150, 180, 81, 31, "Acc Sampling")
        self.accSensitivityLabel = self.create_label(self.configTab, "accSensitivityLabel", 150, 230, 81, 31, "Acc Sensibility")
        self.gyroSensitivityLabel = self.create_label(self.configTab, "gyroSensitivityLabel", 150, 280, 81, 31, "Gyro Sensibility")
        self.bme688SamplingLabel = self.create_label(self.configTab, "bme688SamplingLabel", 130, 320, 91, 31, "BME688 Sampling")
        self.discontinuousTimeLabel = self.create_label(self.configTab, "discontinuousTimeLabel", 130, 370, 91, 31, "Discontinuous time")
        self.tcpPortLabel = self.create_label(self.configTab, "tcpPortLabel", 430, 180, 51, 31, "TCP Port")
        self.udpPortLabel = self.create_label(self.configTab, "udpPortLabel", 430, 230, 61, 31, "UDP Port")
        self.hostIpLabel = self.create_label(self.configTab, "hostIpLabel", 430, 280, 61, 31, "Host IP Addr")
        self.ssidLabel = self.create_label(self.configTab, "ssidLabel", 430, 330, 61, 31, "Ssid")
        self.passwordLabel = self.create_label(self.configTab, "passwordLabel", 430, 380, 61, 31, "Pass")
        self.netConfigLabel = self.create_label(self.configTab, "netConfigLabel", 530, 120, 51, 31, "Net Config")
        self.sensorConfigLabel = self.create_label(self.configTab, "sensorConfigLabel", 260, 120, 71, 31, "Sensor config")
        self.consoleLabel1 = self.create_label(self.configTab, "consoleLabel1", 60, 660, 141, 21, "Consola", "color: rgb(0, 0, 0);")
        self.operationModeLabel = self.create_label(self.configTab, "operationModeLabel", 130, 500, 101, 21, "Modo de operacion", "color: rgb(0, 0, 0);")
        self.protocolIdLabel = self.create_label(self.configTab, "protocolIdLabel", 450, 490, 101, 21, "Id protocols", "color: rgb(0, 0, 0);")

        # Buttons
        self.startButton = self.create_button(self.configTab, "startButton", 350, -50, 93, 28, "Inicio")
        self.selectEspButton = self.create_button(self.configTab, "selectEspButton", 400, 50, 121, 31, "Seleccion ESP-32", "background-color: rgb(5, 5, 203);\ncolor: rgb(255, 255, 255);")
        self.configButton = self.create_button(self.configTab, "configButton", 350, 440, 93, 28, "Configurar", "background-color: rgb(5, 5, 203);\ncolor: rgb(255, 255, 255);")
        self.startMonitoringButton = self.create_button(self.configTab, "startMonitoringButton", 240, 610, 121, 31, "Iniciar Monitoreo", "background-color: rgb(34, 111, 22);\ncolor: rgb(255, 255, 255);")
        self.stopMonitoringButton = self.create_button(self.configTab, "stopMonitoringButton", 420, 610, 121, 31, "Detener monitoreo", "background-color: rgb(103, 8, 8);\ncolor: rgb(255, 255, 255);")

        # ComboBoxes
        self.selectEspComboBox = self.create_combobox(self.configTab, "selectEspComboBox", 300, 50, 81, 31, "background-color: rgb(255, 255, 255);")
        self.operationModeComboBox = self.create_combobox(self.configTab, "operationModeComboBox", 100, 530, 181, 31, "background-color: rgb(255, 255, 255);")
        self.operationModeComboBox.addItems(["Configuración por Bluetooth", "Configuración vía TCP en BD", "Conexión TCP continua", "Conexión TCP discontinua", "Conexión UDP", "BLE continua", "BLE discontinua"])
        self.protocolIdComboBox = self.create_combobox(self.configTab, "protocolIdComboBox", 420, 520, 181, 31, "background-color: rgb(255, 255, 255);")
        self.protocolIdComboBox.addItems(["1", "2", "3", "4", "5"])

        # TextEdits
        self.accSamplingTextEdit = self.create_textedit(self.configTab, "accSamplingTextEdit", 240, 180, 104, 31)
        self.accSensitivityTextEdit = self.create_textedit(self.configTab, "accSensitivityTextEdit", 240, 230, 104, 31)
        self.gyroSensitivityTextEdit = self.create_textedit(self.configTab, "gyroSensitivityTextEdit", 240, 280, 104, 31)
        self.bme688SamplingTextEdit = self.create_textedit(self.configTab, "bme688SamplingTextEdit", 240, 320, 104, 31)
        self.discontinuousTimeTextEdit = self.create_textedit(self.configTab, "discontinuousTimeTextEdit", 240, 370, 104, 31)
        self.tcpPortTextEdit = self.create_textedit(self.configTab, "tcpPortTextEdit", 500, 180, 104, 31)
        self.udpPortTextEdit = self.create_textedit(self.configTab, "udpPortTextEdit", 500, 230, 104, 31)
        self.hostIpTextEdit = self.create_textedit(self.configTab, "hostIpTextEdit", 500, 280, 104, 31)
        self.ssidTextEdit = self.create_textedit(self.configTab, "ssidTextEdit", 500, 330, 104, 31)
        self.passwordTextEdit = self.create_textedit(self.configTab, "passwordTextEdit", 500, 380, 104, 31)
        self.consoleTextEdit1 = self.create_textedit(self.configTab, "consoleTextEdit1", 60, 690, 681, 81, "background-color: rgb(255, 255, 255);")

        self.mainTabWidget.addTab(self.configTab, "Pestaña de configuración")

        # Tab 2: Plotting Tab
        self.plottingTab = QtWidgets.QWidget()
        self.plottingTab.setObjectName("plottingTab")

        # Plot Widgets
        # self.plot1 = self.create_plot(self.plottingTab, "plot1", 30, 60, 691, 141)
        # self.plot2 = self.create_plot(self.plottingTab, "plot2", 30, 230, 691, 141)
        # self.plot3 = self.create_plot(self.plottingTab, "plot3", 30, 400, 691, 141)

        # Labels for Plotting Tab
        self.consoleLabel2 = self.create_label(self.plottingTab, "consoleLabel2", 40, 610, 141, 21, "Consola", "color: rgb(0, 0, 0);")
        self.consoleTextEdit2 = self.create_textedit(self.plottingTab, "consoleTextEdit2", 40, 640, 681, 81, "background-color: rgb(255, 255, 255);")
        self.accelerometerXLabel = self.create_label(self.plottingTab, "accelerometerXLabel", 160, 10, 111, 21, "Accelerometer X", "color: rgb(0, 0, 0);")
        self.accelerometerYLabel = self.create_label(self.plottingTab, "accelerometerYLabel", 160, 180, 111, 21, "Accelerometer Y", "color: rgb(0, 0, 0);")
        self.accelerometerZLabel = self.create_label(self.plottingTab, "accelerometerZLabel", 160, 350, 111, 21, "Accelerometer Z", "color: rgb(0, 0, 0);")

        self.mainTabWidget.addTab(self.plottingTab, "Pestaña de graficación")

        self.retranslateUi(Dialog)
        self.mainTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def create_label(self, parent, name, x, y, w, h, text, stylesheet=""):
        label = QtWidgets.QLabel(parent)
        label.setObjectName(name)
        label.setGeometry(QtCore.QRect(x, y, w, h))
        label.setText(text)
        label.setStyleSheet(stylesheet)
        return label

    def create_button(self, parent, name, x, y, w, h, text, stylesheet=""):
        button = QtWidgets.QPushButton(parent)
        button.setObjectName(name)
        button.setGeometry(QtCore.QRect(x, y, w, h))
        button.setText(text)
        button.setStyleSheet(stylesheet)
        return button

    def create_combobox(self, parent, name, x, y, w, h, stylesheet=""):
        combobox = QtWidgets.QComboBox(parent)
        combobox.setObjectName(name)
        combobox.setGeometry(QtCore.QRect(x, y, w, h))
        combobox.setStyleSheet(stylesheet)
        return combobox

    def create_textedit(self, parent, name, x, y, w, h, stylesheet=""):
        textedit = QtWidgets.QTextEdit(parent)
        textedit.setObjectName(name)
        textedit.setGeometry(QtCore.QRect(x, y, w, h))
        textedit.setStyleSheet(stylesheet)
        return textedit

    def create_plot(self, parent, name, x, y, w, h):
        plot = GraphicsLayoutWidget(parent)
        plot.setObjectName(name)
        plot.setGeometry(QtCore.QRect(x, y, w, h))
        return plot

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.configTab), _translate("Dialog", "Pestaña de configuración"))
        self.mainTabWidget.setTabText(self.mainTabWidget.indexOf(self.plottingTab), _translate("Dialog", "Pestaña de graficación"))

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
