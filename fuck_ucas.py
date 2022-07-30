import ddddocr
from time import sleep
from selenium import webdriver
from PIL import Image
import datetime

def global_para():
    # global parameter  
    global user, passwd, driverfile_path, save_path
    global area, area_path
    user="your_ucas_email"
    passwd = "your_password"
    driverfile_path = 'D:\\coding\\python\\edgedriver_win64\\msedgedriver.exe'   # 这里最好用绝对路径
    save_path = '.'       #图片存放位置,用.的时候记得用shell运行
    area = 1     # 1 是西区，2是东区
    if area == 1:
        area_path = "https://ehall.ucas.ac.cn/v2/reserve/reserveDetail?id=6"      # 西区
    elif area == 2:
        area_path = "https://ehall.ucas.ac.cn/v2/reserve/reserveDetail?id=14"     # 东区
# 运行程序的时候需要分辨率为1920x1080(1080p),缩放为100%,不然截图位置会出错
#-----------------------------------------get ocr 
def get_ocr(filepath):       
    ocr = ddddocr.DdddOcr()
    with open(filepath, 'rb') as f:
        image = f.read()
    res = ocr.classification(image)
    return res

'''
Developers
------------------------
Li Tianming
Institue of Physics, CAS
2022.4.6
------------------------
Cao Zhendong
Institue of Physics, CAS
2022.4.6

'''

def get_captcha(imgelement):
    driver.save_screenshot(save_path + '\\printscreen.png')
    location = imgelement.location
    size = imgelement.size  # 获取验证码的长宽
    rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
          int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标
    i = Image.open(save_path + '\\printscreen.png')  # 打开截图
    frame4 = i.crop(rangle)  # 使用Image的crop函数，从截图中再次截取我们需要的区域
    frame4.save(save_path + '\\save.png') #保存我们接下来的验证码图片 进行打码
    res = get_ocr(save_path + '\\save.png')
    return res

def login(user,passwd):
    # driver = webdriver.Edge(executable_path=driverfile_path)
#----------------------------------------login
    driver.get("http://sep.ucas.ac.cn/")
    driver.maximize_window() 
    driver.find_element_by_xpath("/html/body/div/section/div[2]/div/div[1]/div/div[1]/div/form[2]/div[1]/div/div/div[1]/input").send_keys(user)
    driver.find_element_by_xpath("/html/body/div/section/div[2]/div/div[1]/div/div[1]/div/form[2]/div[1]/div/div/div[2]/input").send_keys(passwd)
#--------------------------------------------------------------------------
    try:
        imgelement = driver.find_element_by_xpath("/html/body/div/section/div[2]/div/div[1]/div/div[1]/div/form[2]/div[1]/div/div/div[3]/img")
        res = get_captcha(imgelement)
        driver.find_element_by_xpath("/html/body/div/section/div[2]/div/div[1]/div/div[1]/div/form[2]/div[1]/div/div/div[3]/input").send_keys(res)
        driver.find_element_by_xpath("/html/body/div/section/div[2]/div/div[1]/div/div[1]/div/form[2]/div[3]/div/div/button").click()
    except:
        driver.find_element_by_xpath("/html/body/div/section/div[2]/div/div[1]/div/div[1]/div/form[2]/div[3]/div/div/button").click()
#-------------------------------------------------------

#-------------------------------------------------------main
global_para()    #读取全局变量
time_now =datetime.datetime           # 读取时间模块
driver = webdriver.Edge(executable_path=driverfile_path)
#----------------------------------------login
login(user,passwd)
#---------------------------------------------------------------
driver.find_element_by_xpath("/html/body/div[2]/ul/li[1]/a[3]/img").click()         # 网上办事大厅
driver.get("https://ehall.ucas.ac.cn/v2/reserve/hallView?id=7")
#--------------------------------------------------------------------
while time_now.now().minute != 30:
    sleep(0.1)
# sleep(0.5)
#---------------------------------------------------------------------
driver.get(area_path)
#--------------------------------------------------------------------因为需要点时间才能弹出窗口，所以不能立马点确认
while(True):
    try:
        driver.find_element_by_xpath("/html/body/div[3]/div/div[3]/button").click()          # 出现场地列表
        # sleep(2)
        break
    except:
        continue
