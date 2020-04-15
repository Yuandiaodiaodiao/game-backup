from watchdog.events import FileSystemEventHandler,LoggingEventHandler
from watchdog.observers import Observer
import time
import os
import shutil
FILENAME='save_auto.sav'
print("输入监控文件名(默认为save_auto.sav 敲回车使用默认):\n")
i=input()
if len(i)>0:
    FILENAME=i
print(f"正在监控{FILENAME}")
class FileHandler(FileSystemEventHandler):

    def on_modified(self, event):
        try:
            _,filename=os.path.split(event.src_path)
            if filename==FILENAME:
                print(f"文件被修改了  {filename}")
                shutil.copy(src=FILENAME,dst=f"AUTOBACK{time.strftime('%m-%d %H %M %S',time.localtime(time.time()))}.sav")
                files=list(filter(lambda x: "AUTOBACK" in x, os.listdir('.')))
                files_with_time=list(map(lambda x:(x,os.path.getmtime(x)),files))
                files_with_time.sort(key=lambda x: 1-x[1])
                files_to_delete=files_with_time[20:]
                # print(files_to_delete)
                for file in files_to_delete:
                    print(f"清理旧存档{file}")
                    os.remove(file[0])
        except Exception as e:
            print(e)
            pass

event_handler = FileHandler()
observer = Observer()
observer.schedule(event_handler, ".")
observer.start()
while True:
    time.sleep(1)

