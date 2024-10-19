import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox, QFormLayout
import re
import csv
import database

class ContactApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Agenda de Contatos")
        self.setGeometry(300, 300, 400, 400)
        
        self.layout = QFormLayout()

        self.search_input = QLineEdit(self)
        self.search_input.setPlaceholderText("Buscar contato...")
        self.search_input.textChanged.connect(self.search_contacts)
        self.layout.addRow("Buscar:", self.search_input)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Nome")
        self.layout.addRow("Nome:", self.name_input)

        self.phone_input = QLineEdit(self)
        self.phone_input.setPlaceholderText("Telefone")
        self.layout.addRow("Telefone:", self.phone_input)

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.layout.addRow("Email:", self.email_input)

        self.add_button = QPushButton("Adicionar Contato")
        self.add_button.clicked.connect(self.add_contact)
        self.layout.addRow(self.add_button)

        self.clear_button = QPushButton("Limpar Campos")
        self.clear_button.clicked.connect(self.clear_inputs)
        self.layout.addRow(self.clear_button)

        self.export_button = QPushButton("Exportar Contatos (CSV)")
        self.export_button.clicked.connect(self.export_contacts)
        self.layout.addRow(self.export_button)

        self.contact_list = QListWidget()
        self.layout.addRow("Contatos:", self.contact_list)

        self.edit_button = QPushButton("Editar Contato")
        self.edit_button.clicked.connect(self.edit_contact)
        self.layout.addRow(self.edit_button)

        self.remove_button = QPushButton("Remover Contato")
        self.remove_button.clicked.connect(self.remove_contact)
        self.layout.addRow(self.remove_button)

        self.setLayout(self.layout)

        self.setStyleSheet("""
            QWidget {
                background-color: #f0f0f0;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }

            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
                border: 2px solid #4CAF50;
            }

            QPushButton:hover {
                background-color: #45a049;
            }

            QPushButton:pressed {
                background-color: #3e8e41;
                border: 2px solid #3e8e41;
            }

            QLineEdit {
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 8px;
                background-color: #fff;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 2px solid #4CAF50;
                outline: none;
            }

            QListWidget {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 5px;
                background-color: #fff;
            }

            QListWidget::item {
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }

            QListWidget::item:hover {
                background-color: #e6f7ff;
            }

            QListWidget::item:selected {
                background-color: #4CAF50;
                color: white;
            }

            QMessageBox {
                background-color: #f0f0f0;
                font-size: 14px;
                border-radius: 8px;
            }
        """)

        self.load_contacts()

    def load_contacts(self):
        self.contact_list.clear()
        contacts = database.fetch_contacts()
        for contact in contacts:
            self.contact_list.addItem(f"{contact[0]} - {contact[1]} - {contact[2]} - {contact[3]}")

    def search_contacts(self):
        query = self.search_input.text().lower()
        self.contact_list.clear()
        contacts = database.fetch_contacts()
        
        filtered_contacts = [contact for contact in contacts if query in contact[1].lower() or query in contact[2].lower() or query in contact[3].lower()]
        
        for contact in filtered_contacts:
            self.contact_list.addItem(f"{contact[0]} - {contact[1]} - {contact[2]} - {contact[3]}")

    def add_contact(self):
        name = self.name_input.text()
        phone = self.phone_input.text()
        email = self.email_input.text()

        if not name or not phone:
            QMessageBox.warning(self, "Erro", "Nome e Telefone são obrigatórios!")
            return

        if email and not is_valid_email(email):
            QMessageBox.warning(self, "Erro", "Email inválido!")
            return

        if not is_valid_phone(phone):
            QMessageBox.warning(self, "Erro", "Telefone inválido!")
            return

        database.insert_contact(name, phone, email)
        self.load_contacts()
        self.clear_inputs()
        QMessageBox.information(self, "Sucesso", "Contato adicionado com sucesso!")

    def remove_contact(self):
        selected_item = self.contact_list.currentItem()
        if selected_item:
            contact_id = selected_item.text().split(" - ")[0]
            confirm = QMessageBox.question(self, "Confirmação", "Tem certeza que deseja excluir este contato?", 
                                           QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if confirm == QMessageBox.Yes:
                database.delete_contact(contact_id)
                self.load_contacts()
                QMessageBox.information(self, "Sucesso", "Contato removido com sucesso!")
        else:
            QMessageBox.warning(self, "Erro", "Nenhum contato selecionado!")

    def edit_contact(self):
        selected_item = self.contact_list.currentItem()
        if selected_item:
            contact_id = selected_item.text().split(" - ")[0]
            name = self.name_input.text()
            phone = self.phone_input.text()
            email = self.email_input.text()

            if not name or not phone:
                QMessageBox.warning(self, "Erro", "Nome e Telefone são obrigatórios!")
                return

            if email and not is_valid_email(email):
                QMessageBox.warning(self, "Erro", "Email inválido!")
                return

            if not is_valid_phone(phone):
                QMessageBox.warning(self, "Erro", "Telefone inválido!")
                return

            database.update_contact(contact_id, name, phone, email)
            self.load_contacts()
            self.clear_inputs()
            QMessageBox.information(self, "Sucesso", "Contato atualizado com sucesso!")

    def clear_inputs(self):
        self.name_input.clear()
        self.phone_input.clear()
        self.email_input.clear()

    def export_contacts(self):
        export_contacts_to_csv()
        QMessageBox.information(self, "Sucesso", "Contatos exportados para 'contacts.csv' com sucesso!")

def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(pattern, email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) >= 8

def export_contacts_to_csv():
    contacts = database.fetch_contacts()
    with open('contacts.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['ID', 'Nome', 'Telefone', 'Email'])
        for contact in contacts:
            writer.writerow(contact)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    database.connect()
    
    window = ContactApp()
    window.show()
    
    sys.exit(app.exec_())
