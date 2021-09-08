import os
import sys
import writeXLSX
import webbrowser
from writeJson import writeJson


def get_user():
    return os.path.expanduser('~')


output_log_path = get_user() + '/AppData/LocalLow/miHoYo/原神/output_log.txt'

if __name__ == '__main__':
    url = ""
    with open(output_log_path, "r", encoding="mbcs", errors="ignore") as f:
        log = f.readlines()

    for line in log:
        if line.startswith("OnGetWebViewPageFinish") and line.endswith("#/log\n"):
            url = line.replace("OnGetWebViewPageFinish:", "").replace("\n", "")

    if url == "":
        print("路径" + output_log_path + "下：\r\n日志文件中找不到OnGetWebViewPageFinish的链接\r\n")
        print("请进游戏后按f3 查询一次祈愿历史记录！")
        os.system("pause")
    else:
        spliturl = url.split("?")
        spliturl[0] = "https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog"
        writeJson(spliturl)
        writeXLSX.main()
        print("清除临时文件\r\n", end="...", flush=True)
        gen_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        del_paths = [name for name in os.listdir(gen_path) if
                     name.startswith("gacha") and (name.endswith(".json"))]
        for del_path in del_paths:
            try:
                os.remove(gen_path + "\\" + del_path)
            except:
                pass
        print("\t数据抓取完成,试着将excel文件拖入打开的网页？")
        webbrowser.open_new_tab('https://api.heycmm.cn/genshin-gacha-analyzer/')
        os.system("pause")
