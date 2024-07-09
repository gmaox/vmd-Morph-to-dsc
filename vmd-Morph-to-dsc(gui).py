# -*- coding: utf-8 -*-
import re
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser

filenamea = 0
# 定义处理函数
def process_file(input_file):
    asdad(text_box.get("1.0", tk.END).strip())
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
        filename = input_file
        try:
            vmd = Vmd.from_file(filename, model_name_encode="gb2312")
        except Exception as e:
            try:
                print("编码方式改变，可能需要些时间(Changing the encoding method may take some time)")
                vmd = Vmd.from_file(filename, model_name_encode="utf-16")
            except Exception as e:
                print("编码方式改变，可能需要些时间(Changing the encoding method may take some time)")
                vmd = Vmd.from_file(filename)
        from pprint import pprint
        pprint(vmd.morph_keyframe_record)
    #######
    #感谢Saki_Ryou的转换表
        print(str_array)
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
        if bianlianga.get()==0:buzhenjianshu=100
        for i in range(vmd.morph_keyframe_number):
            xa = 1
            for s,sb in enumerate(str_mouth):
                if vmd.morph_keyframe_record[i]['MorphName']==str_mouth[s]:
                    # if vmd.morph_keyframe_record[i]['Weight']== 0 :
                    #     break
                    pianyizi+=1
                    text1 = 'TIME('+str(int(vmd.morph_keyframe_record[i]['FrameTime'] * 3333+pianyizi))+');\n'
                    if bianlianga.get()==1:
                        buzhenjianshu = (vmd.morph_keyframe_record[i]['FrameTime']-vmd.morph_keyframe_record[i-1]['FrameTime'])*33
                        if buzhenjianshu < 0 : buzhenjianshu = 0
                    text2 ='MOUTH_ANIM('+str(jue_se.get())+', 0,' +str(s)+ ' , '+str(int(buzhenjianshu))+', '+str(int(vmd.morph_keyframe_record[i]['Weight'] * 1000))+');\n'
                    xa =0
                    break
            if xa == 1 :
                for s,sb in enumerate(str_expre):
                    if vmd.morph_keyframe_record[i]['MorphName']==str_expre[s]:
                        # if vmd.morph_keyframe_record[i]['Weight']== 0 :
                        #     break
                        pianyizi+=1
                        text1 = 'TIME('+str(int(vmd.morph_keyframe_record[i]['FrameTime'] * 3333+pianyizi))+');\n'
                        if bianlianga.get()==1:
                            buzhenjianshu = (vmd.morph_keyframe_record[i]['FrameTime']-vmd.morph_keyframe_record[i-1]['FrameTime'])*33
                            if buzhenjianshu < 0 : buzhenjianshu = 0
                        text2 ='EXPRESSION('+str(jue_se.get())+', ' +str(s)+ ', '+str(int(buzhenjianshu))+', '+str(int(vmd.morph_keyframe_record[i]['Weight'] * 1000))+');\n'
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
        time_anim_pairs = []
        for i in range(0, len(lines), 2):
            time = int(lines[i].split('(')[1].split(')')[0])
            anim = lines[i + 1]
            time_anim_pairs.append((time, anim))
    
        # gpt--假设time_anim_pairs是一个元组列表，每个元组的第一个元素是排序的关键字
        time_anim_pairs.sort(key=lambda x: x[0])
    
        # 打印成功消息
        print("time_anim_pairs已经成功排序。")
    
    
    
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
        filenamea = filedialog.asksaveasfilename(title="Select file",filetypes=(("text files", "*.txt"), ("all files", "*.*")),initialfile="dsc"+str(jue_se.get())+".txt")
    with open(filenamea, 'w') as f:
        f.write(fixed_text)
    global afilenamea
    afilenamea=filenamea
    subprocess.run(["start", filenamea], shell=True)
    #Pyinstaller -F vmd-Morph-to-dsc.py
    return '完成'

