import json
import lib.config as config
from colorama import Fore, Back, Style
from time import sleep, time
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.tmt.v20180321 import tmt_client, models


old_time = 0

cred = credential.Credential(config.secretId, config.secretKey)
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

    except TencentCloudSDKException:
        print(Fore.RED + Back.BLACK + Style.BRIGHT + "\n请检查网络连接或 secretId 和 secretKey 是否正确！")
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

    except TencentCloudSDKException:
        print(Fore.RED + Back.BLACK + Style.BRIGHT + "\n请检查网络连接或 secretId 和 secretKey 是否正确！")
        return text_list
