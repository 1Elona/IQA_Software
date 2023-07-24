import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # create a button and a label
        self.folder_path_label = QLabel()
        self.open_folder_button = QPushButton("Open Folder")
        self.open_folder_button.clicked.connect(self.open_folder)

        # create a layout
        layout = QVBoxLayout()
        layout.addWidget(self.folder_path_label)
        layout.addWidget(self.open_folder_button)
        self.setLayout(layout)

    def open_folder(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder", options=options)
        if folder_path:
            self.folder_path_label.setText(folder_path)
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    # do something with the file, like printing the file name
                    print(file_name)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()
