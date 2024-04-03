import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET

img_path_old = r'D:\BaiduNetdiskDownload\door\dataset\images'  # 原图片文件夹路径
img_path_new = r'D:\BaiduNetdiskDownload\dataset\door\images' # 修改大小后的图片文件夹路径
xml_path_old = r'D:\BaiduNetdiskDownload\door\dataset\xml'   # 原xml的文件夹路径
xml_path_new = r'D:\BaiduNetdiskDownload\dataset\door\xml'  # 新xml的文件夹路径
if not os.path.exists(img_path_new): os.makedirs(img_path_new)
if not os.path.exists(xml_path_new): os.makedirs(xml_path_new)
c_w, c_h = 320, 240  # 目标图片的尺寸

def edit_xml(xml_file, ratio, i):
    all_xml_file = os.path.join(xml_path_old, xml_file)
    # print(all_xml_file)
    tree = ET.parse(all_xml_file)
    size_o = tree.find('size') # 修改xml文件中的图像尺寸大小为新的尺寸大小
    size_width = size_o.find('width')
    size_height = size_o.find('height')
    size_width.text = str(c_w)
    size_height.text = str(c_h)

    obj_filename = tree.find('filename')
    obj_filename.text = str(i)+ '.jpg'

    objs = tree.findall('object') # 修改每个目标对应的坐标
    for obj in objs:
        obj_bnd = obj.find('bndbox')
        obj_bnd = obj.find('bndbox')
        obj_xmin = obj_bnd.find('xmin')
        obj_ymin = obj_bnd.find('ymin')
        obj_xmax = obj_bnd.find('xmax')
        obj_ymax = obj_bnd.find('ymax')
        xmin = float(obj_xmin.text)
        ymin = float(obj_ymin.text)
        xmax = float(obj_xmax.text)
        ymax = float(obj_ymax.text)
        obj_xmin.text = str(round(xmin * ratio))
        obj_ymin.text = str(round(ymin * ratio))
        obj_xmax.text = str(round(xmax * ratio))
        obj_ymax.text = str(round(ymax * ratio))

    newfile = os.path.join(xml_path_new, str(i)+'.xml')
    tree.write(newfile, method='xml', encoding='utf-8')  # 更新xml文件
    print ('new xml genereated:'+newfile)

if __name__ == '__main__':
    files = os.listdir(img_path_old)  # 获取文件名列表
    i = 0
    total = len(files)
    print (img_path_old+' total files:'+ str(total) )
    for file in files:
        img_zeros = np.zeros((c_w, c_h, 3), np.uint8)  # 创建全黑的图像
        if file.endswith('.jpg'):
            imgName = os.path.join(img_path_old, file)  # 获取文件完整路径
            print (file + ' done with:'+str(i/total*100)+'%')
            xml_file = file.replace('.jpg', '.xml')
            img = cv2.imread(imgName)  # 读图
            h, w, _ = img.shape  # 获取图像宽高
            # 缩放图像，宽高大于c_w的按长边等比例缩放，小于c_w的保持原图像大小：
            if max(w, h) > c_w:
                ratio = c_w / max(w, h)
                imgcrop = cv2.resize(img, (round(w * ratio), round(h * ratio)))
                # 将缩放后的图像复制进全黑图像里
                img_zeros[0:round(h * ratio), 0:round(w * ratio)] = imgcrop
                edit_xml(xml_file, ratio, i)
            else:
                img_zeros[0:h, 0:w] = img
                edit_xml(xml_file, 1, i)

            # 设置新的文件名：
            newName = os.path.join(img_path_new, str(i)+'.jpg')
            i += 1
            print('generate new file: '+newName)
            cv2.imwrite(newName, img_zeros)  # 存储按新文件名命令的图片