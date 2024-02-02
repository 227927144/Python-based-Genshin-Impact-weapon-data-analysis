import re #正则表达式文字匹配
import bs4 #网页解析获取数据
import urllib.request
import urllib.error
import xlwt #excel
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib#字体问题
import matplotlib.ticker as ticker#x轴问题

#爬虫
def PaChong(WangZhi):
    # 爬取网页
    TouBuXinXi={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Safari/537.36 Edg/103.0.1264.71'}
    #头部信息    #伪装成浏览器
    JieShou=urllib.request.Request(WangZhi,headers=TouBuXinXi)#接收
    WangYe=''#网页
    try:
        XiangYing=urllib.request.urlopen(JieShou)#发起请求
        WangYe=XiangYing.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e,'code'):
            print(e.code)
        if hasattr(e,'reason'):
            print(e.reason)

    WQMC_GuiZe=re.compile(r'title="(.*)"><img alt="')#创建正则表达式对象表示字符串模式规则
    #r忽视特殊符号   #(.*)一个或者多个字符
    WQTP_GuiZe=re.compile(r'srcset="(.*) 1.5x"')
    WQLX_GuiZe=re.compile(r'data-param1="(.*)" data-param2')
    WQFSX_GuiZe=re.compile(r'<td class="visible-md visible-sm visible-lg">(.*)<br/>(.*)')
    WQGJL_GuiZe=re.compile(r'data-param6="(.*)">')
    WQTag_GuiZe=re.compile(r'data-param3="(.*)" data-param4=')

    AllWuQiShuJu=[]  #所有武器数据
    #逐一解析
    JuBuBianLiang=bs4.BeautifulSoup(urllib.request.urlopen(WangZhi),'html.parser') #使用html.parser解析器解析WangZhi   #局部变量
    for i in JuBuBianLiang.find_all('tr',class_='divsort'):#查找需要的字符串，并形成列表
        AWuQiShuJu=[]#一把武器数据
        i=str(i)
        WQMingCheng=re.findall(WQMC_GuiZe,i)#武器名称
        #通过re通过正则表达式查找指定字符串武器名称
        AWuQiShuJu.append(WQMingCheng)
        WQTuPian = re.findall(WQTP_GuiZe, i)#武器图片
        AWuQiShuJu.append(WQTuPian)
        WQLeiXing=re.findall(WQLX_GuiZe,i)#武器类型
        AWuQiShuJu.append(WQLeiXing)
        WQFuShuXing=re.findall(WQFSX_GuiZe,i)#武器属性
        AWuQiShuJu.append(WQFuShuXing)
        WQGongJiLi=re.findall(WQGJL_GuiZe, i)#武器攻击力
        AWuQiShuJu.append(WQGongJiLi)
        WQTag = re.findall(WQTag_GuiZe, i)#武器Tag
        AWuQiShuJu.append(WQTag)
        AllWuQiShuJu.append(AWuQiShuJu)
    PC_DuoYuShuJuTiChu(AllWuQiShuJu)
    BaoCun(AllWuQiShuJu)


##爬虫_多余数据剔除
def PC_DuoYuShuJuTiChu(AllWuQiShuJu):
    for i in range(136):  #行
        if not AllWuQiShuJu[i][3]:
            pass
        else:
            AllWuQiShuJu[i][3] = list(AllWuQiShuJu[i][3][0])
    return AllWuQiShuJu



#保存数据
def BaoCun(AllWuQiShuJu):
    BiaoGe = xlwt.Workbook(encoding='utf-8')  # 创建表格对象
    GongZuoBiao = BiaoGe.add_sheet('GenShin impact 武器数据')  # 创建工作表
    GongZuoBiao.write(0, 0, '名称')
    GongZuoBiao.write(0, 1, '图片')
    GongZuoBiao.write(0, 2, '类型')
    GongZuoBiao.write(0, 3, '初始属性')
    GongZuoBiao.write(0, 4, '初始攻击力')
    GongZuoBiao.write(0, 5, '标签')
    for i in range(1,136):#行
        for j in range(6):#列
            zfc=''
            zfc=str(AllWuQiShuJu[i-1][j])
            GongZuoBiao.write(i,j,zfc)
    BiaoGe.save(r'D:\2022夏小学期Python\项目\原神武器数据.xlsx')
    ShuJuKeShiHua(AllWuQiShuJu)



#数据可视化
def ShuJuKeShiHua(AllWuQiShuJu):
    ShuJu=pd.read_excel(r'D:\2022夏小学期Python\项目\原神武器数据.xlsx','GenShin impact 武器数据')
    KSH_WuQuLeiXing(AllWuQiShuJu)
    KSH_GongJiLi(ShuJu,AllWuQiShuJu)
    KSH_ChuShiShuXing(ShuJu,AllWuQiShuJu)