# 定义刷新并保存文本框内容的函数
def fwread():
    # 获取文本框内容
    content = text_box.get("1.0", tk.END).strip()
    # 处理文本框内容（例如，打印到控制台）
    print(f"文本框内容: {content}")
    # 在这里可以保存到文件或执行其他操作
    return content

# 选择输入文件
def select_input_file():
    file_path = filedialog.askopenfilename(filetypes = [("file", "*.vmd")])
    input_file_path.set(file_path)
    result_var.set("")  # 清空之前的结果

# 选择并读取TXT文件，填入文本框
def open_txt_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            asdad(content)
            text_box.delete("1.0", tk.END)  # 清空文本框
            text_box.insert(tk.END, content)  # 插入文件内容
        except UnicodeDecodeError:
            messagebox.showerror("错误", "无法解码文件，请选择一个有效的UTF-8编码文件")
#
def asdad(content):
    fwread=content.replace('\n','')
    global str_array
    str_array = re.split('[—]',fwread)
    print(str_array)
# 保存文本框内容到文件
def save_text():
    content = fwread()
    file_path = filedialog.asksaveasfilename(filetypes=[("Text Files", "*.txt")],initialfile="diva-morph.txt")
    if file_path:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        messagebox.showinfo("信息", "文件保存成功")

# 执行文件处理
def execute():
    input_file = input_file_path.get()
    if not input_file:
        select_input_file()
        input_file = input_file_path.get()
    # 保存文本框内容
    fwread()
    result = process_file(input_file)
    result_var.set(result)

# 创建主窗口
root = tk.Tk()
root.title("文件处理器")

# 输入文件路径
input_file_path = tk.StringVar()
tk.Label(root, text="选择输入文件:").grid(row=0, column=0, padx=10, pady=10)
tk.Entry(root, textvariable=input_file_path, width=50).grid(row=0, column=1, padx=10, pady=10)
tk.Button(root, text="浏览", command=select_input_file).grid(row=0, column=2, padx=10, pady=10)

