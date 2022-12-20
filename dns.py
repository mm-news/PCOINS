#參考：https://gist.github.com/pklaus/b5a7876d4d2cf7271873
import time, datetime
import sys, traceback, threading
from dnslib import *
import socketserver
import struct

class DN(str):
    def __getattr__(self, item):
        return DN(item+'.'+self)

