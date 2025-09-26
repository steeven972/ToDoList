from PyQt5.QtWidgets import QLineEdit, QLabel, QPushButton, QWidget, QVBoxLayout, QApplication, QGroupBox, QHBoxLayout, QListWidgetItem,QListWidget, QMessageBox, QCheckBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
import sys
from App.task import Task

class TaskWidget(QWidget):
    def __init__(self, task, parent_list):
        super().__init__()
        self.task = task
        self.parent_list = parent_list

        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        # Label de la tâche
        self.label = QLabel(f"{self.task.name} | Accomplish: {self.task.status}")
        layout.addWidget(self.label)

        # Bouton supprimer

        self.btnCheck = QCheckBox()
        self.btnCheck.setFixedWidth(25)
        self.btnCheck.setStyleSheet("color: green; font-weight: bold")
        layout.addWidget(self.btnCheck)
        
        self.btnCheck.stateChanged.connect(self.update_status_label)

        self.btnDelete = QPushButton("✖")
        self.btnDelete.setFixedWidth(25)
        self.btnDelete.setStyleSheet("color: red; font-weight: bold;")
        self.btnDelete.clicked.connect(self.delete_task)
        layout.addWidget(self.btnDelete)

        self.setLayout(layout)

    def delete_task(self):
        Task.remove_task(self.task.id)  # supprime du JSON
        
        # Supprime l'item correspondant dans QListWidget
        for i in range(self.parent_list.count()):
            item = self.parent_list.item(i)
            widget = self.parent_list.itemWidget(item)
            if widget == self:
                self.parent_list.takeItem(i)
                break
    def update_status_label(self, state):
        self.task.set_status(state)

        self.label.setText(f"{self.task.name} | Accomplish: {self.task.status}")
    

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(15)

        # Widgets
        self.labelTitre = QLabel("ToDoList")
        self.labelTitre.setAlignment(Qt.AlignCenter)
        self.labelTitre.setStyleSheet("font-size: 24px; font-weight: bold; color: #2c3e50 ")
        self.layout.addWidget(self.labelTitre)

        taskBox = QGroupBox("Add a task")
        taskLayout = QVBoxLayout()
        self.labelEntry = QLabel("Task Name: ")
        self.entry = QLineEdit()
        self.btnSave = QPushButton(text="Add")
        self.btnSave.setStyleSheet("Background: #3498db; color: white; border-radius:5px; padding:8px ")
        

        inputLayout = QHBoxLayout()
        inputLayout.addWidget(self.entry)
        inputLayout.addWidget(self.btnSave)

        taskLayout.addWidget(self.labelEntry)
        taskLayout.addLayout(inputLayout)
        taskBox.setLayout(taskLayout)
        self.layout.addWidget(taskBox)

        self.taskListWidget = QListWidget()
        self.layout.addWidget(self.taskListWidget)
    

        self.data = Task.load() 
        for key, task_data in self.data.items():
            task = Task(data=task_data[0], task_id=key)  # recrée l’objet Task depuis le dict
            self.add_task_to_list(task)

        self.btnSave.clicked.connect(self.createTask)
    

    def add_task_to_list(self, task):
        item = QListWidgetItem()
        task_widget = TaskWidget(task, self.taskListWidget)
        item.setSizeHint(task_widget.sizeHint())
        self.taskListWidget.addItem(item)
        self.taskListWidget.setItemWidget(item, task_widget)
    def createTask(self):
        
        name = self.entry.text()
        if name:
            new_task = Task(name)
            self.add_task_to_list(new_task)
            #self.taskListWidget.addItem(f"{new_task.name} | Accomplish: {new_task.status}")
            self.entry.clear()
            return new_task
        else:
            message = QMessageBox()
            message.setText("Name the task")
            message.setIcon(QMessageBox.Information)
            message.setStandardButtons(QMessageBox.Cancel | QMessageBox.Ok)
            
            returnValue = message.exec()
            if returnValue == QMessageBox.Ok:
                print("Ok clicked")

    

        

    @staticmethod
    def run():
        app = QApplication([])
        widget = MyWidget()
        widget.resize(500, 400)
        widget.show()
        sys.exit(app.exec())
        return app


    

    