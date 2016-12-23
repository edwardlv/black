# encoding: utf-8  
''''' 
@author: Techzero 
@email: techzero@163.com 
@time: 2014-5-18 下午5:06:29 
'''  
import cStringIO  
import getopt  
import time  
import urllib2  
import subprocess  
import sys  
  
from datetime import datetime  
  
MEDIA_PLAYER = 'C:/Program Files/Windows Media Player/wmplayer.exe'  
MEDIA_FILE = 'D:/notify.mp3'  
CHROME = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe'  
URL = 'http://detail.ju.taobao.com/home.htm?spm=608.2214381.2.1.SY0wVT&item_id=16761325430&id=10000002801432'  
NO_X11 = False  
  
def get_current_button():  
    '''''获取当前按钮状态'''  
    content = urllib2.urlopen(URL).read() #获取页面内容  
      
    buf = cStringIO.StringIO(content.decode('gbk').encode('utf8')) #将页面内容转换为输入流  
    current_button = None  
    for line in buf:  
        line = line.strip(' \n\r') #去掉回车换行  
          
        if line.find(r'<a href="#" class="extra  notice J_BuyButtonSub">开团提醒</a>') != -1:  
            current_button = '开团提醒'  
            break  
        elif line.find(r'<div class="main-box chance ">') != -1:  
            current_button = '还有机会'  
            break  
        elif line.find(r'<span class="out floatright">卖光了...</span>') != -1:  
            current_button = '卖光了'  
            break  
        elif line.find(r'<span class="out floatright">已结束...</span>') != -1:  
            current_button = '已结束'  
            break  
        elif line.find(r'<input type="submit" class="buyaction J_BuySubmit"  title="马上抢" value="马上抢"/>') != -1:  
            current_button = '马上抢'  
            break  
          
    buf.close()  
    return current_button  
  
  
def notify():  
    '''''发出通知并用Chrome打开秒杀页面'''  
    subprocess.Popen([MEDIA_PLAYER, MEDIA_FILE])  
    if not NO_X11:  
        subprocess.Popen([CHROME, URL])  
        print '打开页面'  
  
  
def monitor_button(interval, last):  
    '''''开始监视按钮'''  
    elapse = 0  
    while elapse < last:  
        current_button = get_current_button()  
  
        now = datetime.now()  
        print '%d-%d-%d %d:%d:%d - 现在按钮是 %s' % (now.year, now.month, now.day, now.hour, now.minute, now.second, current_button)  
  
        if current_button == '马上抢' or current_button == '还有机会':  
            print '赶紧抢购！'  
            notify()  
            break  
        elif current_button == '卖光了' or current_button == '已结束':  
            print '下次再试吧！'  
            break  
        else:  
            print '还没开始呢，再等等吧！'  
  
        time.sleep(interval)  
        elapse += interval  
  
  
def usage():  
    print ''''' 
usage: monitor_mac_price.py [options] 
 
Options: 
    -i interval: 30 seconds by default. 
    -l last: 1800 seconds by default. 
    -h: Print this usage. 
    -X: Run under no X11. 
'''  
  
if __name__ == '__main__':  
    try:  
        opts, args = getopt.getopt(sys.argv[1:], 'i:l:hX')  
    except getopt.GetoptError, err:  
        print str(err)  
        sys.exit(1)  
  
    interval = 0.1  
    last = 1800  
  
    for opt, val in opts:  
        if opt == '-i':  
            interval = int(val)  
        elif opt == '-l':  
            last = int(val)  
        elif opt == '-X':  
            NO_X11 = True  
        elif opt == '-h':  
            usage()  
            sys.exit()  
  
    monitor_button(interval, last)  