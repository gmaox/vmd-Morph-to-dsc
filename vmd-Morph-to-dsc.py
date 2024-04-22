# -*- coding: utf-8 -*-

import json
import re
from tkinter import filedialog

type = 0  #角色编号
trans = 100  #补间帧数

class Vmd:

    def __init__(self):
        pass

    @staticmethod
    def from_file(filename, model_name_encode="shift-JIS"):

        with open(filename, "rb") as f:
            from functools import reduce
            array = bytes(reduce(lambda x, y: x+y, list(f)))

        vmd = Vmd()

        VersionInformation = array[:30].decode("ascii")
        if VersionInformation.startswith("Vocaloid Motion Data file"):
            vision = 1
        elif VersionInformation.startswith("Vocaloid Motion Data 0002"):
            vision = 2
        else:
            raise Exception("unknow vision")

        vmd.vision = vision

        vmd.model_name = array[30: 30+10*vision].split(bytes([0]))[0].decode(model_name_encode)
        vmd.bone_keyframe_number = int.from_bytes(array[30+10*vision: 30+10*vision+4], byteorder='little', signed=False)
        vmd.bone_keyframe_record = []
        vmd.morph_keyframe_record = []
        vmd.camera_keyframe_record = []
        vmd.light_keyframe_record = []

        current_index = 34+10 * vision
        import struct
        for i in range(vmd.bone_keyframe_number):
            vmd.bone_keyframe_record.append({
                "BoneName": array[current_index: current_index+15].split(bytes([0]))[0].decode("shift-JIS"),
                "FrameTime": struct.unpack("<I", array[current_index+15: current_index+19])[0],
                "Position": {"x": struct.unpack("<f", array[current_index+19: current_index+23])[0],
                            "y": struct.unpack("<f", array[current_index+23: current_index+27])[0],
                            "z": struct.unpack("<f", array[current_index+27: current_index+31])[0]
                            },
                "Rotation":{"x": struct.unpack("<f", array[current_index+31: current_index+35])[0],
                            "y": struct.unpack("<f", array[current_index+35: current_index+39])[0],
                            "z": struct.unpack("<f", array[current_index+39: current_index+43])[0],
                            "w": struct.unpack("<f", array[current_index+43: current_index+47])[0]
                            },
                "Curve":{
                    "x":(array[current_index+47], array[current_index+51], array[current_index+55], array[current_index+59]),
                    "y":(array[current_index+63], array[current_index+67], array[current_index+71], array[current_index+75]),
                    "z":(array[current_index+79], array[current_index+83], array[current_index+87], array[current_index+91]),
                    "r":(array[current_index+95], array[current_index+99], array[current_index+103], array[current_index+107])
                }

            })
            current_index += 111

        # vmd['MorphKeyFrameNumber'] = int.from_bytes(array[current_index: current_index+4], byteorder="little", signed=False)
        vmd.morph_keyframe_number = int.from_bytes(array[current_index: current_index+4], byteorder="little", signed=False)
        current_index += 4

        for i in range(vmd.morph_keyframe_number):
            vmd.morph_keyframe_record.append({
                'MorphName': array[current_index: current_index+15].split(bytes([0]))[0].decode("shift-JIS"),
                'FrameTime': struct.unpack("<I", array[current_index+15: current_index+19])[0],
                'Weight': struct.unpack("<f", array[current_index+19: current_index+23])[0]
            })
            current_index += 23

        vmd.camera_keyframe_number = int.from_bytes(array[current_index: current_index+4], byteorder="little", signed=False)
        current_index += 4

        for i in range(vmd.camera_keyframe_number):
            vmd.camera_keyframe_record.append({
                'FrameTime': struct.unpack("<I", array[current_index: current_index+4])[0],
                'Distance': struct.unpack("<f", array[current_index+4: current_index+8])[0],
                "Position": {"x": struct.unpack("<f", array[current_index+8: current_index+12])[0],
                            "y": struct.unpack("<f", array[current_index+12: current_index+16])[0],
                            "z": struct.unpack("<f", array[current_index+16: current_index+20])[0]
                            },
                "Rotation":{"x": struct.unpack("<f", array[current_index+20: current_index+24])[0],
                            "y": struct.unpack("<f", array[current_index+24: current_index+28])[0],
                            "z": struct.unpack("<f", array[current_index+28: current_index+32])[0]
                            },
                "Curve": tuple(b for b in array[current_index+32: current_index+36]),
                "ViewAngle": struct.unpack("<I", array[current_index+56: current_index+60])[0],
                "Orthographic": array[60]
            })
            current_index += 61

        vmd.light_keyframe_number = int.from_bytes(array[current_index: current_index+4], byteorder="little", signed=False)
        current_index += 4

        for i in range(vmd.light_keyframe_number):
            vmd.light_keyframe_record.append({
                'FrameTime': struct.unpack("<I", array[current_index: current_index+4])[0],
                'Color': {
                    'r': struct.unpack("<f", array[current_index+4: current_index+8])[0],
                    'g': struct.unpack("<f", array[current_index+8: current_index+12])[0],
                    'b': struct.unpack("<f", array[current_index+12: current_index+16])[0]
                },
                'Direction':{"x": struct.unpack("<f", array[current_index+16: current_index+20])[0],
                            "y": struct.unpack("<f", array[current_index+20: current_index+24])[0],
                            "z": struct.unpack("<f", array[current_index+24: current_index+28])[0]
                            }
            })
            current_index += 28

        vmd_dict = {}
        # vmd_dict['Vision'] = vision
        # vmd_dict['ModelName'] = vmd.model_name
        # vmd_dict['BoneKeyFrameNumber'] = vmd.bone_keyframe_number
        # vmd_dict['BoneKeyFrameRecord'] = vmd.bone_keyframe_record
        # vmd_dict['MorphKeyFrameNumber'] = vmd.morph_keyframe_number
        vmd_dict['MorphKeyFrameRecord'] = vmd.morph_keyframe_record
        # vmd_dict['CameraKeyFrameNumber'] = vmd.camera_keyframe_number
        # vmd_dict['CameraKeyFrameRecord'] = vmd.camera_keyframe_record
        # vmd_dict['LightKeyFrameNumber'] = vmd.light_keyframe_number
        # vmd_dict['LightKeyFrameRecord'] = vmd.light_keyframe_record

        vmd.dict = vmd_dict
