import socket, subprocess,sys
from datetime import datetime

subprocess.call('clear',shell=True)
rmip = raw_input("t Enter the host IP to scan:")
r1 = int(raw_input("t Enter the start port numbert"))
r2 = int (raw_input("t Enter the last port numbert"))
print "*"*40
print "n Scanner is working on ",rmip
print "*"*40

t1= datetime.now()
try:
  for port in range(r1,r2):
    sock= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)

    result = sock.connect_ex((rmip,port))
    if result==0:
      print "Port Open:-->t", port
      # print desc[port]
    sock.close()

except KeyboardInterrupt:
  print "You stop this "
  sys.exit()

except Exception as e :
  print e
  sys.exit()

t2= datetime.now()

total =t2-t1
print "scanning complete in " , total
