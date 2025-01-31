from qgis.PyQt import QtWidgets, uic
from qgis.PyQt.QtCore import Qt, pyqtSignal, QEvent
from qgis.core import QgsProject


class CheckableComboBox(QtWidgets.QComboBox):
    selectionChanged = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setEditable(True)
        self.lineEdit().setReadOnly(True)
        self._selected_items = []

        # Connect signals
        self.model().dataChanged.connect(self.update_text)
        self.lineEdit().installEventFilter(self)

    def addItem(self, text, userData=None):
        super().addItem(text, userData)
        item = self.model().item(self.count() - 1, 0)
        item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
        item.setCheckState(Qt.Unchecked)

    def addItems(self, texts):
        for text in texts:
            self.addItem(text)

    def eventFilter(self, widget, event):
        if widget == self.lineEdit():
            if event.type() == QEvent.MouseButtonRelease:
                self.showPopup()
                return True
        return False

    def update_text(self):
        self._selected_items = []
        texts = []

        for i in range(self.count()):
            item = self.model().item(i, 0)
            if item.checkState() == Qt.Checked:
                texts.append(item.text())
                self._selected_items.append(i)

        text = ", ".join(texts) if texts else "Select layers..."
        self.lineEdit().setText(text)
        self.selectionChanged.emit(self._selected_items)

    def get_selected_items(self):
        return self._selected_items