#感谢crossous的vmd格式读取解析代码https://mmdybk.gitee.io/md/用python解析VMD格式读取/
        return vmd
if __name__ == '__main__':
    filename = filedialog.askopenfilename(filetypes = [("Text", "*.vmd")])
    vmd = Vmd.from_file(filename, model_name_encode="gb2312")
    from pprint import pprint
    pprint(vmd.morph_keyframe_record)
#######
#感谢Saki_Ryou的转换表
    str_array = ["ADMIRATION", "感嘆", "ADMIRATION_CL", "まばたき", "ADMIRATION_OLD", "感嘆２", "ADMIRATION_OLD_CL", "まばたき", "CLARIFYING", "真面目", "CLARIFYING_CL", "まばたき", "CLARIFYING_OLD", "真面目２", "CLARIFYING_OLD_CL", "まばたき", "CLOSE", "まばたき", "CLOSE_OLD", "まばたき", "COOL", "COOL", "COOL_CL", "まばたき", "CRY", "CRY", "CRY_OLD", "CRY_OLD", "DAZZLING", "DAZZLING", "DAZZLING_CL", "まばたき", "DAZZLING_OLD", "DAZZLING_OLD", "DAZZLING_OLD_CL", "まばたき", "EYEBROW_UP_LEFT", "眉上", "EYEBROW_UP_LEFT_CL", "まばたき", "EYEBROW_UP_RIGHT", "眉上右", "EYEBROW_UP_RIGHT_CL", "まばたき", "GENKI", "元気", "GENKI_CL", "まばたき", "GENKI_OLD", "元気２", "GENKI_OLD_CL", "まばたき", "GENTLE", "優しい", "GENTLE_CL", "まばたき", "GENTLE_OLD", "優しい２", "GENTLE_OLD_CL", "まばたき", "KIRI", "きり", "KIRI_CL", "まばたき", "KIRI_OLD", "きり２", "KIRI_OLD_CL", "まばたき", "KOMARIEGAO", "困り顔", "KOMARIWARAI", "困る", "KOMARIWARAI_CL", "まばたき", "KONWAKU", "困惑", "KONWAKU_CL", "まばたき", "KUMON", "苦悶", "KUMON_CL", "まばたき", "KUTSUU", "苦痛", "KUTSUU_CL", "まばたき", "LASCIVIOUS", "ジト目", "LASCIVIOUS_CL", "まばたき", "LASCIVIOUS_OLD", "ジト目", "LASCIVIOUS_OLD_CL", "まばたき", "LAUGH", "笑い", "LAUGH_OLD", "笑い", "NAGASI", "眼角上", "NAGASI_CL", "まばたき", "NAGASI_OLD", "眼角上２", "NAGASI_OLD_CL", "まばたき", "NAKI", "泣き", "NAKI_CL", "泣き闭", "NAYAMI", "悩み", "NAYAMI_CL", "まばたき", "NEW_IKARI", "怒り", "NEW_IKARI_CL", "まばたき", "NEW_IKARI_OLD", "怒り", "NEW_IKARI_OLD_CL", "まばたき", "NIRAMI_OLD", "睨み", "NIRAMI_OLD_CL", "まばたき", "OMOU", "思う", "OMOU_CL", "まばたき", "OMOU_OLD", "思う２", "OMOU_OLD_CL", "まばたき", "RESET", "RESET", "RESET_OLD", "RESET_OLD", "SAD", "悲しい", "SAD_CL", "まばたき", "SAD_OLD", "悲しい２", "SAD_OLD_CL", "まばたき", "SETTLED", "平然に", "SETTLED_CL", "まばたき", "SETTLED_OLD", "平然に２", "SETTLED_OLD_CL", "まばたき", "SETUNA", "せつな", "SETUNA_CL", "まばたき", "SETUNA_OLD", "じと目", "SETUNA_OLD_CL", "まばたき", "SMILE", "にこり", "SMILE_CL", "まばたき", "SMILE_OLD", "にこり", "SMILE_OLD_CL", "まばたき", "STRONG", "STRONG", "STRONG_CL", "まばたき", "STRONG_OLD", "STRONG_OLD", "STRONG_OLD_CL", "まばたき", "SUPSERIOUS", "びっくり", "SUPSERIOUS_CL", "まばたき", "SURPRISE", "びっくり", "SURPRISE_CL", "まばたき", "SURPRISE_OLD", "びっくり", "SURPRISE_OLD_CL", "まばたき", "TSUYOKIWARAI", "強気笑い", "TSUYOKIWARAI_CL", "まばたき", "UTURO", "じと目", "UTURO_CL", "まばたき", "UTURO_OLD", "きり", "UTURO_OLD_CL", "まばたき", "WINK", "ウィンク", "WINKG_L", "ウィンク左", "WINKG_R", "ウィンク右", "WINK_FT_CL", "まばたき", "WINK_FT_OLD_CL", "まばたき", "WINK_L", "ウィンク左", "WINK_L_OLD", "ウィンク左", "WINK_OLD", "ウィンク", "WINK_R", "ウィンク右", "WINK_R_OLD", "ウィンク右", "YARU", "殺す", "YARU_CL", "まばたき", "YARU_OLD", "殺す２", "YARU_OLD_CL", "まばたき", "M_A", "あ", "M_A_OLD", "あ", "M_CHU", "ちゅ", "M_CHU_OLD", "う", "M_E", "え", "M_E_OLD", "え", "M_E_DOWN", "M_E_DOWN", "M_HAMISE", "い２", "M_HAMISE_DOWN", "はみせ", "M_HAMISE_E", "はみせ２", "M_HE", "ん", "M_HE_OLD", "口横狭め", "M_HE_S", "ん", "M_HERAHERA", "へらへら", "M_I", "い", "M_I_OLD", "い", "M_MOGUMOGU", "モグモグ", "M_NEKO", "ω", "M_NEUTRAL", "口角上げ", "M_NIYA", "にやにや", "M_NIYA_OLD", "にやにや", "M_O", "お", "M_O_OLD", "お", "M_PSP_A", "あ", "M_PSP_E", "え", "M_PSP_NIYA", "にや", "M_PSP_NIYARI", "にやり", "M_PSP_O", "お", "M_PSP_SURPRISE", "え２", "M_SAKEBI", "あ２", "M_SAKEBI_L", "あ", "M_SANKAKU", "▲", "M_SHIKAKU", "◆", "M_SMILE", "え", "M_SMILE_OLD", "え", "M_SMILE_L", "え", "M_SURPRISE", "え２", "M_SURPRISE_OLD", "え２", "M_U", "う", "M_U_OLD", "う"]
