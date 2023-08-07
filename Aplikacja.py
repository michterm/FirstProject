#!/usr/bin/env python
import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QWidget, QVBoxLayout, QLabel, QListView, QPushButton, QFileDialog, QLineEdit, QMessageBox
from PyQt5.QtGui import QStandardItemModel, QStandardItem
import pickle
import tkinter as tk
from tkinter import simpledialog
from rsa import *
from podpis_cyfrowy import *
from faza_wstepna import *

class AnotherWindow(QWidget):

    def __init__(self):
        """
        Inicjalizacja okna 
        i jego elementów.
        """
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
        '''
        Funkcja aktualizująca label.
        '''
        self.label.setText('\n'.join(file_list))

    def update_list(self, plik):
        '''
        Funkcja aktualizująca listę
        '''
        self.model.clear()
        for file in plik:
            filename = os.path.basename(file)
            item = QStandardItem(filename)
            self.model.appendRow(item)


class AnotherWindow2(QWidget):

    def __init__(self, callback):
        '''
        Inicjalizacja okna i jego elementów.
        '''
        super(AnotherWindow2, self).__init__()
        self.resize(400, 400)
        self.move(300, 100)
        self.callback = callback

        layout = QVBoxLayout()
        self.file_name = QFileDialog.getOpenFileName(self, 'Wybierz klucz publiczny do zaszyfrownia', '')[0]
        if self.file_name:
            self.kluczpub = pickle.load(open(self.file_name, "rb"))

        self.label = QLabel("Podaj wiadomość do zaszyfrowania:")
        layout.addWidget(self.label)


        self.input_field = QLineEdit()  # Pole tekstowe do wpisywania wiadomości
        layout.addWidget(self.input_field)
 
        self.label2 = QLabel("Podaj nazwę pliku, do którego zostanie zapisana wiadomość (bez rozszerzenia):")
        layout.addWidget(self.label2)


        self.input_field2 = QLineEdit()  # Pole tekstowe do wpisywania wiadomości
        layout.addWidget(self.input_field2)
        self.input_button = QPushButton("Zaszyfruj")
        layout.addWidget(self.input_button)
        self.input_button.clicked.connect(self.encrypt_message)

        self.setLayout(layout)

    def encrypt_message(self):
        '''
        Funkcja wykorzystująca callback do zaszyfrowania wiadomości.
        '''
        message = MD4.from_string(self.input_field.text())
        message.get_hash()
        sumkon=[int(frag,0) for frag in divide_message(self.kluczpub,message.suma_kontrolna)]
        file_name = self.input_field2.text() 
        if message:
            encrypted_message = [self.kluczpub.encrypt(frag) for frag in sumkon]
            if encrypted_message:
                self.save_encrypted_message(encrypted_message,file_name)


    def save_encrypted_message(self, encrypted_message,file_name):
        '''
        Funkcja zapisująca zaszyfrowaną wiadomość do pliku.
        '''

        try:
            with open(file_name+".txt", "w") as file:
                for frag in encrypted_message:
                    file.write(str(frag)+"\n")  # Zapisanie zaszyfrowanej wiadomości do pliku
                QMessageBox.information(self, "Zapisano", "Zaszyfrowana wiadomość została zapisana do pliku.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas zapisywania pliku: {str(e)}")


