import os
import glob
import cv2
import xml.etree.ElementTree as ET


# Define the directory paths
images_dir = 'images_bak/'  # Update this path
xmls_dir = 'xml_bak/'      # Update this path

# Output directories
output_images_dir = 'JPEGImages/'  # Update this path
output_xmls_dir = 'Annotations/'   # Update this path

# Create output directories if they don't exist
os.makedirs(output_images_dir, exist_ok=True)
os.makedirs(output_xmls_dir, exist_ok=True)

# Function to update the XML according to the new image size and rename the tags
def update_xml(xml_file, original_size, new_width, new_height, new_filename):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Calculate scale factors
    scale_x = new_width / original_size[0]
    scale_y = new_height / original_size[1]

    # Update the size in the XML
    for size in root.findall('size'):
        size.find('width').text = str(new_width)
        size.find('height').text = str(new_height)
    
    # Update the filename in the XML
    for filename in root.findall('filename'):
        filename.text = new_filename
    
    # Remove the path
    for path in root.findall('path'):
        root.remove(path)

    # Update the object names and bounding boxes
    for object in root.findall('object'):
        for name in object.findall('name'):
            if name.text == 'Electric-bicycle':
                name.text = 'moto'
            elif name.text == 'person':
                name.text = 'peop'
            elif name.text == 'bicycle':
                name.text = 'bike'
            elif name.text == 'B1':
                name.text = 'b1'
        
        for bndbox in object.findall('bndbox'):
            xmin = int(float(bndbox.find('xmin').text) * scale_x)
            ymin = int(float(bndbox.find('ymin').text) * scale_y)
            xmax = int(float(bndbox.find('xmax').text) * scale_x)
            ymax = int(float(bndbox.find('ymax').text) * scale_y)
            bndbox.find('xmin').text = str(xmin)
            bndbox.find('ymin').text = str(ymin)
            bndbox.find('xmax').text = str(xmax)
            bndbox.find('ymax').text = str(ymax)
    
    # Save the updated XML
    tree.write(os.path.join(output_xmls_dir, new_filename.replace('.jpg', '.xml')))

# def update_xml(xml_file,new_filename):
#     tree = ET.parse(xml_file)
#     root = tree.getroot()

    
#     # Update the filename in the XML
#     for filename in root.findall('filename'):
#         filename.text = new_filename
    
#     # Remove the path
#     for path in root.findall('path'):
#         root.remove(path)

#     # Update the object names and bounding boxes
#     for object in root.findall('object'):
#         for name in object.findall('name'):
#             if name.text == 'Electric-bicycle':
#                 name.text = 'moto'
#             elif name.text == 'person':
#                 name.text = 'peop'
#             elif name.text == 'bicycle':
#                 name.text = 'bike'
#             elif name.text == 'B1':
#                 name.text = 'bike'

#     # Save the updated XML
#     tree.write(os.path.join(output_xmls_dir, new_filename.replace('.jpg', '.xml')))

# Function to resize image without keeping aspect ratio and update corresponding XML
def process_image_and_xml(image_path, xml_path, count, total):
    # Read the original image to get its size
    img = cv2.imread(image_path)
    original_size = img.shape[1], img.shape[0]  # width, height
    
    # Resize image not keeping aspect ratio
    img_resized = cv2.resize(img, (224, 224))
    
    new_image_filename = f'{count:05d}.jpg'
    cv2.imwrite(os.path.join(output_images_dir, new_image_filename), img_resized)
    # cv2.imwrite(os.path.join(output_images_dir, new_image_filename), img)
    
    # Update XML
    update_xml(xml_path, original_size, 224, 224, new_image_filename)

    # Update XML
    # update_xml(xml_path,new_image_filename)

    # Print progress
    print(f'Processed {count}/{total} files.')
    

# Main function to process all images and XMLs
def main():
    image_paths = sorted(glob.glob(images_dir + '*.jpg'))
    xml_paths = sorted(glob.glob(xmls_dir + '*.xml'))
    total_files = len(image_paths)
    print(f'total files {total_files}.')
    for count, (image_path, xml_path) in enumerate(zip(image_paths, xml_paths), start=1):
        process_image_and_xml(image_path, xml_path, count, total_files)

# Run the main function
main()