#######
#感谢stewie的id表
    str_mouth = ["M_A", "M_E", "M_O", "M_SURPRISE", "M_HE", "M_SMILE", "M_NIYA", "M_CHU", "M_RESET", "M_RESET_OLD", "M_I", "M_U", "M_E_DOWN", "M_HAMISE", "M_HAMISE_DOWN", "M_HE_S", "M_HERAHERA", "M_RESET", "M_MOGUMOGU", "M_SAKEBI", "M_SAKEBI_L", "M_SMILE_L", "M_NEUTRAL", "M_NIYA_OLD", "M_A_OLD", "M_O_OLD", "M_SURPRISE_OLD", "M_HE_OLD", "M_RESET_OLD", "M_I_OLD", "M_U_OLD", "M_E_OLD", "M_SMILE_OLD", "M_CHU_OLD", "M_PSP_A", "M_PSP_E", "M_PSP_O", "M_PSP_SURPRISE", "M_PSP_NIYA", "M_PSP_NIYARI", "M_HAMISE_E", "M_SANKAKU", "M_SHIKAKU"]
#######
    str_expre = ["SAD", "LAUGH", "CRY", "SURPRISE", "WINK_OLD", "ADMIRATION", "SMILE", "SETTLED", "DAZZLING", "LASCIVIOUS", "STRONG", "CLARIFYING", "GENTLE", "NAGASI", "RESET", "KIRI", "UTURO", "OMOU", "SETUNA", "GENKI", "YARU", "RESET", "CLOSE", "null", "FACE MOT INDEX 0", "FACE MOT INDEX 1", "FACE MOT INDEX 2", "FACE MOT INDEX 3", "FACE MOT INDEX 4", "FACE MOT INDEX 5", "FACE MOT INDEX 6", "FACE MOT INDEX 7", "FACE MOT INDEX 8", "FACE MOT INDEX 9", "COOL", "KOMARIWARAI", "KUMON", "KUTSUU", "NAKI", "NAYAMI", "SUPSERIOUS", "TSUYOKIWARAI", "WINK_L", "WINK_R", "WINKG_L", "WINKG_R", "RESET", "RESET", "RESET", "RESET", "RESET", "WINK_OLD", "SAD_OLD", "SURPRISE_OLD", "SMILE_OLD", "DAZZLING_OLD", "LASCIVIOUS_OLD", "STRONG_OLD", "CLARIFYING_OLD", "GENTLE_OLD", "NAGASI_OLD", "KIRI_OLD", "OMOU_OLD", "SETUNA_OLD", "NEW_IKARI_OLD", "CRY_OLD", "LAUGH_OLD", "YARU_OLD", "ADMIRATION_OLD", "GENKI_OLD", "SETTLED_OLD", "UTURO_OLD", "RESET_OLD", "CLOSE_OLD", "EYEBROW_UP_RIGHT", "EYEBROW_UP_LEFT", "KOMARIEGAO", "KONWAKU"]