class AnotherWindow3(QWidget):

    def __init__(self):
        
        '''
        Inicjalizacja okna i jego elementów.
        '''
        super(AnotherWindow3, self).__init__()
        self.resize(400, 400)
        self.move(300, 100)


        layout = QVBoxLayout()
        self.file_name = QFileDialog.getOpenFileName(self, 'Wybierz klucz prywatny do podpisania', '')[0]
        if self.file_name:
            self.kluczpri = pickle.load(open(self.file_name, "rb"))
 
        self.label2 = QLabel("Podaj nazwę pliku, do którego zostanie zapisana wiadomość z podpisem(bez rozszerzenia):")

        layout.addWidget(self.label2)


        self.input_field2 = QLineEdit()  # Pole tekstowe do wpisywania wiadomości
        layout.addWidget(self.input_field2)

        self.label3 = QLabel("Podaj wiadomość, która zostanie podpisana: ")
        layout.addWidget(self.label3)

        self.input_field_mes = QLineEdit()  # Pole tekstowe do wpisywania wiadomości
        layout.addWidget(self.input_field_mes)
        
        self.input_button = QPushButton("Podpisz")
        layout.addWidget(self.input_button)
        self.input_button.clicked.connect(self.sign_message)

        self.setLayout(layout)
    def sign_message(self):
        sign=Signature_from_string(self.kluczpri,self.input_field_mes.text())
        file_name = self.input_field2.text() 
        if sign:
            self.save_signature(sign,file_name)
    
    def save_signature(self,sign,file_name):
        '''
        Funkcja zapisująca  wiadomość i jej podpis do pliku.
        '''
        try:
            with open(file_name+".txt", "w") as file:
                file.write(str(sign[0])+"\n")
                for frag in sign[1]:
                    file.write(str(frag)+"\n")  # Zapisanie podpisu wiadomości do pliku
                QMessageBox.information(self, "Zapisano", "Wiadmość i podpis zostały zapisane do pliku.")
        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Wystąpił błąd podczas zapisywania pliku: {str(e)}")


class AnotherWindow4(QWidget):

    def __init__(self):
        '''
        Inicjalizacja okna i jego elementów.
        '''
        super(AnotherWindow4, self).__init__()
        self.resize(400, 400)
        self.move(300, 100)
      #  self.callback = callback

        layout = QVBoxLayout()
        self.label = QLabel("Podaj nazwę klucza (bez rozszerzenia):")
        layout.addWidget(self.label)

        self.input_field = QLineEdit()  # Pole tekstowe do wpisywania wiadomości
        self.wiadomosc=self.input_field.text

        layout.addWidget(self.input_field)

        self.input_button = QPushButton("Zaakceptuj")
        layout.addWidget(self.input_button)
        self.input_button.clicked.connect(self.generate_keys)

        self.setLayout(layout)
    def generate_keys(self):
        '''
        Funkcja wykorzystująca klasę RSA do wygenerowania kluczy.
        '''
        self.klucz = RSA().generate_keys()
        RSA.save_keys(self.klucz[0], self.klucz[1],self.input_field.text())
        #RSA.load_keys()
        self.label.setText("Wczytano klucze")

