# SD的扩展：推送微信消息

这是一个属于SD的扩展插件。

它的作用是当批量生成任务结束后，自动推送一条微信消息通知你。

更主要的作用是，当批量任务执行中途异常终止（俗称崩显存，崩内存，CUDA），自动推送一条微信消息，通知你及时检查处理。

![Image text](https://github.com/zozi11/sd_auto_sendwxmsg/blob/main/webUI%E7%95%8C%E9%9D%A2%E4%B8%AD%E7%9A%84%E5%8A%9F%E8%83%BD%E5%9D%97.png)


微信消息通知接口来自pushplus，新用户需要注册，可以扫码自动注册。

注册后自动获取推送token，将key填写到设置中即可。



## 安装方式

使用SD扩展功能的从网址安装，当然你也可以手动安装。

手动安装方式是下载后解压放在 extensions 目录下。

注册获取token：

https://pushplus.plus

登录后点击 发送消息-一对一消息，即可查看你的token

将本扩展安装好之后，进入webUI的设置-微信推送设置，将token填入并保存，之后重载。
![Image text](https://github.com/zozi11/sd_auto_sendwxmsg/blob/main/%E5%A6%82%E4%BD%95%E5%A1%AB%E5%86%99token.jpg)

一切顺利的话，你就可以在界面中，大概在ADetailer和ControlNet标签最下方，看到新增的 自动推送微信消息 标签了。



## 注意：不填写你自己的token是不能正确工作的！

## 爱来自叶小猴，欢迎加入墨幽炼丹阁QQ群 858495398

## 墨幽老婆大模型天下第一！
