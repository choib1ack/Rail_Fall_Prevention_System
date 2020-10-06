from playsound import playsound

def firstNoti():
    playsound("noti.wav")


status = True
while status:
    firstNoti()
    status = not status