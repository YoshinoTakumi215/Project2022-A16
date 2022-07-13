from google.cloud import vision
from google.oauth2 import service_account
import io
IMG_URL =  'download.jpg'
from google.cloud.vision_v1 import types
# 身元証明書のjson読み込み
credentials = service_account.Credentials.from_service_account_file('Key.json')
 
client = vision.ImageAnnotatorClient(credentials=credentials)
image = vision.Image()
with io.open(IMG_URL, 'rb') as image_file:
    content = image_file.read()
image = types.Image(content=content)
response = client.label_detection(image=image)
labels = response.label_annotations
 
print("-------------画像解析結果--------------")
for label in labels:
    print(label.description + " : " + str(label.score))
    print("---------------------------------------")
 
if response.error.message:
    raise Exception(
        '{}\nFor more info on error messages, check: '
        'https://cloud.google.com/apis/design/errors'.format(
            response.error.message))