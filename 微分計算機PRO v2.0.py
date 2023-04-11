#微分計算機PRO V2.0  20230124

#導入模組
import numpy as np #numpy模組
import matplotlib.pyplot as plt #繪圖模組
from sympy.abc import _clash1,x,y #sympy表達式轉換、變數
from sympy.plotting import plot3d #sympy繪圖
from sympy import Symbol,diff,sympify,pprint,pretty,parse_expr,Poly,plot #sympy計算套件
import warnings #設定圖畫不出來警告

#導入使用者設定、歷史紀錄、函數
def data_access():
  global setup
  f = open("setting.txt", mode="r", encoding="utf-8")
  setup = f.read().splitlines()
  f.close()
  global history
  f = open("history.txt", mode="r", encoding="utf-8")
  history = f.read().splitlines()
  f.close()
  global calc_type
  f = open("calc_type.txt", mode="r", encoding="utf-8")
  calc_type = f.read().splitlines()
  f.close()
  if setup[2] == "1": #自動清除歷史紀錄
    print("\n∣＜自動清除歷史紀錄已開啟＞∣")
  if setup[5] == "1": #無痕模式
    print("\n∣＜無痕模式已開啟＞∣")
  
#保存歷史紀錄函數
def save_history():
  f = open("history.txt", mode="w", encoding="utf-8")
  for save in history:
    print(save, file=f)
  f.close()
  f = open("calc_type.txt", mode="w", encoding="utf-8")
  for save in calc_type:
    print(save, file=f)
  f.close()

#顯示歷史紀錄函數
def show_history():
  x = Symbol('x')
  y = Symbol('y')
  print("\n歷史紀錄→")
  if len(history) == 0:
    print("\n#空白......#\n")
  else:
    if len(history)>int(setup[13]):
      for i in range (0,int(setup[13])):
        print("\n"+str(i+1)+". ")
        if (setup[4] == "1"): #漂亮輸出
          pprint(sympify(history[i], locals=_clash1), wrap_line = False)
        elif (setup[4] == "0"): #普通輸出
          print(str(history[i]))
    elif len(history)<=int(setup[13]):
      for i in range (len(history)):
        print("\n"+str(i+1)+". ")
        if (setup[4] == "1"): #漂亮輸出
          pprint(sympify(history[i], locals=_clash1), wrap_line = False)
        elif (setup[4] == "0"): #普通輸出
          print(str(history[i]))

#繪圖函數
def draw(z,t):
  if t == 1 or t == 2:
    plot((z,(x,(-1*eval(setup[1])),eval(setup[1]))),line_color=setup[3],xlabel='x',ylabel='y',title=z)
  elif t==3:
    expr = parse_expr(str(z))
    plot3d(expr, (x, -1*int(setup[1]), int(setup[1])), (y, -1*int(setup[1]), int(setup[1])), nb_of_points=350, xlabel='x-axis', ylabel='y-axis', zlabel='z-axis')

#計算微分、偏微分函數
def differential(f,t):
  try:
    warnings.filterwarnings('error')
    if (t==1 or t==2): #多項式微分、進階微分
      var=Symbol('x') #變數 x 指定為 SymPy Symbol
    elif (t==3): #偏微分
      var=input("\n請問要微分哪個變數\n→")
      var=Symbol(var)
    f=sympify(f, locals=_clash1) #將輸入轉換為 SymPy 表達式
    m=1 #多次微分次數
    if setup[10]=="1": #多次微分開
      if setup[11]=="1": #有預設值
        print("\n已套用預設多次微分次數→"+setup[12])
        m=int(setup[12])
      else:
        m=int(input("\n請輸入多次微分次數→"))
    f=diff(f,var,m) #計算f對var的微分(微分m次)
    print("\n計算結果:")
    if (setup[4]=="1"): #漂亮輸出
      pprint(f.simplify(),wrap_line=False)
    elif (setup[4]=="0"): #普通輸出
      print(str(f.simplify()))
    if (setup[0]=="1"): #自動繪圖
      draw(f.simplify(),t)
    if (setup[6]=="1"): #代入計算
      substitute(f,t)
    if (setup[5]=="0"): #保存歷史紀錄(無痕模式為關閉狀態)
      history.insert(0,f)
      calc_type.insert(0,eval(type))
      save_history()
  except SyntaxError:
    print("\n#請確定輸入之內容正確#\n")
  except ValueError:
    print("\n#請確定輸入之內容正確#\n")

