import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from subprocess import call
from time import sleep
import os

class Watcher:
    DIRECTORY_TO_WATCH="."

    def __init__(self):
        self.observer = Observer()
    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print "Error"

        self.observer.join()


class Handler(PatternMatchingEventHandler):
    currentEvent = ""
    update=False
    def __init__(self):
        super(Handler, self).__init__(ignore_directories=True, ignore_patterns=[val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk('./.git')] for val in sublist]+['.DS_Store'])
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
        # Take any action here when a file is first created.
            print "Received event - %s." % event.src_path
            call('./bash.sh', shell=True)
            call('clear', shell=True)
            sleep(5)
        elif event.event_type == 'modified':
        # Taken any action here when a file is modified.
            print "Received event - %s." % event.src_path
            call('./bash.sh', shell=True)
            call('clear', shell=True)
            sleep(5)



if __name__ == '__main__':
    w = Watcher()
    w.run()
