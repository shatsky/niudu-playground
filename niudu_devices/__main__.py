#!/usr/bin/env python3

import sys
from PySide2 import QtWidgets, QtGui

# "Must construct a QApplication before a QWidget"
# i. e. before importing stuff that instantiates QWidget
app = QtWidgets.QApplication(sys.argv)

from .ui_devices_view import DevicesView
from .ui_device_props_view import device_props_tree_widget


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        menu_bar = self.menuBar()
        tree_menu = QtWidgets.QMenu('Tree', self)
        self.action_set_view_kernel_device_entries = tree_menu.addAction('View - Kernel device entries')
        self.action_set_view_kernel_device_entries.triggered.connect(self.set_view_kernel_device_entries__handler)
        self.action_set_view_kernel_device_entries_by_subsystem = tree_menu.addAction('View - Kernel device entries, by subsystem')
        self.action_set_view_kernel_device_entries_by_subsystem.triggered.connect(self.set_view_kernel_device_entries_by_subsystem__handler)
        self.action_set_view_kernel_device_entries_by_seat = tree_menu.addAction('View - Kernel device entries, by seat')
        self.action_set_view_kernel_device_entries_by_seat.triggered.connect(self.set_view_kernel_device_entries_by_seat__handler)
        self.action_set_view_kernel_device_entries_by_iommu_group = tree_menu.addAction('View - Kernel device entries, by IOMMU group')
        self.action_set_view_kernel_device_entries_by_iommu_group.triggered.connect(self.set_view_kernel_device_entries_by_iommu_group__handler)
        self.action_set_view_kernel_device_entries_by_iommu_group = tree_menu.addAction('View - Hardware locality')
        self.action_set_view_kernel_device_entries_by_iommu_group.triggered.connect(self.set_view_hardware_locality__handler)
        action = tree_menu.addAction(QtGui.QIcon.fromTheme('view-refresh'), 'Reload')
        action.triggered.connect(self.reload__handler)
        action = tree_menu.addAction('Go to last added device')
        action.triggered.connect(self.last_added_device__handler)
        menu_bar.addMenu(tree_menu)
        menu = QtWidgets.QMenu('Current', self)
        self.action_back = menu.addAction(QtGui.QIcon.fromTheme('go-previous'), 'Back')
        self.action_back.setEnabled(False)
        self.action_back.triggered.connect(self.back__handler)
        self.action_forward = menu.addAction(QtGui.QIcon.fromTheme('go-next'), 'Forward')
        self.action_forward.setEnabled(False)
        self.action_forward.triggered.connect(self.forward__handler)
        menu_bar.addMenu(menu)
        
        toolbar = QtWidgets.QToolBar()
        self.toolbar_action_back = toolbar.addAction(QtGui.QIcon.fromTheme('go-previous'), 'Back')
        self.toolbar_action_back.setEnabled(False)
        self.toolbar_action_back.triggered.connect(self.back__handler)
        self.toolbar_action_forward = toolbar.addAction(QtGui.QIcon.fromTheme('go-next'), 'Forward')
        self.toolbar_action_forward.setEnabled(False)
        self.toolbar_action_forward.triggered.connect(self.forward__handler)
        self.addToolBar(toolbar)

        self.devices_view = DevicesView()
        self.devices_view.history_signal.connect(self.devices_view__history_signal__handler)

        layout_base = QtWidgets.QHBoxLayout()
        layout_base.addWidget(self.devices_view)
        layout_base.addWidget(device_props_tree_widget)        
        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout_base)
        self.setCentralWidget(central_widget)
        
        self.showMaximized()
    
    def reload__handler(self, action):
        self.devices_view.model.reload()
    
    def last_added_device__handler(self, action):
        from ui_devices_view import last_added_device, set_current_device
        set_current_device(last_added_device)
    
    def back__handler(self, action):
        self.devices_view.history_back()
    
    def forward__handler(self, action):
        self.devices_view.history_forward()
    
    def devices_view__history_signal__handler(self, history_back_flag, history_forward_flag):
        self.action_back.setEnabled(history_back_flag)
        self.action_forward.setEnabled(history_forward_flag)
        self.toolbar_action_back.setEnabled(history_back_flag)
        self.toolbar_action_forward.setEnabled(history_forward_flag)
    
    def set_view_kernel_device_entries__handler(self):
        current_device_path = self.devices_view.get_current_device()
        from .ui_devices_view import DevicesModel
        self.devices_view.setModel(DevicesModel())
        self.devices_view.reload()
        if current_device_path is not None:
            self.devices_view.set_current_device(current_device_path)

    def set_view_kernel_device_entries_by_subsystem__handler(self):
        current_device_path = self.devices_view.get_current_device()
        from .ui_devices_view import DevicesBySubsystemModel
        self.devices_view.setModel(DevicesBySubsystemModel())
        self.devices_view.reload()
        if current_device_path is not None:
            self.devices_view.set_current_device(current_device_path)

    def set_view_kernel_device_entries_by_seat__handler(self):
        current_device_path = self.devices_view.get_current_device()
        from .ui_devices_view import DevicesBySeatModel
        self.devices_view.setModel(DevicesBySeatModel())
        self.devices_view.reload()
        if current_device_path is not None:
            self.devices_view.set_current_device(current_device_path)

    def set_view_kernel_device_entries_by_iommu_group__handler(self):
        current_device_path = self.devices_view.get_current_device()
        from .ui_devices_view import DevicesByIOMMUGroupModel
        self.devices_view.setModel(DevicesByIOMMUGroupModel())
        self.devices_view.reload()
        if current_device_path is not None:
            self.devices_view.set_current_device(current_device_path)
    
    def set_view_hardware_locality__handler(self):
        current_device_path = self.devices_view.get_current_device()
        from .ui_devices_view import HwLocModel
        self.devices_view.setModel(HwLocModel())
        self.devices_view.reload()
        if current_device_path is not None:
            self.devices_view.set_current_device(current_device_path)


print('imported')
window = MainWindow()
app.exec_()