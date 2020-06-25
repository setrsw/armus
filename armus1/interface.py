import tkinter as tk
import tkinter.messagebox  # 要使用messagebox先要导入模块
from db_model.notifications import *
notification=Notification()

window= tk.Tk()
window.title('学术信息爬取系统')
window.geometry('800x600') # 这里的乘号不是 * ，而是小写英文字母 x

#part1：显示默认学校网址
li  = ['华工软件学院 http://www.scut.edu.cn/sse/ \n',\
    '华工计算机学院 http://www.scut.edu.cn/cs/ \n',\
    '暨南大学信息学院 http://xxxy.jnu.edu.cn/ \n' ,\
    '华南农业大学信息学院 http://info.scau.edu.cn/news-cate-3.asp \n',\
    '北京大学信息学院 http://eecs.pku.edu.cn/ \n',\
    '清华大学交叉信息学院 http://iiis.tsinghua.edu.cn/zh/seminars/ \n',\
    '信息安全国家重点实验室 http://sklois.iie.cas.cn/tzgg/tzgg_16520/ \n',\
    '上海交通大学, http://www.cs.sjtu.edu.cn/NewNotice.aspx \n']
def hit_me():
    tkinter.messagebox.showinfo(title='默认学校网址', message=li) 

a1 = tk.Label(window,text='点击查看默认抓取的学术网址：',\
        fg='black',\
        font=('微软雅黑',12),width=100,height=2)
a1.pack()
btn1 = tk.Button(window, text='查看', bg='white', font=('Arial', 11), command=hit_me)
btn1.pack(fill=tk.BOTH)

#part2：选择排序方式
a3 = tk.Label(window,text='请选择排序方式：',\
        fg='black',\
        font=('微软雅黑',11),width=100,height=1)
a3.pack()
var = tk.StringVar()    # 定义一个var用来将radiobutton的值和Label的值联系在一起
# 其中variable=var, value='A'的意思是当鼠标选中了其中一个选项
# 把value的值A放到变量var中，然后赋值给variable
r1 = tk.Radiobutton(window, text='按举行时间排序', command=notification.orderbytime)
# s1 = notification.get_info_bytime()
r1.pack()
r2 = tk.Radiobutton(window, text='按通知发布时间来排序',command=notification.orderbyrelease)
# s1=notification.get_info_byrelease()
r2.pack()

#part3：讲座信息显示
a3 = tk.Label(window,text='学术讲座信息显示如下：',\
        fg='black',\
        font=('微软雅黑',12),width=100,height=2)
a3.pack(fill=tk.X)
#创建表格,注意：不要试图在一个主窗口中混合使用pack和grid
list1 = ['      标题', '报告人', '时间','地点','大学','通知链接']
s1 = [' ',' ',' ',' ',' ',' ']
notification.orderbytime()
s2 = notification.get_info_bytime()
print(s2)
#用insert()方法每次从文本框txt的尾部（END）开始追加文本。
def AddTitle():
    for i in range(6):
        s1[i]=str(list1[i])+'      '
        txt.insert(tk.END,s1[i])
txt=tk.Text(window)
txt.pack()
AddTitle()

def Addinfo():
    for info in s2:
        print(list(info.values()))
        list_info=list(info.values())
        for text in list_info:
            txt.insert(tk.END,str(text)+'   ')
txt=tk.Text(window)
txt.pack()
Addinfo()


#part4：备注部分
a4 = tk.Label(window,text='注：只抓取与信息安全，密码学相关的学术报告信息；只显示近一个月的公告',\
        fg='black',\
        font=('微软雅黑',11),width=100,height=2)
a4.pack(fill=tk.X)
btn2 = tk.Button(window, text='点击刷新列表',\
     font=('Arial', 10), \
     width=10, height=1,\
     command=hit_me)
btn2.pack()


#part5：添加新网址
a5 = tk.Label(window,text='点击添加新网址：',\
        fg='black',\
        font=('微软雅黑',11),width=100,height=2)
a5.pack(fill=tk.X,side=tk.LEFT)
btn2 = tk.Button(window, text='添加',\
     font=('Arial', 10), \
     width=10, height=1,)   #缺少command属性
btn2.pack(fill=tk.X,side=tk.LEFT)

window.mainloop()