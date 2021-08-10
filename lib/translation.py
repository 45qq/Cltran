import json
import logging
import configparser
import sys
from time import sleep, time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models

old_time = 0

config = configparser.ConfigParser()
config.read('config.ini', 'utf-8')

cred = credential.Credential(config.get('api', 'secretId'), config.get('api', 'secretKey'))
httpProfile = HttpProfile()
httpProfile.endpoint = "tmt.tencentcloudapi.com"

clientProfile = ClientProfile()
clientProfile.httpProfile = httpProfile
client = tmt_client.TmtClient(cred, "ap-guangzhou", clientProfile)


def get_tran(text):
    try:
        req = models.TextTranslateRequest()
        params = {
            "SourceText": text,
            "Source": "en",
            "Target": "zh",
            "ProjectId": 0,
        }
        req.from_json_string(json.dumps(params))

        global old_time
        new_time = time()
        timing = time() - old_time
        if timing < 200:
            sleep((200 - timing) / 1000.0)
        old_time = new_time

        return client.TextTranslate(req).TargetText

    except TencentCloudSDKException as err:
        logging.error("请检查网络连接！", err.args)
        return text


def get_tran_list(text_list):
    try:
        req = models.TextTranslateBatchRequest()
        params = {
            "Source": "en",
            "Target": "zh",
            "ProjectId": 0,
            "SourceTextList": text_list
        }
        req.from_json_string(json.dumps(params))

        global old_time
        new_time = time()
        timing = time() - old_time
        if timing < 200:
            sleep((200 - timing) / 1000.0)
        old_time = new_time

        return client.TextTranslateBatch(req).TargetTextList

    except TencentCloudSDKException as err:
        logging.error("请检查网络连接！", err.args)
        return text_list
