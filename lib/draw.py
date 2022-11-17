import cv2
import os
import shutil

class draw():
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    COLORS = {'RED': (0, 0, 255),
            'BLUE': (255, 0, 0),
            'GREEN': (0, 255, 0)}
    
    @staticmethod
    def draw_text(img, text='Hello', location=(100,100), font_scale=1.0, color='RED', thickness=1):
        img = cv2.putText(img, text, location, draw.FONT, font_scale,draw.COLORS[color], thickness, cv2.LINE_AA)
        return img

    @staticmethod
    def draw_rectangle(self, img, start_point, end_point, color='GREEN', info=None, font_scale=1.0, thickness=1):
        img  = cv2.rectangle(img, start_point, end_point, self.colors['RED'], thickness)
        if info is not None:
            img = cv2.putText(img, str(info), start_point, draw.FONT, font_scale, draw.COLORS[color], thickness)
        return img
    
    
def main():
    save_dir = '../debug'
    if os.path.exists(save_dir):
        shutil.rmtree(save_dir)
    os.mkdir(save_dir)
    
    filename = '../asset/1.jpg'
    img = cv2.imread(filename)
    
    img = draw.draw_text(img)
    cv2.imwrite(os.path.join(save_dir, 'debug_draw.jpg'), img)
    
if __name__ == '__main__':
    main()