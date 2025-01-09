# -*- coding: utf-8 -*-
# @File    : table_view.py
# 功能：
# @Time    : 2025/1/9 上午9:38
# @Author  : lhy
# @Software: PyCharm
from PyQt5.QtWidgets import QTableView,QTreeWidgetItem,QPushButton,QGridLayout,QFrame,QSpacerItem,QVBoxLayout,QAbstractItemView
from  PyQt5.QtWidgets import  QWidget,QLabel,QDialog,QFileDialog,QLineEdit,QAbstractScrollArea,QSizePolicy,QHeaderView,QMessageBox
from PyQt5.QtCore import Qt, QPointF,QRect,QMetaObject,QCoreApplication,QEvent
from PyQt5.QtGui import QStandardItemModel,QStandardItem
import pandas as pd

class TableShow(object):

    def __init__(self,data_df,Dialog):

        self.data_df = data_df
        self.columns = self.data_df.columns
        self.vol_num = len(self.data_df)
        self.dialog = Dialog
        self.table_view = QTableView()


        self.setupUi()

    def setupUi(self):

        _translate = QCoreApplication.translate
        self.dialog.setWindowTitle(_translate("Dialog", "table"))

        self.dialog.setObjectName("file_name")

        self.dialog.resize(1000, 400)
        self.centerWidget = QWidget(self.dialog)

        self.gridLayout = QVBoxLayout()
        self.dialog.setLayout( self.gridLayout)
        self.table_model = QStandardItemModel(0,len(self.columns))
        self.table_model.setHorizontalHeaderLabels([str(x) for x in self.columns])

        self.gridLayout.addWidget(self.table_view,stretch=1)
        self.table_view.setModel(self.table_model)

        self.table_view.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table_view.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setStyleSheet("""
                        QHeaderView::section {
                            background-color: lightgray;
                            font-weight: bold;
                        }
                    """)


        self.save_button = QPushButton(self.dialog)
        self.gridLayout.addWidget(self.save_button)
        self.save_button.setText("文件保存")

        self.tableview_add()
        self.save_button.clicked.connect(lambda:self.save_data())

    def tableview_add(self):
        for num,data in self.data_df.iterrows():
            data_row = [QStandardItem(str(x)) for x in data ]
            self.table_model.appendRow(data_row)

    def table_view_del_now(self):
        index = self.table_view.currentIndex()
        self.table_model.removeRow(index.row())

    def table_view_clear(self):
        self.table_model.clear()


    def save_data(self):
        model = self.table_view.model()
        destpath,filetype = QFileDialog.getSaveFileName(self.dialog,"文件保存","my_data.csv","CSV Files (*.csv)")
        if destpath:
            rows = model.rowCount()
            columns = model.columnCount()
            data_c_r = []
            for rol in range(rows):
                data = []
                for col in range(columns):
                    data.append(model.data(model.index(rol,col)))
                data_c_r.append(data)
            df = pd.DataFrame(data_c_r,columns=self.columns)
            df.to_csv(destpath, index=True)
        else:
            QMessageBox.information(self.dialog,"提示","未选择保存位置，文件保存操作取消")

    # def get_select_df(self):
    #     if self.table_link
