import modules.scripts as scripts
import gradio as gr
import os

from modules import shared
from modules import script_callbacks

def on_ui_settings():
    section = ('template', "推送微信消息")
    shared.opts.add_option(
        "plus_token",
        shared.OptionInfo(
            "",
            "请输入你的token后保存（登录 https://pushplus.plus 获取，登录后点击发送消息-一对一发送）",
            gr.Textbox,
            {"interactive": True},
            section=section)
    )
script_callbacks.on_ui_settings(on_ui_settings)