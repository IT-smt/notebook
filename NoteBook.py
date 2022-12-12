import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QTextEdit, QMenuBar, QPushButton, QVBoxLayout, \
    QFileDialog, QMessageBox


class Window(QMainWindow):
    """Блокнот"""
    def __init__(self):
        """Инициализирует"""
        super().__init__()
        self.src = None
        self.file_name = None
        self.text_edit = QTextEdit(self)
        self.font = "Sans serif"
        self.font_size = 14
        self.text_edit.setFont(QFont(self.font, self.font_size))
        self.init_ui()

    def init_ui(self):
        """Front"""
        self.setWindowTitle("Блокнот")
        self.resize(1200, 720)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vbox = QVBoxLayout(central_widget)
        vbox.addWidget(self.text_edit)
        central_widget.setLayout(vbox)
        self._create_menu_bar()

    def _create_menu_bar(self):
        """Создает меню"""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Файл")
        self.file_menu(file_menu)
        edit_menu = menu_bar.addMenu("Редактировать")
        self.edit_menu(edit_menu)
        self.setMenuBar(menu_bar)

    def file_menu(self, file_menu):
        button_save = QAction("Сохранить", self)
        button_save.setShortcut("F1")
        button_save.setIcon(QIcon.fromTheme("document-save"))
        button_save.triggered.connect(self.save_file)
        button_save_how = QAction("Сохранить как", self)
        button_save_how.setShortcut("F2")
        button_save_how.setIcon(QIcon.fromTheme("document-save-as"))
        button_save_how.triggered.connect(self.save_file_how)
        button_open = QAction("Открыть", self)
        button_open.setShortcut("F3")
        button_open.setIcon(QIcon.fromTheme("document-open"))
        button_open.triggered.connect(self.open_file)
        button_close = QAction("Закрыть", self)
        button_close.setShortcut("F4")
        button_close.setIcon(QIcon.fromTheme("application-exit"))
        button_close.triggered.connect(self.close)
        file_menu.addAction(button_save)
        file_menu.addAction(button_save_how)
        file_menu.addAction(button_open)
        file_menu.addSeparator()
        file_menu.addAction(button_close)

    def edit_menu(self, edit_menu):
        font_size_menu = edit_menu.addMenu("Размер шрифта...")
        self.font_size_menu(font_size_menu)
        edit_menu.addSeparator()
        button_clear = QAction("Очистить", self)
        button_clear.setShortcut("F8")
        button_clear.setIcon(QIcon.fromTheme("edit-clear"))
        button_clear.triggered.connect(self.clear)
        edit_menu.addAction(button_clear)

    def font_size_menu(self, font_size_menu):
        font_size_menu.setIcon(QIcon.fromTheme("zoom-fit-best"))
        button_plus = QAction("Увеличить", self)
        button_plus.setShortcut("F5")
        button_plus.setIcon(QIcon.fromTheme("zoom-in"))
        button_plus.triggered.connect(self.font_size_plus)
        font_size_menu.addAction(button_plus)
        button_minus = QAction("Уменьшить", self)
        button_minus.setShortcut("F6")
        button_minus.setIcon(QIcon.fromTheme("zoom-out"))
        button_minus.triggered.connect(self.font_size_minus)
        font_size_menu.addAction(button_minus)
        font_size_menu.addSeparator()
        button_reset = QAction("Сбросить", self)
        button_reset.setShortcut("F7")
        button_reset.setIcon(QIcon.fromTheme("zoom-original"))
        button_reset.triggered.connect(self.font_size_reset)
        font_size_menu.addAction(button_reset)

    def save_file(self):
        text = self.text_edit.toPlainText()
        try:
            path = self.file_name[0]
            with open(path, "w") as f:
                f.write(text)
        except TypeError:
            self.save_file_how()

    def save_file_how(self):
        try:
            file_name = QFileDialog.getSaveFileName(self)
            text = self.text_edit.toPlainText()
            with open(file_name[0], "w") as f:
                f.write(text)
        except FileNotFoundError:
            pass

    def open_file(self):
        try:
            self.file_name = QFileDialog.getOpenFileName(self)
            try:
                with open(self.file_name[0]) as f:
                    self.src = f.read()
                self.text_edit.setText(self.src)
            except UnicodeDecodeError:
                message_box = QMessageBox()
                message_box.setIcon(QIcon)
                message_box.setText("Не поддерживаемое расширение!")
                message_box.setWindowTitle("Ошибка")
                message_box.setStandardButtons(QMessageBox.StandardButton.Ok)
                message_box.show()
                message_box.exec()
        except FileNotFoundError:
            pass

    def font_size_plus(self):
        if self.font_size < 1000:
            self.font_size += 1
        self.text_edit.setFont(QFont(self.font, self.font_size))

    def font_size_minus(self):
        if self.font_size > 1:
            self.font_size -= 1
        self.text_edit.setFont(QFont(self.font, self.font_size))

    def font_size_reset(self):
        self.font_size = 14
        self.text_edit.setFont(QFont(self.font, self.font_size))

    def clear(self):
        self.text_edit.setText("")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F1:
            self.save_file()
        elif event.key() == Qt.Key.Key_F2:
            self.save_file_how()
        elif event.key() == Qt.Key.Key_F3:
            self.open_file()
        elif event.key() == Qt.Key.Key_F4:
            self.close()
        elif event.key() == Qt.Key.Key_F5:
            self.font_size_plus()
        elif event.key() == Qt.Key.Key_F6:
            self.font_size_minus()
        elif event.key() == Qt.Key.Key_F7:
            self.font_size_reset()
        elif event.key() == Qt.Key.Key_F8:
            self.clear()

    def close(self):
        if self.text_edit.toPlainText() != "":
            message_box = QMessageBox()
            message_box.setText("Вы хотите сохранить изменения перед выходом?")
            message_box.setWindowTitle("Сохранение")
            message_box.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            message_box.show()
            result = message_box.exec()
            if result == QMessageBox.StandardButton.Yes:
                self.save_file()
        sys.exit()

    def closeEvent(self, event):
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    win = Window()
    win.show()
    app.exec()
