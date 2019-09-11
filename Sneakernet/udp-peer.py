#!/usr/bin/env python3

# sn/udp-peer.py

# import bluetooth
import base64
import select
import socket
import sys
import time

LOGS_DIR = 'logs'
import lib.gg       as gg
import lib.local_db as ldb

# server_sock=bluetooth.BluetoothSocket( bluetooth.L2CAP )

PEER_PORT = 0x1001
PUSH_PORT = 0x1002

# ---------------------------------------------------------------------------

def peer_loop(cmd_sock, push_sock, peer, push_port, peerID):
    print(f"** talking to {peer} ({peerID}), push_port is {push_port}")
    remote_push_port = 0
    push_queue = []

    local_db = ldb.LOCAL_DB()
    local_db.load(LOGS_DIR)

    cmd_queue = [ f'PORT {push_port}'.encode('utf8'), b'RECV 1']
    if len(local_db.max) > 0:
        lst = [ f'+{base64.b64encode(fs[0]).decode("utf8")}/{fs[1]}' for fs in local_db.max.items() ]
        # print(lst)
        cmd_queue.append(f'HAVE {" ".join(lst)}'.encode('utf'))
    #
    tend = time.time() + 5
    while time.time() < tend:
        if len(cmd_queue) > 0:
            msg = cmd_queue[0]
            cmd_queue = cmd_queue[1:]
            cmd_sock.sendto(msg, peer)
        if remote_push_port > 0 and len(push_queue) > 0:
            msg = push_queue[0]
            push_queue = push_queue[1:]
            push_sock.sendto(msg, (peer[0],remote_push_port))
        r,w,e = select.select([cmd_sock, push_sock],[],[], 0.5)
        if push_sock in r:
            data,_ = push_sock.recvfrom(1024)
            print(f'-- push socket: {len(data)} bytes')
            local_db.ingest(data)
            tend = time.time() + 5
        elif cmd_sock in r:
            data,_ = cmd_sock.recvfrom(1024)
            print(f'-- cmd socket: {data}')
            data = data.decode('utf8').split(' ')
            if data[0] == 'PORT':
                remote_push_port = int(data[1])
            elif data[0] == 'WANT':
                for fs in data[1:]:
                    fs = fs.split('/')
                    if fs[0][0] != '+':
                        continue
                    feed,seq = base64.b64decode(fs[0][1:]), int(fs[1])
                    while feed in local_db.db and seq in local_db.db[feed]:
                        push_queue.append(local_db.db[feed][seq])
                        seq += 1
            elif data[0] == 'HAVE':
                for fs in data[1:]:
                    fs = fs.split('/')
                    if fs[0][0] != '+':
                        continue
                    feed,seq = base64.b64decode(fs[0][1:]), int(fs[1])
                    if not feed in local_db.db:
                        cmd_queue.append(f'WANT +{fs[0][1:]}/1'.encode('utf8'))
                    elif seq > local_db.max[feed]:
                        cmd_queue.append(f'WANT +{fs[0][1:]}/{local_db.max[feed]+1}'.encode('utf8'))

    print("** peer_loop done")


# ----------------------------------------------------------------------
if __name__ == '__main__':

    if len(sys.argv) > 1:
        my_push_port = int(sys.argv[1])
        push_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        push_sock.bind(('', my_push_port))

        client_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client_sock.bind(('', PEER_PORT+2))
        # client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_sock.settimeout(1.0)

        peer = ("127.0.0.1", PEER_PORT)
        # client_sock.connect(peer)

        helo = b'HELO client\n'
        for i in range(10):
            # client_sock.send(helo)
            client_sock.sendto(helo, peer)
            try:
                # data = client_sock.recv(1024)
                data, peer = client_sock.recvfrom(1024)
                data = data.decode('utf8').split()
                if data[0] != 'HELO':
                    print("** received non-HELO message, trying again")
                    continue
                peer_loop(client_sock, push_sock, peer, my_push_port, data[1])
                client_sock.close()
                push_sock.close()
                sys.exit()
            except socket.timeout:
                print('** request timed out')
        print("** giving up")
        client_sock.close()
        push_sock.close()
    else:
        push_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        push_sock.bind(('', PUSH_PORT))

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # server_sock.listen(1)
        server_sock.bind(('', PEER_PORT))

        client_sock = server_sock
        while True:
            if False:
                client_sock, peer = server_sock.accept()
                print("Accepted connection from ", peer)
                # data, peer = client_sock.recvfrom(1024)
                data = client_sock.recv(2014)
            print(f"** listing on port {PEER_PORT}, push port is {PUSH_PORT}")
            data, peer = client_sock.recvfrom(1024)
            if not data:
                break
            data = data.decode('utf8').split()
            if data[0] != 'HELO':
                print("** received non-HELO message, trying again")
                continue
            # client_sock.sendto(('HELO server').encode('utf8'), peer)
            client_sock.sendto(('HELO server').encode('utf8'), peer)
            peer_loop(client_sock, push_sock, peer, PUSH_PORT, data[1])
            # print("Data received: ", str(data))
            # # client_sock.send('Echo => ' + str(data))
            # client_sock.sendto(('Echo => ' + str(data)).encode('utf8'), addr)

        push_sock.close()
        client_sock.close()
        server_sock.close()
