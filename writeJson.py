import json
import os
import sys
import time
from api import checkApi, getGachaTypes, getGachaLogs, mergeDataFunc


def writeJson(spliturl: list):
    url = "?".join(spliturl)
    if checkApi(url):
        print("获取抽卡记录", flush=True)
        gachaTypes = getGachaTypes(url)
        gachaTypeIds = [banner["key"] for banner in gachaTypes]
        gachaTypeNames = [banner["name"] for banner in gachaTypes]
        gachaTypeDict = dict(zip(gachaTypeIds, gachaTypeNames))
        gachaData = {}
        gachaData["gachaType"] = gachaTypes
        gachaData["gachaLog"] = {}
        for gachaTypeId in gachaTypeIds:
            gachaLog = getGachaLogs(url, gachaTypeId, gachaTypeDict)
            gachaData["gachaLog"][gachaTypeId] = gachaLog

        uid_flag = 1
        for gachaType in gachaData["gachaLog"]:
            for log in gachaData["gachaLog"][gachaType]:
                if uid_flag and log["uid"]:
                    gachaData["uid"] = log["uid"]
                    uid_flag = 0

        gen_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        uid = gachaData["uid"]
        localDataFilePath = f"{gen_path}\\gachaData-{uid}.json"

        if os.path.isfile(localDataFilePath):
            with open(localDataFilePath, "r", encoding="utf-8") as f:
                localData = json.load(f)
            mergeData = mergeDataFunc(localData, gachaData)
        else:
            mergeData = gachaData
        print("写入文件", end="...", flush=True)
        with open(f"{gen_path}\\gachaData.json", "w", encoding="utf-8") as f:
            json.dump(mergeData, f, ensure_ascii=False, sort_keys=False, indent=4)
        with open(f"{gen_path}\\gachaData-{uid}.json", "w", encoding="utf-8") as f:
            json.dump(mergeData, f, ensure_ascii=False, sort_keys=False, indent=4)
        print("JSON", flush=True)
        t = time.strftime("%Y%m%d%H%M%S", time.localtime())
        with open(f"{gen_path}\\gachaData-{uid}-{t}.json", "w", encoding="utf-8") as f:
            json.dump(gachaData, f, ensure_ascii=False, sort_keys=False, indent=4)
