from win32file import CreateFile, SetFileTime, CloseHandle,GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
import zipfile
import os
import schedule
import time
import multiprocessing
import json
import shutil

with open("config.json",'r')as f:
    myconfig=json.load(f)

myconfig=myconfig["Avorion"]
save_folder = os.path.dirname(myconfig['save_path'])
back_folder=myconfig.get("back_folder")

def backup(name):
    starttime = time.time()

    f = zipfile.ZipFile(name, 'w', zipfile.ZIP_STORED)
    for dirpath, dirnames, filenames in os.walk(myconfig['save_path']):
        dirpathrel = os.path.relpath(dirpath, save_folder)
        print(dirpathrel)
        for n in filenames:
            try:
                f.write(os.path.join(dirpath, n), os.path.join(dirpathrel, n))
            except Exception as e:
                print(e)
    f.close()
    print(f"压缩用时{time.time() - starttime}")


def exact(filePath):
    starttime = time.time()
    unZf = zipfile.ZipFile(filePath, 'r')
    shutil.rmtree(myconfig['save_path'],ignore_errors=True)
    time.sleep(0.1)
    # os.makedirs(save_folder, exist_ok=True)
    # unZf.extractall(path=save_folder,members=unZf.namelist())


    for name in unZf.namelist():

        unZfTarge = os.path.join(save_folder, name)
        dirname = os.path.dirname(unZfTarge)
        os.makedirs(dirname, exist_ok=True)
        with open(unZfTarge, 'wb') as f:
            f.write(unZf.read(name))
        fh = CreateFile(unZfTarge, GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)
        #伪造写入时间
        createtime = unZf.getinfo(name).date_time
        time_formated = time.strptime(str(createtime), "(%Y, %m, %d, %H, %M, %S)")
        time_win = Time(time.mktime(time_formated))
        SetFileTime(fh,time_win,time_win,time_win)
    unZf.close()
    print(f"解压用时{time.time() - starttime}")


def get_create_time(filename):
    create_time = os.path.getmtime(os.path.join(back_folder, filename))
    return (create_time, filename)


def get_can_used():
    backup_set = set()
    back_list = list(filter(lambda x: "pythonbackup" in x, os.listdir(back_folder)))
    for filename in back_list:
        backupNum = filename.replace("pythonbackup", '').replace('.zip', '')
        try:
            backup_set.add(int(backupNum))
        except:
            pass
    for a in range(myconfig["back_num"]):
        if a not in backup_set:
            return a
    back_list = list(map(get_create_time, back_list))
    back_list.sort(key=lambda x: x[0])
    print(back_list)
    can_use_filename = back_list[0][1]
    return int(can_use_filename.replace("pythonbackup", '').replace('.zip', ''))


def do_back():
    id = get_can_used()
    backup(os.path.join(back_folder, f'pythonbackup{id}.zip'))
    print('finish')


def get_last_file():
    backup_set = set()
    back_list = list(filter(lambda x: "pythonbackup" in x, os.listdir(back_folder)))
    back_list = list(map(get_create_time, back_list))
    back_list.sort(key=lambda x: 0 - x[0])
    print(back_list)
    can_use_filename = back_list[0][1]
    return int(can_use_filename.replace("pythonbackup", '').replace('.zip', ''))


def do_reback():
    id = get_last_file()
    print("解压"+str(id))
    exact(os.path.join(back_folder, f'pythonbackup{id}.zip'))


def back_Thread(quit):
    print("开始备份")
    schedule.every(myconfig["back_minutes"]).minutes.do(do_back)
    while quit.value == 0:
        schedule.run_pending()
        time.sleep(1)
    quit.value = 0


message_quit = multiprocessing.Value("B", 0)
threads: multiprocessing.Process = multiprocessing.Process(target=back_Thread, args=(message_quit,))


def start_back():
    global threads
    if threads and not threads.is_alive():
        threads.start()
        return True
    return False


def stop_back():
    global threads
    global message_quit
    if threads and threads.is_alive():
        message_quit.value = 1
        threads.join()
        print("end")
        threads = multiprocessing.Process(target=back_Thread, args=(message_quit,))
        return True
    return False


if __name__ == "__main__":
    schedule.every(myconfig["back_minutes"]).minutes.do(do_back)
    # backup(os.path.join(save_folder,'pythonbackup1.zip'))
    # exact(os.path.join(save_folder,'pythonbackup1.zip'))
    while True:
        schedule.run_pending()
        time.sleep(1)
