from PySide6.QtCore import QObject, Signal


class SignalBus(QObject):
    onTasksChanged = Signal()
    onTaskCompleted = Signal(object)
    onTaskCreated = Signal(object)
    CreateSubprocess = Signal(object)
    CreateConsoleAlert = Signal(object)


signalBus = SignalBus()
