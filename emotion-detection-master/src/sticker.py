import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import MaxPooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

# command line argument
ap = argparse.ArgumentParser()
ap.add_argument("--mode",help="train/display")
mode = ap.parse_args().mode


num_train = 28709
num_val = 7178
batch_size = 64
num_epoch = 50

# Create the model
model = Sequential()

model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=(48,48,1)))
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Conv2D(128, kernel_size=(3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(1024, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(7, activation='softmax'))

def main():
    model.load_weights('model.h5')
    
    # prevents openCL usage and unnecessary logging messages
    # cv2.ocl.setUseOpenCL(False)
    
     # dictionary which assigns each label an emotion (alphabetical order)
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    emotion_words = {0: "WHAT!", 1: "Ugh!", 2: "Oh my gosh!", 3: "LOL", 4: "Hmm", 5: "NOOOOO!", 6: "Wow!"}
    
    img = cv2.imread('input_imgs/img5(2-Fearful).jpg',1)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    height, width, channels = img.shape
#     print(img.shape)

    cropped_img = np.expand_dims(np.expand_dims(cv2.resize(gray_img, (48, 48)), -1), 0)
    prediction = model.predict(cropped_img)
    maxindex = int(np.argmax(prediction))
#     print(maxindex)
    
    # font 
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    if maxindex == 0 or maxindex == 1 or maxindex == 3 or maxindex == 4 or maxindex == 6:
        fontScale = width // 100
    elif maxindex == 5:
        fontScale = width // 150
    else:
        fontScale = width // 200
    
    # Blue color in BGR 
    color = (255, 255, 255) 
    
    # Line thickness of 2 px 
    thickness = width // 50   
    
    # Calculates the width and height of the emotion text string.
    (text_width, text_height), baseline = cv2.getTextSize(emotion_words[maxindex], font, fontScale, thickness)

    # org
    org = ((width - text_width) // 2, height - 50)
 
    # Using cv2.putText() method 
    output = cv2.putText(img, emotion_words[maxindex], org, font, fontScale, color, thickness, cv2.LINE_AA) 
    
    cv2.imwrite('output_imgs/output.jpg', output) 
    
main()
