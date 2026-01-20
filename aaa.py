import re

input_path = r"C:\Users\godv\Desktop\1.天下就没有偶然，那不过是化了妆的戴了面具的必然。.txt"
output_path = r"C:\Users\godv\Desktop\aaa.txt"

with open(input_path, "r", encoding="utf-8") as f:
    content = f.read()

# 去掉每一行开头的“数字 + .”
result = re.sub(r'^\d+\.', '', content, flags=re.MULTILINE)

with open(output_path, "w", encoding="utf-8") as f:
    f.write(result)

print("处理完成，已生成 aaa.txt")
