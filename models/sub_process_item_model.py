from typing import Callable, Any


class SubProcessItemModel:
    def __init__(self, pid: str, task: Callable[[...], Any] | Callable[[], Any], params: Any = None,
                 onComplete: Callable[..., Any] = None,
                 onError: Callable[..., Any] = None,
                 onStart: Callable[..., Any] = None,
                 description: str = None, name: str = None,
                 onStartParams: Any = None,
                 onErrorParams: Any = None,
                 onCompleteParams: Any = None,
                 ):
        """
        model for creating subprocesses.
        @param pid: the process id
        @param task: the task to be executed
        @param params: the parameters of the task
        @param onComplete: action to be done when the task is completed, (result)=>Any
        @param onError: action to be done when there is an error in executing the task, (error)=>Any
        @param onStart: action to be done when the task begins execution, ()=>Any
        @param description: the description of the process.
        @param name: short name of the process
        """
        self.__pid: str = pid
        self.__task: Callable[[...], Any] | Callable[[], Any] = task
        self.__params: Any = params
        self.__onComplete: Callable[[...], Any] = onComplete or self.__void
        self.__onError: Callable[[...], Any] = onError or self.__void
        self.__onStart: Callable[[...], Any] = onStart or self.__void
        self.__description: str = description
        self.__onStartParams: Any = onStartParams
        self.__onCompleteParams: Any = onCompleteParams
        self.__onErrorParams: Any = onErrorParams
        self.__name: str = name

    def name(self):
        return self.__name

    def description(self):
        return self.__description

    def pid(self):
        return self.__pid

    def task(self):
        return self.__task

    def params(self):
        return self.__params

    def onComplete(self):
        return self.__onComplete

    def onError(self):
        return self.__onError

    def onStart(self):
        return self.__onStart

    def startParams(self):
        return self.__onStartParams

    def errorParams(self):
        return self.__onErrorParams

    def completeParams(self):
        return self.__onCompleteParams

    @staticmethod
    def __void(value: Any = None):
        return value