str_array = ["ADMIRATION", "感嘆", "ADMIRATION_CL", "まばたき", "ADMIRATION_OLD", "感嘆２", "ADMIRATION_OLD_CL", "まばたき", "CLARIFYING", "真面目", "CLARIFYING_CL", "まばたき", "CLARIFYING_OLD", "真面目２", "CLARIFYING_OLD_CL", "まばたき", "CLOSE", "まばたき", "CLOSE_OLD", "まばたき", "COOL", "COOL", "COOL_CL", "まばたき", "CRY", "CRY", "CRY_OLD", "CRY_OLD", "DAZZLING", "DAZZLING", "DAZZLING_CL", "まばたき", "DAZZLING_OLD", "DAZZLING_OLD", "DAZZLING_OLD_CL", "まばたき", "EYEBROW_UP_LEFT", "眉上", "EYEBROW_UP_LEFT_CL", "まばたき", "EYEBROW_UP_RIGHT", "眉上右", "EYEBROW_UP_RIGHT_CL", "まばたき", "GENKI", "元気", "GENKI_CL", "まばたき", "GENKI_OLD", "元気２", "GENKI_OLD_CL", "まばたき", "GENTLE", "優しい", "GENTLE_CL", "まばたき", "GENTLE_OLD", "優しい２", "GENTLE_OLD_CL", "まばたき", "KIRI", "きり", "KIRI_CL", "まばたき", "KIRI_OLD", "きり２", "KIRI_OLD_CL", "まばたき", "KOMARIEGAO", "困り顔", "KOMARIWARAI", "困る", "KOMARIWARAI_CL", "まばたき", "KONWAKU", "困惑", "KONWAKU_CL", "まばたき", "KUMON", "苦悶", "KUMON_CL", "まばたき", "KUTSUU", "苦痛", "KUTSUU_CL", "まばたき", "LASCIVIOUS", "ジト目", "LASCIVIOUS_CL", "まばたき", "LASCIVIOUS_OLD", "ジト目", "LASCIVIOUS_OLD_CL", "まばたき", "LAUGH", "笑い", "LAUGH_OLD", "笑い", "NAGASI", "眼角上", "NAGASI_CL", "まばたき", "NAGASI_OLD", "眼角上２", "NAGASI_OLD_CL", "まばたき", "NAKI", "泣き", "NAKI_CL", "泣き闭", "NAYAMI", "悩み", "NAYAMI_CL", "まばたき", "NEW_IKARI", "怒り", "NEW_IKARI_CL", "まばたき", "NEW_IKARI_OLD", "怒り", "NEW_IKARI_OLD_CL", "まばたき", "NIRAMI_OLD", "睨み", "NIRAMI_OLD_CL", "まばたき", "OMOU", "思う", "OMOU_CL", "まばたき", "OMOU_OLD", "思う２", "OMOU_OLD_CL", "まばたき", "RESET", "RESET", "RESET_OLD", "RESET_OLD", "SAD", "悲しい", "SAD_CL", "まばたき", "SAD_OLD", "悲しい２", "SAD_OLD_CL", "まばたき", "SETTLED", "平然に", "SETTLED_CL", "まばたき", "SETTLED_OLD", "平然に２", "SETTLED_OLD_CL", "まばたき", "SETUNA", "せつな", "SETUNA_CL", "まばたき", "SETUNA_OLD", "じと目", "SETUNA_OLD_CL", "まばたき", "SMILE", "にこり", "SMILE_CL", "まばたき", "SMILE_OLD", "にこり", "SMILE_OLD_CL", "まばたき", "STRONG", "STRONG", "STRONG_CL", "まばたき", "STRONG_OLD", "STRONG_OLD", "STRONG_OLD_CL", "まばたき", "SUPSERIOUS", "びっくり", "SUPSERIOUS_CL", "まばたき", "SURPRISE", "びっくり", "SURPRISE_CL", "まばたき", "SURPRISE_OLD", "びっくり", "SURPRISE_OLD_CL", "まばたき", "TSUYOKIWARAI", "強気笑い", "TSUYOKIWARAI_CL", "まばたき", "UTURO", "じと目", "UTURO_CL", "まばたき", "UTURO_OLD", "きり", "UTURO_OLD_CL", "まばたき", "WINK", "ウィンク", "WINKG_L", "ウィンク左", "WINKG_R", "ウィンク右", "WINK_FT_CL", "まばたき", "WINK_FT_OLD_CL", "まばたき", "WINK_L", "ウィンク左", "WINK_L_OLD", "ウィンク左", "WINK_OLD", "ウィンク", "WINK_R", "ウィンク右", "WINK_R_OLD", "ウィンク右", "YARU", "殺す", "YARU_CL", "まばたき", "YARU_OLD", "殺す２", "YARU_OLD_CL", "まばたき", "M_A", "あ", "M_A_OLD", "あ", "M_CHU", "ちゅ", "M_CHU_OLD", "う", "M_E", "え", "M_E_OLD", "え", "M_E_DOWN", "M_E_DOWN", "M_HAMISE", "い２", "M_HAMISE_DOWN", "はみせ", "M_HAMISE_E", "はみせ２", "M_HE", "ん", "M_HE_OLD", "口横狭め", "M_HE_S", "ん", "M_HERAHERA", "へらへら", "M_I", "い", "M_I_OLD", "い", "M_MOGUMOGU", "モグモグ", "M_NEKO", "ω", "M_NEUTRAL", "口角上げ", "M_NIYA", "にやにや", "M_NIYA_OLD", "にやにや", "M_O", "お", "M_O_OLD", "お", "M_PSP_A", "あ", "M_PSP_E", "え", "M_PSP_NIYA", "にや", "M_PSP_NIYARI", "にやり", "M_PSP_O", "お", "M_PSP_SURPRISE", "え２", "M_SAKEBI", "あ２", "M_SAKEBI_L", "あ", "M_SANKAKU", "▲", "M_SHIKAKU", "◆", "M_SMILE", "え", "M_SMILE_OLD", "え", "M_SMILE_L", "え", "M_SURPRISE", "え２", "M_SURPRISE_OLD", "え２", "M_U", "う", "M_U_OLD", "う"]
atxt = '—\n\n'.join('—\n'.join(str_array[i:i+2]) for i in range(0, len(str_array), 2))


