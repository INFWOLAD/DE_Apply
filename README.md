# DE_Apply

这个脚本可以帮助你尽可能快的获取到预定资格。

如需使用该脚本，请按照如下步骤：

1. 请填写`config_template.ini`中的值，并将文件重命名为`config.ini`
   - 如果您不想使用企业微信进行推送，请将其中的`wecom_on`设置为 False，不影响核心功能。
   - 如果您需要使用多线程，请将`close_multi`设置为False。程序会根据您的网络状况自动判断线程数。
2. 运行`Core.py`。请确保`Get_Position.py`， `Position_Apply.py` 以及`config.ini`在同一目录。
3. 当出现名额会 推送/控制台显示 给你。

另外：Web_Extension 为油猴插件，可以帮助你更快的手动抢名额。只需要在其中填写好你的个人信息，进入官方页面便会看到“自动填写”的按钮

仅供自用
