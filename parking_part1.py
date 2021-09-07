import math
import time
import csv
import os
import cv2
import torch, torchvision
import matplotlib.pyplot as plt
# from google.colab import drive
# from google.colab.patches import cv2_imshow
from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.util import crop

"""Need a PyTorch "1.8.0+cu101" installed"""
# Check pyTorch version
# print(torch.__version__, torch.cuda.is_available())
# print(torchvision.__version__)
assert torch.__version__.startswith("1.8.0")

"""# **Download the Parking-Space Video from Google-Drive**
Perform **Authorization**
"""
# drive.mount('/content/drive/')

"""Reach my Google Drive and **Copy** Video-Content
# Make a temporary directory in Google colab
# Copy Video stored in Google Drive to COLAB
Only for Special Cases [1]: Copy Produced Frames from Google Colab --> Google Drive"""

MAIN_FOLDER = './inputs'
VIDEOS_FOLDER = MAIN_FOLDER + '/Videos/'
OUTPUT_FRAMES_PATH = VIDEOS_FOLDER + '/frames'

FRAME_NAME = 'frame'

# *** IMPORTANT - How Many Frames to Save / Frame-Rate ***
one_frame_each = 24

all_video_files = [f for f in os.listdir(VIDEOS_FOLDER) if os.path.isfile(os.path.join(VIDEOS_FOLDER, f))]
# Α5 parking-space
print(all_video_files)
video_file = all_video_files[0]

# A7 parking-space
# video_file = all_video_files[1]

# A7 parking-space (b)
# video_file = all_video_files[2]

print('Parking Space Video Found for Analysis ...' + video_file)

"""# Extract Video-Frames / Framerate = 24 (?)
Capture frames from video and apply **resize** + **rgb2gray** filters --
New Image-Width = **640** 
"""

# Crop Image = Obtain ROI CHECK WHERE TO CUT THE CHOSEN VID

CROP_ROW = 1000
CROP_COL = 1500

print('Ready to Read and Crop Image --> %d x %d' % (CROP_ROW, CROP_COL))

count = 0
success = True

videocap = cv2.VideoCapture(VIDEOS_FOLDER + video_file)  # you need the full path of a file to open

if videocap.isOpened() == False:
    print("Error opening video stream or file")

start_t = time.time()
while success:
    if count % one_frame_each == 0:
        success, image = videocap.read()

        if image is None:
            # Finished reading video - No more frames left
            print('Video is over')
            break

        # STEP CROP : Extract a ROI
        image_gray = rgb2gray(image[0:CROP_ROW, 0:CROP_COL])

        # image_gray = rgb2gray(image)

        # print( "ORI-Image-Shape = %d x %d" % (image.shape[0] , image.shape[1]) )

        if image.shape[1] > 640:
            tmp = resize(image_gray, (math.floor(640 / image_gray.shape[1] * image_gray.shape[0]), 640),
                         mode='constant')

            # print( "TMPimage-Shape-1 = %d" % tmp.shape[1] )

        # roi = tmp.copy()
        # B = crop(roi, ((50, 100), (50, 50), (0,0)), copy=False)

        plt.imsave("%s/%s%d.png" % (OUTPUT_FRAMES_PATH, FRAME_NAME, count), tmp, cmap=plt.cm.gray)
        # plt.imsave("%s/%s%d.png" % (OUTPUT_FRAMES_PATH, FRAME_NAME, count), roi, cmap=plt.cm.gray)

        print('*', end='')
    else:
        success, image = videocap.read()
    count += 1
end_t = time.time()

elapsed_time = end_t - start_t

# Print Performance Statistics of Frames Extraction Procedure
# How Many && How Long
# num_frames = len(OUTPUT_FRAMES_PATH_items)
num_frames = os.listdir(OUTPUT_FRAMES_PATH)
print("\nNumber of Frames Extracted (frameXXX.PNG) == %d" % len(num_frames) + '\n*** Elapsed Time = ' +
      str(elapsed_time) + ' (msecs) ***')

"""## **Frames-ALL**: Capture All frames from input video"""

# !rm parking-space/Videos/frames-all/masked*.png  PROBABLY WILL HAVE TO LEAVE IT HERE TO MAKE IT EXECUTE ON OTHER VIDS

OUTPUT_FRAMES_PATH_ALL = './inputs/Videos/frames-all'
FRAME_NAME = 'frame'
count = 0
success = True

videocap = cv2.VideoCapture(VIDEOS_FOLDER + video_file)
one_frame_each = 2

start_t = time.time()
while success:
    if count % one_frame_each == 0:
        success, image = videocap.read()

        if image is None:
            # Finished reading video - No more frames left
            break

        image_gray = rgb2gray(image)

        if image.shape[1] > 640:
            tmp = resize(image_gray, (math.floor(640 / image_gray.shape[1] * image_gray.shape[0]), 640),
                         mode='constant')

        plt.imsave("%s/%s%d.png" % (OUTPUT_FRAMES_PATH_ALL, FRAME_NAME, count), tmp, cmap=plt.cm.gray)
        # print('Finished saving frame-%d' % count)
    else:
        success, image = videocap.read()
    count += 1

end_t = time.time()

elapsed_time = end_t - start_t

# Print Performance Statistics of Frames Extraction Procedure
# How Many && How Long
num_frames = os.listdir(OUTPUT_FRAMES_PATH_ALL)
print("\nNumber of Frames Extracted (frameXXX.PNG) == %d" % len(num_frames) + '\n*** Elapsed Time = ' + str(
    elapsed_time) + ' (msecs) ***')

