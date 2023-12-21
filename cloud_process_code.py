"""以下为云端处理部分的续写"""
import os
import json

import pandas as pd

fp = r""
abnormal_temp_diff_dict = {}
abnormal_max_temp_dict = {}
abnormal_min_temp_dict = {}
suit_temp_rate_dict = {}
temp_down_rate_dict = {}
temp_down_duration_dict = {}
high_soc_temp_dict = {}
fault_dict = {}
static_duration_dict = {}
static_soc_dict = {}
static_temp_down_dict = {}
balance_list = []
dod_list = []
day_charge_time_list = []
day_discharge_time_list = []
start_charge_list = []
start_discharge_list = []
for file in os.listdir(fp):
    box_name = "1"  # 暂定
    result_dict = json.loads(file)

    # 以下为续写部分
    # 温差异常时空调工作状态
    if box_name not in abnormal_temp_diff_dict.keys():
        abnormal_temp_diff_dict[box_name] = [[], [[], [], [], [], []]]
        abnormal_temp_diff_dict[box_name][0] += result_dict["chart26"]["x"]
        for pp in range(len(abnormal_temp_diff_dict[box_name][1])):
            abnormal_temp_diff_dict[box_name][1][pp] += result_dict["chart26"]["y"][pp]
    else:
        abnormal_temp_diff_dict[box_name][0] += result_dict["chart26"]["x"]
        for pp in range(len(abnormal_temp_diff_dict[box_name][1])):
            abnormal_temp_diff_dict[box_name][1][pp] += result_dict["chart26"]["y"][pp]
    # 高温异常时空调工作状态
    if box_name not in abnormal_max_temp_dict.keys():
        abnormal_max_temp_dict[box_name] = [[], [[], [], []]]
        abnormal_max_temp_dict[box_name][0] += result_dict["chart27"]["x"]
        for pp in range(len(abnormal_max_temp_dict[box_name][1])):
            abnormal_max_temp_dict[box_name][1][pp] += result_dict["chart27"]["y"][pp]
    else:
        abnormal_max_temp_dict[box_name][0] += result_dict["chart27"]["x"]
        for pp in range(len(abnormal_max_temp_dict[box_name][1])):
            abnormal_max_temp_dict[box_name][1][pp] += result_dict["chart27"]["y"][pp]
    # 低温异常时空调工作状态
    if box_name not in abnormal_min_temp_dict.keys():
        abnormal_min_temp_dict[box_name] = [[], [[], [], []]]
        abnormal_min_temp_dict[box_name][0] += result_dict["chart28"]["x"]
        for pp in range(len(abnormal_min_temp_dict[box_name][1])):
            abnormal_min_temp_dict[box_name][1][pp] += result_dict["chart28"]["y"][pp]
    else:
        abnormal_min_temp_dict[box_name][0] += result_dict["chart28"]["x"]
        for pp in range(len(abnormal_min_temp_dict[box_name][1])):
            abnormal_min_temp_dict[box_name][1][pp] += result_dict["chart28"]["y"][pp]
    # 恒温占比
    if box_name not in suit_temp_rate_dict.keys():
        suit_temp_rate_dict[box_name] = []
        suit_temp_rate_dict[box_name].append(result_dict["chart29"]["y"])
    else:
        suit_temp_rate_dict[box_name].append(result_dict["chart29"]["y"])
    # 静置回温速率
    if box_name not in temp_down_rate_dict.keys():
        temp_down_rate_dict[box_name] = []
        temp_down_rate_dict[box_name].append(result_dict["chart30"]["y"])
    else:
        temp_down_rate_dict[box_name].append(result_dict["chart30"]["y"])
    # 静置回温时长
    if box_name not in temp_down_duration_dict.keys():
        temp_down_duration_dict[box_name] = []
        temp_down_duration_dict[box_name].append(result_dict["chart31"]["y"])
    else:
        temp_down_duration_dict[box_name].append(result_dict["chart31"]["y"])
    # 50%-100%SOC温度表现,先假定传过来的是列表，周六看看是不是列表
    if box_name not in high_soc_temp_dict.keys():
        high_soc_temp_dict[box_name] = [[], [], []]
        for pp in range(len(high_soc_temp_dict[box_name])):
            high_soc_temp_dict[box_name][pp] += result_dict["chart32"]["y"][pp]
    else:
        for pp in range(len(high_soc_temp_dict[box_name])):
            high_soc_temp_dict[box_name][pp] += result_dict["chart32"]["y"][pp]
    # 故障汇总
    if box_name not in fault_dict.keys():
        fault_dict[box_name] = [[], [], []]
        for pp in range(len(fault_dict[box_name])):
            fault_dict[box_name][pp] += result_dict["chart33"]["y"][pp]
    else:
        for pp in range(len(fault_dict[box_name])):
            fault_dict[box_name][pp] += result_dict["chart33"]["y"][pp]
    # 以下为静置部分
    if box_name not in static_duration_dict.keys():  # 静置时长
        static_duration_dict[box_name] = [[], []]
        static_duration_dict[box_name][0] += result_dict["chart34"]["x"]
        static_duration_dict[box_name][1] += result_dict["chart34"]["y"]
    else:
        static_duration_dict[box_name][0] += result_dict["chart34"]["x"]
        static_duration_dict[box_name][1] += result_dict["chart34"]["y"]

    if box_name not in static_soc_dict.keys():  # 静置SOC
        static_soc_dict[box_name] = [[], []]
        static_soc_dict[box_name][0] += result_dict["chart35"]["x"]
        static_soc_dict[box_name][1] += result_dict["chart35"]["y"]
    else:
        static_soc_dict[box_name][0] += result_dict["chart35"]["x"]
        static_soc_dict[box_name][1] += result_dict["chart35"]["y"]

    if box_name not in static_temp_down_dict.keys():  # 静置温度下降
        static_temp_down_dict[box_name] = [[], []]
        static_temp_down_dict[box_name][0] += result_dict["chart36"]["x"]
        static_temp_down_dict[box_name][1] += result_dict["chart36"]["y"]
    else:
        static_temp_down_dict[box_name][0] += result_dict["chart36"]["x"]
        static_temp_down_dict[box_name][1] += result_dict["chart36"]["y"]

    # 以下为均衡部分
    if len(result_dict["chart37"]["y"]):
        for x in result_dict["chart37"]["y"]:
            x.insert(0, box_name)  # 插入箱子名
        balance_list += result_dict["chart37"]["y"]

    # 以下为放电深度部分
    if not len(dod_list):
        dod_list = result_dict["chart39"]["y"]
    else:
        for ii in range(len(dod_list)):
            dod_list[ii] += result_dict["chart39"]["y"][ii]

    # 每日充电部分
    day_charge_time_list += result_dict["string1"]["y"]
    day_discharge_time_list += result_dict["string2"]["y"]
    if not len(day_charge_time_list):
        day_charge_time_list = result_dict["chart40"]["y"]
    else:
        for ii in range(len(day_charge_time_list)):
            day_charge_time_list[ii] += result_dict["chart40"]["y"][ii]

    if not len(day_discharge_time_list):
        day_discharge_time_list = result_dict["chart41"]["y"]
    else:
        for ii in range(len(day_discharge_time_list)):
            day_discharge_time_list[ii] += result_dict["chart41"]["y"][ii]