#----------------------------------------------------------------------场地选择子函数
def xpath_generate(div_num, time_num, Type='span'):
    if Type == 'span':
        return "/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div["+str(time_num)+"]/div["+str(div_num)+"]/div/div/span/span"
    elif Type == 'div':
        return "/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div["+str(time_num)+"]/div["+str(div_num)+"]/div/div"
    elif Type == 'div-span':
        return "/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div["+str(time_num)+"]/div["+str(div_num)+"]/div/span"
    else:
        return "/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div["+str(time_num)+"]/div["+str(div_num)+"]/div"

def try_place(div_num, num):
    try:
        driver.find_element_by_xpath(xpath_generate(div_num, num, 'div-span')).click()
        print('div-span')
    except:
        try:
            driver.find_element_by_xpath(xpath_generate(div_num, num, 'none')).click()
            print('none')
        except:
            driver.find_element_by_xpath(xpath_generate(div_num, num, 'span')).click()
            print('span')
    print(num)
#----------------------------------------------------------------------选择时段（包括日期）
#点两次后一天。。。(作者表示日了狗)
while(True):
    try:
        try_place(1,3)
        break
    except:
        continue
driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[1]/button[3]").click()
driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[1]/button[3]").click()
#--------------------------------------------------------------
#东区 3 号场 7-9点   for test 
# try:
#     driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[14]/div[2]/div").click()
# except:
#     driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[14]/div[2]/div/div/span/span").click()
# try:
#     driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[15]/div[2]/div").click()
# except:
#     driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[15]/div[2]/div/div/span/span").click()
#---------------------------------------------------------------------
#---------------------------------------------------------------------
# for test 4.10 
# 西区 2号场 15：00 - 17：00
'''
reference data (access span)
#/html/body/div[1]/div[3]/div/div[2]/div[2]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/div[16]/div[3]/div/div/span/span
'''
# try:
#     driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[12]/div[3]/div/div").click()
# except:
#     driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[12]/div[3]/div/div/span/span").click()
# try:
#     driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[14]/div[3]/div/div").click()
# except:
#     driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[14]/div[3]/div/div/span/span").click()

# ----------------------------------------------------

# for test 4.12
# 西区 1号场 14:00-16:00/14:30-16:30
# div_num: 1; time_num, 14:00-10, 14:30-11, 15:00-12, 15:30-13
# try_place(1,3)
# try_place(1,4)
# /html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[3]/div[1]/div
# /html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[3]/div[1]/div/span
# /html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[3]/div[1]/div/div/span/span

# try:
#     try_place(1,9)
#     try_place(1,11)
#     print('13:30-15:30')
# except:
#     try:
#         try_place(1,10)
#         try_place(1,12)
#         print('14:00-16:00')
#     except:
#         try_place(1,11)
#         try_place(1,13)
#         print('14:00-16:00')

# try_place(1,10)
# try_place(1,12)
# try_place(1,11)
# try_place(1,13)

#/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[12]/div[2]/div/div
#/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[14]/div[2]/div/div
#--------------------------------------------------------------------
# 4.9抢4.11 东区
#/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[4]/div[3]/div  3号场9-10
#/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[5]/div[3]/div  3号场10-11
#------------------------------------------------------------------
# reference span x path (experimental data) 东区
#/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[14]/div[2]/div/div/span/span
#/html/body/div[1]/div[2]/div/div[3]/div/div[1]/div[1]/div[2]/div/div/div[2]/div/div[14]/div[2]/div/div/span/span

#----------------------------------------------------------------确定预约时候的验证码
driver.save_screenshot(save_path + '\\printscreen.png')
imgelement = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[2]/img")
res = get_captcha(imgelement)
driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/div[2]/div[2]/input").send_keys(res)
#driver.find_element_by_xpath("/html/body/div[1]/div[2]/div/div[3]/div/div[2]/div/a").click()        #  确定预约

print("FUCK UCAS")