##可视化_武器类型
def KSH_WuQuLeiXing(AllWuQiShuJu):
    dsj,ssj,fq,cq,gong=0,0,0,0,0
    for i in range(len(AllWuQiShuJu)):
        if not AllWuQiShuJu[i][2]:
            pass
        else:
            if AllWuQiShuJu[i][2][0]=='单手剑':
                dsj=dsj+1
            elif AllWuQiShuJu[i][2][0]=='双手剑':
                ssj=ssj+1
            elif AllWuQiShuJu[i][2][0]=='法器':
                fq=fq+1
            elif AllWuQiShuJu[i][2][0]=='长柄武器':
                cq=cq+1
            elif AllWuQiShuJu[i][2][0]=='弓':
                gong=gong+1
    zonghe=dsj+ssj+fq+cq+gong
    BiLi=[dsj/zonghe,ssj/zonghe,fq/zonghe,cq/zonghe,gong/zonghe]
    KSH_BingTu(BiLi,['单手剑','双手剑','法器','长枪','弓'],'原神武器类型饼图',[0, 0, 0, 0, 0])



##可视化_攻击力
def KSH_GongJiLi(ShuJu,AllWuQiShuJu):
    KSH_SanDianTu(ShuJu['名称'],ShuJu['初始攻击力'],'原神武器初始攻击力散点图',1,7,90)
    ZH=[]
    for i in range(len(AllWuQiShuJu)):
        GongJiLi = []
        if not AllWuQiShuJu[i][0]:
            pass
        elif not AllWuQiShuJu[i][4]:
            pass
        else:
            GongJiLi.append(AllWuQiShuJu[i][0][0])
            GongJiLi.append(AllWuQiShuJu[i][4][0])
            ZH.append(GongJiLi)
    zhmc,zhgjl=PaiXu(ZH)
    KSH_SanDianTu(zhmc,zhgjl, '原神武器初始攻击力散点图_有序版', 1,7,90)
    KSH_BingTu(KSH_GJL_BT_QiuBiLi(AllWuQiShuJu),['23-30','31-35','36-40','41-45','46-49'],'原神武器初始攻击力饼图',[0, 0, 0, 0, 0])


####可视化_攻击力_饼图_求比例
def KSH_GJL_BT_QiuBiLi(AllWuQiShuJu):
    # '23-30','31-35','36-40','41-45','46-49'
    bl2330=0
    bl3135=0
    bl3640=0
    bl4145=0
    bl4649=0
    for i in range(136):
        if not AllWuQiShuJu[i][4][0]:
            pass
        else:
            if int(AllWuQiShuJu[i][4][0])>=23 and int(AllWuQiShuJu[i][4][0])<=30:
                bl2330=bl2330+1
            elif int(AllWuQiShuJu[i][4][0])>=30 and int(AllWuQiShuJu[i][4][0])<=35:
                bl3135 = bl3135 + 1
            elif int(AllWuQiShuJu[i][4][0])>=36 and int(AllWuQiShuJu[i][4][0])<=40:
                bl3640 = bl3640 + 1
            elif int(AllWuQiShuJu[i][4][0])>=41 and int(AllWuQiShuJu[i][4][0])<=45:
                bl4145 = bl4145 + 1
            elif int(AllWuQiShuJu[i][4][0])>=46 and int(AllWuQiShuJu[i][4][0])<=49:
                bl4649 = bl4649 + 1
    zonghe=bl2330+bl3135+bl3640+bl4145+bl4649
    BiLi=[bl2330/zonghe,bl3135/zonghe,bl3640/zonghe,bl4145/zonghe,bl4649/zonghe]
    return BiLi