#######
    print(vmd.morph_keyframe_record[1]['MorphName'])
    print(str_array[1])
    #将vmd表情转diva
    for i in range(vmd.morph_keyframe_number):
        for s,sb in enumerate(str_array):
            if vmd.morph_keyframe_record[i]['MorphName']==str_array[s]:
             vmd.morph_keyframe_record[i]['MorphName']=str_array[s-1]
             print(vmd.morph_keyframe_record[i]['MorphName'])
             break
    #编写dsc
    xb=1
    pianyizi=0
    str_text = []
    for i in range(vmd.morph_keyframe_number):
        xa = 1
        for s,sb in enumerate(str_mouth):
            if vmd.morph_keyframe_record[i]['MorphName']==str_mouth[s]:
                # if vmd.morph_keyframe_record[i]['Weight']== 0 :
                #     break
                pianyizi+=1
                text1 = 'TIME('+str(vmd.morph_keyframe_record[i]['FrameTime'] * 3333+pianyizi)+');\n'
                text2 ='MOUTH_ANIM('+str(type)+', 0,' +str(s)+ ' , '+str(trans)+', '+str(vmd.morph_keyframe_record[i]['Weight'] * 1000)+');\n'
                xa =0
                break
        if xa == 1 :
            for s,sb in enumerate(str_expre):
                if vmd.morph_keyframe_record[i]['MorphName']==str_expre[s]:
                    # if vmd.morph_keyframe_record[i]['Weight']== 0 :
                    #     break
                    pianyizi+=1
                    if vmd.morph_keyframe_record[i]['FrameTime'] * 3333+pianyizi==1217309:
                        print(1)
                    text1 = 'TIME('+str(vmd.morph_keyframe_record[i]['FrameTime'] * 3333+pianyizi)+');\n'
                    text2 ='EXPRESSION('+str(type)+', ' +str(s)+ ', '+str(trans)+', '+str(vmd.morph_keyframe_record[i]['Weight'] * 1000)+');\n'
                    break
        # str_text[i] = text1 + '\n' + text2
        # str_text.append(text1 + "\n" + text2)
        # 长数据纠错：
        if 'text1' in locals():
            if xb==1:
                str_text.append(text1 + text2)
                xb=0
            elif xb==0:
                if str(text1 + text2)!=str_text[-1]:
                    str_text.append(text1 + text2)
        text = ''.join(str_text)
        # pai xu time# str_list = str_text.split('\n')# numbers = sorted([int(re.findall(r'\d+', x)[0]) for x in text1 if re.findall(r'\d+', x)])# sorted_str_mixed = ' '.join([x[1] for x in sorted(numbers, key=lambda x: x[0])])# 分析并重新组织文本，以确保时间是递增的
