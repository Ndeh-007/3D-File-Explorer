from time import time
from uuid import uuid4

import qtawesome
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon

from core.structs import AlertCode, AlertType, AlertDisplayType
from core.variables.color import appColors


class BaseAlertModel:
    def __init__(self, title: str = None, description: str = None, location: str = None,
                 code: AlertCode = AlertCode.CUSTOM, alertType: AlertType = AlertType.EVENT,
                 createTime: int = time(), solution: str = None, pid: str = None,
                 displayType: AlertDisplayType = AlertDisplayType.NOTIFICATION):
        self.__title: str = title
        self.__description: str = description
        self.__location: str = location
        self.__code: AlertCode = code
        self.__type: AlertType = alertType
        self.__displayType: AlertDisplayType = displayType
        self.__time: int = createTime
        self.__solution: str = solution
        self.__id: str = pid or str(uuid4())

        self.__icon: QIcon = QIcon()
        self.__iconSize: QSize = QSize(16, 16)
        self.__alertName = "Event"
        self.__color = appColors.dark_rbg

        self.__configure()

    def __configure(self):
        if self.__type == AlertType.EVENT:
            self.__color = appColors.tertiary_rbg
            self.__icon = qtawesome.icon("msc.info", color=self.__color).pixmap(self.__iconSize)
            self.__alertName = "Event"
        if self.__type == AlertType.WARNING:
            self.__color = appColors.warning_rbg
            self.__icon = qtawesome.icon("msc.warning", color=self.__color).pixmap(self.__iconSize)
            self.__alertName = "Warning"
        if self.__type == AlertType.ERROR:
            self.__color = appColors.danger_rbg
            self.__icon = qtawesome.icon("msc.bug", color=self.__color).pixmap(self.__iconSize)
            self.__alertName = "Error"
        if self.__type == AlertType.SUCCESS:
            self.__color = appColors.success_rbg
            self.__icon = qtawesome.icon("msc.pass-filled", color=self.__color).pixmap(self.__iconSize)
            self.__alertName = "Success"

    # region getters
    def displayType(self):
        return self.__displayType

    def alertName(self):
        return self.__alertName

    def icon(self):
        return self.__icon

    def iconSize(self):
        return self.__iconSize

    def color(self):
        return self.__color

    def id(self):
        return self.__id

    def time(self):
        return self.__time

    def solution(self):
        return self.__solution

    def title(self):
        return self.__title

    def description(self):
        return self.__description

    def type(self):
        return self.__type

    def code(self):
        return self.__code

    def location(self):
        return self.__location

    # endregion

    # region setters

    def setSolution(self, value: str):
        self.__solution = value

    def setTime(self, value: int):
        self.__time = value

    def setTitle(self, value: str):
        self.__title = value

    def setDescription(self, value: str):
        self.__description = value

    def setType(self, value: AlertType):
        self.__type = value
        self.__configure()

    def setDisplayType(self, value: AlertDisplayType):
        self.__displayType = value

    def setCode(self, value: AlertCode):
        self.__code = value

    def setLocation(self, value: str):
        self.__location = value

    # endregion


class SuccessAlertModel(BaseAlertModel):
    def __init__(self, title: str = None, description: str = None, location: str = None,
                 code: AlertCode = AlertCode.CUSTOM, alertType: AlertType = AlertType.SUCCESS,
                 createTime: int = time(), solution: str = None, icon=None, color: str = appColors.success_rbg):
        super().__init__(title, description, location, code, alertType, createTime, solution)
        self.__icon = icon
        self.__color: str = color


class WarningAlertModel(BaseAlertModel):
    def __init__(self, title: str = None, description: str = None, location: str = None,
                 code: AlertCode = AlertCode.CUSTOM, alertType: AlertType = AlertType.WARNING,
                 createTime: int = time(), solution: str = None, icon=None, color: str = appColors.warning_rbg):
        super().__init__(title, description, location, code, alertType, createTime, solution)
        self.__icon = icon
        self.__color: str = color


class EventAlertModel(BaseAlertModel):
    def __init__(self, title: str = None, description: str = None, location: str = None,
                 code: AlertCode = AlertCode.CUSTOM, alertType: AlertType = AlertType.EVENT,
                 createTime: int = time(), solution: str = None, icon=None, color: str = appColors.secondary_rbg):
        super().__init__(title, description, location, code, alertType, createTime, solution)
        self.__icon = icon
        self.__color: str = color


class ErrorAlertModel(BaseAlertModel):
    def __init__(self, title: str = None, description: str = None, location: str = None,
                 code: AlertCode = AlertCode.CUSTOM, alertType: AlertType = AlertType.ERROR,
                 createTime: int = time(), solution: str = None, icon=None, color: str = appColors.danger_rbg):
        super().__init__(title, description, location, code, alertType, createTime, solution)
        self.__icon = icon
        self.__color: str = color
