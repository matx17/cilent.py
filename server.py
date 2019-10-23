import socket,re,sys,select
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if (len(sys.argv)!=2):
   print("how to use for terminals-> python chatserver.py server_ip_add:port")
args= str(sys.argv[1]).split(':')
host = str(args[0])
port = int(args[1])
clients_dict={}
cli_socket=[]
cli_socket.append(s)
cli_socket_temp=[]
cli_socker_perm=[]
s.bind((host,port))
s.listen(100)

def broadcast(message, cli_conn):
    for conn in cli_socket_perm:
         if conn != cli_conn :
            try:
	        conn.send(message.encode('utf-8'))
            except:
                conn.close()
                cli_socket_perm.remove(conn)
                del clients_dict[conn]
                cli_socket.remove(conn)
                
           

def acpt_clients():
    while 1:
        read_list,write_list,error_list=select.select(Socket_list,[],[])
        for conn in read_list:
            if conn == s:
               newconn,addr=s.accept()
               print("connected with", addr)
               newconn.send("HELLO 1 \n".encode('utf-8'))
               cli_socket.append(newconn)
               cli_socket_temp.append(newconn)
            elif conn in cli_socket_temp:
                try:
          	   nick = conn.recv(1024).decode('utf-8')
          	   if nick:
                      find = re.search(r'NICK\s(\S*)',nick)
                      name = str(find.group(1))
                      if len(name)>12:
                	 conn.send("Error-> your nickname shouls be less than 12 characters")
            	      elif re.search(r'#',name) or re.search(r'\$',name) or re.search(r'!',name) or re.search(r'@',name) or re.search(r'\*',name):
                         conn.send("Error-> Don't use special characters i your nickname")
             	      elif find:
                         conn.send("%s connect to chat \n"%name)
                         cli_socket_perm.append(conn)
                         clients_dict[conn]=name
                         cli_socket_temp.remove(conn)
                      else: 
                         conn.send("Error-> Actual command protocal is NICK <nick>")
                   else:
                      conn.close()
                      cli_socket.remove(conn) 
                      cli_socket_temp.remove(conn)
                except:
                   continue
            elif conn in cli_socket_perm:
                try:	
                   message= conn.recv(1024).decode('utf-8')
                   if message:
                            find = re.search(r'MSG\s',message)
                            if len(message)>250:
                               conn.send("Error-> message should not exceed 250 char")
                            elif find:
                               msg = 'MSG '+str(clients_dict[conn])+':'+message[4:]
                               broadcast(msg,conn)
                            else:
                               conn.send("Error Actual command is MSG <msg>")
                   else: 
                       conn.close()
                       cli_socket.remove(conn)
                       cli_socket_perm.remove(conn)
                       del clients_dict[conn]
                except:
                    continue

   s.close()
if __name__ == "__main__":
    acpt_clients()
