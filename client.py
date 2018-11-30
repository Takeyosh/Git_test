# -*- coding: utf-8 -*-
# client.py
#https://news.mynavi.jp/article/python-32/
#http://blog.fujimisakari.com/network_programing_with_python/

from socket import *
import time
import sys
import pbl2018

def SIZE(client, fn):
	#要求するファイルのデータサイズを取得
	client.send(('SIZE ' + fn + '\n').encode())	#ファイルのサイズを要求
	message = client.recv(1024).decode()		#メッセージを受け取る
	print(message)
	message = message.split()

	if message[0] == 'OK':
		return int(message[2])
	elif message[1] == 101 :
		print('Please change the file name.\n')
		sys.exit()
	else :
		print('Please rewrite the command.\n') 
		sys.exit()

def GET(client, fs, fn, gd):
	#ファイル全体を要求し、ファイルデータを受信
	message = 'GET ' + fn + ' ' + gd + ' ALL\n'
	print(message)
	recv_bytearray = bytearray()
	while True:
		b = client.recv(1)
		recv_bytearray.append(b[0]) 
		if b == b'\n':
			recv_str = recv_bytearray.decode()
			break
	recv_message = recv_str.split()
	print(recv_str)
	if recv_message[0] == 'OK':				
		data = client.recv(int(fs)).decode()
		return data	
	elif recv_message[1] == '101':
		print('No such file.\n')
		sys.exit()
	elif recv_message[1] == '102':
		print('Invalid range.\n')
		sys.exit()
	else:
		print('Please rewrite the command.\n')
		sys.exit()	

	
def REP(client, fn, dig):
	#受信したファイルのダイジェストをサーバに報告
	client.send('REP ' + fn + ' ' + dig + '\n').encode()
	message = client.recv(1024).decode().split()
	if message[0] == 'OK':
		print('Tile transfer finished: Transmission time: {0}'.format(float(message[9]))) 
	elif message[1] == 101 :
		print('Please change the file name.\n')
		sys.exit()
	elif message[1] =='103':
		print('Failed to receive file data.\n')
		sys.exit()
	else :
		print('Please rewrite the command.\n') 
		sys.exit()


if __name__ == '__main__':
	# main program
	server_name = sys.argv[1]	#第一引数　サーバのIPアドレスあるいはホスト名
	server_port = int(sys.argv[2])	#第二引数　ポート番号
	file_name = sys.argv[3]		#第三引数　ファイル名
	token_str = sys.argv[4]		#第四引数　トークン文字列
	genkey_data = pbl2018.genkey(token_str)

	#ファイルサイズ要求
	size_socket = socket(AF_INET, SOCK_STREAM)
	size_socket.connect((server_name, server_port))
	file_size = SIZE(size_socket, file_name)
	size_socket.close()	

	#ファイル全体を要求
	get_socket = socket(AF_INET, SOCK_STREAM)
	get_socket.connect((server_name, server_port))	
	file_data = GET(get_socket, file_size, file_name, genkey_data)
	get_socket.close()

	#ダイジェストを計算
#	digest = pbl2018.repkey(token_str, file_name)	

	#ダイジェストを報告
#	digest_socket = socket(AF_INET, SOCK_STREAM)
#	digest_socket.connect((server_name, server_port))
#	REP(client_socket, file_name, digest)
#	digest_socket.close()
