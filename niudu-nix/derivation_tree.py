from PySide2.QtWidgets import QTreeView
from PySide2.QtCore import QItemSelectionModel
from PySide2.QtGui import QStandardItem, QStandardItemModel
import subprocess
import json


def get_derivation(path):
    command = 'nix show-derivation ' + path
    process = subprocess.Popen(command.split(' '), stdout=subprocess.PIPE)
    (output, _) = process.communicate()
    _ = process.wait()
    if _ == 0:
        return json.loads(output.decode())
    return {}


def add_dict_item(key, val, parent):
    if type(val) is dict:
        child = QStandardItem('"'+key+'": { ... }')
        for key, val in val.items():
            add_dict_item(key, val, child)
    elif type(val) is list:
        child = QStandardItem('"'+key+'": [ ... ]')
        for item in val:
            child.appendRow(QStandardItem('"'+item+'"'))
    else:
        child = QStandardItem('"'+key+'": "'+str(val)+'"')
    parent.appendRow(child)


class DerivationView(QTreeView):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = QStandardItemModel()
        self.setModel(self.model)
        self.setHeaderHidden(True)
    
    def update(self, store_path):
        derivation_view = self
        derivation_model = self.model
        derivation_dict = get_derivation(store_path)
        derivation_model.removeRows(0, 1)
        for key, val in derivation_dict.items():
            add_dict_item(key, val, derivation_model.invisibleRootItem())
        derivation_view.expandAll()
        # Highlight output path matching selected store path
        derivation_item = derivation_model.invisibleRootItem().child(0)
        for i in range(derivation_item.rowCount()):
            if derivation_item.child(i).text() == 'outputs':
                outputs_item = derivation_item.child(i)
                for i in range(outputs_item.rowCount()):
                    path_item = outputs_item.child(i).child(0)
                    if path_item.text() == 'path: "' + store_path + '"':
                        print(path_item)
                        derivation_view.selectionModel().select(path_item.index(), QItemSelectionModel.ClearAndSelect)