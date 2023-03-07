from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    #def on_any_event(self, event):
    #    print(event.event_type, event.src_path)

    def on_created(self, event):
        print("file Created", event.src_path)
        print(event.src_path.strip())
        #if((event.src_path).strip() == r".\test.xml"):
        #    print("Execute your logic here!")
        #else:
        #    print("here: ", (event.src_path).strip())

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, path='.', recursive=False)
observer.start()


while True:
    try:
        pass
    except KeyboardInterrupt:
        observer.stop()