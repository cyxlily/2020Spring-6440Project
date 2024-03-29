# -*-coding:utf-8-*-
from flask import Flask, render_template, request, jsonify
#from flask_uploads import configure_uploads, UploadSet
import os, base64,sys,requests,json,traceback
import base64
import time
from datetime import date
import random
import string
import psycopg2

app = Flask(__name__)

# config location of uploaded files
#base = os.path.dirname(os.path.abspath(__file__))
#base = os.path.join(base, 'static')
#app.config['UPLOADS_DEFAULT_DEST'] = base
#photo = UploadSet()
#configure_uploads(app, photo)


@app.route('/up_file', methods=['GET', 'POST'])  # accept and store images
def up_file():
    if request.method == "POST":
        # receipt image
        file_name = ''.join(random.sample(string.ascii_letters + string.digits, 8)) + '.png'
 #       print(file_name)
#        photo.save(request.files['file'], 'img1', file_name)  # save image
#        sticker_img = send_req_to_API(file_name)
        gen_dict = send_req_to_API(request.files['file'])
        return jsonify(gen_dict)


@app.route('/', methods=['get', 'post'])
def index():
    return render_template('image.html')


def send_req_to_API(file_name):
#    imgpath = 'static/files/img1/' + file_name
#    with open(imgpath, 'rb') as fin:
#    image_byte_client = fin.read()
    image_byte_client = file_name.read()  # bytes
    base64data_client = base64.b64encode(image_byte_client)  # bytes
    strdata_client = base64data_client.decode('utf-8')  # str
    json_dict_client = {"imgbase64": strdata_client}  # dict

    json_dict_client = {"imgbase64": strdata_client}  # dict
#    json_dict_client = {"imgbase64": file_name}
    json_str_client = json.dumps(json_dict_client)  # str
    try:

        t0 = time.time()
        # request = requests.post(url='http://0.0.0.0:5000/api', data=json_str_client)
        request = requests.post(url='http://ApiDemo-env.eba-qyf98pxi.us-east-1.elasticbeanstalk.com/api',
                                data=json_str_client)
        t1 = time.time()
        print('send time is %.3f' % (t1 - t0))

        response = request.json()
        print("response: ", response)
        print(response['code'])
        json_dict_server = response['data']
        emotion = json_dict_server['emotion']
        print("The image emotion: ", emotion)
        img_client = json_dict_server['sticker']
        # print(f"img {img_client}")
        
        sticker = "data:image/png;base64,"+img_client
        bg_path = "/static/files/Background/"
        background = bg_path + emotion + ".png"
        gen_dict = {"sticker": sticker, "background":background, "emotion":emotion}
        
        send_img_info_to_DB(img_client, emotion)
        return gen_dict
        # print(img_client)

        # base64data_server = img_client.encode('utf-8')
        # image_byte_server = base64.b64decode(base64data_server)
        # nparr = np.fromstring(image_byte_server, dtype=np.uint8)
        # img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        # cv2.imwrite('output_imgs/sticker.jpg', img)
    except Exception as e:
        print("exception: " + str(e))
        traceback.print_exc(file=sys.stdout)


def send_img_info_to_DB(sticker_img_base64, emotionInfo):
    connection = psycopg2.connect(
        host = 'stickermakerdb.cmqjbt64rbvq.us-east-1.rds.amazonaws.com',
        port = 5432,
        user = 'master',
        password = 'stickermakerpwd',
        database = 'sticker_maker'
    )

    cursor = connection.cursor()
    cursor.execute("insert into stickers(sticker_img, emotion, uploadDate) values(%s, %s, %s)", (sticker_img_base64, emotionInfo ,date.today()))
    connection.commit()

if __name__ == "__main__":
    app.run()
