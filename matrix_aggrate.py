# -*- coding: utf-8 -*-
# @File    : matrix_aggrate.py
# 功能：
# @Time    : 2025/1/8 下午9:01
# @Author  : lhy
# @Software: PyCharm
from PyQt5.QtWidgets import QFileDialog,QTextEdit,QApplication, QMainWindow,QDialog
from PyQt5 import QtCore, QtGui, QtWidgets
import os
import pandas as pd
from table_view import TableShow
import numpy as np

class Ui_Aggrate_Dialog(QDialog):

    def __init__(self,matrix_data):
        super().__init__()
        self.setObjectName("Dialog")
        self.resize(437, 209)
        self.matrix_data = matrix_data

        self.setupUi()

    def setupUi(self):
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setGeometry(QtCore.QRect(60, 140, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.verticalLayoutWidget = QtWidgets.QWidget(self)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 331, 92))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)

        self.lineEdit = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.comboBox = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.horizontalLayout_2.addWidget(self.comboBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_2 = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_3.addWidget(self.label_2)
        self.comboBox_2 = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.horizontalLayout_3.addWidget(self.comboBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi()
        self.buttonBox.accepted.connect(self.accept) # type: ignore
        self.buttonBox.rejected.connect(self.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(self)
        self.buttonBox.clicked.connect(self.aggrate_matrix_do)

        self.pushButton.clicked.connect(self.open_index_file)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "open file"))
        self.label.setText(_translate("Dialog", "org index"))
        self.label_2.setText(_translate("Dialog", "aggrate index"))

    def open_index_file(self):
        fileName, _ = QFileDialog.getOpenFileName(None, "Open index", "", " index Files (*.csv)")
        if fileName:

            self.index_df = pd.read_csv(fileName)
            self.lineEdit.setText(fileName)
            for com_index in self.index_df.columns:
                self.comboBox.addItem(com_index)
                self.comboBox_2.addItem(com_index)

    def aggrate_matrix_do(self):
        orig_index = self.comboBox.currentText()
        aggra_index = self.comboBox_2.currentText()
        assert len(self.index_df[orig_index]) == len(self.matrix_data)
        aggrate_matrix_df = self.matrix_aggregate_by_index2(self.matrix_data, self.index_df,aggra_index)

        self.table_dig = QDialog()
        table_show = TableShow(aggrate_matrix_df,self.table_dig)
        self.table_dig.show()


    @staticmethod
    def matrix_aggregate_by_index(matrix_p, zone_table_index):
        """将矩阵根据索引集计"""

        big_taz = sorted(set(zone_table_index))
        len_matrix = len(matrix_p[0])
        data_list = []
        for i in range(len_matrix):
            for j in range(len_matrix):
                data_list.append([zone_table_index[i], zone_table_index[j], i, j, matrix_p[i][j]])
        df_taz = pd.DataFrame(data_list, columns=['big_taz_i', 'big_taz_j', 'taz_i', 'taz_j', "values"])
        df_big = df_taz.groupby(['big_taz_i', 'big_taz_j'])["values"].sum()
        data_big = []
        for big_id_i in big_taz:
            data_list_i = []
            for big_id_j in big_taz:
                data_list_i.append(df_big[(big_id_i, big_id_j)])
            data_big.append(data_list_i)
        data_big_df = pd.DataFrame(data_big, columns=big_taz)
        data_big_df.index = big_taz
        return data_big_df

    @staticmethod
    def matrix_aggregate_by_index2(matrix_p, zone_table_df,big_column):
        """将矩阵根据索引集计"""
        assert len(zone_table_df) == len(matrix_p[0])
        index = [x for x in range(len(matrix_p[0]))]
        matrix_df = pd.DataFrame(matrix_p,columns= index,index=index)

        matrix_df_reset = matrix_df.stack().reset_index().rename(columns={"level_0": "FROM", "level_1": "TO", "level_2": "Values"})
        matrix_df_reset.columns = ["FROM", "TO", "Values"]

        zone_table_df.index = index
        matrix_df1 = pd.merge(matrix_df_reset, zone_table_df.rename(columns={big_column: "from_big"}), left_on='FROM', right_on='index')
        matrix_df2 = pd.merge(matrix_df1, zone_table_df.rename(columns={big_column: "to_big"}), left_on='TO', right_on='index')

        big_taz = sorted(set(zone_table_df[big_column]))
        data_big = matrix_df2.pivot_table(index='from_big', columns='to_big', values='Values',aggfunc='sum')
        data_big = np.nan_to_num(data_big)
        data_big_df = pd.DataFrame(data_big, columns=big_taz)
        data_big_df.index = big_taz
        return data_big_df



