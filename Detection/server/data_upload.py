from uuid import uuid4
from time import sleep
# import schedule as schedule
import firebase_admin
from firebase_admin import credentials, db, storage
# from google.cloud import storage
from datetime import datetime
import cv2


# -----------------------------------------------------------------------------

def fileUpload(bucket, file):
    blob = bucket.blob(file)
    # new token and metadata 설정
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token}  # access token이 필요하다.
    blob.metadata = metadata

    # upload file
    blob.upload_from_filename(filename=file, content_type='image/jpg')
    print(blob.public_url)


class Upload:
    def __init__(self):
        # Storage Snapshot Image Upload
        # 버킷은 바이너리 객체의 상위 컨테이너이다. 버킷은 Storage에서 데이터를 보관하는 기본 컨테이너이다.
        self.bucket = None
    
    # -----------------------------------------------------------------------------

    def firebase_init(self):
        # real-time database
        # Firebase database 인증 및 앱 초기화
        PROJECT_ID = "train-notification-677f6"  # 자신의 project id
        cred=credentials.Certificate('./server/adminsdk.json')
        firebase_admin.initialize_app(cred,{
            'databaseURL':'https://train-notification-677f6.firebaseio.com/',
            'storageBucket': f"{PROJECT_ID}.appspot.com"
        })
        self.bucket = storage.bucket()  # 기본 버킷 사용

    # -----------------------------------------------------------------------------
    # Database Upload

    def uploadDangerData(self, img, filepath, filetype, location, datetime, state):
        ref = db.reference()
        users_ref = ref.child('DangerList').child(location).push()
        image_name = filepath + users_ref.key + filetype
        cv2.imwrite(image_name, img)

        users_ref.set({
            'id': users_ref.key,
            'datetime': datetime,
            'image_name': image_name,
            'location': location,
            'state': state
        })

        # upload snapshop image
        fileUpload(self.bucket, image_name)

        return users_ref.key




'''
# cloud Firestore
cred = credentials.Certificate('mykey.json')
firebase_admin.initialize_app(cred)

db=firestore.client()

doc_ref=db.collection(u'users').document(u'user01')
doc_ref.set({
    u'승강장':5,
    u'시간':time,
    u'job':"student"
})
'''


'''
# 버킷은 바이너리 객체의 상위 컨테이너이다. 버킷은 Storage에서 데이터를 보관하는 기본 컨테이너이다.
bucket = storage.bucket()  # 기본 버킷 사용


# def execute_camera():
#     # 사진찍기 코드 추가 될 곳
#     # 중복없는 파일명 만들기
#
#     filename = "logo.png"
#     fileUpload(filename)


def fileUpload(file):
    blob = bucket.blob(file)
    # new token and metadata 설정
    new_token = uuid4()
    metadata = {"firebaseStorageDownloadTokens": new_token}  # access token이 필요하다.
    blob.metadata = metadata

    # upload file
    blob.upload_from_filename(filename=file, content_type='image/png')
    print(blob.public_url)

# schedule.every(10).seconds.do(execute_camera)
#
# while True:
#     schedule.run_pending()
#     sleep(1)

fileUpload("logo.png")

''' 