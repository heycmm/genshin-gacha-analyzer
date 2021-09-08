import json
import os
import sys

uid = ""
gachaInfo = []
gachaTypes = []
gachaLog = []
gachaTypeIds = []
gachaTypeNames = []
gachaTypeDict = {}
gachaTypeReverseDict = {}


def getInfoByItemId(item_id):
    for info in gachaInfo:
        if item_id == info["item_id"]:
            return info["name"], info["item_type"], info["rank_type"]
    return


def writeXLSX(uid, gachaLog, gachaTypeIds):
    import xlsxwriter
    import time

    gen_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    t = time.strftime("%Y%m%d%H%M%S", time.localtime())
    workbook = xlsxwriter.Workbook(f"{gen_path}\\{uid}-{t}.xlsx")
    for id in gachaTypeIds:
        gachaDictList = gachaLog[id]
        gachaTypeName = gachaTypeDict[id]
        gachaDictList.reverse()
        header = "时间,名称,类别,星级,总次数,保底内"
        worksheet = workbook.add_worksheet(gachaTypeName)
        content_css = workbook.add_format(
            {"align": "left", "font_name": "微软雅黑", "border_color": "#c4c2bf", "bg_color": "#ebebeb", "border": 1})
        title_css = workbook.add_format(
            {"align": "left", "font_name": "微软雅黑", "color": "#757575", "bg_color": "#dbd7d3", "border_color": "#c4c2bf",
             "border": 1, "bold": True})
        excel_col = ["A", "B", "C", "D", "E", "F"]
        excel_header = header.split(",")
        worksheet.set_column("A:A", 22)
        worksheet.set_column("B:B", 14)
        for i in range(len(excel_col)):
            worksheet.write(f"{excel_col[i]}1", excel_header[i], title_css)
        worksheet.freeze_panes(1, 0)
        idx = 0
        pdx = 0
        i = 0
        for gacha in gachaDictList:
            time = gacha["time"]
            name = gacha["name"]
            item_type = gacha["item_type"]
            rank_type = gacha["rank_type"]
            idx = idx + 1
            pdx = pdx + 1
            excel_data = [time, name, item_type, rank_type, idx, pdx]
            excel_data[3] = int(excel_data[3])
            for j in range(len(excel_col)):
                worksheet.write(f"{excel_col[j]}{i + 2}", excel_data[j], content_css)
            if excel_data[3] == 5:
                pdx = 0
            i += 1

        star_5 = workbook.add_format({"color": "#bd6932", "bold": True})
        star_4 = workbook.add_format({"color": "#a256e1", "bold": True})
        star_3 = workbook.add_format({"color": "#8e8e8e"})
        worksheet.conditional_format(f"A2:F{len(gachaDictList) + 1}",
                                     {"type": "formula", "criteria": "=$D2=5", "format": star_5})
        worksheet.conditional_format(f"A2:F{len(gachaDictList) + 1}",
                                     {"type": "formula", "criteria": "=$D2=4", "format": star_4})
        worksheet.conditional_format(f"A2:F{len(gachaDictList) + 1}",
                                     {"type": "formula", "criteria": "=$D2=3", "format": star_3})

    workbook.close()


def main():
    gen_path = os.path.dirname(os.path.realpath(sys.argv[0]))
    f = open(f"{gen_path}\\gachaData.json", "r", encoding="utf-8")
    s = f.read()
    f.close()
    j = json.loads(s)

    global uid
    global gachaInfo
    global gachaTypes
    global gachaLog
    global gachaTypeIds
    global gachaTypeNames
    global gachaTypeDict
    global gachaTypeReverseDict

    uid = j["uid"]
    gachaTypes = j["gachaType"]
    gachaLog = j["gachaLog"]
    gachaTypeIds = [banner["key"] for banner in gachaTypes]
    gachaTypeNames = [key["name"] for key in gachaTypes]
    gachaTypeDict = dict(zip(gachaTypeIds, gachaTypeNames))
    gachaTypeReverseDict = dict(zip(gachaTypeNames, gachaTypeIds))

    print("写入文件", end="...", flush=True)
    writeXLSX(uid, gachaLog, gachaTypeIds)
    print("XLSX", end=" ", flush=True)


if __name__ == "__main__":
    main()