"""
# **Start Reading Parking-Slot Coordinates**
Copy CSV file with coordinates .. from Google-Drive to Colab


HOST_FOLDER = '/content/drive/MyDrive/ML-apps/parking-space-monitoring/'

FILE_EXTENSION = 'csv'
# COORDS_FILE = 'intracom-a7.' + FILE_EXTENSION
COORDS_FILE = 'intracom-a7_b.' + FILE_EXTENSION

# Copy COORDS file from Google Drive to Local Colab
# os.system('cp {HOST_FOLDER}'/'{COORDS_FILE} {MAIN_FOLDER}')

LOCAL_COORDS_FILE = "%s/%s" % (MAIN_FOLDER, COORDS_FILE)
# print( 'Local Parking-Space Coordinates File --> ' + LOCAL_COORDS_FILE )
# os.system('ls -l {LOCAL_COORDS_FILE}')

# **Read Coords from a CSV file**
print(csv.__version__)

# Read Initial Image
# all_frames = items_of(OUTPUT_FRAMES_PATH)
all_frames = os.system('ls {OUTPUT_FRAMES_PATH} / *.png')
frame = all_frames[0]
img = cv2.imread(frame)

_radius = 2

all_parking_slots = []

with open(LOCAL_COORDS_FILE, 'r') as stream:
    csv_reader = csv.reader(stream, delimiter=',')
    line_count = 0

    for row in csv_reader:
        if line_count == 0:
            # print('Column names are: {' + " , ".join(row) )
            line_count += 1
        else:
            park_row = row[0]

            slot = row[1]

            corner_01 = row[2]
            if 'None' not in corner_01:
                c01 = corner_01.split('-')
                corner_01_x = int(c01[0])
                corner_01_y = int(c01[1])

                image = cv2.circle(img, (corner_01_x, corner_01_y), radius=_radius, color=(255, 255, 10), thickness=-1)

            corner_02 = row[3]
            if 'None' not in corner_02:
                c02 = corner_02.split('-')
                corner_02_x = int(c02[0])
                corner_02_y = int(c02[1])
                image = cv2.circle(img, (corner_02_x, corner_02_y), radius=_radius, color=(255, 255, 10), thickness=-1)

            corner_03 = row[4]
            if 'None' not in corner_03:
                c03 = corner_03.split('-')
                corner_03_x = int(c03[0])
                corner_03_y = int(c03[1])
                image = cv2.circle(img, (corner_03_x, corner_03_y), radius=_radius, color=(255, 255, 10), thickness=-1)

            corner_04 = row[5]
            if 'None' not in corner_04:
                c04 = corner_04.split('-')
                corner_04_x = int(c04[0])
                corner_04_y = int(c04[1])
                image = cv2.circle(img, (corner_04_x, corner_04_y), radius=_radius, color=(255, 255, 10), thickness=-1)

            # print("Slot=%d , Corner-01=(%d / %d), Corner-02=%s, Corner-03=%s" % (int(slot), corner_01_x, corner_01_y, corner_02, corner_03))

            # image = cv2.circle(img, (114, 162), radius=6, color=(255,255, 10), thickness=-1)
            # image = cv2.circle(img, (114, 162), radius=6, color=(255,255, 10), thickness=-1)

            all_parking_slots.append([park_row, slot, corner_01, corner_02, corner_03, corner_04])

            line_count += 1

    cv2.imshow(image)

# For illustration purposes only: DISPLAY FIRST 10 LINES OF PARKING_SLOTS_COORDS array
# all_parking_slots[0:10]
*! Finished Reading Parking Space Data - Slots Coordinates are Available !*

corners_anti_01_0A = {0: (107, 206), 1: (211, 227), 2: (239, 197), 3: (145, 177)}

# corners_anti_05_0A = {}
# corners_anti_05_0A[0] = (219, 118)
# corners_anti_05_0A[1] = (305, 132)
# corners_anti_05_0A[2] = (320, 115)
#
# corners_anti_01_0B = {}
# corners_anti_01_0B[0] = (373, 222)
# corners_anti_01_0B[1] = (354, 255)
# corners_anti_01_0B[2] = (498, 281)

img = cv2.imread(video_file)

image = cv2.circle(img, (114, 162), radius=6, color=(255, 255, 10), thickness=-1)
# image = cv2.circle(img, (212, 227), radius=6, color=(255, 255, 10), thickness=-1)
#
# image = cv2.circle(img, (223, 90), radius=6, color=(255, 255, 10), thickness=-1)
# image = cv2.circle(img, (300, 131), radius=6, color=(255, 255, 10), thickness=-1)
#
# image = cv2.circle(img, (384, 201), radius=6, color=(255, 255, 10), thickness=-1)
# image = cv2.circle(img, (513, 272), radius=6, color=(255, 255, 10), thickness=-1)
#
# image = cv2.circle(img, corners_anti_01_0A[0], radius=4, color=(0, 255, 255), thickness=-1)
# image = cv2.circle(img, corners_anti_01_0A[1], radius=4, color=(0, 255, 255), thickness=-1)
# image = cv2.circle(img, corners_anti_01_0A[2], radius=4, color=(0, 255, 255), thickness=-1)
#
# image = cv2.circle(img, corners_anti_05_0A[0], radius=4, color=(0, 255, 255), thickness=-1)
# image = cv2.circle(img, corners_anti_05_0A[1], radius=4, color=(0, 255, 255), thickness=-1)
# image = cv2.circle(img, corners_anti_05_0A[2], radius=4, color=(0, 255, 255), thickness=-1)
#
# image = cv2.circle(img, corners_anti_01_0B[0], radius=4, color=(0, 255, 255), thickness=-1)
# image = cv2.circle(img, corners_anti_01_0B[1], radius=4, color=(0, 255, 255), thickness=-1)
# image = cv2.circle(img, corners_anti_01_0B[2], radius=4, color=(0, 255, 255), thickness=-1)

cv2.imshow(image)
"""