######################
#感谢Leua的代码，省了好多事
# print(asp38(example_text)) 作者：Leua https://www.bilibili.com/read/cv29516422/?spm_id_from=333.999.0.0 出处：bilibili
# 将原始文本分割为单独的行
    lines = text.strip().split('\n')
    # i = 0
    # while i < len(lines):
    #     if lines[i].startswith('TIME(') and i + 1 < len(lines) and lines[i + 1].strip() == '':
    #         del lines[i:i + 2]  # 删除时间行及其后的空行
    #     else:
    #         i += 1
    # 处理每一行，将时间和动画行分开
    time_anim_pairs = []
    for i in range(0, len(lines), 2):
        time = int(lines[i].split('(')[1].split(')')[0])
        anim = lines[i + 1]
        time_anim_pairs.append((time, anim))

    # 检查时间序列并进行线性修复
    for i in range(1, len(time_anim_pairs)):
        if time_anim_pairs[i][0] < time_anim_pairs[i - 1][0]:
            # 找到前一个时间点
            start_index = i - 1
            while start_index > 0 and time_anim_pairs[start_index][0] > time_anim_pairs[i][0]:
                start_index -= 1

            # 计算新的时间间隔
            start_time = time_anim_pairs[start_index][0]
            end_time = time_anim_pairs[i][0]
            num_intervals = i - start_index
            time_interval = (end_time - start_time) // num_intervals

            # 修复时间
            for j in range(start_index + 1, i):
                new_time = start_time + time_interval * (j - start_index)
                time_anim_pairs[j] = (new_time, time_anim_pairs[j][1])

    # 格式化为原始格式输出
    fixed_text = '\n'.join([f"TIME({time});\n{anim}" for time, anim in time_anim_pairs])
################

    print(fixed_text)
######################################################################
#     # 使用filedialog.asksaveasfilename获取用户选择的文件名
#     filename = filedialog.asksaveasfilename(title="Select file",filetypes=(("text files", "*.txt"), ("all files", "*.*")),initialfile="vmd to diva.txt")
# # 使用'w'模式打开文件，如果文件已存在则会被覆盖
# with open(filename, 'w') as f:
#     # 使用json.dumps将字典转换为字符串，然后写入到文件中
#     f.write(json.dumps(vmd.morph_keyframe_record, ensure_ascii=False, indent=4))
######################################################################
 # 使用filedialog.asksaveasfilename获取用户选择的文件名
    filename = filedialog.asksaveasfilename(title="Select file",filetypes=(("text files", "*.txt"), ("all files", "*.*")),initialfile="dsc.txt")
# 使用'w'模式打开文件，如果文件已存在则会被覆盖
with open(filename, 'w') as f:
# 使用json.dumps将字典转换为字符串，然后写入到文件中
    f.write(fixed_text)