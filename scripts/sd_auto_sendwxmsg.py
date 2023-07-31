import modules.scripts as scripts
import gradio as gr
import modules.shared as shared
import urllib.request
import urllib.parse
from modules import script_callbacks
import time
import threading



# 请在设置中填写你的token，位置在设置-微信推送信息
pushtoken = shared.opts.plus_token

isworking = False
hasthread=False
totalcount=0

def mainchk():
    global isworking
    while True:
        if shared.state.job:
            isworking=True
            check_death()
        time.sleep(10)

thread = threading.Thread(target=mainchk)
thread.start()

def check_death():
    global hasthread
    if not hasthread:
        hasthread=True
        thread = threading.Thread(target=chk_thread)
        thread.start()

def chk_thread():
    global isworking,hasthread,totalcount
    while isworking:
        if not shared.state.job:
            workover()
            isworking=False
            hasthread=False
        else:
            time.sleep(5)

def mydebug():
    # 获取 shared.state 对象的属性列表
    attributes = dir(shared.state)
    print(f"------------------")
    # 循环打印每个属性的名称和值
    for attribute in attributes:
        value = getattr(shared.state, attribute)
        print(f"{attribute}: {value}")

i=0
checked=False
def checkbox_changed(checkbox_input):
    global checked
    if checkbox_input:
        checked=True
    else:
        checked=False
    
def on_image_saved(params : script_callbacks.ImageSaveParams):
    global i,isworking,totalcount
    i=i+1
    totalcount=shared.state.job_count
    isworking=True
    check_death()

def workover():
    global i,pushtoken,checked,totalcount
    if not checked:
        print("当前未启用微信消息推送，不推送微信消息" )
        return
    html="本次生成图片总数："+str(i)+"<br>"
    nowjob=shared.state.job_no + 1
    if nowjob < totalcount:
        v=totalcount-nowjob
        wxtitle="生成任务中途终止"
        html="生成任务已经停止！<br>本次任务计划总批次: "+str(totalcount)+" 实际成功执行批次: "+ str(nowjob)+"<br>缺少 <b color=red>"+ str(v)+"</b> 个批次没有执行。<br><br> -------------------<br><br>本次总计成功生成 <b color=red>"+ str(i)+"</b> 张图片。<br><br><b color=red>注意：</b>如果终止任务不是您手动操作，可能是因为显存或内存不足，出现异常，请检查控制台输出后重试"
    else:
        wxtitle="成功执行完毕！"
        html="图片已经全部成功生成。<br>本次计划批次："+str(totalcount)+"<br><br> -------------------<br><br>本次总计成功生成 <b color=red>"+ str(i)+"</b> 张图片。"
    rehtml=wxsend(wxtitle,html)
    i=0
    print("微信消息推送完毕" )

def wxtest(tmp):
    #mydebug()
    global i,pushtoken
    html="作者：叶小猴<br>欢迎加入墨幽炼丹阁，QQ群：858495398"
    rehtml=wxsend("测试微信消息",html)
    print(rehtml)
    print("微信消息推送完毕" )
def wxsend(wxtitle,wxcontent):
    url="http://www.pushplus.plus/send?token="+pushtoken+"&title="+wxtitle+"&content="+wxcontent+"&template=html"
    encoded_url = urllib.parse.quote(url, safe=':/?&=')
    response = urllib.request.urlopen(encoded_url)
    byte_content = response.read()
    webpage_content = byte_content.decode('utf-8')
    return webpage_content
    
script_callbacks.on_image_saved(on_image_saved)
class SendWxMsg(scripts.Script):
    # Extension title in menu UI
    def title(self):
        return "自动推送微信消息"
    def show(self,is_img2img):
        return scripts.AlwaysVisible

    def ui(self,is_img2img):
        global md
        global markdown,pushtoken
        with gr.Accordion('自动推送微信消息', open=True):
            with gr.Row():
                checkbox = gr.Checkbox(
                    False,
                    label="启用，批量任务完成或异常终止时，推送微信通知"
                )
                checkbox.change(checkbox_changed,inputs=checkbox)
                btn = gr.Button("点击发送测试消息")
                btn.click(wxtest)
            with gr.Row():
                markdown=gr.Markdown("注意，你需要先在设置中配置正确的plus_token，当前token："+pushtoken)
                return [checkbox,  btn]
