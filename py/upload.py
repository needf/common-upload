# -*- coding: utf-8 -*-
import pycurl
import StringIO
import os
import math

chunksize=30000000
filename="/home/test.flv"

class FileReader:

    def __init__(self, fp, start, length):
        self.fp = fp
        self.fp.seek(start)
        self.length = length
    
    def read_callback(self, size):
        #print 'read_callback(%d)' % size
        if self.length == 0: # read all
            return "" 
        if self.length > size:
            self.length -= size
            #print 'set size = %d' % size
            return self.fp.read(size)
        else:
            size = self.length
            self.length -= size
            return self.fp.read(size)

fout = StringIO.StringIO()
filesize = os.path.getsize(filename)

c = pycurl.Curl()
c.setopt(c.URL, 'http://127.0.0.1/upload')
pf = [('test', (c.FORM_FILE, filename,c.FORM_CONTENTTYPE,'application/x-rar-compressed')) ]
c.setopt(c.HTTPPOST, pf)
c.setopt(c.VERBOSE, 1)
num=int(filesize/chunksize)+1
b = StringIO.StringIO()
c.setopt(pycurl.WRITEFUNCTION, b.write)
for i in range(1,num):
    c.setopt(pycurl.INFILESIZE, chunksize)
    c.setopt(pycurl.READFUNCTION, FileReader(open(filename, 'rb'), (i-1)*chunksize,chunksize).read_callback)
    c.setopt(pycurl.RANGE,'%s-%s' % ((i-1)*chunksize,i*chunksize))
    c.perform()
    print b.getvalue()
    #response_code = c.getinfo(pycurl.RESPONSE_CODE)
    #response_data = fout.getvalue()
    #print response_code
    #print response_data
c.close()
