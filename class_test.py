import pysftp
import unittest
import mock

class SFTPHelper(object):
    def __init__(self, host, username, password, files_dir):
        self.host = host
        self.username = username
        self.password = password
        self.files_dir = files_dir

    def list_files(self):
        with pysftp.Connection(
                self.host,
                username=self.username,
                password=self.password) as sftp:
            return sftp.listdir(self.files_dir)