# 文本框
tk.Label(root, text="字典文本框:").grid(row=1, column=0, padx=10, pady=10)
text_box = tk.Text(root, width=60, height=5)
text_box.grid(row=1, column=1, padx=10, pady=10, columnspan=2)
text_box.insert(tk.END, atxt)

# 打开TXT文件按钮
tk.Button(root, text="打开字典TXT文件", command=open_txt_file).grid(row=2, column=1, pady=10)

# 保存文本按钮
tk.Button(root, text="保存字典文本（退出前请务必保存）", command=save_text).grid(row=3, column=1, pady=10)




class ArrayEditorWindow:
    def __init__(self, parent, array):
        self.parent = parent
        self.array = array
        self.create_widgets()

    def create_widgets(self):
        self.top_frame = tk.Frame(self.parent)
        self.top_frame.pack(padx=10, pady=10)

        self.search_var = tk.StringVar()
        tk.Label(self.top_frame, text="搜索(结果高亮):").grid(row=0, column=0, padx=5, pady=5)
        self.search_entry = tk.Entry(self.top_frame, textvariable=self.search_var, width=20)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)
        search_button = tk.Button(self.top_frame, text="查找", command=self.search_text)
        search_button.grid(row=0, column=2, padx=5, pady=5)

        self.canvas = tk.Canvas(self.parent)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.parent, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor=tk.NW)

        self.text_boxes = []
        for i, item in enumerate(self.array):
            row = i // 2
            col = i % 2
            # label = tk.Label(self.scrollable_frame, text=item)
            # label.grid(row=row, column=col, padx=5, pady=5)
            text_box = tk.Text(self.scrollable_frame, width=30, height=3)
            text_box.insert(tk.END, item)
            text_box.grid(row=row + 1, column=col, padx=5, pady=5)
            self.text_boxes.append(text_box)

        # 返回按钮
        back_button = tk.Button(self.parent, text="保存返回", command=self.save_and_close)
        back_button.pack(pady=10)

        self.scrollable_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def search_text(self):
        search_term = self.search_var.get().strip()
        if search_term:
            for text_box in self.text_boxes:
                text = text_box.get("1.0", tk.END).strip()
                if search_term in text:
                    text_box.tag_configure("highlight", background="yellow")
                    text_box.tag_add("highlight", "1.0", tk.END)
                else:
                    text_box.tag_remove("highlight", "1.0", tk.END)

    def save_and_close(self):
        for i, text_box in enumerate(self.text_boxes):
            updated_text = text_box.get("1.0", tk.END).strip()
            self.array[i] = updated_text
        asdfg()
        self.parent.destroy()
def asdfg():
    content = '—\n\n'.join('—\n'.join(str_array[i:i+2]) for i in range(0, len(str_array), 2))
    text_box.delete("1.0", tk.END)  # 清空文本框
    text_box.insert(tk.END, content)  # 插入文件内容
def open_editor_window():
    asdad(text_box.get("1.0", tk.END).strip())
    editor_window = tk.Toplevel(root)
    editor_window.geometry("500x850")
    editor_window.title("字典编辑器窗口（直接关闭窗口不保存）")
    editor = ArrayEditorWindow(editor_window, str_array)
edit_button = tk.Button(root, text="处理字典文本数据", command=open_editor_window).grid(row=4, column=1, pady=0)
# 定义变量
bianlianga = tk.IntVar(value=1)
jue_se = tk.IntVar(value=1)  # 默认值为1