#代入計算函式
def substitute(f,t):
  f=sympify(f, locals=_clash1)
  if t==1 or t==2:
    x=Symbol('x')
    if setup[7]=="1":
      x_value=setup[8]
      print("\n使用x代入計算預設值→"+x_value)
    else:
      x_value=input("\n請輸入x值→")
    if (setup[4]=="1"):
      print("→\n"+pretty(f.subs(x,x_value).simplify()))
    elif (setup[4]=="0"):
      print("→"+str(f.subs(x,x_value).simplify()))
  elif t==3:
    x=Symbol('x')
    y=Symbol('y')
    if setup[7]=="1":
      x_value=setup[8]
      y_value=setup[9]
      print("\n使用x代入計算預設值→"+x_value)
      print("使用y代入計算預設值→"+y_value)
    else:
      x_value=input("\n請輸入x值→")
      y_value=input("請輸入y值→")
    if (setup[4]=="1"):
      print("→\n"+pretty(f.subs(x,x_value).subs(y,y_value).simplify()))
    elif (setup[4]=="0"):
      print("→"+str(f.subs(x,x_value).subs(y,y_value).simplify()))

#開始使用
print("歡迎使用 微分計算機PRO V2.0")
while(1):
  data_access() # 導入歷史紀錄、設定
  number=[] #儲存輸入係數
  f="" #算式
  #模式選擇
  type=input("\n請選擇模式\n1=多項式微分\n2=進階微分\n3=偏微分\n4=其他功能\n5=設定\n6=進階微分函數表\n7=關於此程式\n8=離開\n→")
  if type=="1":
    #輸入最高次方&各項係數
    try:
      begin=int(input("\n請問你的最高次方數是多少?(僅能輸入正整數)\n→"))
      if begin<0:
        print("\n#請輸入正整數#\n")
      elif begin==0:
        f=0
        differential(f,1)
      elif begin>=1:
        print("請依序輸入各項係數")
        #輸入各項係數
        for i in range (0,begin+1):
          a=input("→")
          number.append(a)
        poly_numpy = np.poly1d(number)
        x = Symbol('x')
        poly_sympy = Poly(poly_numpy.coef, x)
        f = poly_sympy.as_expr()
        differential(f,1)
    except ValueError:
      print("\n#請輸入正整數#\n")
    except NameError:
      print("\n#請輸入正確數字#\n")
    except SyntaxError:
      print("\n#請輸入正確數字#\n")
      
  elif type=="2":
    f=input("\n請輸入完整算式(特殊函數可參考函數表):\n→")
    differential(f,2)

  elif type=="3":
    f=input("\n請輸入完整算式(特殊函數可參考函數表):\n→")
    differential(f,3)
    
  elif type=="4":
    function=input("\n請選擇功能\n1=查看歷史紀錄\n2=刪除指定歷史紀錄\n3=刪除全部歷史紀錄\n4=以歷史紀錄繪圖\n5=以歷史紀錄代入計算\n→")
    if function=="1":
      show_history()
    elif function=="2":
      show_history()
      if len(history)!=0:
        d=input("\n請問要刪除第幾項?\n→")
        try:
          if int(d)>0:
            popped=history.pop(int(d)-1)
            print("\n#已刪除#:",popped)
            show_history()
            save_history()
          else:
            print("\n#請輸入正確項數#\n")
        except ValueError:
          print("\n#請輸入正確項數#\n")
    elif function=="3":
      ask=input("\n確定刪除? 是:Y 否:N\n→")
      if ask=="Y" or ask=="y":
        history=[]
        calc_type=[]
        save_history()
        print("\n#已全部刪除#\n")
      else:
        print("\n#已取消刪除#\n")
    elif function=="4":
      show_history()
      if len(history)!=0:
        try:
          d=input("\n請問要將歷史紀錄第幾項繪圖?\n→")
          if int(d)>0:
            x=Symbol('x')
            y=Symbol('y')
            f=history[int(d)-1]
            draw(f,int(calc_type[int(d)-1]))
          else:
            print("\n#請輸入正確項數#\n")
        except ValueError:
          print("\n#請輸入正確項數#\n")
    elif function=="5":
      show_history()
      try:
        if len(history)!=0:
          d=int(input("\n請問要將歷史紀錄第幾項代入計算?\n→"))
          f=history[d-1]
          substitute(f,int(calc_type[d-1]))
      except IndexError:
        print("\n#請輸入正確項數#\n")
      except ValueError:
        print("\n#請輸入正確項數#\n")
    else:
      print("\n#請輸入正確數字#\n")
      
  elif type=="5":
    setting=input("\n請選擇要修改的設定\n1=自動繪圖設定\n2=繪圖範圍設定\n3=歷史紀錄自動清除設定\n4=繪圖線條顏色設定\n5=算式輸出設定\n6=無痕模式設定\n7-1=代入計算設定\n7-2=代入計算預設值設定\n8-1=多次微分設定\n8-2=多次微分預設值設定\n9=歷史紀錄顯示前n筆\n10=恢復預設設定\n→")
    if setting=="1":
      print("\n目前為:",setup[0])
      ask=input("\n1=開\n0=關\n→")
      if ask=="1" or ask=="0":
        setup[0]=ask
        print("\n#已修改#")
      else:
        print("\n#請輸入正確數字#")
    
    elif setting=="2":
      print("\n目前為:",setup[1])
      ask=input("\n調整範圍為(>0):\n→")
      try:
        if eval(ask)<=0:
          print("\n#請輸入正確數字#")
        else:
          setup[1]=eval(ask)
          print("\n#已修改#")
      except SyntaxError:
        print("\n#請輸入正確數字#")
    
    elif setting=="3":
      print("\n目前為:",setup[2])
      ask=input("\n1=開\n0=關\n→")
      if ask=="0" or ask=="1":
        setup[2]=ask
        print("\n#已修改#")
      else:
        print("\n#請輸入正確數字#")
    
    elif setting=="4":
      print("\n目前為:",setup[3])
      ask=input("\n請選擇顏色(顏色表[default,red,orange,yellow,green,blue,purple])\n→")
      if ask=="red" or ask=="orange" or ask=="yellow" or ask=="green" or ask=="blue" or ask=="purple":
        setup[3]=ask
        print("\n#已修改#")
      elif ask=="default":
        setup[3]="#1f77b4"
        print("\n#已修改#")
      else:
        print("\n#請輸入正確顏色#")
    
    elif setting=="5":
      print("\n目前為:",setup[4])
      ask=input("\n1=漂亮輸出\n0=普通輸出\n→")
      if ask=="0" or ask=="1":
        setup[4]=ask
        print("\n#已修改#")
      else:
        print("\n#請輸入正確數字#")
    
    elif setting=="6":
      print("\n目前為:",setup[5])
      ask=input("\n1=開\n0=關\n→")
      if ask=="1" or ask=="0":
        setup[5]=ask
        print("\n#已修改#")
      else:
        print("\n#請輸入正確數字#")
    
    elif setting=="7-1":
      print("\n目前為:",setup[6])
      ask=input("\n1=開\n0=關\n→")
      if ask=="1" or ask=="0":
        setup[6]=ask
        print("\n#已修改#")
      else:
        print("\n#請輸入正確數字#")
    
    elif setting=="7-2":
      try:
        if setup[6]=="0":
          print("\n#代入計算功能未開啟#\n")
        else:
          print("\n目前為:",setup[7])
          ask=input("\n1=開\n0=關\n→")
          if ask=="1" or ask=="0":
            setup[7]=ask
            print("\n#已修改#")
            if setup[6]=="1" and setup[7]=="1":
              print("\n目前x為:",setup[8])
              print("\n目前y為:",setup[9])
              setup[8]=eval(input("\n請輸入x值\n→"))
              setup[9]=eval(input("\n請輸入y值\n→"))
              print("\n#已修改#")
          else:
            print("\n#請輸入正確數字#")
      except NameError:
        print("\n#請輸入正確數字#")
      except SyntaxError:
        print("\n#請輸入正確數字#")
    
    elif setting=="8-1":
      print("\n目前為:",setup[10])
      ask=input("\n1=開\n0=關\n→")
      if ask=="1" or ask=="0":
        setup[10]=ask
        print("\n#已修改#")
      else:
        print("\n#請輸入正確數字#")
    
    elif setting=="8-2":
      try:
        if setup[10]=="0":
          print("\n#多次微分功能未開啟#\n")
        else:
          print("\n目前為:",setup[11])
          ask=input("\n1=開\n0=關\n→")
          if ask=="1" or ask=="0":
            setup[11]=ask
            print("\n#已修改#")
            if setup[10]=="1" and setup[11]=="1":
              print("\n目前預設值為:",setup[12])
              setup[12]=int(input("\n請輸入多次微分次數\n→"))
              print("\n#已修改#")
          else:
            print("\n#請輸入正確數字#")
      except NameError:
        print("\n#請輸入正確數字#")
      except ValueError:
        print("\n#請輸入正確數字#")
   
    elif setting=="9":
      print("\n目前為:",setup[13])
      ask=input("\n調整範圍為(>0):\n→")
      try:
        if eval(ask)<=0:
          print("\n#請輸入正整數#")
        else:
          setup[13]=eval(ask)
          print("\n#已修改#")
      except SyntaxError:
        print("\n#請輸入正確數字#")

    elif setting=="10":
      setup=["1","100","0","#1f77b4","1","0","1","0","2","3","1","0","2","10"]
      print("\n#已修改#")
    
    else:
      print("\n#請輸入正確數字#")
    data=open("setting.txt", mode="w", encoding="utf-8")
    for save in setup:
      print(save, file=data)
    data.close()

  elif type=="6":
    print("\n進階微分輸入函數表:\npi → π\nsqrt(x) → 平方根函數\ncbrt(x) → 立方根函數\nsin(x)、cos(x)、tan(x)、csc(x)、sec(x)、cot(x) → 三角函數\nasin(x)、acos(x)、atan(x)、acsc(x)、asec(x)、acot(x) → 反三角函數\nexp(x) → e^x\npow(x,y) → x^y\nln(x) → 自然對數\nlog(x,b) → 對數函數(以b為底)\nfactorial(x) → x!\n") 
    
  elif type=="7":
    print("\n程式名稱 → 微分計算機PRO\n版本 → v2.0\n更新日期 → 2023-01-24\n作者 → 沈啟安\n聯繫作者 → 10931047@stu.tshs.tp.edu.tw\n系統需求 → CPU i5、RAM 4g、SSD、WIN10/11")
    ask=input("\n是否要顯示版本紀錄(y or n)→")
    if ask=="y":
      data = open("version.txt", mode="r",encoding="utf-8")
      words = data.read()
      print("\n版本紀錄 → ")
      print(words)
      data.close()
    else:
      print("\n#請確認輸入之內容正確#\n")
    
  elif type=="8":
    if setup[2]=="0":
      break
    elif setup[2]=="1":
      history=[]
      calc_type=[]
      save_history()
      break
    
  else:
    print("\n#請輸入正確數字#\n")
