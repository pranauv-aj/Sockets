import socket
import mimetypes as m

hostIp = "192.168.29.18"
port = 80

#Response Template
httpResponseTemplate = """HTTP/1.1 200 OK
Connection: Keep-Alive
Content-Type: {type}
Accept-Ranges: bytes
Content-Length: {length}
Vary: Accept-Encoding
Server: Apache/2.4.41 (Ubuntu)

{body}"""



#Creating Socket
sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Binding the Socket
sck.bind((hostIp,port))
print("[+] Waiting For Connection")
sck.listen()
while True:
	conn,addr = sck.accept()
	print("[+] Received Connection from "+str(addr[0])+" through "+str(addr[1]))
	receivedData = conn.recv(4096).decode()
	print("Request:\n")
	print(receivedData)
	path = receivedData.split(" ")[1]
	if path == "/":
		fetchFile = "htdocs/index.html"
	else:
		fetchFile = "htdocs"+path
	print("Response\n")
	print("Fetching File: "+str(fetchFile))
	if(m.guess_type(fetchFile)[0]=="image/svg+xml" or m.guess_type(fetchFile)[0]=="image/png" or m.guess_type(fetchFile)[0] == "image/jpeg" or m.guess_type(fetchFile)[0] == "image/gif"):
		print("File Type: "+str(m.guess_type(fetchFile)[0]))
		outFile = open(fetchFile, "rb")	
		body = outFile.read()
		conn.sendall(httpResponseTemplate.format(length=len(body),type = m.guess_type(fetchFile)[0],body=bytes(body)).encode())
	else:
		print("File Type: "+str(m.guess_type(fetchFile)[0]))
		with open(fetchFile,'r') as outFile:
			body = outFile.read()
			conn.sendall(httpResponseTemplate.format(length=len(body),type = m.guess_type(fetchFile)[0],body=body).encode())
