import xml.etree.ElementTree as ET
import pandas as pd
import cv2
import os
import time
import json
import argparse


#path_folder have type /path/folder/contain/image/and/xml/datasetname/
def convert_coco_format(path_folder, path_save, save_csv = False):
    dataset = path_folder.split('/')[-1]
    filenames = os.listdir(path_folder)
    xml_filenames = [s for s in filenames if "xml" in s]
    xml_filenames.sort()
    img_filenames = [s for s in filenames if "jpg" in s]
    img_filenames.sort()

    list_infor = []
    for xml_filename in xml_filenames:
        print(xml_filename)
        png_filename = xml_filename.split('.')[0]+'.jpg'
        image = cv2.imread(os.path.join(path_folder,png_filename))
        width_frame = image.shape[1]
        height_frame = image.shape[0]
        xml_file = ET.parse(os.path.join(path_folder, xml_filename))
        root = xml_file.getroot()
        for obj in root.iter('object'):
            vehicle_type = obj.find('name').text
            for bbox in obj.iter('bndbox'):
                xmin = int(bbox.find('xmin').text)
                ymin = int(bbox.find('ymin').text)
                xmax = int(bbox.find('xmax').text)
                ymax = int(bbox.find('ymax').text)
            if vehicle_type == 'unknown':
                image = cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 0, 0), -1)
                cv2.imwrite(os.path.join(path_folder, png_filename),image)
            else:
                bbox = {'filename': png_filename,
                        'width': width_frame,
                        'height': height_frame,
                        'class': vehicle_type,
                        'xmin':xmin,
                        'ymin':ymin,
                        'xmax':xmax,
                        'ymax':ymax}
                list_infor.append(bbox)
                
    list_infor = pd.DataFrame(list_infor)
    if save_csv: #For debug
        with open(os.path.join(path_save,'./' + dataset +'.csv'), 'a') as f:
                list_infor.to_csv(f, encoding='utf-8', header=True,index=False)

    json_dict = {
            'images': [],
            'type': 'instances',
            'annotations': [],
            'categories': [{
                'supercategory': 'none',
                'id': 1,
                'name': 'categories1'
            },{
                'supercategory': 'none',
                'id': 2,
                'name': 'categories2'
            },{
                'supercategory': 'none',
                'id': 3,
                'name': 'categories3'
            },{
                'supercategory': 'none',
                'id': 4,
                'name': 'categories4'
            },{
                'supercategory': 'none',
                'id': 5,
                'name': 'categories5'
            },{
                'supercategory': 'none',
                'id': 6,
                'name': 'categories6'
            }]
        }

    annotation_id = 0

    for image_idx, img_filename in zip(range(0, len(img_filenames)), img_filenames):
        print(img_filename)
        image_df = list_infor.loc[list_infor['filename'] == img_filename]
        if len(image_df.index) == 0:
            continue
        for index, row in image_df.iterrows():
            width, height, class_name, xmin, ymin, xmax, ymax = int(row['width']), int(row['height']), row['class'], int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
            print(img_filename)
            print(class_name)
            #Fix label
            if class_name in ['categories1_error1','categories1_error2']:
                class_name = 'categories1'
            if class_name == ['categories2_error1','categories2_error2']:
                class_name = 'categories2'
            category_id = [c for c in json_dict['categories'] if c['name'] == class_name][0]['id']
            if not any(i['file_name'] == img_filename for i in json_dict['images']):
                image_object = {
                    'file_name': img_filename,
                    'height': height,
                    'width': width,
                    'id': image_idx
                }
                json_dict['images'].append(image_object)

            annotation_object = {
                'segmentation': [],
                'area': 0,
                'iscrowd': 0,
                'image_id': image_idx,
                'bbox': [xmin, ymin, xmax - xmin, ymax - ymin],
                'category_id': category_id,
                'id': annotation_id,
                'ignore': 0
            }
            json_dict['annotations'].append(annotation_object)
            annotation_id += 1

    with open(os.path.join(path_save,'./'+dataset+'.json'), 'w') as f:
        json.dump(json_dict, f)

if __name__ == '__main__':
	path_folder_data = '/folder/contain/image/and/xml'
	path_save = '/folder/save/jsonfile'
	convert_coco_format(path_folder_data, path_save, False)