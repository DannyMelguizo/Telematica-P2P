from datetime import datetime

def create_log_file():
    #Create or open the log file
    open('log.log', 'a').close()
    write_log_file("Server started", 1)

def get_type(type):
    if type == 1:
        return "INFO"
    elif type == 2:
        return "WARNING"
    elif type == 3:
        return "ERROR"
    else:
        return "UNKNOWN"

def write_log_file(message, type=None):

    ctime = datetime.now()

    #Format the date: yyyy-mm-dd hh:mm:ss
    ctime = ctime.strftime("%Y-%m-%d %H:%M:%S")

    with open('log.log', 'a') as file:
            
        if type:
            _type = get_type(type)
            file.write(f"[{ctime}] {_type}: {message}\n")
        else:
            file.write(f"[{ctime}] {message}\n")