# 以下为空调部分汇总续写
# 温差异常，高温异常，低温异常温度表现，筛选一段较长时间的进行展示


# 以下为静置部分
date_static_dict = {}
for key, value in static_duration_dict.items():
    temp = pd.Series(static_duration_dict[key][1],
                     index=pd.to_datetime(static_duration_dict[key][0])).resample('D').sum()
    for index, date in enumerate([str(x).split(" ")[0] for x in temp.index]):
        if date not in date_static_dict.keys():
            date_static_dict[date] = []
            date_static_dict[date].append(temp.loc[date])
        else:
            date_static_dict[date].append(temp.loc[date])
chart34 = [list(date_static_dict.keys()),  # 静置时长
           [round(sum(date_static_dict[key]) / len(date_static_dict[key]), 2) for key in date_static_dict.keys()]]

static_soc_dict["总"] = [[], []]
for key, value in static_soc_dict.items():
    static_soc_dict["总"][0] += static_soc_dict[key][0]
    static_soc_dict["总"][1] += static_soc_dict[key][1]

static_soc_series = pd.DataFrame({"time": static_soc_dict["总"][0], "soc": static_soc_dict["总"][1]})
static_soc_series.drop_duplicates(subset=["time"], inplace=True)
static_soc_series.sort_values(by=["time"])
chart35 = [list(static_soc_series["time"]), list(static_soc_series["soc"])]  # 静置SOC

temp_down_area_list = ["0℃", "1℃", "2℃", "3℃", "4℃", "5℃", "6℃", "7℃", "8℃", "8℃以上"]
temp_down_count_list = [0] * 10
static_temp_down_dict["总"] = []
for key, value in static_temp_down_dict.items():
    for temp in static_temp_down_dict[key][1]:
        num = temp if temp <= 8 else 9
        temp_down_count_list[num] += 1
chart36 = [temp_down_area_list, temp_down_count_list]

# 均衡部分
chart37 = [["储能箱", "状态", "末端时间点", "BECUSN", "压差", "电态", "均衡情况"], balance_list]

# DOD
chart39 = [
    ["10%以下", "10%-20%", "20%-30%", "30%-40%", "40%-50%", "50%-60%", "60%-70%", "70%-80%", "80%-90%", "90%-100%"],
    [dod_list]]

# 每日充电部分
string1 = round(sum(day_charge_time_list) / len(day_charge_time_list), 2)
string2 = round(sum(day_discharge_time_list) / len(day_discharge_time_list), 2)
chart40 = [["0:00-1:00", "1:00-2:00", "2:00-3:00", "3:00-4:00", "4:00-5:00", "5:00-6:00", "6:00-7:00", "7:00-8:00",
            "8:00-9:00", "9:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
            "15:00-16:00",
            "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00", "20:00-21:00", "21:00-22:00", "22:00-23:00",
            "23:00-24:00",
            ], start_charge_list]
chart41 = [["0:00-1:00", "1:00-2:00", "2:00-3:00", "3:00-4:00", "4:00-5:00", "5:00-6:00", "6:00-7:00", "7:00-8:00",
            "8:00-9:00", "9:00-10:00", "10:00-11:00", "11:00-12:00", "12:00-13:00", "13:00-14:00", "14:00-15:00",
            "15:00-16:00",
            "16:00-17:00", "17:00-18:00", "18:00-19:00", "19:00-20:00", "20:00-21:00", "21:00-22:00", "22:00-23:00",
            "23:00-24:00",
            ], start_discharge_list]
