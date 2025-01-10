# -*- coding: utf-8 -*-
# @File    : omx_viewer_ui.py
# 功能：
# @Time    : 2025/1/8 上午11:26
# @Author  : lhy
# @Software: PyCharm

from PyQt5.QtWidgets import QFileDialog,QTextEdit,QApplication, QMainWindow,QDialog,QMenu,QAction
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import sys
import openmatrix as omx
from PyQt5.QtGui import QStandardItemModel,QStandardItem
import os

from omx_operate.pyqt_tabel_matrix import MatrixModel
from omx_operate.matrix_aggrate import Ui_Aggrate_Dialog
import pandas as pd

class Ui_OmxViewer(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setObjectName("OMX viewer V1.0")
        self.resize(1131, 662)

        self.omx_file = None
        self._keyname_list = None
        self.list_map = None
        self.current_index = "Orgin index"
        self.current_key = None
        self.matrix_data = None

        self.setupUi()
    def __del__(self):
        if self.omx_file:
            self.omx_file.close()
    def setupUi(self):

        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(2, 2, 1, 1)
        self.horizontalLayout.setObjectName("horizontalLayout")

        # 左侧，矩阵的名称排列
        self.treeView = QtWidgets.QTreeView(self.centralwidget)
        self.treeView.setObjectName("treeView")
        self.treeView.setMaximumWidth(300)
        self.horizontalLayout.addWidget(self.treeView)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Matrix Names'])
        self.treeView.setModel(self.model)

        # 右侧
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        # 矩阵标签显示
        self.label_name = QtWidgets.QLabel(self.centralwidget)
        self.label_name.setObjectName("label_name")
        self.horizontalLayout_2.addWidget(self.label_name)
        self.combo_box_index = QtWidgets.QComboBox(self.centralwidget)
        self.combo_box_index.setObjectName("combo_box_index")
        self.combo_box_index.addItem("Orgin index")
        # self.lineEdit_name = QtWidgets.QLineEdit(self.centralwidget)
        # self.lineEdit_name.setObjectName("lineEdit_name")
        self.horizontalLayout_2.addWidget(self.combo_box_index)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        # 显示起点标签
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_org = QtWidgets.QLabel(self.centralwidget)
        self.label_org.setObjectName("label_org")
        self.horizontalLayout_3.addWidget(self.label_org)
        self.lineEdit_org = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_org.setObjectName("lineEdit_org")
        self.horizontalLayout_3.addWidget(self.lineEdit_org)
        # 终点标签
        self.label_end = QtWidgets.QLabel(self.centralwidget)
        self.label_end.setObjectName("label_end")
        self.horizontalLayout_3.addWidget(self.label_end)
        self.lineEdit_end = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit_end.setObjectName("lineEdit_end")
        self.horizontalLayout_3.addWidget(self.lineEdit_end)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        # 计算
        self.radio_butron_min  = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_butron_min.setObjectName("radio_butron_min")
        self.horizontalLayout_4.addWidget(self.radio_butron_min)
        self.radio_butron_max = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_butron_max.setObjectName("radio_butron_max")
        self.horizontalLayout_4.addWidget(self.radio_butron_max)
        self.radio_butron_sum = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_butron_sum.setObjectName("radio_butron_sum")
        self.horizontalLayout_4.addWidget(self.radio_butron_sum)
        self.radio_butron_avg = QtWidgets.QRadioButton(self.centralwidget)
        self.radio_butron_avg.setObjectName("radio_butron_avg")
        self.horizontalLayout_4.addWidget(self.radio_butron_avg)
        self.verticalLayout.addLayout(self.horizontalLayout_4)

        self.tableView_matrix = QtWidgets.QTableView(self.centralwidget)
        self.tableView_matrix.setObjectName("tableView_matrix")
        self.tableView_matrix.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addWidget(self.tableView_matrix)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 4)


        # self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1131, 26))
        self.menubar.setObjectName("menubar")
        self.menufile = QtWidgets.QMenu(self.menubar)
        self.menufile.setObjectName("menufile")
        self.menutools = QtWidgets.QMenu(self.menubar)
        self.menutools.setObjectName("menutools")
        self.menufind = QtWidgets.QMenu(self.menubar)
        self.menufind.setObjectName("menufind")
        self.menuhelp = QtWidgets.QMenu(self.menubar)
        self.menuhelp.setObjectName("menuhelp")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.actionopen_file = QtWidgets.QAction(self)
        self.actionopen_file.setObjectName("actionopen_file")
        self.actionsave_as = QtWidgets.QAction(self)
        self.actionsave_as.setObjectName("actionsave_as")
        self.actionnew = QtWidgets.QAction(self)
        self.actionnew.setObjectName("actionnew")
        self.actionsum = QtWidgets.QAction(self)
        self.actionsum.setObjectName("actionsum")
        self.actionavg = QtWidgets.QAction(self)
        self.actionavg.setObjectName("actionavg")
        self.actionagg = QtWidgets.QAction(self)
        self.actionagg.setObjectName("actionagg")
        self.actionsingle_value = QtWidgets.QAction(self)
        self.actionsingle_value.setObjectName("actionsingle_value")
        self.actionsum_index = QtWidgets.QAction(self)
        self.actionsum_index.setObjectName("actionsum_index")
        self.actionhelp_files = QtWidgets.QAction(self)
        self.actionhelp_files.setObjectName("actionhelp_files")
        self.actionabout = QtWidgets.QAction(self)
        self.actionabout.setObjectName("actionabout")
        self.actionexports = QtWidgets.QAction(self)
        self.actionexports.setObjectName("actionexports")
        self.actionimport = QtWidgets.QAction(self)
        self.actionimport.setObjectName("actionimport")
        self.actionFormula = QtWidgets.QAction(self)
        self.actionFormula.setObjectName("actionFormula")
        self.actionAggrate = QtWidgets.QAction(self)
        self.actionAggrate.setObjectName("actionAggrate")
        self.menufile.addAction(self.actionopen_file)
        self.menufile.addAction(self.actionsave_as)
        self.menufile.addAction(self.actionnew)
        self.menutools.addAction(self.actionsum)
        self.menutools.addAction(self.actionavg)
        self.menutools.addAction(self.actionFormula)
        self.menutools.addAction(self.actionAggrate)
        self.menufind.addAction(self.actionsingle_value)
        self.menufind.addAction(self.actionsum_index)
        self.menuhelp.addAction(self.actionhelp_files)
        self.menuhelp.addAction(self.actionabout)
        self.menubar.addAction(self.menufile.menuAction())
        self.menubar.addAction(self.menutools.menuAction())
        self.menubar.addAction(self.menufind.menuAction())
        self.menubar.addAction(self.menuhelp.menuAction())

        self.status_bar = self.statusBar()
        self.status_bar.showMessage("welcome to use it by lhy!")

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        # 槽函数激活
        self.signal_slots_connection()
        self.treeView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.showContextMenu)
        self.actionsingle_value.triggered.connect(self.search_value_show)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "OMX Viewer V1.0"))
        self.label_org.setText(_translate("MainWindow", "Origions"))
        self.label_end.setText(_translate("MainWindow", "destinations"))
        self.label_name.setText(_translate("MainWindow", "Matrix index"))
        self.radio_butron_min.setText(_translate("MainWindow", "show min"))
        self.radio_butron_max.setText(_translate("MainWindow", "show max"))
        self.radio_butron_sum.setText(_translate("MainWindow", "show sum"))
        self.radio_butron_avg.setText(_translate("MainWindow", "show avarage"))
        self.menufile.setTitle(_translate("MainWindow", "File"))
        self.menutools.setTitle(_translate("MainWindow", "Edit"))
        self.menufind.setTitle(_translate("MainWindow", "Find"))
        self.menuhelp.setTitle(_translate("MainWindow", "Help"))
        self.actionopen_file.setText(_translate("MainWindow", "Open"))
        self.actionsave_as.setText(_translate("MainWindow", "Save"))
        self.actionnew.setText(_translate("MainWindow", "New"))
        self.actionsum.setText(_translate("MainWindow", "Import"))
        self.actionavg.setText(_translate("MainWindow", "Export"))
        self.actionagg.setText(_translate("MainWindow", "agg"))
        self.actionsingle_value.setText(_translate("MainWindow", "Single Value Search"))
        self.actionsum_index.setText(_translate("MainWindow", "Sum Value Search"))
        self.actionhelp_files.setText(_translate("MainWindow", "User Helps"))
        self.actionabout.setText(_translate("MainWindow", "Abouts"))
        self.actionexports.setText(_translate("MainWindow", "exports"))
        self.actionimport.setText(_translate("MainWindow", "import"))
        self.actionFormula.setText(_translate("MainWindow", "Formula"))
        self.actionAggrate.setText(_translate("MainWindow", "Aggrate"))

    def signal_slots_connection(self):
        def get_OMX_file():
            fileName, _ = QFileDialog.getOpenFileName(None, "Open OMX", "",  "OMX Files (*.omx)")
            if fileName:
                file_name_with_extension = os.path.basename(fileName)

                # 使用os.path.splitext()移除后缀，返回一个元组，其中第一个元素是文件名
                file_name_without_extension = os.path.splitext(file_name_with_extension)[0]
                self.omx_file = omx.open_file(fileName, mode='r')
                self._keyname_list = self.omx_file.list_matrices()
                self.list_map = self.omx_file.list_mappings()
                if self.list_map:
                    for map_index in self.list_map:
                        self.combo_box_index.addItem(map_index)

                if self._keyname_list:
                    self.updata_tree_view(file_name_without_extension)
        self.actionopen_file.triggered.connect(lambda: get_OMX_file())

        self.treeView.doubleClicked.connect(self.on_treeView_doubleClicked)

        # 修改索引值
        self.combo_box_index.currentIndexChanged.connect(self.onComboBoxChanged)
        # 矩阵数据统计
        self.radio_butron_min.toggled.connect(lambda: self.onRadioToggled(self.radio_butron_min))
        self.radio_butron_max.toggled.connect(lambda: self.onRadioToggled(self.radio_butron_max))
        self.radio_butron_sum.toggled.connect(lambda: self.onRadioToggled(self.radio_butron_sum))
        self.radio_butron_avg.toggled.connect(lambda: self.onRadioToggled(self.radio_butron_avg))

        # 矩阵聚合
        self.actionAggrate.triggered.connect(self.matrix_aggrate)

    def showContextMenu(self,pos):
        menu = QMenu(self)
        action1_export = QAction("export csv", self)
        action2_addmap = QAction("add map", self)
        menu.addAction(action1_export)
        menu.addAction(action2_addmap)

        # 连接菜单项的触发信号到处理函数
        action1_export.triggered.connect(lambda:self.onAction1Clicked_export(pos))
        action2_addmap.triggered.connect(lambda:self.onAction1Clicked_addmap(pos))

        # 获取当前点击的索引
        # pos = event  # 获取鼠标位置
        # index = self.treeView.indexAt(pos)
        # if index.isValid():
        #     # 可以在这里根据索引进行一些操作
        #     print(f"右键点击了: {index.data()}")

        # 显示菜单
        menu.exec(self.treeView.mapToGlobal(pos))

    def onAction1Clicked_export(self, pos):
        # print("菜单项1被点击")
        index = self.treeView.indexAt(pos)
        if index.isValid():
            # 可以在这里根据索引进行一些操作
            kay_name = index.data()
            print(kay_name)
            matrix_data = self.omx_file[kay_name][:,:]
            index = [x for x in range(len(matrix_data[0]))]
            df_matrix = pd.DataFrame(matrix_data,columns=index,index=index)
            destpath,filetype = QFileDialog.getSaveFileName(self,"文件保存",kay_name+".csv","CSV Files (*.csv)")
            # print(destpath)
            df_matrix.to_csv(destpath, index=True)

    def onAction2Clicked(self):
        print("菜单项2被点击")

    def updata_tree_view(self,file_name_without_extension):
        self.model.clear()
        self.model.setHorizontalHeaderLabels([file_name_without_extension])
        if self._keyname_list:
            for name in self._keyname_list:
                item = QStandardItem(name)
                self.model.appendRow(item)

    def display_matrix(self, matrix,column,show_type):
        if matrix is not None:
            self.tableView_matrix.setModel(None)
            model_matrix = MatrixModel(matrix,column,column,show_type)
            self.tableView_matrix.setModel(model_matrix)
            self.tableView_matrix.setStyleSheet("""
                        QHeaderView::section {
                            background-color: lightgray;
                            font-weight: bold;
                        }
                    """)
    def on_treeView_doubleClicked(self, index):
        if index.isValid():
            matrix_name = self.model.data(index, QtCore.Qt.DisplayRole)
            if matrix_name in self._keyname_list:
                self.current_key = matrix_name
                self.matrix_data = self.omx_file[matrix_name][:,:]

                if self.current_index == "Orgin index":
                    columns = range(0,self.matrix_data.shape[1])
                else:
                    columns = self.omx_file.mapping(self.current_index) .keys()

                self.display_matrix(self.matrix_data,columns,None)

    def onRadioToggled(self,raddio_button):
        if raddio_button.isChecked():
            if raddio_button.text() == "show min":
                show_type = "show min"
            elif raddio_button.text() == "show max":
                show_type = "show max"
            elif raddio_button.text() == "show sum":
                show_type = "show sum"
            elif raddio_button.text() == "show avarage":
                show_type = "show avg"
        else:
            show_type = None

        if self.current_index == "Orgin index":
            columns = range(0, self.matrix_data.shape[1])
        else:
            columns = self.omx_file.mapping(self.current_index).keys()
        self.display_matrix(self.matrix_data,columns,show_type)

    def onComboBoxChanged(self, index):
        self.current_index = self.combo_box_index.currentText()


    def matrix_aggrate(self, index):
        """

        :param index:
        :return:
        """
        self._dialog = Ui_Aggrate_Dialog(self.matrix_data)
        self._dialog.show()

    def search_value_show(self):
        """值的搜索"""
        pass






if __name__ == '__main__':
    app = QApplication(sys.argv)
    editor = Ui_OmxViewer()
    editor.show()
    sys.exit(app.exec_())
