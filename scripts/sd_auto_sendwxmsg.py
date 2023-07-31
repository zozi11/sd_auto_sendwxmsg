import modules.scripts as scripts
import gradio as gr
import modules.shared as shared
import urllib.request
import urllib.parse
from modules import script_callbacks



# 填写你的token，从https://www.pushplus.plus/ 获取，发送消息=>一对一消息
pushtoken = 'c217a446b9c24e55a6d8b535ab95d07b'  




i=0
checked=False
def checkbox_changed(checkbox_input):
    global checked
    if checkbox_input:
        checked=True
    else:
        checked=False
    
def on_image_saved(params : script_callbacks.ImageSaveParams):
    global i
    i=i+1
def on_image_grid(params : script_callbacks.ImageGridLoopParams):
    #on_image_grid会在生成任务完毕后调用，暂时还没发现问题，先用着
    global i,pushtoken,checked
    if not checked:
        print("任务结束，当前未启用微信消息推送，不推送微信消息" )
        return
    html="本次生成图片总数："+str(i)+"<br>"
    totalcount=shared.state.job_count
    nowjob=shared.state.job_no + 1
    if nowjob < totalcount:
        v=totalcount-nowjob
        wxtitle="生成任务中途终止"
        html="生成任务已经停止！<br>本次任务计划总批次: "+str(totalcount)+" 实际成功执行批次: "+ str(nowjob)+"<br>缺少 <b color=red>"+ str(v)+"</b> 个批次没有执行。<br><br> -------------------<br><br>本次总计成功生成 <b color=red>"+ str(i)+"</b> 张图片。<br><br><b color=red>注意：</b>如果终止任务不是您手动操作，可能是因为显存或内存不足，出现异常，请检查控制台输出后重试"
    else:
        wxtitle="成功执行完毕！"
        html="图片已经全部成功生成。<br>本次计划批次："+str(totalcount)+"<br><br> -------------------<br><br>本次总计成功生成 <b color=red>"+ str(i)+"</b> 张图片。"
    #print("time_start: %d" % shared.state.time_start)
    #print("job_count: %d" % shared.state.job_count)
    #print("job_no: %d" % shared.state.job_no)
    #print("sampling_step: %d" % shared.state.sampling_step)
    #print("running: %d" % (shared.state.job_count * shared.state.sampling_step))
    #print("sampling_steps: %d" % shared.state.sampling_steps)
    rehtml=wxsend(wxtitle,html)
    print(rehtml)
    i=0
    print("微信消息推送完毕" )

def wxtest(tmp):
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
    
script_callbacks.on_image_grid(on_image_grid)
script_callbacks.on_image_saved(on_image_saved)
class SendWxMsg(scripts.Script):
    # Extension title in menu UI
    def title(self):
        return "自动推送微信消息"
    def show(self,is_img2img):
        return scripts.AlwaysVisible

    def ui(self,is_img2img):
        global md
        global markdown
        with gr.Accordion('自动推送微信消息', open=False):
            with gr.Row():
                checkbox = gr.Checkbox(
                    False,
                    label="启用，批量任务完成或异常终止时，推送微信通知"
                )
                checkbox.change(checkbox_changed,inputs=checkbox)
                btn = gr.Button("点击发送测试消息")
                btn.click(wxtest)
            with gr.Row():
                markdown=gr.Markdown("注意，你需要先在脚本中配置token，文件位置：extensions/sd_auto_sendwxmsg/scripts/sd_auto_sendwxmsg.py")
                return [checkbox,  btn]
