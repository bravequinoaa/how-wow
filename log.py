import os
import datetime

log_path = './logs/'
log_file = 'how-wow'
log_file_path = log_path + log_file


class Log:
    def __init__(self):
        self.log_file = self.__start_logger()
    

    def __start_logger():
        global log_file_path
        l = None
        if os.path.exists(log_file_path):
            l = open(log_file_path, 'a')
        else:
            l = open(log_file_path, 'w')

        return l
        
        
    def __check_time_stamp(self):
        os.stat(log_file_path)

    def __get_time_stamp(self):
        return datetime.now()


    def __del__(self):
        self.log_file.close()

    
    def info(self, msg):
        self.log_file.writeln(f'{self.__get_time_stamp()}: {msg}')