# -*- coding: utf-8 -*-
# @File    : omx_operate.py
# 功能：矩阵文件操作
# @Time    : 2025/1/8 上午9:34
# @Author  : lhy
# @Software: PyCharm
import openmatrix as omx

import sys
import numpy as np
import openmatrix as omx
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, \
    QWidget, QFileDialog, QMessageBox


class MatrixViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OMX Matrix Viewer")
        self.setGeometry(100, 100, 800, 600)

        self.matrix = None

        self.table = QTableWidget()
        self.open_button = QPushButton("Open OMX File")
        self.open_button.clicked.connect(self.open_omx_file)

        self.sum_rows_button = QPushButton("Sum Rows")
        self.sum_rows_button.clicked.connect(self.sum_rows)

        self.sum_cols_button = QPushButton("Sum Columns")
        self.sum_cols_button.clicked.connect(self.sum_cols)

        layout = QVBoxLayout()
        layout.addWidget(self.open_button)
        layout.addWidget(self.sum_rows_button)
        layout.addWidget(self.sum_cols_button)
        layout.addWidget(self.table)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def open_omx_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open OMX File", "", "OMX Files (*.omx)")
        if file_path:
            with omx.open_file(file_path) as omx_file:
                matrix_names = omx_file.list_matrices()
                if matrix_names:
                    self.matrix = omx_file[matrix_names[0]]
                    self.display_matrix()
                else:
                    QMessageBox.warning(self, "No Matrices", "The selected OMX file contains no matrices.")

    def display_matrix(self):
        if self.matrix is not None:
            rows, cols = self.matrix.shape
            self.table.setRowCount(rows)
            self.table.setColumnCount(cols)
            for i in range(rows):
                for j in range(cols):
                    item = QTableWidgetItem(str(self.matrix[i, j]))
                    self.table.setItem(i, j, item)

    def sum_rows(self):
        if self.matrix is not None:
            row_sums = np.sum(self.matrix, axis=1)
            QMessageBox.information(self, "Row Sums", str(row_sums))

    def sum_cols(self):
        if self.matrix is not None:
            col_sums = np.sum(self.matrix, axis=0)
            QMessageBox.information(self, "Column Sums", str(col_sums))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MatrixViewer()
    window.show()
    sys.exit(app.exec_())
