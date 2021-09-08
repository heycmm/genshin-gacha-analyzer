import urllib.parse
import requests
import json


def checkApi(url) -> bool:
    if not url:
        print("url为空")
        return False
    if "getGachaLog" not in url:
        print("错误的url，检查是否包含getGachaLog")
        return False
    try:
        r = requests.get(url)
        s = r.content.decode("utf-8")
        j = json.loads(s)
    except Exception as e:
        print("API请求解析出错：" + str(e))
        return False

    if not j["data"]:
        if j["message"] == "authkey valid error":
            print("authkey错误")
        else:
            print("数据为空，错误代码：" + j["message"])
        return False
    return True


def getApi(url: str, gachaType: str, size: str, page: int, end_id="") -> str:
    parsed = urllib.parse.urlparse(url)
    querys = urllib.parse.parse_qsl(parsed.query)
    param_dict = dict(querys)
    param_dict["size"] = size
    param_dict["gacha_type"] = gachaType
    param_dict["page"] = page
    param_dict["lang"] = "zh-cn"
    param_dict["end_id"] = end_id
    param = urllib.parse.urlencode(param_dict)
    path = url.split("?")[0]
    api = path + "?" + param
    return api


def getGachaLogs(url: str, gachaTypeId: str, gachaTypeDict: dict) -> list:
    size = "20"
    # api限制一页最大20
    gachaList = []
    end_id = "0"
    for page in range(1, 9999):
        print(f"正在获取 {gachaTypeDict[gachaTypeId]} 第 {page} 页", flush=True)
        api = getApi(url, gachaTypeId, size, page, end_id)
        r = requests.get(api)
        s = r.content.decode("utf-8")
        j = json.loads(s)
        gacha = j["data"]["list"]
        if not len(gacha):
            break
        for i in gacha:
            gachaList.append(i)
        end_id = j["data"]["list"][-1]["id"]

    return gachaList


def getGachaTypes(url: str) -> list:
    tmp_url = url.replace("getGachaLog", "getConfigList")
    parsed = urllib.parse.urlparse(tmp_url)
    querys = urllib.parse.parse_qsl(parsed.query)
    param_dict = dict(querys)
    param_dict["lang"] = "zh-cn"
    param = urllib.parse.urlencode(param_dict)
    path = tmp_url.split("?")[0]
    tmp_url = path + "?" + param
    r = requests.get(tmp_url)
    s = r.content.decode("utf-8")
    configList = json.loads(s)
    return configList["data"]["gacha_type_list"]


def mergeDataFunc(localData: dict, gachaData: dict) -> dict:
    gachaTypes = gachaData["gachaType"]
    gachaTypeIds = [banner["key"] for banner in gachaTypes]
    gachaTypeNames = [banner["name"] for banner in gachaTypes]
    gachaTypeDict = dict(zip(gachaTypeIds, gachaTypeNames))

    for banner in gachaTypeDict:
        bannerLocal = localData["gachaLog"][banner]
        bannerGet = gachaData["gachaLog"][banner]
        if bannerGet == bannerLocal:
            pass
        else:
            print("合并", gachaTypeDict[banner])
            flaglist = [1] * len(bannerGet)
            loc = [[i["time"], i["name"]] for i in bannerLocal]
            for i in range(len(bannerGet)):
                gachaGet = bannerGet[i]
                get = [gachaGet["time"], gachaGet["name"]]
                if get in loc:
                    pass
                else:
                    flaglist[i] = 0

            print("获取到", len(flaglist), "条记录")
            tempData = []
            for i in range(len(bannerGet)):
                if flaglist[i] == 0:
                    gachaGet = bannerGet[i]
                    tempData.insert(0, gachaGet)
            print("追加", len(tempData), "条记录")
            for i in tempData:
                localData["gachaLog"][banner].insert(0, i)

    return localData




