import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget,\
    QTabWidget, QGridLayout, QTableWidget, QTableWidgetItem, QHeaderView, QSlider, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

from db import work_with_db


ORDER_AGGREGATE = {
    'Без просрочки': 0,
    '1-30': 1,
    '31-90': 2,
    '91-180': 3,
    '181-360': 4,
    '360+': 5,
}
TEMPLATE_LABEL = 'Мин. количество кредитов: {}'

COUNT_MIN_CREDITS = 1
COUNT_MAX_CREDITS = 5


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Клиенты'
        self.setMinimumSize(900, 600)
        self.setWindowIcon(QIcon('sources/images/icon.png'))
        self.setWindowTitle(self.title)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # START TABS
        self.tabs = QTabWidget()

        self.aggregate = QWidget()
        self.clients_one_bank = QWidget()
        self.active_clients = QWidget()

        self.tabs.addTab(self.aggregate, "Агрегированные данные")
        self.tabs.addTab(self.active_clients, "Действующие клиенты")
        self.tabs.addTab(self.clients_one_bank, "Клиенты одного банка")
        self.layout.addWidget(self.tabs)
        # END TABS

        # START TABLE
        self.table = QTableWidget(self)

        self.table_header = [
            'Дней непрерывной \nпросрочки по ОД или %',
            'Сумма ссудной задолженности',
            'Выданная сумма',
            'Сумма просроченной\n ссудной задолженности',
        ]

        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setColumnCount(len(self.table_header))
        self.table.setHorizontalHeaderLabels(self.table_header)
        self.table.verticalHeader().setVisible(False)

        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        # END TABLE

        # START SLIDERS
        self.sld_clients = QSlider(Qt.Horizontal, self)
        self.sld_clients.setMinimum(COUNT_MIN_CREDITS)
        self.sld_clients.setMaximum(COUNT_MAX_CREDITS)
        self.sld_clients.setValue(3)
        self.sld_clients.valueChanged[int].connect(self.sld_clients_action)

        self.sld_clients_one_bank = QSlider(Qt.Horizontal, self)
        self.sld_clients_one_bank.setMinimum(COUNT_MIN_CREDITS)
        self.sld_clients_one_bank.setMaximum(COUNT_MAX_CREDITS)
        self.sld_clients_one_bank.setValue(3)
        self.sld_clients_one_bank.valueChanged[int].connect(self.sld_clients_one_bank_action)
        # END SLIDERS

        # START LABELS
        self.label_active_clients = QLabel(TEMPLATE_LABEL.format(self.sld_clients.value()))
        self.label_clients_one_bank = QLabel(TEMPLATE_LABEL.format(self.sld_clients_one_bank.value()))
        # END LABELS

        # START BUTTON
        self.btn_update = QPushButton("Обновить данные")
        self.btn_update.clicked.connect(self.view_info)
        # END BUTTON

        # START PLOTS
        self.plot_active_clients = MatPlot(
            self.active_clients,
            labels=(
                'Остальные клиенты',
                'Клиенты с {} и более\nактивными кредитами'
            )
        )
        self.plot_clients_one_bank = MatPlot(
            self.clients_one_bank,
            labels=(
                'Остальные клиенты',
                'Клиенты одного банка\nс {} и более кредитами'
            )
        )
        # END PLOTS

        # START FILLING TABS
        self.layout_aggregate = QGridLayout()
        self.aggregate.setLayout(self.layout_aggregate)

        self.layout_active_clients = QGridLayout()
        self.active_clients.setLayout(self.layout_active_clients)

        self.layout_clients_one_bank = QGridLayout()
        self.clients_one_bank.setLayout(self.layout_clients_one_bank)
        # END FILLING TABS

        self.set_position()

        self.view_info()

    def set_position(self):
        self.layout_aggregate.addWidget(self.btn_update, 0, 8, 1, 1)
        self.layout_aggregate.addWidget(self.table, 1, 0, 1, 9)

        self.layout_active_clients.addWidget(self.sld_clients, 0, 70, 1, 30)
        self.layout_clients_one_bank.addWidget(self.sld_clients_one_bank, 0, 70, 1, 30)

        self.layout_active_clients.addWidget(self.label_active_clients, 0, 55, 1, 12)
        self.layout_clients_one_bank.addWidget(self.label_clients_one_bank, 0, 55, 1, 12)

        self.layout_active_clients.addWidget(self.plot_active_clients.canvas, 1, 0, 1, 100)
        self.layout_clients_one_bank.addWidget(self.plot_clients_one_bank.canvas, 1, 0, 1, 100)

    def view_info(self):
        self.update_table()
        self.refresh_plot_active_clients()
        self.refresh_plot_clients_one_bank()

    def fill_table(self, data):
        self.table.setRowCount(len(data))
        for row, row_items in enumerate(data):
            for column, value in enumerate(row_items):
                item = QTableWidgetItem(str(value))
                self.table.setItem(row, column, item)

    def update_table(self):
        data = work_with_db.get_aggregate_data()[0]
        data.sort(key=lambda x: ORDER_AGGREGATE.get(x[0], float('inf')))
        self.fill_table(data)

    def sld_clients_action(self, val):
        self.label_active_clients.setText(TEMPLATE_LABEL.format(val))
        self.refresh_plot_active_clients()

    def sld_clients_one_bank_action(self, val):
        self.label_clients_one_bank.setText(TEMPLATE_LABEL.format(val))
        self.refresh_plot_clients_one_bank()

    def refresh_plot_active_clients(self):
        cnt_credits = self.sld_clients.value()
        cnt_all_clients = work_with_db.get_count_clients()[0][0][0]
        cnt_target = work_with_db.get_count_valid_clients(cnt_credits)[0][0][0]
        self.plot_active_clients.plot_pie(cnt_all_clients - cnt_target, cnt_target, cnt_credits)

    def refresh_plot_clients_one_bank(self):
        cnt_credits = self.sld_clients_one_bank.value()
        cnt_all_clients = work_with_db.get_count_clients()[0][0][0]
        cnt_target = work_with_db.get_count_clients_one_bank(cnt_credits)[0][0][0]
        self.plot_clients_one_bank.plot_pie(cnt_all_clients - cnt_target, cnt_target, cnt_credits)


class MatPlot(object):
    def __init__(self, parent, labels):
        self.labels = labels
        self.colors = ('lightskyblue', 'yellowgreen')
        self.explode = (0, 0.2)
        self.fig, self.ax1 = plt.subplots()

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(parent)

    def plot_pie(self, all_clients, target, label):
        self.ax1.clear()
        labels = self.labels[0], self.labels[1].format(label)
        sizes = [all_clients, target]
        explode = self.explode

        if not all_clients:
            sizes = sizes[1:]
            labels = labels[1:]
            explode = self.explode[1:]

        if not target:
            sizes = sizes[:1]
            labels = labels[:1]
            explode = self.explode[:1]

        self.ax1.pie(
            sizes,
            explode=explode,
            labels=labels,
            colors=self.colors,
            autopct=lambda x: get_labels_pie(x, sizes),
            shadow=True,
            startangle=90
        )

        self.ax1.axis('equal')
        self.canvas.draw()


def get_labels_pie(pct, all_value):
    absolute = int(round(pct / 100. * sum(all_value)))
    label_human = 'человек' + 'а' * (absolute % 10 in [2, 3, 4] and absolute % 100 not in [12, 13, 14])
    return "{:.1f}%\n({} {})".format(pct, absolute, label_human)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
