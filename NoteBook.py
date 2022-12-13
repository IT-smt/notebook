import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QFont, QIcon
from PyQt6.QtWidgets import QWidget, QMainWindow, QApplication, QTextEdit, QMenuBar, QPushButton, QVBoxLayout, \
    QFileDialog, QMessageBox, QListWidget, QCheckBox, QHBoxLayout, QLabel


class Window(QMainWindow):
    """Блокнот."""
    def __init__(self):
        """Инициализирует."""
        super().__init__()
        self.src = None
        self.file_name = None
        self.bold = 400
        self.cursive = False
        self.text_edit = QTextEdit(self)
        self.font = "Sans serif"
        self.font_size = 14
        self.set_font()
        self.init_ui()

    def init_ui(self):
        """Front."""
        self.setWindowTitle("Блокнот")
        self.setWindowIcon(QIcon("1.png"))
        self.resize(1200, 720)
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        vbox = QVBoxLayout(central_widget)
        vbox.addWidget(self.text_edit)
        central_widget.setLayout(vbox)
        self._create_menu_bar()

    def _create_menu_bar(self):
        """Создает меню."""
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("Файл")
        self.file_menu(file_menu)
        edit_menu = menu_bar.addMenu("Редактировать")
        self.edit_menu(edit_menu)
        self.setMenuBar(menu_bar)

    def file_menu(self, file_menu):
        """Добавляет кнопки в file_menu."""
        self.create_action(file_menu, "Сохранить", "F1", self.save_file, "document-save")
        self.create_action(file_menu, "Сохранить как", "F2", self.save_file_how, "document-save-as")
        self.create_action(file_menu, "Открыть", "F3", self.open_file, "document-open")
        file_menu.addSeparator()
        self.create_action(file_menu, "Закрыть", "F4", self.close, "application-exit")

    def save_file(self):
        """Сохраняет файл."""
        text = self.text_edit.toPlainText()
        try:
            path = self.file_name[0]
            with open(path, "w") as f:
                f.write(text)
        except TypeError:
            self.save_file_how()

    def save_file_how(self):
        """Сохраняет файл в выбранный каталог."""
        try:
            file_name = QFileDialog.getSaveFileName(self)
            text = self.text_edit.toPlainText()
            with open(file_name[0], "w") as f:
                f.write(text)
        except FileNotFoundError:
            pass

    def open_file(self):
        """Открывает файл."""
        try:
            self.file_name = QFileDialog.getOpenFileName(self)
            try:
                with open(self.file_name[0]) as f:
                    self.src = f.read()
                self.text_edit.setText(self.src)
            except UnicodeDecodeError:
                self.message_box("Ошибка", "Не поддерживаемое расширение!", QMessageBox.StandardButton.Ok)
        except FileNotFoundError:
            pass

    def close(self):
        """Выводит всплывающее окно и закрывает приложение."""
        if self.text_edit.toPlainText() != "":
            if self.message_box("Сохранение", "Вы хотите сохранить изменения перед выходом?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
                self.save_file()
        sys.exit()

    def message_box(self, title, text, buttons):
        message_box = QMessageBox()
        message_box.setText(text)
        message_box.setWindowTitle(title)
        message_box.setStandardButtons(buttons)
        message_box.show()
        return message_box.exec()

    def edit_menu(self, edit_menu):
        """Добавляет кнопки в edit_menu."""
        font_size_menu = edit_menu.addMenu("Размер шрифта...")
        self.font_size_menu(font_size_menu)
        font_menu = edit_menu.addMenu("Шрифт...")
        self.font_menu(font_menu)
        edit_menu.addSeparator()
        self.create_action(edit_menu, "Очистить", "F10", self.clear, "edit-clear")

    def font_size_menu(self, font_size_menu):
        """Добавляет кнопки в font_size_menu."""
        font_size_menu.setIcon(QIcon.fromTheme("zoom-fit-best"))
        self.create_action(font_size_menu, "Увеличить", "F5", self.font_size_plus, "zoom-in")
        self.create_action(font_size_menu, "Уменьшить", "F6", self.font_size_minus, "zoom-out")
        font_size_menu.addSeparator()
        self.create_action(font_size_menu, "Сбросить", "F7", self.font_size_reset, "zoom-original")

    def font_size_plus(self):
        """Увеличивает размер шрифта на 1."""
        if self.font_size < 1000:
            self.font_size += 1
        self.set_font()

    def font_size_minus(self):
        """Уменьшает размер шрифта на 1."""
        if self.font_size > 1:
            self.font_size -= 1
        self.set_font()

    def font_size_reset(self):
        """Изменяет размер шрифта на размер по умолчанию."""
        self.font_size = 14
        self.set_font()

    def font_menu(self, font_menu):
        """Добавляет checkbox'ы в font_menu."""
        font_menu.setIcon(QIcon.fromTheme("preferences-desktop-font"))
        self.button_bold = QAction("Жирный", self)
        self.add_action_methods(font_menu, self.button_bold, "F8", True, "preferences-desktop-font", self.font_bold)
        font_menu.addSeparator()
        self.button_cursive = QAction("Курсив", self)
        self.add_action_methods(font_menu, self.button_cursive, "F9", True, "preferences-desktop-font", self.font_cursive)

    def create_action(self, menu, name, key, func, icon):
        """Создает action."""
        button = QAction(name, self)
        button.setShortcut(key)
        button.setIcon(QIcon.fromTheme(icon))
        button.triggered.connect(func)
        menu.addAction(button)

    def add_action_methods(self, menu, button, key, check, icon, func):
        button.setShortcut(key)
        button.setCheckable(check)
        button.setIcon(QIcon.fromTheme(icon))
        button.triggered.connect(func)
        menu.addAction(button)

    def font_bold(self):
        """Изменяет жирность текста."""
        if self.button_bold.isChecked():
            self.button_bold.setCheckable(True)
            self.bold = 800
        else:
            self.button_bold.setCheckable(True)
            self.bold = 400
        self.set_font()

    def font_cursive(self):
        """Изменяет курсив текста."""
        if self.button_cursive.isChecked():
            self.button_cursive.setCheckable(True)
            self.cursive = True
        else:
            self.button_cursive.setCheckable(True)
            self.cursive = False
        self.set_font()

    def set_font(self):
        """Ставит шрифт."""
        self.text_edit.setFont(QFont(self.font, self.font_size, self.bold, self.cursive))

    def clear(self):
        """Очищает поле ввода."""
        self.text_edit.setText("")

    def keyPressEvent(self, event):
        """Обрабатывает нажатия клавиш."""
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
            self.font_bold()
        elif event.key() == Qt.Key.Key_F9:
            self.font_cursive()
        elif event.key() == Qt.Key.Key_F10:
            self.clear()

    def closeEvent(self, event):
        """Срабатывает, когда закрывается приложение."""
        self.close()


if __name__ == "__main__":
    app = QApplication([])
    win = Window()
    win.show()
    app.exec()