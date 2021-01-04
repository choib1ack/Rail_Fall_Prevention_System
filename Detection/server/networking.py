import os
import socket, threading
import server.data_upload as upload
from datetime import datetime
import cv2


# TODO: argument로 바꿔도 좋음
location = "gachon 4-3"
directory = 'noti/danger/' + location


# 연결된 모든 client정보를 저장해둠. 나중에 알림 주기 위해서~
def addClientList(client_list, client):
    client_list.append(client)

    print("-------------[Client List]-------------")
    for client in client_list:
        print(client)
    print('---------------------------------------')


def removeClientList(client_list, client):
    client_list.remove(client)
    print("-------------[Client List]-------------")
    for client in client_list:
        print(client)
    print('---------------------------------------')


def close_client_socket(client_list):
    try:
        while True:
            for client in client_list:
                    check = client.recv(2048)
                    print(check)
                    if check <= 0:                
                        removeClientList(client_list, client)
                        client.close()

    except:
        print("client delete error")


class Server:
    def __init__(self):
        self.client_list = []


    def sendNotification(self, fb, img):
        filepath = 'noti/danger/' + location + '/'
        filetype = '.jpg'
        temp = location + filetype
        
        cv2.imwrite(filepath + temp, img)
        date = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

        id = fb.uploadDangerData(img, filepath, filetype, location, date, "미처리")
                        
        filepath = filepath + id + '.jpg'
        filesize = os.path.getsize(filepath)
        
        # firebase 데이터베이스에 위험 감지 데이터 업로드 - 업로드하는 데에 시간이 걸려서 앱 전송 먼저 진행
        for client_socket in self.client_list:
            infodata = (str(filesize) + "@" + location + "@" + date + "@" + filepath).encode()
            len_infodata = len(infodata)
            client_socket.send(str(len_infodata).encode())
            client_socket.send(infodata)

            with open(filepath, "rb") as f:
                bytes_read = f.read(filesize)
                client_socket.sendall(bytes_read)
                print(bytes_read)

    
    def runServer(self):
        # 소켓생성
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 소켓 레벨과 데이터 형태를 설정한다.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 서버는 복수 ip를 사용하는 pc의 경우는 ip를 지정하고 그렇지 않으면 None이 아닌 ''로 설정한다.
        # 포트는 pc내에서 비어있는 포트를 사용한다.
        server_socket.bind(('', 9999))
        # server 설정이 완료되면 listen를 시작한다. (connection 대기)
        server_socket.listen(10)  # 숫자는 최대 연결 client 개수
        print("Server Start ...")

        # 서버 ip 확인
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        ip = s.getsockname()[0]
        print(ip)

        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' +  directory)
            raise

        # threading.Thread(target=close_client_socket, args=(self.client_list)).start()
        # 쓰레드를 이용해서 client 접속 대기를 만들고 다시 accept로 넘어가서 다른 client를 대기한다.

        try:
            # 서버는 여러 클라이언트를 상대하기 때문에 무한 루프를 사용한다.
            while True:
                # client로 접속이 발생하면 accept가 발생한다. accept는 client가 들어올 때까지 무한 대기. 계속 루프를 돌진 않음.
                # 그럼 client 소켓과 addr(주소)를 튜플로 받는다.
                print("\n[Main Thread] Listening ...")
                client_socket, addr = server_socket.accept()
                print('[Main Thread]', addr, 'Accepting')
                addClientList(self.client_list, client_socket)
                print('[Client Thread]', addr)
        except:
            print("run server error")
        finally:
            # 에러가 발생하면 서버 소켓을 닫는다.
            server_socket.close()




# def binder(client_list, client_socket, addr):
#     print('[Connect Thread] Connected by', addr)

#     try:
#         while True:
#             # option = input("Enter option (1: send image, 2: exit) : ")

#             # if option == '1':
#             #     now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
#             #     filename = "train3.jpg"
#             #     location = "4호선 테스트역"
#             #     # sendNotification(client_socket, filename, location, now)    # 앱에 알림 전송
#             #     sendNotification(filename, location, now)
#             #     upload.uploadDangerData(filename, location, now, "미처리")   # firebase 데이터베이스에 위험 감지 데이터 업로드 - 업로드하는 데에 시간이 걸려서 앱 전송 먼저 진행
#             # elif option == '2':
#             #     removeClientList(client_list, client_socket)
#             #     client_socket.close()
#             #     print("socket closed")
#             # else:
#             #     print("option을 다시 입력해주세요.")

#     except Exception as ex:
#         # 접속이 끊기면 except가 발생한다.
#         print("except : ", addr, ex)
#         removeClientList(client_list, client_socket)
#         client_socket.close()

#     # finally:
#     #     # 접속이 끊기면 socket 리소스를 닫는다.
#     #     client_socket.close()