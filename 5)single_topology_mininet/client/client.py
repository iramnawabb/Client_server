from ftplib import FTP
import os
import ftplib
import socket
import time
import datetime
import sys
import time, random
import threading

class ftpClient:
    total_length = 0
    start_time = 0

    def __init__(self):
        pass
    def log(self, s):
        # print ('%s : %s'%(datetime.datetime.now(), s)
        return 0

    def progressBar(self, bytes_for_a_dot, dot_bytes) :
            while dot_bytes > bytes_for_a_dot :
                sys.stdout.write('.')
                sys.stdout.flush()
                dot_bytes -= bytes_for_a_dot 
            return dot_bytes

    def start(self, fileName):
        with FTP('10.0.0.2', 'user', '12345') as ftp:
            # List files
            files = []
            ftp.dir(files.append)  # Takes a callback for each file
            #for f in files:
               #	 print(f)
            filename = fileName
            # Write file in binary mode
            # with open(filename, "wb") as file:
            #     # Command for Downloading the file "RETR filename"
            #     res = ftp.retrbinary('RETR %s' % filename, file.write)
            #     if not res.startswith('226 Transfer complete'):
            #         logging.error('Downloaded of file {0} is not compile.'.format(filename))
            #         os.remove(filename)
            #     else:
            #         print(filename)
            local_filename = filename
            # ftp = ftplib.FTP()
            ftp.set_debuglevel(0)
            ftp.set_pasv(True)
            

            with open(local_filename, 'w+b') as f :
                ftpClient.total_length = 0
                ftpClient.start_time = datetime.datetime.now()
                max_attempts = 3
                while True :
                    try :
                        # ftp.connect(self.host, self.port)
                        # ftp.login(self.login, self.passwd)
                        ftp.voidcmd('TYPE I')
                        filesize = ftp.size(filename)
                        sys.stdout.write('%sMB : '%(filesize / 1024 /1024))
                        bytes_for_a_dot = filesize / 80
                        dot_bytes = 0
                        if f.tell() :
                            sock = ftp.transfercmd('RETR ' + filename, f.tell()) 
                        else :
                            sock = ftp.transfercmd('RETR ' + filename)
                        while True :
                            blocksize = 1024*1024 #But it always takes 64KB?
                            block = sock.recv(blocksize)
                            if not block:
                                break
                            ftp.voidcmd('NOOP')
                            previous = f.tell()
                            f.write(block)
                            dot_bytes = self.progressBar(bytes_for_a_dot, dot_bytes + f.tell() - previous)
                        sock.close()
                        print
                        if filesize == f.tell() :
                            ftpClient.total_length += filesize
                            elapsed = (datetime.datetime.now() - ftpClient.start_time)
                            speed = (ftpClient.total_length / elapsed.total_seconds())
                            print("\n File: {2} Elapsed: {0} Throughput: {1:.2f} kB/s ".format(str(elapsed), speed / 1024, filename), end="\n")
                            # print( '\n Time taken ' + str(time.time() - start) + ' \n')  #r
                            break
                        else :
                            log("Filesize %s not matching FTP filesize %s" %(f.tell(),filesize))
                            raise
                    except :
                        max_attempts -= 1
                        if max_attempts == 0:
                            log("Giving up")
                            print(0)  #r
                            break
                        log('Waiting 10 seconds')
                        time.sleep(10)
                        log('Reconnecting')
                    print( '\n Time taken ' + str(time.time() - start) + ' \n')  #r
                    break
    def run(self,name):
        t1 = threading.Thread(target=self.start, args=(name,))
        t2 = threading.Thread(target=self.start, args=(name,))
        t3 = threading.Thread(target=self.start, args=(name,))
        t4 = threading.Thread(target=self.start, args=(name,))
        t5 = threading.Thread(target=self.start, args=(name,))
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()


ftpcli = ftpClient()

#-----Single Connections-----#

ftpcli.start("War and Peace.txt")
#ftpcli.start("The Secret of Chimneys.txt")
#ftpcli.start("Anna Karenina.txt")
#ftpcli.start("The Cat's Paw.txt")
#ftpcli.start("The Murder on the Links.txt")


#-----Multiple Connections-----#

#ftpcli.run("War and Peace.txt")
#ftpcli.run("The Secret of Chimneys.txt")
#ftpcli.run("Anna Karenina.txt")
#ftpcli.run("The Cat's Paw.txt")
#ftpcli.run("The Murder on the Links.txt")



