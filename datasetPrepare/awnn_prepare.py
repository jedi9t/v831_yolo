import os
import shutil

# 路径设置
val_txt_path = "ImageSets/Main/val.txt"
jpeg_images_path = "JPEGImages"
destination_path = "awnn/images"

# 确保目标目录存在
os.makedirs(destination_path, exist_ok=True)

# 读取 val.txt 文件并将内容放入列表
with open(val_txt_path, 'r') as file:
    file_list = file.read().splitlines()

# 遍历列表并复制文件
for filename in file_list:
    source_file = os.path.join(jpeg_images_path, filename + ".jpg")
    destination_file = os.path.join(destination_path, filename + ".jpg")

    # 复制文件
    shutil.copy(source_file, destination_file)
    print(f"Copied {source_file} to {destination_file}")
