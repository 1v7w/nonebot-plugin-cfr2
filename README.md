<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-plugin-cfr2

_✨ cloudfare R2 客服端插件，用于连接R2存储桶 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/guyiiyu/nonebot-plugin-cfr2.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot-plugin-cfr2">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-cfr2.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

</div>



## 📖 介绍

cloudfare R2 客服端插件，用于连接R2存储桶，可以用作图床。

欢迎提issue。

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-cfr2

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-plugin-cfr2
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-plugin-cfr2
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-plugin-cfr2
</details>
<details>
<summary>conda</summary>

    conda install nonebot-plugin-cfr2
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_cfr2"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| access_key | 是 | 无 | 应用密钥ID |
| secret_key | 是 | 无 | 应用密钥 |
| bucket_name | 是 | 无 | 桶名 |
| region | 是 | 无 | 地区 |
| endpoint_url | 是 | 无 | 自定义节点（请以https开头）（非Amazon必填） |
| custom_domain | 否 | 无 | 自定义域名（请以https开头） |

## 🎉 使用
```python
from nonebot import require

require("nonebot_plugin_cfr2")

from nonebot_plugin_cfr2 import uploader

# 上传文件
uploader.upload_file(str(image_file_path))
# 上传字节
uploader.upload_file_bytes(image_file_bytes, "jpg")
```
