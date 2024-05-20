import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QListWidget, QMessageBox, QSpinBox


class LRUCache:
    def __init__(self, capacity: int):
        self.cache = {}
        self.capacity = capacity
        self.order = []

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache[key] = value
            self.order.remove(key)
            self.order.append(key)
        else:
            if len(self.cache) >= self.capacity:
                lru_key = self.order.pop(0)
                del self.cache[lru_key]
            self.cache[key] = value
            self.order.append(key)

    def display(self):
        return self.cache, self.order


class LRUCacheApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('LRU Cache Demo')

        # Layouts
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox2 = QHBoxLayout()

        # Widgets
        self.capacity_label = QLabel('Capacity:')
        self.capacity_input = QSpinBox()
        self.capacity_input.setValue(3)
        self.capacity_input.setMinimum(1)
        self.capacity_input.valueChanged.connect(self.set_capacity)

        self.key_label = QLabel('Key:')
        self.key_input = QLineEdit()
        self.value_label = QLabel('Value:')
        self.value_input = QLineEdit()
        self.put_button = QPushButton('Put')
        self.get_button = QPushButton('Get')
        self.cache_list = QListWidget()
        self.order_list = QListWidget()

        # Add widgets to layouts
        hbox1.addWidget(self.capacity_label)
        hbox1.addWidget(self.capacity_input)
        hbox1.addWidget(self.key_label)
        hbox1.addWidget(self.key_input)
        hbox1.addWidget(self.value_label)
        hbox1.addWidget(self.value_input)
        hbox1.addWidget(self.put_button)
        hbox1.addWidget(self.get_button)

        hbox2.addWidget(QLabel('Cache:'))
        hbox2.addWidget(self.cache_list)
        hbox2.addWidget(QLabel('Order:'))
        hbox2.addWidget(self.order_list)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)

        self.setLayout(vbox)

        # Connect buttons to functions
        self.put_button.clicked.connect(self.put)
        self.get_button.clicked.connect(self.get)

        # Initialize LRUCache with default capacity
        self.cache = LRUCache(self.capacity_input.value())

    def set_capacity(self):
        self.cache = LRUCache(self.capacity_input.value())
        self.update_display()

    def update_display(self):
        cache, order = self.cache.display()
        self.cache_list.clear()
        self.order_list.clear()
        for k, v in cache.items():
            self.cache_list.addItem(f'{k}: {v}')
        for k in order:
            self.order_list.addItem(str(k))

    def put(self):
        try:
            key = int(self.key_input.text())
            value = self.value_input.text()
            if value == '':
                raise ValueError("Value cannot be empty")
            self.cache.put(key, value)
            self.update_display()
        except ValueError as e:
            QMessageBox.warning(self, 'Input Error', str(e))

    def get(self):
        try:
            key = int(self.key_input.text())
            value = self.cache.get(key)
            if value != -1:
                self.value_input.setText(str(value))
            else:
                self.value_input.setText('')
            self.update_display()
        except ValueError as e:
            QMessageBox.warning(self, 'Input Error', 'Key must be an integer')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = LRUCacheApp()
    ex.show()
    sys.exit(app.exec())