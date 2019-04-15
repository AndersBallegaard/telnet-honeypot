import select, socket, sys, queue
import logging
import logging.handlers

LOGFILE = "log/telnet.log"
LOGSIZEBYTES = 100000
LOGROTATIONCOUNT = 5

FORMAT = '%(asctime)-15s %(type)s %(address)s %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger("TELNET")
logger.setLevel(logging.DEBUG)
handler = logging.handlers.RotatingFileHandler(LOGFILE, maxBytes=LOGSIZEBYTES, backupCount=LOGROTATIONCOUNT)
handler.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(handler)




def log_raw(type_, address, msg):

    logger.warning(msg, extra={'type': type_, 'address': address})

def log_connected(address):
    log_raw('Connected', address, "Recived connection")

def log_disconnected(address):
    log_raw('Disonnected', address, "Client disconnected")

recived_tmp_store = {}

def log_recived(address, data):
    if address not in recived_tmp_store.keys():
        recived_tmp_store[address] = ''
    
    if data == '\r\x00' or data == '\n':
        log_raw("Recived", address, recived_tmp_store[address])
        recived_tmp_store[address] = ''
    else:
        #logger.info(data)
        recived_tmp_store[address] += data
    

HOST = '0.0.0.0'
PORT = 23


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setblocking(0)
server.bind((HOST, PORT))
server.listen(5)
inputs = [server]
outputs = []
message_queues = {}


while inputs:
    readable, writable, exceptional = select.select(
        inputs, outputs, inputs)
    for s in readable:
        if s is server:
            connection, client_address = s.accept()
            connection.setblocking(0)
            log_connected(client_address[0])
            inputs.append(connection)
            message_queues[connection] = queue.Queue()
        else:
            data = s.recv(1024)
            if data:
                message_queues[s].put(data)
                log_recived(client_address[0], data.decode('utf-8', errors='ignore'))
                if s not in outputs:
                    outputs.append(s)
            else:
                if s in outputs:
                    outputs.remove(s)
                inputs.remove(s)
                s.close()
                del message_queues[s]

    for s in writable:
        try:
            next_msg = message_queues[s].get_nowait()
        except queue.Empty:
            outputs.remove(s)
        else:
            s.send(next_msg)
            #s.send('d'.encode('utf-8'))

    for s in exceptional:
        inputs.remove(s)
        if s in outputs:
            outputs.remove(s)
        s.close()
        del message_queues[s]