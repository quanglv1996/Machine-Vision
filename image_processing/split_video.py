import cv2
import shutil
import numpy as np
import os
import datetime
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

time_now = datetime.datetime.now()


def split_video(path_video, path_save, start_time, end_time):
	type_video = path_video.split('.')[-1]
	video_name = path_video.split('/')[-1].split('.')[0]
	ffmpeg_extract_subclip(path_video, start_time,end_time, targetname= video_name + '_' + str(start_time) + '_' +str(end_time) + "." + type_video)


def split_video2frame(path_video, path_save, distand_frame =3):
    vidcap = cv2.VideoCapture(path_video)
    success,image = vidcap.read()
    count_frame = 0
    while success:
        if count_frame % distand_frame==0:
            cv2.imwrite(os.path.join(path_save,'frame'+str(count_frame).zfill(8)+'.png'), image)     # save frame as JPEG file      
        success,image = vidcap.read()
        print('Read frame {}'.format(count_frame), end = '\\')
        count_frame += 1
        
def get_stream(path_camera, path_save, size, fps, num_frames, save_image = False, distand_frame = 3):
    count_frame = 0
    cap = cv2.VideoCapture(path_camera)
    out = cv2.VideoWriter('video_' + str(num_frames) + '_' +time_now.strftime("%H:%M:%S")+ '.avi',cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    while(True):
        print('Frame number {}'.format(count_frame), end = '\\')
        ret, frame = cap.read()
        if frame is not None:
            out.write(frame)
            if count_frame % distand_frame ==0 and save_image:
                cv2.imwrite(os.path.join(path_save, 'frame'+str(count_frame).zfill(6)+'.png'), frame)
            
        # Display the resulting frame
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if count_frame == num_frames:
            break
        else:
            count_frame +=1
    # When everything done, release the capture
    out.release()
    cap.release()
    cv2.destroyAllWindows()
if __name__ == '__main__':
	path_video = '/path/video/name.mp4'
	path_save = os.path.join('/path/save/video/split',  time_now.strftime("%H:%M:%S"))
	if os.path.exists(path_save):
		shutil.rmtree(path_save)
	os.mkdir(path_save)
	num_video_spliting = 10
	length = 30 #minutes
	for i in range(0, 10):
		stime = i * 60 *30
		etime = (i+1) * 60 * 30
		split_video(path_video, stime, etime)
  
