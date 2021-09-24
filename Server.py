import socket as sock
import mimetypes as m
import base64 
from termcolor import colored

httpResponse = """
HTTP/1.1 200 OK
Connection: Keep-Alive
Content-Type: {type}
Accept-Ranges: bytes
Content-Length: {length}
Vary: Accept-Encoding
Server: Apache/2.4.41 (Ubuntu)


{body}

"""

HOST = "192.168.29.176"
PORT = 9999
sockObj = sock.socket(sock.AF_INET,sock.SOCK_STREAM)
sockObj.setsockopt(sock.SOL_SOCKET,sock.SO_REUSEADDR,1)
sockObj.bind((HOST,PORT))
sockObj.listen(0)
while True:
	conn, addr = sockObj.accept()
	print("\n[+] Connection Established with {IP}:{Port}".format(IP = addr[0],Port = addr[1]))
	receivedData = conn.recv(4096).decode()
	print(colored("\n[+] Request:\n",'red'))
	print(receivedData)
	requestedPath = receivedData.split(" ")[1]
	print()
	if(requestedPath == "/"):
		fetchFile = "htdocs"+"/"+"index.html"
	else:
		fetchFile = "htdocs"+requestedPath

	print(colored("[+] Response",'green'))
	print("[+] Fetching the File from "+fetchFile)
	print(m.guess_type(fetchFile)[0])
	if( m.guess_type(fetchFile)[0]=="image/png" or m.guess_type(fetchFile)[0] == "image/jpeg" or m.guess_type(fetchFile)[0] == "image/gif" or m.guess_type(fetchFile)[0] == "image/x-icon"):
		with open(fetchFile,"rb") as outFile:
			imageBinaryData = outFile.read()
		conn.sendall(httpResponse.format(length=len(imageBinaryData),type = m.guess_type(fetchFile)[0] ,body=imageBinaryData).encode())
	else:
		with open(fetchFile,"r") as outFile:
			data = outFile.read()
		httpResponse.format(length=len(data),type = m.guess_type(fetchFile)[0],body=data)
		conn.sendall(httpResponse.format(length=len(data),type = m.guess_type(fetchFile)[0],body=data).encode())