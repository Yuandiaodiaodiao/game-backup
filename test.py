
from win32file import CreateFile, SetFileTime, CloseHandle,GENERIC_READ, GENERIC_WRITE, OPEN_EXISTING
from pywintypes import Time
import time
fh = CreateFile("pythonbackup0.zip", GENERIC_READ | GENERIC_WRITE, 0, None, OPEN_EXISTING, 0, 0)

timex=time.localtime(time.time())
time2=time.mktime(timex)
createTimes = Time(time2)
print(createTimes)
SetFileTime(fh,createTimes,createTimes,createTimes)
CloseHandle(fh)