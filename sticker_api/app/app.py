# app/app.py

# Common python package imports.
import os
from flask import Flask, jsonify, request, render_template
#import pickle
import numpy as np
import cv2
import base64
import json
from tensorflow.keras.models import load_model

# Initialize the app and set a secret_key.
app = Flask(__name__)
app.secret_key = 'something_secret'

# Load the emotion h5 model.
model = load_model('e_model.h5')

# dictionary which assigns each label an emotion (alphabetical order)
emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
emotion_words = {0: "WHAT!", 1: "Ugh!", 2: "Oh my gosh!", 3: "LOL", 4: "Hmm", 5: "NOOOOO!", 6: "Wow!"}

@app.route('/')
def docs():
    """Describe the model API inputs and outputs for users."""
    return render_template('docs.html')


@app.route('/api', methods=['POST'])
def api():
    """Handle request and output model score in json format."""
    # Handle empty requests.
    if not request.data:
        return jsonify(code=401, message='no request received')
    if request.method == 'POST': 
        try:
        
            json_str_server =  request.get_data().decode("utf-8")
            json_dict_server = json.loads(json_str_server)
            strdata_server = json_dict_server['imgbase64']
            base64data_server = strdata_server.encode('utf-8')
            image_byte_server = base64.b64decode(base64data_server)    
            nparr = np.fromstring(image_byte_server,dtype=np.uint8)
            img = cv2.imdecode(nparr,cv2.IMREAD_COLOR)
        #cv2.imwrite('input.jpg', img)
        except Exception as e:
            msg = "Fail to decode image " 
            return jsonify(code=402,message=msg)
        
        try:
	    #predict emotion and make sticker
            maxindex = predict_emotion(img)
            output_img = sticker(img,maxindex)
            cv2.imwrite('output_imgs/output.jpg', output_img)

            #encode output image
            imgpath = 'output_imgs/output.jpg'
            with open(imgpath,'rb') as fin:
                image_byte_client = fin.read()#bytes
                base64data_client = base64.b64encode(image_byte_client)#bytes
                strdata_client = base64data_client.decode('utf-8')#str
                emo = emotion_dict[maxindex]
            
            return jsonify({'code':200, 'message':'success','data': {'sticker':strdata_client,'emotion':emo}})
            #return jsonify(code=200,message="success",data = strdata_client)

        except Exception as e:
            fail_str="Fail to get image emotion "
            return jsonify(code=403,message=fail_str)

def predict_emotion(img):
    """Predict emotion from image."""
    #Process img
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    #Predict image emotion
    cropped_img = np.expand_dims(np.expand_dims(cv2.resize(gray_img, (48, 48)), -1), 0)
    prediction = model.predict(cropped_img)
    maxindex = int(np.argmax(prediction))
    return maxindex

def sticker(img,maxindex):
    """Make sticker."""
    
    height, width, channels = img.shape
    
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
    
    return output
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
