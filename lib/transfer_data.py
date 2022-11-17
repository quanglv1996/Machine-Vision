import base64
from PIL import Image
import numpy as np
from io import BytesIO
import pickle
import codecs

def stringToImage(base64_string):
    # base64_string of rgb image
    # retun bgr image
    base64_string += "=" * ((4 - len(base64_string) % 4) % 4)
    imgdata = base64.b64decode(str(base64_string))
    image = Image.open(BytesIO(imgdata))
    image = np.array(image)[:,:,:3]
    return image[:,:,::-1]

def imageToString(img):
    # numpy array
    pil_img = Image.fromarray(img)
    buff = BytesIO()
    pil_img.save(buff, format="JPEG")
    img_2_str = base64.b64encode(buff.getvalue()).decode("utf-8")
    return img_2_str


def obj2str(obj):
    return codecs.encode(pickle.dumps(obj), "base64").decode()

def str2obj(obj):
    return pickle.loads(codecs.decode(obj.encode(), "base64"))