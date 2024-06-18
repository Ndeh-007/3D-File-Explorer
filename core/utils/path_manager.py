import os.path
from uuid import uuid4


class PathManager:
    def __init__(self):

        self.__id_idx_map: dict[str, int] = {}
        self.__idx_id_map: dict[int, str] = {}
        self.__cIdx: int = -1

        self.__paths: list[str] = []
        self.__currentPath: str = ""

    def updatePaths(self, path: str):

        if not os.path.exists(path):
            return

        self.__paths.append(path)
        idx = len(self.__paths) - 1
        pid = str(uuid4())

        self.__id_idx_map.update({pid: idx})
        self.__idx_id_map.update({idx: pid})

        self.__currentPath = path
        self.__cIdx = idx

    def previous(self):
        """
        gets the previous path from a target path
        :return:
        """
        pid = self.__idx_id_map.get(self.__cIdx)

        i = self.__id_idx_map.get(pid) - 1
        if i < 0:
            return self.__paths[self.__cIdx]
        return self.__paths[i]

    def next(self):
        """
        gets the next path from a target path.
        if it does not exist, it returns the provided path as the next
        :return:
        """
        pid = self.__idx_id_map.get(self.__cIdx)
        i = self.__id_idx_map.get(pid) + 1
        if i >= len(self.__paths):
            return self.__paths[self.__cIdx]
        return self.__paths[i]

    def reset(self):
        self.__paths.clear()
        self.__id_idx_map.clear()
        self.__idx_id_map.clear()

    def paths(self):
        """
        gets all the paths navigated through
        :return:
        """
        return self.__paths

    def currentPath(self):
        """
        gets the current path
        :return:
        """
        if self.__cIdx < 0:
            return None
        return self.__paths[self.__cIdx]

    def isLastPath(self, path: str):
        """
        checks if the path is the last path
        :param path:
        :return:
        """
        return self.__paths[-1] == path

    def isFirstPath(self, path: str):
        """
        checks if the first path is the provided path
        :param path:
        :return:
        """
        return self.__paths[0] == path

    def isOnlyPath(self):
        """
        checks if there is only one path in the manager. the first and last
        paths must be the same
        :return:
        """
        return len(self.__paths) == 1

    def isMiddlePath(self, path: str):
        """
        if the path is in the middle
        :param path:
        :return:
        """
        return not self.isFirstPath(path) and not self.isLastPath(path)