##可视化_初始属性
def KSH_ChuShiShuXing(ShuJu,AllWuQiShuJu):
    gjl=0
    gjl_lb=[]
    smz=0
    smz_lb = []
    fyl = 0
    fyl_lb = []
    wlsh = 0
    wlsh_lb = []
    ysjt = 0
    ysjt_lb = []
    yscn = 0
    yscn_lb = []
    bjl = 0
    bjl_lb = []
    bjsh = 0
    bjsh_lb = []
    for i in range(136):
        if not AllWuQiShuJu[i][3]:
            pass
        else:
            lbi=[AllWuQiShuJu[i][0][0]]
            if AllWuQiShuJu[i][3][0]=='攻击力%':
                gjl=gjl+1
                gjlsz=re.findall('[\d+\.\d+]*',AllWuQiShuJu[i][3][1])
                lbi.append(float(gjlsz[0]))
                gjl_lb.append(lbi)
            elif AllWuQiShuJu[i][3][0]=='生命值':
                smz=smz+1
                smzsz = re.findall('[\d+\.\d+]*', AllWuQiShuJu[i][3][1])
                lbi.append(float(smzsz[0]))
                smz_lb.append(lbi)
            elif AllWuQiShuJu[i][3][0]=='防御力':
                fyl=fyl+1
                fylsz = re.findall('[\d+\.\d+]*', AllWuQiShuJu[i][3][1])
                lbi.append(float(fylsz[0]))
                fyl_lb.append(lbi)
            elif AllWuQiShuJu[i][3][0]=='物理伤害加成':
                wlsh=wlsh+1
                wlshsz = re.findall('[\d+\.\d+]*', AllWuQiShuJu[i][3][1])
                lbi.append(float(wlshsz[0]))
                wlsh_lb.append(lbi)
            elif AllWuQiShuJu[i][3][0]=='元素精通':
                ysjt=ysjt+1
                ysjtsz = AllWuQiShuJu[i][3][1]
                lbi.append(int(ysjtsz))
                ysjt_lb.append(lbi)
            elif AllWuQiShuJu[i][3][0]=='元素充能效率':
                yscn=yscn+1
                yscnsz = re.findall('[\d+\.\d+]*', AllWuQiShuJu[i][3][1])
                lbi.append(float(yscnsz[0]))
                yscn_lb.append(lbi)
            elif AllWuQiShuJu[i][3][0]=='暴击率':
                bjl=bjl+1
                bjlsz = re.findall('[\d+\.\d+]*', AllWuQiShuJu[i][3][1])
                lbi.append(float(bjlsz[0]))
                bjl_lb.append(lbi)
            elif AllWuQiShuJu[i][3][0]=='暴击伤害':
                bjsh=bjsh+1
                bjshsz = re.findall('[\d+\.\d+]*', AllWuQiShuJu[i][3][1])
                lbi.append(float(bjshsz[0]))
                bjsh_lb.append(lbi)
    zongshu=gjl+smz+fyl+wlsh+ysjt+yscn+bjl+bjsh
    BiLi = [gjl/zongshu,smz/zongshu,fyl/zongshu,wlsh/zongshu,ysjt/zongshu,yscn/zongshu,bjl/zongshu,bjsh/zongshu]
    gjlmc, gjlsz=PaiXu(gjl_lb)
    smzmc, smzsz = PaiXu(smz_lb)
    fylmc, fylsz = PaiXu(fyl_lb)
    wlshmc, wlshsz = PaiXu(wlsh_lb)
    ysjtmc, ysjtsz = PaiXu(ysjt_lb)
    yscnmc, yscnsz = PaiXu(yscn_lb)
    bjlmc, bjlsz = PaiXu(bjl_lb)
    bjshmc, bjshsz = PaiXu(bjsh_lb)

    KSH_SanDianTu(gjlsz,gjlmc, '原神武器初始属性_攻击力散点图',0.1,10,90)
    KSH_SanDianTu(smzsz, smzmc, '原神武器初始属性_生命值散点图',0.1,10,0)
    KSH_SanDianTu(fylsz, fylmc, '原神武器初始属性_防御力散点图',0.1,10,90)
    KSH_SanDianTu(wlshsz, wlshmc, '原神武器初始属性_物理伤害散点图',0.1,10,90)
    KSH_SanDianTu(ysjtsz, ysjtmc, '原神武器初始属性_元素精通散点图',1,10,0)
    KSH_SanDianTu(yscnsz, yscnmc, '原神武器初始属性_元素充能散点图',0.1,10,90)
    KSH_SanDianTu(bjlsz, bjlmc, '原神武器初始属性_暴击率散点图',0.1,10,90)
    KSH_SanDianTu(bjshsz, bjshmc, '原神武器初始属性_暴击伤害散点图',0.1,8,90)
    KSH_BingTu(BiLi, ['攻击力','生命值','防御力','物理伤害','元素精通','元素充能','暴击率','暴击伤害'], '原神武器属性饼状图',[0,0,0,0,0,0,0,0])


#排序
def PaiXu(lb):
    mc=[]
    sz=[]
    for i in range(len(lb)):
        for j in range(i,len(lb)):
            if lb[i][1]>lb[j][1]:
                temp=lb[i]
                lb[i]=lb[j]
                lb[j]=temp
    for i in range(len(lb)):
        mc.append(lb[i][0])
        sz.append(lb[i][1])
    return mc,sz



##可视化_散点图
def KSH_SanDianTu(x,y,BiaoTi,BQMiDu,BQDaXiao,Qingxie):
    matplotlib.rc("font", family='Microsoft YaHei')#设置成包含中文语言
    Dian=plt.figure(figsize=(20, 8))#设置画布大小
    ax=Dian.add_subplot(1,1,1)#添加子图
    plt.tick_params(axis='x', labelsize=BQDaXiao)  # 设置x轴标签大小
    ax.xaxis.set_major_locator(ticker.MultipleLocator(BQMiDu))# 设置x轴密度
    plt.xticks(rotation=Qingxie)#标签倾斜
    ax.scatter(x,y) #x, y, 点的大小, 颜色，标记
    plt.title(BiaoTi)#设置标题
    plt.show()


##可视化_饼图
def KSH_BingTu(BiLi,TuLi,BiaoTi,explode):
    matplotlib.rc("font", family='Microsoft YaHei')  # 设置成包含中文语言
    ax=plt.subplot()#画饼
    ax.pie(BiLi,explode=explode, autopct='%1.1f%%', shadow=True)
    ax.set_title(BiaoTi)
    ax.legend(labels=TuLi)#设置图例
    plt.show()


if __name__ == '__main__':
    WangZhi = 'https://wiki.biligame.com/ys/%E6%AD%A6%E5%99%A8%E5%9B%BE%E9%89%B4'  # 网址
    PaChong(WangZhi)
