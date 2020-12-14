
import firebase_admin
from firebase_admin import credentials, db, storage
# from google.cloud import storage
from datetime import datetime


PROJECT_ID = "train-notification-677f6"  # 자신의 project id
cred=credentials.Certificate('adminsdk.json')
firebase_admin.initialize_app(cred,{
    'databaseURL':'https://train-notification-677f6.firebaseio.com/',
    'storageBucket': f"{PROJECT_ID}.appspot.com"
})

# ex = ["notification"]

ref = db.reference()

# users_ref = ref.child('MyPlatform').child("w932FPOfGqXRMrcn6JWM3XEfLag2")
#
# users_ref.set({
#     'star_platform_list': ex
# })

now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

users_ref = ref.child('DangerList').child("Platform3").push()

users_ref.set({
        'id': users_ref.key,
        'datetime': now,
        'image_name': "example1",
        'location': "Platform3",
        'state': "미처리"
    })


users_ref = ref.child('DangerList').child("Platform4").push()

users_ref.set({
        'id': users_ref.key,
        'datetime': now,
        'image_name': "example1",
        'location': "Platform4",
        'state': "처리완료"
    })
