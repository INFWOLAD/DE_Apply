# DE_Apply

这个脚本可以帮助你尽可能快的获取到预定资格。

注意：本版本为重写版本，以梳理逻辑。

如需使用该脚本，请按照如下步骤：

1. 请填写`config_template.ini`中的值，并将文件重命名为`config.ini`。如果您不想使用企业微信进行推送，请将其中的`wecom_on`设置为False，不影响核心功能。
2. 运行`Core.py`。请确保`Get_Position.py`， `Position_Apply.py` 以及`config.ini`在同一目录。
3. 当出现名额会推送（控制台显示）给你。

另外请注意：合理添加time.sleep()进行缓冲。

仅供自用