# based on https://realpython.com/python-sockets/

import os
import socket
import selectors
import types
import logging

class Rcon:
    def __init__(self, receive_event_callback):
        self.host = os.environ.get('SERVER_HOST', '192.168.0.80')
        self.port = int(os.environ.get('SERVER_PORT', '65432'))
        self.receive_event_callback = receive_event_callback        
        self.print()
        self.create_socket()        
        
    def create_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.socket.setblocking(False)
        sel = selectors.DefaultSelector()
        sel.register(self.socket, selectors.EVENT_READ, data=None)
        self.event_loop(sel)        
    
    def event_loop(self, sel):
        while True:
            events = sel.select(timeout=None)
            for key, mask in events:
                if key.data is None:
                    self.accept(key.fileobj, sel)
                else:
                    self.service_connection(key, mask, sel)
                    
    def accept(self, socket, selector):
        connection, address = socket.accept()
        logging.info('accepted connection from ' + str(address))
        connection.setblocking(False)
        data = types.SimpleNamespace(addr=address, intb=b'', outb=b'')
        events = selectors.EVENT_READ | selectors.EVENT_WRITE
        selector.register(connection, events, data=data)
        
    def service_connection(self, key, mask, selector):
        self.socket = key.fileobj
        data = key.data
        if mask & selectors.EVENT_READ:
            receive_data = self.socket.recv(1024)
            if receive_data:
                logging.debug('received data: ' + str(receive_data))
                data.outb += receive_data
                self.receive_event_callback(receive_data.decode('utf-8'))
            else:
                logging.info('closing connection to ' + str(data.addr))
                selector.unregister(self.socket)
                self.socket.close()
        if mask & selectors.EVENT_WRITE:
            if data.outb:
               print('echoing', repr(data.outb), 'to', data.addr)
               sent = self.socket.send(data.outb)
               data.outb = data.outb[sent:]
    
    def print(self):
        logging.info('host ' + self.host + ' and port ' + str(self.port))