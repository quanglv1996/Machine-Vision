import cv2
import base64
import os
import shutil
import json
from PIL import Image
from io import BytesIO


class LabelSegmentationCreating(object):
    def __init__(self, save_dir):
        self.save_dir = save_dir
        if os.path.exists(self.save_dir):
            shutil.rmtree(self.save_dir)
        os.mkdir(self.save_dir)

    @staticmethod
    def imageToString(img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(img)
        buff = BytesIO()
        pil_img.save(buff, format="JPEG")
        img_2_str = base64.b64encode(buff.getvalue()).decode("utf-8")
        return img_2_str

    @staticmethod
    def define_format_json_file(version='4.6.0', flag={}, polygon_with_label=[], img_path=None, img_data=None, h_img=None, w_img=None):
        if not (len(polygon_with_label) == 0 or img_path is None or img_data is None or h_img is None or w_img is None):
            list_object = [{"label": label, "points": points, "group_id": None,
                            "shape_type": "polygon", "flags": {}} for points, label in polygon_with_label]
            json_file = {
                "version": version,
                "flags": flag,
                "shapes": list_object,
                "imagePath": img_path,
                "imageData": img_data,
                "imageHeight": h_img,
                "imageWidth": w_img
            }
            return json_file

    def create_json_file(self, img, polygon_with_label, img_filename):
        h, w = img.shape[:2]
        img_data = self.imageToString(img)

        json_format = self.define_format_json_file(polygon_with_label=polygon_with_label, img_data=img_data,
                                                   img_path=img_filename, h_img=h, w_img=w)
        json_file = json.dumps(json_format, indent=4)

        path_save_json = os.path.join(
            self.save_dir, img_filename.replace('.jpg', '.json'))
        with open(path_save_json, 'w') as f:
            f.write(json_file)

        path_save_img = os.path.join(self.save_dir, img_filename)
        cv2.imwrite(path_save_img, img)


def main():
    save_dir = './save_segmetation_labeling'

    path_img = "img.jpg"
    img = cv2.imread(path_img)

    labeling = LabelSegmentationCreating(save_dir)

    points1 = [
        [
            4.196217494089833,
            45.744680851063826
        ],
        [
            19.089834515366427,
            39.95271867612293
        ],
        [
            30.437352245862876,
            27.777777777777775
        ],
    ]
    label1 = 'label1'
    polygon1 = [points1, label1]

    polygon_with_label = [polygon1]

    labeling.create_json_file(img, polygon_with_label,
                              os.path.basename(path_img))


if __name__ == '__main__':
    main()