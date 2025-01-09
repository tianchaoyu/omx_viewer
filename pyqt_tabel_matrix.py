# -*- coding: utf-8 -*-
# @File    : pyqt_tabel_matrix.py
# 功能：
# @Time    : 2025/1/8 下午7:14
# @Author  : lhy
# @Software: PyCharm
from PyQt5.QtWidgets import QFileDialog,QTextEdit,QApplication, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets



class MatrixModel(QtCore.QAbstractTableModel):
    def __init__(self, data,row_labels=None, column_labels=None,show_type=None):
        super(MatrixModel, self).__init__()
        self._data = data
        self._row_labels = row_labels if row_labels is not None else [str(i) for i in range(data.shape[0])]
        self._column_labels = column_labels if column_labels is not None else [str(i) for i in range(data.shape[1])]
        self.show_type = show_type
        self.add_column = 0

        self.up_data_type()

    def up_data_type(self):
        if self.show_type:
            self.add_column = 1
            # self.row_sums = [sum(row) for row in self._data]
            # self.column_sums = [sum(column) for column in zip(*self._data)]
            # self.max_values = [max(row) for row in self._data]
            # self.min_values = [min(row) for row in self._data]
            # self.avg_values = [sum(row) / len(row) for row in self._data]
            self.row_sum_max_min_avg = [[sum(row), max(row), min(row), sum(row) / len(row)] for row in
                                        self._data]  # 安行计算
            self.col_sum_max_min_avg = [[sum(column), max(column), min(column), sum(column) / len(column)] for column in
                                        zip(*self._data)]  # 安列计算

        else:
            self.add_column = 0
            pass

    def data(self, index, role):
        row = index.row()
        column = index.column()

        if role == QtCore.Qt.DisplayRole:
            if row < len(self._data) and column < len(self._data[0]): # 矩阵数据
                return str(self._data[row][column])
            elif row == len(self._data) and column < len(self._data[0]): # 最后一行
                if self.show_type == "show sum":
                    return str(self.col_sum_max_min_avg[column][0])
                elif self.show_type == "show max":
                    return str(self.col_sum_max_min_avg[column][1])
                elif self.show_type == "show min":
                    return str(self.col_sum_max_min_avg[column][2])
                elif self.show_type  == "show avg":
                    return str(self.col_sum_max_min_avg[column][3])
            elif column == len(self._data[0]) and row < len(self._data):  # 最后一列
                if self.show_type == "show sum":
                    return str(self.row_sum_max_min_avg[row][0])
                elif self.show_type == "show max":
                    return str(self.row_sum_max_min_avg[row][1])
                elif self.show_type == "show min":
                    return str(self.row_sum_max_min_avg[row][2])
                elif self.show_type == "show avg":
                    return str(self.row_sum_max_min_avg[row][3])
            elif row == len(self._data) and column == len(self._data[0]):  # 最后一个值
                if self.show_type == "show sum":
                    return str(sum([x[0] for x in self.col_sum_max_min_avg]))
                elif self.show_type == "show max":
                    return str(max([x[1] for x in self.col_sum_max_min_avg]))
                elif self.show_type == "show min":
                    return str(min([x[2] for x in self.col_sum_max_min_avg]))
                elif self.show_type == "show avg":
                    return  str(sum([x[3] for x in self.col_sum_max_min_avg]) / len(self.row_sum_max_min_avg))

            # return str(self._data[index.row(), index.column()])
        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter  # 设置居中对齐
        return None
    def rowCount(self, index):
        return self._data.shape[0] + self.add_column

    def columnCount(self, index):
        return self._data.shape[1] + self.add_column

    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if orientation == QtCore.Qt.Horizontal:
                if section < len(self._column_labels):
                    return self._column_labels[section]
                else:
                    if self.show_type == "show sum":
                        return "sum"
                    elif self.show_type == "show max":
                        return "max"
                    elif self.show_type == "show min":
                        return "min"
                    elif self.show_type == "show avg":
                        return "avg"
            elif orientation == QtCore.Qt.Vertical:
                if section < len(self._row_labels):
                    return self._row_labels[section]
                else:
                    if self.show_type == "show sum":
                        return "sum"
                    elif self.show_type == "show max":
                        return "max"
                    elif self.show_type == "show min":
                        return "min"
                    elif self.show_type == "show avg":
                        return "avg"
        return None

    def clearData(self):
        # 清空数据
        self.beginResetModel()
        self._data = []
        self.endResetModel()