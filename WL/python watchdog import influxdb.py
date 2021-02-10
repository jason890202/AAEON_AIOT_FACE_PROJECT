import os, sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from influxdb import InfluxDBClient
from ExportCsvToInflux import ExporterObject
client = InfluxDBClient('192.168.0.10', 8086,'Little_YY', 'Little_YY', 'yolo') #初始化連線設定 
class FileEventHandler(FileSystemEventHandler):
    def __init__(self):
        FileSystemEventHandler.__init__(self)

    def on_modified(self, event):
        if not event.is_directory:
            path = os.path.realpath(event.src_path)
            print("修改的文件> {0}".format(path))
            ext = os.path.splitext(path)[1]
            if ext == '.txt':
                txt = open(path).read()
                print("檔案內容>")
                print(txt)
                data = [
                    {
                        "measurement": "Temperature",
                        "tags": {
                            "yolo": txt
                        },
                        "fields": {
                            "tem": 123
                        }
                    }
                ] # 資料
                client.write_points(data) # 寫入數據，同時創建表
                
                
                
                
if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = FileEventHandler()
    observer = Observer()
    observer.schedule(event_handler, path='C:\\Users\\CSIE_AIOT_03\\Desktop\\testdata\\exp2\\labels', recursive=True)
    observer.start()
    print('監控中：%s' % os.path.realpath(path))
    print('Ctrl-C 退出!')
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
