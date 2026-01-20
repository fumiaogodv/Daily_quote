input_path = r"C:\Users\godv\Desktop\aaa.txt"
output_path = r"C:\Users\godv\Desktop\bbb.txt"

with open(input_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

# 删除空行（包括只含空白字符的行）
non_empty_lines = [line for line in lines if line.strip() != ""]

with open(output_path, "w", encoding="utf-8") as f:
    f.writelines(non_empty_lines)

print("处理完成，已生成 bbb.txt")
