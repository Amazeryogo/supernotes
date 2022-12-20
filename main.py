from PySide6 import QtWidgets
from PySide6.QtWidgets import QFileDialog


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("SuperNotes v0")
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.fn = ""

        try:
            with open(".cache.txt","r") as f:
                x = f.read()
                if len(x) > 0:
                    with open(x, "r") as f:
                        text = f.read()
                else:
                    text = ""
        except FileNotFoundError:
            text = ""


        self.markdown_editor = QtWidgets.QTextEdit()
        self.markdown_editor.setText(text)
        self.markdown_viewer = QtWidgets.QTextEdit(readOnly=True)
        self.stacked_widget.addWidget(self.markdown_editor)
        self.stacked_widget.addWidget(self.markdown_viewer)

        foo_menu = self.menuBar().addMenu("&Menu")
        self.edit_action = foo_menu.addAction("🔒 Lock")
        self.savex = foo_menu.addAction("&save")
        self.open_filex = foo_menu.addAction("Open")
        self.edit_action.setCheckable(True)
        self.savex.triggered.connect(self.save)
        self.edit_action.triggered.connect(self.handle_edit_mode)
        self.open_filex.triggered.connect(self.open_file)
    def save(self):
        l = []
        for i in self.markdown_editor.toPlainText().split('\n'):
            l.append(i)
        if self.fn == "":
            if "$" not in l[0]:
                l[0] = l[0].replace("#","")
                if len(l[0]) != 0:
                    with open("notes/"+l[0]+".md", 'w') as f:
                        f.write(self.markdown_editor.toMarkdown())
                    with open(".cache.txt","w") as f:
                        f.write("notes/"+l[0]+".md")
                        f.close()
            else:
                l[0] = l[0].replace("$","")
                if len(l[0]) != 0:
                    with open("notes/"+l[0], 'w') as f:
                        for k in l[1:]:
                            f.write(k)
                            f.write("\n")
                    with open(".cache.txt","w") as f:
                        f.write("notes/"+l[0])
                        f.close()
        else:
            with open(self.fn, 'w') as f:
                for k in l:
                    f.write(k)
                    f.write("\n")

    def handle_edit_mode(self):
        self.stacked_widget.setCurrentWidget(
            self.markdown_viewer
            if self.edit_action.isChecked()
            else self.markdown_editor
        )
        if self.stacked_widget.currentWidget() == self.markdown_viewer:
            self.markdown_viewer.setMarkdown(self.markdown_editor.toPlainText())

    def open_file(self):
        name = QFileDialog.getOpenFileName(self, 'Open File')
        self.fn = name[0]
        file = open(name[0], 'r')
        with file:
            text = file.read()
            self.markdown_editor.setText(text)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainWindow()
    w.resize(800, 600)
    w.show()

    sys.exit(app.exec())