class Aplikacja(QMainWindow):

    def __init__(self):
        '''
        Inicjalizacja okna i jego elementów.
        '''
        super(Aplikacja, self).__init__()
        self.resize(600, 400)
        self.move(300, 100)
        self.setWindowTitle("Aplikacja 1")



        self.initUI()

    def initUI(self):
        '''
        Funkcja inicjalizująca interfejs użytkownika.
        '''
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
        self.button2 = QPushButton("Odczytaj zawartość pliku")
        self.button3 = QPushButton("Podpisz wiadomość")
        self.button4 = QPushButton("Sprawdź podpis cyfrowy")
        self.button5 = QPushButton("Zaszyfruj wiadomość")
        self.button6 = QPushButton("Odszyfruj wiadomość")
        self.label = QLabel("")

        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)
        layout.addWidget(self.button5)
        layout.addWidget(self.button6)
        layout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        self.window1 = AnotherWindow()
        self.window4 = AnotherWindow4()

        self.button1.clicked.connect(self.name_and_generate_keys)
        self.button2.clicked.connect(self.select_file2)
        self.button3.clicked.connect(self.show_sign_window)
        self.button4.clicked.connect(self.check_signature)
        self.button5.clicked.connect(self.show_encrypt_window)
        self.button6.clicked.connect(self.show_decrypt_window)



    def check_signature(self):
        self.file_name = QFileDialog.getOpenFileName(self, 'Wybierz klucz publiczny osoby, która podpisała wiadomość', '')[0]
        if self.file_name:
            self.kluczpub = pickle.load(open(self.file_name, "rb"))
        self.file_message = QFileDialog.getOpenFileName(self, 'Wybierz plik z zaszyfrowaną wiadomością', '')[0]
        file = open(self.file_message, 'r')
        Lines = file.readlines()
        message=Lines[0][:-1]
        sign=[]
        for frag in Lines[1::]:
            sign.append(int(frag))
        is_correct=Check_signature(self.kluczpub,message,sign)

        if is_correct==True:
            self.label.setText("Wiaddomość została podpisana przez osobę o tym kluczu publicznym")
        else:
            self.label.setText("Wiaddomość nie została podpisana przez osobę o tym kluczu publicznym")

    def encrypt_message(self, message):
        # Tutaj umieść logikę szyfrowania wiadomości

        encrypted_message = "Zaszyfrowana wiadomość: " + message
        return encrypted_message

    def decrypt_message(self, selected_file):
        # Tutaj umieść logikę odszyfrowywania wiadomości
        decrypted_message = "Odszyfrowana wiadomość z pliku: " + selected_file
        return decrypted_message

    def toggle_window1(self):
        '''
        Funkcja wyświetlająca okno z listą kluczy publicznych.
        '''
        if self.window1.isVisible():
            self.window1.hide()
        else:
            if hasattr(self, 'keys'):
                self.window1.update_list(self.window1.list_of_files)
            self.window1.show()


    def name_and_generate_keys(self):
        self.window4.show()

    def show_encrypt_window(self):
        self.window2 = AnotherWindow2(self.encrypt_message)
        '''
        Funkcja wyświetlająca okno do wyboru pliku do zaszyfrowania.
        '''
        self.window2.show()
    def show_sign_window(self):
        '''
        Funkcja wyświetlająca okno do wyboru pliku do zaszyfrowania.
        '''
        self.window3 = AnotherWindow3()

        self.window3.show()   

    def show_decrypt_window(self):
        '''
        Funkcja wyświetlająca okno do wyboru pliku do odszyfrowania.
        '''

        self.file_name = QFileDialog.getOpenFileName(self, 'Wybierz klucz prywatny', '')[0]
        if self.file_name:
            self.kluczpri = pickle.load(open(self.file_name, "rb"))
        self.file_message = QFileDialog.getOpenFileName(self, 'Wybierz plik z zaszyfrowaną wiadomością', '')[0]
        file = open(self.file_message, 'r')
        Lines = file.readlines()
        dec_frag=[]
        for line in Lines:
            dec_frag.append(self.kluczpri.decrypt(int(line)))


        decrypted_message="0x"
        for frag in dec_frag:
            decrypted_message += hex(frag)[2::]
        if decrypted_message is not None:
            self.label.setText("Odszyfrowana wiadomość: "+decrypted_message)

    def select_file(self):
        '''
        Funkcja wyświetlająca okno dialogowe do wyboru pliku.
        '''
        self.window1.list_of_files = []
        self.label = QLabel("Klucze")
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        file_name = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if file_name:
            self.keys = pickle.load(open(file_name, "rb"))
            self.label.setText(str(self.keys))
            self.window1.list_of_files.append(file_name)
            self.window1.update_list(self.window1.list_of_files)
    def select_file2(self):
        '''
        Funkcja wyświetlająca okno dialogowe do wyboru pliku.
        '''
        self.window1.list_of_files = []

        file_name = QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]
        if file_name:
            with open(file_name) as f:
                self.wiadomosc=f.read()
            self.label.setText(self.wiadomosc)

if __name__ == "__main__":

    app = QApplication(sys.argv)
    aplikacja = Aplikacja()
    aplikacja.show()
    sys.exit(app.exec_())
