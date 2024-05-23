# 分析并重新组织文本，以确保时间是递增的
from fileinput import filename
from tkinter import filedialog

filename = filedialog.askopenfilename()
with open(filename, 'r',encoding='utf-8') as f:
    example_text = f.read()
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
filename = filedialog.asksaveasfilename(title="Select file",filetypes=(("text files", "*.txt"), ("all files", "*.*")),initialfile="asp38.txt")
with open(filename, 'w') as f:
    f.write(fixed_text) 
# 原作者：Leua https://www.bilibili.com/read/cv29516422/?spm_id_from=333.999.0.0 出处：bilibili 有删改