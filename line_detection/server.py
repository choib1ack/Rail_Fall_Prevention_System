# 소켓을 사용하기 위해서는 socket을 import해야 한다.
# 이미지 데이터를 문자열로 바꾸는 라이브러리
import base64
import os
import socket
import threading


def binder(client_socket, addr):
    # 커넥션이 되면 접속 주소가 나온다.
    print('Connected by', addr)

    try:
        while True:
            option = input("Enter option (1: send image, 2: exit) : ")
            # 접속 상태에서는 클라이언트로 부터 받을 데이터를 무한 대기한다.
            # 만약 접속이 끊기게 된다면 except가 발생해서 접속이 끊기게 된다.
            # while True:
            if option == '1':
                filename = "3.png"
                filesize = os.path.getsize(filename)
                print("filesize", filesize)

                # start sending the file
                with open(filename, "rb") as f:
                    bytes_read = f.read(filesize)

                print(type(bytes_read))
                client_socket.sendall(bytes_read)

                '''
                progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
                with open(filename, "rb") as f:
                    for _ in progress:
                        # read the bytes from the file
                        bytes_read = f.read(1024)
                        if not bytes_read:
                            break
                        # print("A")
                        client_socket.sendall(bytes_read)
                        # print(type(bytes_read))
                        # print("B")
                        # print(len(bytes_read))
                        progress.update(len(bytes_read))    # update the progress bar
                '''
            elif option == '2':
                client_socket.close()
                print("socket closed")
            else:
                print("option을 다시 입력해주세요.")

    except:
        # 접속이 끊기면 except가 발생한다.
        print("except : ", addr)

    finally:
        # 접속이 끊기면 socket 리소스를 닫는다.
        client_socket.close()


def runServer():
    # 소켓생성
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 소켓 레벨과 데이터 형태를 설정한다.
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # 서버는 복수 ip를 사용하는 pc의 경우는 ip를 지정하고 그렇지 않으면 None이 아닌 ''로 설정한다.
    # 포트는 pc내에서 비어있는 포트를 사용한다.
    server_socket.bind(('', 9999))
    # server 설정이 완료되면 listen를 시작한다. (connection 대기)
    server_socket.listen(10)  # 숫자는 최대 연결 client 개수
    print("Server Start ... Listening ...")

    # 서버 ip 확인
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    ip = s.getsockname()[0]
    print(ip)

    try:
        # 서버는 여러 클라이언트를 상대하기 때문에 무한 루프를 사용한다.
        while True:
            # client로 접속이 발생하면 accept가 발생한다. accept는 client가 들어올 때까지 무한 대기. 계속 루프를 돌진 않음.
            # 그럼 client 소켓과 addr(주소)를 튜플로 받는다.
            client_socket, addr = server_socket.accept()

            print(addr, 'Accepting')
            th = threading.Thread(target=binder, args=(client_socket, addr))
            # 쓰레드를 이용해서 client 접속 대기를 만들고 다시 accept로 넘어가서 다른 client를 대기한다.
            th.start()
    except:
        print("run server error")
    finally:
        # 에러가 발생하면 서버 소켓을 닫는다.
        server_socket.close()


runServer()
