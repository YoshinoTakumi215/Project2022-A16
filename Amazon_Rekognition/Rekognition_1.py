# AWSを使用するためのライブラリを読み込む
import boto3
# iniファイルを使用するためのライブラリを読み込む
import configparser
# 認識結果を表示するためのライブラリを読み込む
from matplotlib import pyplot as plt
from PIL import Image
import random

#configparserのインスタンスを作る
ini = configparser.ConfigParser()
#あらかじめ作ったiniファイルを読み込む
ini.read("\\Users\\yosta\\Desktop\\config.ini", "UTF-8")

# 認識させるファイルを指定する
filename = "\\Users\\yosta\\Desktop\\landscape2.jpg"

#画像を開いて、サイズを取得する
img = Image.open(filename)
img_width = img.size[0]
img_height = img.size[1]

# 使用するバケットを指定する
bucket = "project2022a16"
# 使用するリージョンを指定する
region = "us-west-2"

# サービスを利用するための識別情報(iniファイルの中身）を読み込む
access_key = ini["AWS_KEY"]["awsaccesskeyid"]
secret_key = ini["AWS_KEY"]["awssecretkey"]
# サービスへの接続情報を取得する
session = boto3.Session(
    aws_access_key_id=access_key, aws_secret_access_key=secret_key, region_name=region
)

# S3サービスに接続する
s3 = session.client("s3")
# Rekognitionサービスに接続する
rekognition = session.client("rekognition")

# ファイルを読み込む
with open(filename, "rb") as f:
    # 読み込んだファイルをS3サービスにアップロード
    s3.put_object(Bucket=bucket, Key=filename, Body=f)

# S3に置いたファイルをRekognitionに認識させる
res = rekognition.detect_labels(
    Image={"S3Object": {"Bucket": bucket, "Name": filename}})

# Rekognitionの認識結果を表示する
print("Detected labels for " + filename)
print()
for label in res["Labels"]:
    print("Label: " + label["Name"])
    print("Confidence: " + str(label["Confidence"]))
    print("Instances:")
    for instance in label["Instances"]:
        print("  Bounding box")
        print("    Top: " + str(instance["BoundingBox"]["Top"]))
        print("    Left: " + str(instance["BoundingBox"]["Left"]))
        print("    Width: " + str(instance["BoundingBox"]["Width"]))
        print("    Height: " + str(instance["BoundingBox"]["Height"]))
        print("  Confidence: " + str(instance["Confidence"]))
        print()

        print("Parents:")
        for parent in label["Parents"]:
            print("   " + parent["Name"])
        print("----------")
        print()

# 画像と枠を表示させる
colors = {}
for label in res["Labels"]:
    label_name = label["Name"]
    if label_name not in colors:
        colors[label_name] = (random.random(), random.random(), random.random())
        for instance in label["Instances"]:
            bb = instance["BoundingBox"]

            rect = plt.Rectangle(
                (bb["Left"] * img_width, bb["Top"] * img_height),
                bb["Width"] * img_width,
                bb["Height"] * img_height,
                fill=False,
                edgecolor=colors[label_name],
            )
            plt.gca().add_patch(rect)

plt.imshow(img)
plt.show()
# S3サービスにアップロードしたファイルを削除する
s3.delete_object(Bucket=bucket, Key=filename)
