import tornado.ioloop
import tornado.web
import webbrowser
import json
from main import start_back,do_back,do_reback,stop_back
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")

class StartBackupHandler(tornado.web.RequestHandler):
    def post(self):
        js=json.loads(self.request.body)
        print(js)
        if js.get("start")==True:
            res=start_back()
            self.write("启动成功" if res else "已经启动备份")
        if js.get("start") == False:
            res = stop_back()
            self.write("关闭成功" if res else "关闭失败")
        if js.get("backUpNow")==True:
            do_back()
            self.write("备份成功")
        if js.get("reBack")==True:
            try:
                do_reback()
                self.write("回档成功")
            except Exception as e:
                self.write(f"回档失败\n{e}")




if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/startBackup",StartBackupHandler)
    ])
    application.listen(11451)
    webbrowser.open("http://localhost:11451")
    tornado.ioloop.IOLoop.current().start()