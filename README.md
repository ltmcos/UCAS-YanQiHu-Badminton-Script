# UCAS

### fuck_ucas.py version=0.0.1
```
Python     3.8.5    
Pillow     8.4.0   
selenium   4.1.3  
ddddocr    1.1.0
```
 
1. 下载对应版本的edge驱动(https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/)
2. 在程序中设置driverfile_path,设置为msedgedriver.exe的绝对路径
3. 在程序中填写sep账号信息
4. 设置东区或者西区场地
5. 替换程序中xpath为目标时间的xpath  
 
### 注意：
(1)若要使用其他浏览器，只需要下载对应浏览的driver，并且把driver = webdriver.Edge换成对应的浏览器操作即可  
(2)运行程序的时候需要分辨率为1920x1080(1080p),缩放为100%,不然截图位置会出错   
(3)东区xpath 3->2，西区xpath 2->3  
(4)程序默认30分开抢,测试请注释掉相关代码    

  
    