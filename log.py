# log.py

class Log:
    
    def __init__(self):
        self.log = "" # string to hold the messages
        self.count = 0 # number of messages, used to id each row
        
    # sender is the name of the subsystem sending the message
    # receiver is the name of the subsystem receiving the message
    # message is the message sent
    def log_message(self, sender, receiver, message):
        self.count += 1
        self.log += f'{str(self.count):<4}' + ' | '+ sender + ' -> ' + receiver + ' | ' + message + '\n'
        
    # return string of the message log
    def to_string(self):
        return self.log
    
    # export txt file of message log
    def to_txt(self, filename = 'log_output.txt'):
        f = open(filename,'w')
        f.write(self.log)
        f.close()