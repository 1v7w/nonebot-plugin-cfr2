import hashlib
import os
import secrets
from datetime import datetime
from pathlib import Path

import boto3
from botocore.exceptions import NoCredentialsError, ClientError

import nonebot
import nonebot.drivers
from nonebot.plugin import PluginMetadata
from nonebot.log import logger


from .config import Config

__plugin_meta__ = PluginMetadata(
    name="cloudfare R2 客服端",
    description="cloudfare R2 客服端插件",
    usage=(
        '声明依赖: `require("nonebot_plugin_cfr2")\n'
        "导入上传器: `from nonebot_plugin_cfr2 import uploader`\n"
        "上传文件: `uploader.upload_file(...)`\n"
        "上传文件字节: `uploader.upload_file_bytes(...)\n`"
    ),
    type="library",
    homepage="https://github.com/1v7w/nonebot-plugin-cfr2/",
    config=Config,
    supported_adapters=None,
)

class S3Uploader:
    def __init__(self, access_key: str, secret_key: str, bucket_name: str, region: str, endpoint_url: str, custom_domain: str):
        if access_key == "":
            return
        self.access_key = access_key
        self.secret_key = secret_key
        self.bucket_name = bucket_name
        self.region = region
        self.endpoint_url = endpoint_url
        self.custom_domain = custom_domain
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.endpoint_url,
            region_name=self.region
        )

    def generate_md5(self, file_path: str) -> str:
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    async def upload_file(self, local_file_path: str) -> str:
        try:
            ext_name = os.path.splitext(local_file_path)[1][1:]  # 获取文件扩展名
            md5_hash = self.generate_md5(local_file_path)  # 生成文件的MD5值
            now = datetime.now()
            s3_file_path = f"{now.year}/{now.month}/{md5_hash}.{ext_name}"

            self.s3_client.upload_file(local_file_path, self.bucket_name, s3_file_path)
            logger.debug(f"File {local_file_path} uploaded to {self.bucket_name}/{s3_file_path}")

            if self.custom_domain:
                file_url = f"{self.custom_domain}/{s3_file_path}"
            else:
                file_url = f"{self.bucket_name}.{self.endpoint_url}/{s3_file_path}"
            return file_url

        except FileNotFoundError:
            logger.debug(f"The file {local_file_path} was not found")
        except NoCredentialsError:
            logger.debug("Credentials not available")
        except ClientError as e:
            logger.error(f"Failed to upload {local_file_path}. Error: {e}")
        return ""


# 初始化
logger.debug("开始初始化cfr2")
config = nonebot.get_driver().config
try:
    access_key = config.access_key
except Exception as e:
    logger.error(f"access_key 未设置")
try:
    secret_key = config.secret_key
except Exception as e:
    logger.error(f"secret_key 未设置")
try:
    bucket_name = config.bucket_name
except Exception as e:
    logger.error(f"bucket_name 未设置")
try:
    region = config.region
except Exception as e:
    logger.error(f"reginon 未设置")
try:
    endpoint_url = config.endpoint_url
except Exception as e:
    logger.error(f"endpoint_url 未设置")
try:
    custom_domain = config.custom_domain
except Exception as e:
    logger.debug(f"custom_domain 未设置，将采用{endpoint_url}")

uploader: S3Uploader = S3Uploader(access_key, secret_key, bucket_name, region, endpoint_url, custom_domain)

async def upload_file_bytes(file_bytes: bytes, ext_name: str) -> str:
    file_name = secrets.token_urlsafe(16) + "." + ext_name
    with open(file_name, "rb") as f:
        f.write(file_bytes)
    ret: str = await uploader.upload_file(str(Path(__file__).parent / file_name))
    os.remove(file_name)
    return ret