import traceback
from typing import Any, Callable

from PySide6.QtCore import QObject, QThread, Signal

from core.signal_bus import signalBus
from models.alert_models import WarningAlertModel, EventAlertModel
from models.sub_process_item_model import SubProcessItemModel


class ProcessThread(QThread, QObject):
    threadStarted = Signal(str)
    threadFinished = Signal(str)

    def __init__(self, pid: str, task: Callable[[...], Any] | Callable[[], Any], params: Any = None,
                 description: str = None, name: str = None):
        super().__init__()

        self.__result: Any = None
        self.__error: Any = None
        self.__errorOccurred: bool = False

        self.__pid = pid
        self.__task: Callable[[...], Any] | Callable[[], Any] = task
        self.__params: Any = params
        self.__description: str = description
        self.__name: str = name

        self.__configure()

    def __configure(self):
        self.started.connect(self.__handleThreadStarted)
        self.finished.connect(self.__handleThreadFinished)

    # region event handlers
    def __handleThreadStarted(self):
        self.threadStarted.emit(self.__pid)

    def __handleThreadFinished(self):
        self.threadFinished.emit(self.__pid)

    # endregion

    # region override

    def run(self) -> None:
        try:
            if self.__params is not None:
                self.__result = self.__task(self.__params)
            else:
                self.__result = self.__task()
            self.__errorOccurred = False
        except Exception as e:
            self.__error = e
            self.__errorOccurred = True
            print(traceback.format_exc())

    # endregion

    # region getters

    def name(self):
        return self.__name

    def description(self):
        return self.__description

    def result(self):
        return self.__result

    def errorOccurred(self):
        return self.__errorOccurred

    def error(self):
        return self.__error

    def pid(self):
        return self.__pid

    # endregion


class ProcessManger:
    def __init__(self):
        self.__threads: dict[str, ProcessThread] = {}
        self.__processModels: dict[str, SubProcessItemModel] = {}

        self.__connectSignals()

    def initialize(self):
        pass

    # region getters

    def threads(self):
        """
        gets all the active threads and returns to the user
        @return:
        """
        return self.__threads

    def processModels(self):
        """
        gets all the current process models and returns them
        @return:
        """
        return self.__processModels

    # endregion

    # region - event handlers
    def handleThreadStarted(self, pid: str):
        p = self.__processModels.get(pid)
        if p is not None:
            sTask = p.onStart()
            sTask(p.startParams())

    def handleThreadFinished(self, pid: str):
        p = self.__processModels.get(pid)
        if p is None:
            return

        thread = self.__threads.get(pid)
        if thread is None:
            return thread

        # if error occurred during execution, handle and return
        if thread.errorOccurred():
            eTask = p.onError()
            eTask(thread.error())
        else:
            cTask = p.onComplete()
            cTask(thread.result())

        self.purge(pid)

        signalBus.onTasksChanged.emit()
        signalBus.onTaskCompleted.emit(thread)

    # endregion

    # region - workers

    def kill(self, pid: str):
        """
        kills the process with target id
        @param pid:
        @return:
        """
        thread = self.__threads.get(pid)
        if thread is None:
            alert = WarningAlertModel(
                title="Subprocess Not Found",
                description="Tried to terminate a process with 'pid' that was not found",
                location="From the sub process manager. The trigger command mostly likely came from an api call made in the task explorer.",
                solution="Unknown. Issue occurred because processes were created with the same process id. The actual subprocess may still be running in the background.",
            )
            signalBus.CreateConsoleAlert.emit([alert])
            return

        # we will use return code 1 to show that the process was user terminated
        thread.terminate()
        thread.wait(1)

    def launch(self, subprocess: SubProcessItemModel, override: bool = False):
        """
        launches a new subprocess.
        if overridden, it will kill old process with same id and run the new one
        @param subprocess:
        @param override:
        @return:
        """

        if override:
            if self.processExists(subprocess):
                self.kill(subprocess.pid())
        else:
            if self.processExists(subprocess):
                return self.throwProcessAlreadyRunning(subprocess)

        self.__processModels.update({subprocess.pid(): subprocess})

        thread = ProcessThread(subprocess.pid(), subprocess.task(), subprocess.params(), subprocess.description(),
                               subprocess.name())
        thread.threadFinished.connect(self.handleThreadFinished)
        thread.threadStarted.connect(self.handleThreadStarted)
        self.__threads.update({subprocess.pid(): thread})

        thread.start()
        signalBus.onTasksChanged.emit()
        signalBus.onTaskCreated.emit(thread)

    def purge(self, pid: str):
        """
        removes the target pid from memory
        @param pid:
        @return:
        """
        # remove the process
        self.__threads.pop(pid)
        self.__processModels.pop(pid)

    # endregion

    # region - connect signals
    def __connectSignals(self):
        signalBus.CreateSubprocess.connect(self.launch)

    # endregion
    def processExists(self, subprocess):
        """
        checks if the process is already running
        @param subprocess:
        @return:
        """
        return subprocess.pid() in list(self.__threads.keys())

    @staticmethod
    def throwProcessAlreadyRunning(subprocess):
        """
        creates and emits an error alert stating that the desired process is already running
        @param subprocess:
        @return:
        """
        print(f"Process with id '{subprocess.pid()}' called '{subprocess.name()}' already running")
        alert = EventAlertModel(
            title=f"Duplicate Processes",
            description=f"Process {subprocess.name()} is already running.",
            location="Process Manager",
            solution="Kill Previous process before running again",
        )
        signalBus.CreateConsoleAlert.emit([alert])
        return
