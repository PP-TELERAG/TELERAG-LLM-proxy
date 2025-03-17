import os
from datetime import datetime

from Source.Services.Singleton import Singleton





class Logger(metaclass=Singleton):

    def __init__(self, log_dir, debug=False):
        self.__log_dir = log_dir
        self.__log_history = ""
        self.__debug = debug

    def log_message(self, message, level=1):
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        msg: str
        if level < 1:
            return

        if level == 1:
            if self.__debug:
                msg =  f"[INFO/DEBUG]: {message}"
            else:
                msg = f"[INFO]: {message}"
            col = "\033[32m"
        if level == 2:
            if self.__debug:
                msg = f"[WARN/DEBUG]: {message}"
            else:
                msg = f"[WARN]: {message}"
            col = "\033[33m"
        if level == 3:
            if self.__debug:
                msg = f"[ERROR/DEBUG]: {message}"
            else:
                msg = f"[ERROR]: {message}"
            col = "\033[31m"
        if level == 4:
            if self.__debug:
                msg = f"[FATAL/DEBUG]: {message}"
            else:
                msg = f"[FATAL]: {message}"
            col = "\033[31m"
        msg += " - " + time

        print(col + msg + "\033[0m")
        self.__log_history += msg + '\n'


    def end_logging(self):
        if os.path.exists(self.__log_dir + "latest.txt"):
            os.remove(self.__log_dir + "latest.txt")
        if os.path.exists(self.__log_dir + "latest-debug.txt"):
            os.remove(self.__log_dir + "latest-debug.txt")

        if self.__debug:
            with open(self.__log_dir + "latest-debug.txt", 'a') as file:
                file.write(self.__log_history)
        else:
            with open(self.__log_dir + "latest.txt", 'w') as file:
                file.write(self.__log_history)











