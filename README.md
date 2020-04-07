# 存档备份器
## 使用方法
1.找到 config.json  server.exe 一个是配置文件 一个是主程序  
2.在config.json里配置 你的存档路径等等  
举例:  
```json
{
  "Avorion": {
    "save_path": "C:\\Users\\qq295\\AppData\\Roaming\\Avorion\\galaxies\\defaultgalaxy",
    "back_minutes": 5,
    "back_num": 5,
    "back_folder": "./"
  }
}
```
back_folder里面写./表示备份存在当前exe目录下  
其中defaultgalaxy(存档名) 是你的存档文件夹 文件夹里应该有players sectors等文件夹   
然后back_minutes指每隔N分钟备份一次 back_num指备份数量  
这样你的最大回滚时间就是back_minutes x back_num  
3.启动server.exe 程序将拉起你的浏览器打开一个ui页面 (不要挂梯子)  
暂时提供了三个功能  
立刻备份:将当前存档备份  
立刻回档:将最后保存的存档恢复到你的游戏存档中  
自动备份:按照你的配置文件进行自动备份  
三个按钮均有反馈 比如回档成功之类的
