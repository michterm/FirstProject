import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QVBoxLayout, QLabel, QListView, QPushButton, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import pickle
import rsa  # Importowanie modułu rsa zawierającego logikę szyfrowania i odszyfrowywania

class AnotherWindow(QWidget):
    def __init__(self):
        super(AnotherWindow, self).__init__()
        self.resize(400, 800)
        self.move(300, 100)

        layout = QVBoxLayout()
        self.label = QLabel("Lista kluczy publicznych:")
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.listView = QListView()
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)
        self.listView.setObjectName("listView-1")
        layout.addWidget(self.listView)

        self.list_of_files = []

    def update_label(self, file_list):
        self.label.setText('\n'.join(file_list))

    def update_list(self, plik):
        self.model.clear()
        for file in plik:
            filename = os.path.basename(file)
            item = QStandardItem(filename)
            self.model.appendRow(item)


class AnotherWindow2(QWidget):
    def __init__(self, callback):
        super(AnotherWindow2, self).__init__()
        self.resize(400, 400)
        self.move(300, 100)
        self.callback = callback

        layout = QVBoxLayout()
        self.label = QLabel("Podaj wiadomość do zaszyfrowania:")
        layout.addWidget(self.label)

        self.input_field = QLineEdit()  # Pole tekstowe do wpisywania wiadomości
        layout.addWidget(self.input_field)

        self.input_button = QPushButton("Zaszyfruj")
        layout.addWidget(self.input_button)
        self.input_button.clicked.connect(self.encrypt_message)

        self.setLayout(layout)

    def encrypt_message(self):
        message = self.get_input()
        if message:
            encrypted_message = self.callback(message)
            if encrypted_message:
                self.save_encrypted_message(encrypted_message)

    def get_input(self):
        return self.input_field.text()  # Pobieranie tekstu z pola tekstowego

    def save_encrypted_message(self, encrypted_message):
        try:
            with open("BazaDanych.txt", "a") as file:
                file.write(str(encrypted_message) + '\n')  # Zapisanie zaszyfrowanej wiadomości do pliku
                QMessageBox.information(self, "Zapisano", "Zaszyfrowana wiadomość została zapisana do pliku.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas zapisywania pliku: {str(e)}")


class AnotherWindow3(QWidget):
    def __init__(self, callback):
        super(AnotherWindow3, self).__init__()
        self.resize(400, 400)
        self.move(300, 100)
        self.callback = callback

        layout = QVBoxLayout()
        self.label = QLabel("Lista zaszyfrowanych plików:")
        layout.addWidget(self.label)

        self.listView = QListView()
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)
        self.listView.setObjectName("listView-1")
        layout.addWidget(self.listView)

        self.decrypt_button = QPushButton("Odszyfruj")
        layout.addWidget(self.decrypt_button)
        self.decrypt_button.clicked.connect(self.show_file_dialog)

        self.setLayout(layout)

    def update_list(self, file_list):
        self.model.clear()
        for file in file_list:
            filename = os.path.basename(file)
            item = QStandardItem(filename)
            self.model.appendRow(item)

    def show_file_dialog(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Pliki (*.*)")
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            decrypted_message = self.callback(selected_file)
            if decrypted_message is not None:
                self.show_decrypted_message(decrypted_message)
            else:
                QMessageBox.warning(self, "Błąd", "Nie można odszyfrować pliku.")

    def show_decrypted_message(self, decrypted_message):
        message_box = QMessageBox()
        message_box.setText("Odszyfrowana wiadomość:")
        message_box.setInformativeText(decrypted_message)
        message_box.exec_()

class Aplikacja(QMainWindow):
    def __init__(self):
        super(Aplikacja, self).__init__()
        self.resize(600, 400)
        self.move(300, 100)
        self.setWindowTitle("Aplikacja 1")

        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        new_action = QAction('New', self)
        file_menu.addAction(new_action)

        open_action = QAction('Open', self)
        file_menu.addAction(open_action)

        edit_menu = menubar.addMenu('Edit')

        cut_action = QAction('Cut', self)
        edit_menu.addAction(cut_action)

        copy_action = QAction('Copy', self)
        edit_menu.addAction(copy_action)

        paste_action = QAction('Paste', self)
        edit_menu.addAction(paste_action)

        layout = QVBoxLayout()
        self.button1 = QPushButton("Generuj klucze")
        self.button2 = QPushButton("Wczytaj klucze")
        self.button3 = QPushButton("Lista kluczy publicznych")
        self.button4 = QPushButton("Sprawdź podpis cyfrowy")
        self.button5 = QPushButton("Zaszyfruj wiadomość")
        self.button6 = QPushButton("Odszyfruj wiadomość")

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        layout.addWidget(self.button5)
        layout.addWidget(self.button6)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.window1 = AnotherWindow()
        self.window2 = AnotherWindow2(self.encrypt_message)
        self.window3 = AnotherWindow3(self.decrypt_message)

        self.button1.clicked.connect(self.generate_keys)
        self.button2.clicked.connect(self.select_file)
        self.button3.clicked.connect(self.toggle_window1)
        self.button4.clicked.connect(self.check_signature)
        self.button5.clicked.connect(self.show_encrypt_window)
        self.button6.clicked.connect(self.show_decrypt_window)

    def generate_keys(self):
        self.keys = rsa.generate_keys()
        rsa.save_keys(self.keys[0], self.keys[1])
        rsa.load_keys()

    def check_signature(self):
        pass

    def encrypt_message(self, message):
        # Tutaj umieść logikę szyfrowania wiadomości
        encrypted_message = rsa.encrypt(message, self.keys[0])
        return encrypted_message

    def decrypt_message(self, selected_file):
        # Tutaj umieść logikę odszyfrowywania wiadomości
        try:
            with open(selected_file, "r") as file:
                encrypted_message = file.read()
                decrypted_message = rsa.decrypt(encrypted_message, self.keys[1])
                return decrypted_message
        except Exception as e:
            print(f"Wystąpił błąd podczas odszyfrowywania pliku: {str(e)}")
            return None

    def select_file(self):
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Pliki (*.*)")
        if file_dialog.exec_():
            selected_file = file_dialog.selectedFiles()[0]
            QMessageBox.information(self, "Wybrano plik", f"Wybrano plik: {selected_file}")

    def toggle_window1(self):
        self.window1.show()
        self.window1.update_label(self.list_of_files)

    def show_encrypt_window(self):
        self.window2.show()

    def show_decrypt_window(self):
        self.window3.update_list(self.list_of_files)
        self.window3.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    aplikacja = Aplikacja()
    aplikacja.show()
    sys.exit(app.exec_())