# 定义复选框回调函数
def update_var():
    if bianlianga.get() == 1:
        print("Checked: bianlianga =", bianlianga.get())
    else:
        print("Unchecked: bianlianga =", bianlianga.get())

# 定义 Spinbox 回调函数
def update_vara():
    selected_value = spinbox.get()
    if selected_value:
        jue_se.set(int(selected_value))
        print("当前选择的数字是:", jue_se.get())

# 创建复选框并设置回调函数
checkbox = tk.Checkbutton(root, text="勾选后计算补帧间数（实验性）", variable=bianlianga, command=update_var)
checkbox.grid(row=5, column=1, pady=5)

# 创建 Spinbox 组件，选择范围为1到6
tk.Label(root, text="选择角色:").grid(row=4, column=0, padx=10, pady=10)
spinbox = tk.Spinbox(root, from_=1, to=6, textvariable=jue_se, width=3, command=update_vara)
spinbox.grid(row=5, column=0, pady=0)

tk.Button(root, text="开始执行\nvmd-Morph-to-dsc", command=execute).grid(row=6, column=1, pady=0)

# 结果显示
result_var = tk.StringVar()
tk.Label(root, textvariable=result_var).grid(row=7, column=0, columnspan=3, padx=10, pady=10)

def dscedit():
    webbrowser.open('https://nastys.github.io/dsceditor/')
tk.Button(root, text="  打开\n     dsc编辑器    ", command=dscedit).place(x=120, y=319)
def edit():
    subprocess.run(["start", afilenamea], shell=True)
tk.Button(root, text="打开\n    处理后文件     ", command=edit).place(x=360, y=319)

# 定义按钮点击事件处理函数，用于打开新窗口
def open_new_window():
    new_window = tk.Toplevel(root)
    new_window.title("多人时间自动排序（实验性）")
    
    # 添加文本框：输入文本框
    tk.Label(new_window, text="所有dsc文本粘贴此处（ctrl+V）:").grid(row=1, column=1, pady=10)
    text_Text = tk.Text(new_window, width=60, height=10)
    text_Text.grid(row=2, column=1, pady=10)
    
    # 添加文本框：结果显示文本框
    tk.Label(new_window, text="结果显示（ctrl+A，ctrl+C）：").grid(row=4, column=1, pady=10)
    jieguo_Text = tk.Text(new_window, width=60, height=10)
    jieguo_Text.grid(row=5, column=1, pady=10)
    
    def asp38():
        global fixed_text
        example_text = text_Text.get("1.0", tk.END).strip()
        # 将原始文本分割为单独的行
        lines = example_text.strip().split('\n')
        # 处理每一行，将时间和动画行分开
        time_anim_pairs = []
        for i in range(0, len(lines), 2):
            time = int(lines[i].split('(')[1].split(')')[0])
            anim = lines[i + 1]
            time_anim_pairs.append((time, anim))
        time_anim_pairs.sort(key=lambda x: x[0])
        # 格式化为原始格式输出
        fixed_text = '\n'.join([f"TIME({time});\n{anim}" for time, anim in time_anim_pairs])
        print(fixed_text)
        jieguo_Text.delete("1.0", tk.END)  
        jieguo_Text.insert(tk.END, fixed_text)
    
    tk.Button(new_window, text="开始排序", command=asp38).grid(row=3, column=1, pady=10)
    def baocun():
        filenamea = filedialog.asksaveasfilename(title="Select file",filetypes=(("text files", "*.txt"), ("all files", "*.*")),initialfile="dsc0.txt")
        with open(filenamea, 'w') as f:
            f.write(fixed_text)
        subprocess.run(["start", filenamea], shell=True)
    tk.Button(new_window, text="保存为txt", command=baocun).grid(row=6, column=1, pady=10)

# 创建按钮，点击按钮时打开新窗口
tk.Button(root, text="asp38\n多人排序工具", command=open_new_window).place(x=10, y=319)
# 运行主循环
root.mainloop()
