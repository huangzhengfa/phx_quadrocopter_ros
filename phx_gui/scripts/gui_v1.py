# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_v1.ui'
#
# Created: Fri Sep 18 23:04:39 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1302, 730)
        MainWindow.setTabShape(QtGui.QTabWidget.Rounded)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayoutWidget = QtGui.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 1276, 666))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gui_output = QtGui.QVBoxLayout()
        self.gui_output.setObjectName(_fromUtf8("gui_output"))
        self.plot_tabs = QtGui.QTabWidget(self.horizontalLayoutWidget)
        self.plot_tabs.setObjectName(_fromUtf8("plot_tabs"))
        self.InfoPage = QtGui.QWidget()
        self.InfoPage.setObjectName(_fromUtf8("InfoPage"))
        self.verticalLayout_plots = QtGui.QVBoxLayout(self.InfoPage)
        self.verticalLayout_plots.setObjectName(_fromUtf8("verticalLayout_plots"))
        self.textBrowser = QtGui.QTextBrowser(self.InfoPage)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.verticalLayout_plots.addWidget(self.textBrowser)
        self.plot_tabs.addTab(self.InfoPage, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gps_graphicsView = PlotWidget(self.tab)
        self.gps_graphicsView.setGeometry(QtCore.QRect(20, 20, 591, 491))
        self.gps_graphicsView.setObjectName(_fromUtf8("gps_graphicsView"))
        self.plot_tabs.addTab(self.tab, _fromUtf8(""))
        self.gui_output.addWidget(self.plot_tabs)
        self.gridLayout_sliders = QtGui.QGridLayout()
        self.gridLayout_sliders.setObjectName(_fromUtf8("gridLayout_sliders"))
        self.label_17 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_sliders.addWidget(self.label_17, 2, 1, 1, 1)
        self.horizontalSlider_time_point = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_time_point.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_time_point.setObjectName(_fromUtf8("horizontalSlider_time_point"))
        self.gridLayout_sliders.addWidget(self.horizontalSlider_time_point, 3, 0, 1, 1)
        self.horizontalSlider_delta_time = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_delta_time.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_delta_time.setObjectName(_fromUtf8("horizontalSlider_delta_time"))
        self.gridLayout_sliders.addWidget(self.horizontalSlider_delta_time, 2, 0, 1, 1)
        self.label_18 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_sliders.addWidget(self.label_18, 3, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.comboBox_topic_selection = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.comboBox_topic_selection.setObjectName(_fromUtf8("comboBox_topic_selection"))
        self.horizontalLayout_2.addWidget(self.comboBox_topic_selection)
        self.comboBox_sub_topic_selection = QtGui.QComboBox(self.horizontalLayoutWidget)
        self.comboBox_sub_topic_selection.setObjectName(_fromUtf8("comboBox_sub_topic_selection"))
        self.horizontalLayout_2.addWidget(self.comboBox_sub_topic_selection)
        self.button_add_remove_plot = QtGui.QPushButton(self.horizontalLayoutWidget)
        self.button_add_remove_plot.setObjectName(_fromUtf8("button_add_remove_plot"))
        self.horizontalLayout_2.addWidget(self.button_add_remove_plot)
        self.gridLayout_sliders.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.gui_output.addLayout(self.gridLayout_sliders)
        self.horizontalLayout.addLayout(self.gui_output)
        self.gridLayout_parameters = QtGui.QGridLayout()
        self.gridLayout_parameters.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.gridLayout_parameters.setObjectName(_fromUtf8("gridLayout_parameters"))
        self.lcdNumber_parameter_00 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_00.setObjectName(_fromUtf8("lcdNumber_parameter_00"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_00, 0, 1, 1, 1)
        self.label_parameter_10 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_10.setObjectName(_fromUtf8("label_parameter_10"))
        self.gridLayout_parameters.addWidget(self.label_parameter_10, 10, 2, 1, 1)
        self.horizontalSlider_parameter_10 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_10.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_10.setObjectName(_fromUtf8("horizontalSlider_parameter_10"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_10, 10, 0, 1, 1)
        self.horizontalSlider_parameter_15 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_15.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_15.setObjectName(_fromUtf8("horizontalSlider_parameter_15"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_15, 15, 0, 1, 1)
        self.horizontalSlider_parameter_03 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_03.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_03.setObjectName(_fromUtf8("horizontalSlider_parameter_03"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_03, 3, 0, 1, 1)
        self.lcdNumber_parameter_01 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_01.setObjectName(_fromUtf8("lcdNumber_parameter_01"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_01, 1, 1, 1, 1)
        self.lcdNumber_parameter_03 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_03.setObjectName(_fromUtf8("lcdNumber_parameter_03"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_03, 3, 1, 1, 1)
        self.horizontalSlider_parameter_05 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_05.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_05.setObjectName(_fromUtf8("horizontalSlider_parameter_05"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_05, 5, 0, 1, 1)
        self.label_parameter_00 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_00.setObjectName(_fromUtf8("label_parameter_00"))
        self.gridLayout_parameters.addWidget(self.label_parameter_00, 0, 2, 1, 1)
        self.label_parameter_15 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_15.setObjectName(_fromUtf8("label_parameter_15"))
        self.gridLayout_parameters.addWidget(self.label_parameter_15, 15, 2, 1, 1)
        self.horizontalSlider_parameter_01 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_01.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_01.setObjectName(_fromUtf8("horizontalSlider_parameter_01"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_01, 1, 0, 1, 1)
        self.label_parameter_03 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_03.setObjectName(_fromUtf8("label_parameter_03"))
        self.gridLayout_parameters.addWidget(self.label_parameter_03, 3, 2, 1, 1)
        self.label_parameter_01 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_01.setObjectName(_fromUtf8("label_parameter_01"))
        self.gridLayout_parameters.addWidget(self.label_parameter_01, 1, 2, 1, 1)
        self.horizontalSlider_parameter_00 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_00.setMaximumSize(QtCore.QSize(1000, 16777215))
        self.horizontalSlider_parameter_00.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_00.setObjectName(_fromUtf8("horizontalSlider_parameter_00"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_00, 0, 0, 1, 1)
        self.horizontalSlider_parameter_07 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_07.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_07.setObjectName(_fromUtf8("horizontalSlider_parameter_07"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_07, 7, 0, 1, 1)
        self.horizontalSlider_parameter_02 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_02.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_02.setObjectName(_fromUtf8("horizontalSlider_parameter_02"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_02, 2, 0, 1, 1)
        self.label_parameter_04 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_04.setObjectName(_fromUtf8("label_parameter_04"))
        self.gridLayout_parameters.addWidget(self.label_parameter_04, 4, 2, 1, 1)
        self.horizontalSlider_parameter_04 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_04.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_04.setObjectName(_fromUtf8("horizontalSlider_parameter_04"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_04, 4, 0, 1, 1)
        self.label_parameter_11 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_11.setObjectName(_fromUtf8("label_parameter_11"))
        self.gridLayout_parameters.addWidget(self.label_parameter_11, 11, 2, 1, 1)
        self.horizontalSlider_parameter_12 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_12.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_12.setObjectName(_fromUtf8("horizontalSlider_parameter_12"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_12, 12, 0, 1, 1)
        self.horizontalSlider_parameter_16 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_16.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_16.setObjectName(_fromUtf8("horizontalSlider_parameter_16"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_16, 16, 0, 1, 1)
        self.label_parameter_06 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_06.setObjectName(_fromUtf8("label_parameter_06"))
        self.gridLayout_parameters.addWidget(self.label_parameter_06, 6, 2, 1, 1)
        self.lcdNumber_parameter_06 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_06.setObjectName(_fromUtf8("lcdNumber_parameter_06"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_06, 6, 1, 1, 1)
        self.horizontalSlider_parameter_06 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_06.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_06.setObjectName(_fromUtf8("horizontalSlider_parameter_06"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_06, 6, 0, 1, 1)
        self.label_parameter_07 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_07.setObjectName(_fromUtf8("label_parameter_07"))
        self.gridLayout_parameters.addWidget(self.label_parameter_07, 7, 2, 1, 1)
        self.lcdNumber_parameter_02 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_02.setObjectName(_fromUtf8("lcdNumber_parameter_02"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_02, 2, 1, 1, 1)
        self.label_parameter_02 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_02.setObjectName(_fromUtf8("label_parameter_02"))
        self.gridLayout_parameters.addWidget(self.label_parameter_02, 2, 2, 1, 1)
        self.lcdNumber_parameter_04 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_04.setObjectName(_fromUtf8("lcdNumber_parameter_04"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_04, 4, 1, 1, 1)
        self.lcdNumber_parameter_07 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_07.setObjectName(_fromUtf8("lcdNumber_parameter_07"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_07, 7, 1, 1, 1)
        self.lcdNumber_parameter_05 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_05.setObjectName(_fromUtf8("lcdNumber_parameter_05"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_05, 5, 1, 1, 1)
        self.label_parameter_05 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_05.setObjectName(_fromUtf8("label_parameter_05"))
        self.gridLayout_parameters.addWidget(self.label_parameter_05, 5, 2, 1, 1)
        self.horizontalSlider_parameter_08 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_08.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_08.setObjectName(_fromUtf8("horizontalSlider_parameter_08"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_08, 8, 0, 1, 1)
        self.label_parameter_09 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_09.setObjectName(_fromUtf8("label_parameter_09"))
        self.gridLayout_parameters.addWidget(self.label_parameter_09, 9, 2, 1, 1)
        self.label_parameter_08 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_08.setObjectName(_fromUtf8("label_parameter_08"))
        self.gridLayout_parameters.addWidget(self.label_parameter_08, 8, 2, 1, 1)
        self.horizontalSlider_parameter_13 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_13.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_13.setObjectName(_fromUtf8("horizontalSlider_parameter_13"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_13, 13, 0, 1, 1)
        self.label_parameter_13 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_13.setObjectName(_fromUtf8("label_parameter_13"))
        self.gridLayout_parameters.addWidget(self.label_parameter_13, 13, 2, 1, 1)
        self.horizontalSlider_parameter_11 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_11.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_11.setObjectName(_fromUtf8("horizontalSlider_parameter_11"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_11, 11, 0, 1, 1)
        self.label_parameter_14 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_14.setObjectName(_fromUtf8("label_parameter_14"))
        self.gridLayout_parameters.addWidget(self.label_parameter_14, 14, 2, 1, 1)
        self.label_parameter_12 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_12.setObjectName(_fromUtf8("label_parameter_12"))
        self.gridLayout_parameters.addWidget(self.label_parameter_12, 12, 2, 1, 1)
        self.horizontalSlider_parameter_14 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_14.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_14.setObjectName(_fromUtf8("horizontalSlider_parameter_14"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_14, 14, 0, 1, 1)
        self.horizontalSlider_parameter_09 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_09.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_09.setObjectName(_fromUtf8("horizontalSlider_parameter_09"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_09, 9, 0, 1, 1)
        self.horizontalSlider_parameter_17 = QtGui.QSlider(self.horizontalLayoutWidget)
        self.horizontalSlider_parameter_17.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_parameter_17.setObjectName(_fromUtf8("horizontalSlider_parameter_17"))
        self.gridLayout_parameters.addWidget(self.horizontalSlider_parameter_17, 17, 0, 1, 1)
        self.label_parameter_16 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_16.setObjectName(_fromUtf8("label_parameter_16"))
        self.gridLayout_parameters.addWidget(self.label_parameter_16, 16, 2, 1, 1)
        self.label_parameter_17 = QtGui.QLabel(self.horizontalLayoutWidget)
        self.label_parameter_17.setObjectName(_fromUtf8("label_parameter_17"))
        self.gridLayout_parameters.addWidget(self.label_parameter_17, 17, 2, 1, 1)
        self.lcdNumber_parameter_08 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_08.setObjectName(_fromUtf8("lcdNumber_parameter_08"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_08, 8, 1, 1, 1)
        self.lcdNumber_parameter_09 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_09.setObjectName(_fromUtf8("lcdNumber_parameter_09"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_09, 9, 1, 1, 1)
        self.lcdNumber_parameter_10 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_10.setObjectName(_fromUtf8("lcdNumber_parameter_10"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_10, 10, 1, 1, 1)
        self.lcdNumber_parameter_11 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_11.setObjectName(_fromUtf8("lcdNumber_parameter_11"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_11, 11, 1, 1, 1)
        self.lcdNumber_parameter_12 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_12.setObjectName(_fromUtf8("lcdNumber_parameter_12"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_12, 12, 1, 1, 1)
        self.lcdNumber_parameter_13 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_13.setObjectName(_fromUtf8("lcdNumber_parameter_13"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_13, 13, 1, 1, 1)
        self.lcdNumber_parameter_14 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_14.setObjectName(_fromUtf8("lcdNumber_parameter_14"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_14, 14, 1, 1, 1)
        self.lcdNumber_parameter_15 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_15.setObjectName(_fromUtf8("lcdNumber_parameter_15"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_15, 15, 1, 1, 1)
        self.lcdNumber_parameter_16 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_16.setObjectName(_fromUtf8("lcdNumber_parameter_16"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_16, 16, 1, 1, 1)
        self.lcdNumber_parameter_17 = QtGui.QLCDNumber(self.horizontalLayoutWidget)
        self.lcdNumber_parameter_17.setObjectName(_fromUtf8("lcdNumber_parameter_17"))
        self.gridLayout_parameters.addWidget(self.lcdNumber_parameter_17, 17, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_parameters)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1302, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "phoenixGUI", None))
        self.plot_tabs.setTabText(self.plot_tabs.indexOf(self.tab), _translate("MainWindow", "gps", None))
        self.label_17.setText(_translate("MainWindow", "dt", None))
        self.label_18.setText(_translate("MainWindow", "time", None))
        self.button_add_remove_plot.setText(_translate("MainWindow", "add/remove", None))
        self.label_parameter_10.setText(_translate("MainWindow", "parameter10", None))
        self.label_parameter_00.setText(_translate("MainWindow", "parameter0", None))
        self.label_parameter_15.setText(_translate("MainWindow", "parameter15", None))
        self.label_parameter_03.setText(_translate("MainWindow", "parameter3", None))
        self.label_parameter_01.setText(_translate("MainWindow", "parameter1", None))
        self.label_parameter_04.setText(_translate("MainWindow", "parameter4", None))
        self.label_parameter_11.setText(_translate("MainWindow", "parameter11", None))
        self.label_parameter_06.setText(_translate("MainWindow", "parameter6", None))
        self.label_parameter_07.setText(_translate("MainWindow", "parameter7", None))
        self.label_parameter_02.setText(_translate("MainWindow", "parameter2", None))
        self.label_parameter_05.setText(_translate("MainWindow", "parameter5", None))
        self.label_parameter_09.setText(_translate("MainWindow", "parameter9", None))
        self.label_parameter_08.setText(_translate("MainWindow", "parameter8", None))
        self.label_parameter_13.setText(_translate("MainWindow", "parameter13", None))
        self.label_parameter_14.setText(_translate("MainWindow", "parameter14", None))
        self.label_parameter_12.setText(_translate("MainWindow", "parameter12", None))
        self.label_parameter_16.setText(_translate("MainWindow", "parameter16", None))
        self.label_parameter_17.setText(_translate("MainWindow", "parameter17", None))

from pyqtgraph import PlotWidget
