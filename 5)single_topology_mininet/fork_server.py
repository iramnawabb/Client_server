import logging
import os
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import ThreadedFTPServer
from pyftpdlib.servers import MultiprocessFTPServer
from pyftpdlib.servers import FTPServer
from pyftpdlib.authorizers import DummyAuthorizer


def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user('user', '12345', '.')
    authorizer.add_anonymous(os.getcwd())
    handler = FTPHandler
    handler.authorizer = authorizer
    logging.basicConfig(level=logging.DEBUG)
    server = MultiprocessFTPServer(('10.0.0.2', 21), handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
