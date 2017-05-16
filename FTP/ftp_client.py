# More information around ftp and its purposes and uses
#
#
#
# ftp_client.py
# Wil Hergenrader
# v1.1 5.15.2017
#------------------------------------------------------------


# Import useful models, all standard with Python3.6
import ftplib, os, sys, socket

# Set download/upload folders to be used in retrieving and storing files on ftp
DOWNLOAD = 'parent/download/'
UPLOAD = 'parent/upload/'

# Use os to move to files where you want to download/upload files
os.chdir(os.curdir+DOWNLOAD)


# Open File Transfer Protocol (FTP)
# TIGER database is a subdirectory of ftp2.census.gov host ftp
url = 'ftp2.census.gov'
try:
    ftp = ftplib.FTP(url)
    print('CONNECTED TO HOST: "%s"' % url)
except (socket.error, socket.gaierror) as e:
    print('ERROR: cannot reach "%s"' % url)
    ftp.quit()

# Login to ftp, username and password optional in some cases
# type(username, passwd): strs
username = None
passwd = None
try:
    ftp.login(username, passwd)
    print('LOGGED IN')
except ftplib.error_perm:
    print('ERROR: cannot login anonymously')
    ftp.quit()




# Move to desired folder location, TIGER DATABASE and ROADS GIS DATA
toFolder = '/geo/tiger/TIGER2016/ROADS/'
try:
    ftp.cwd(toFolder)
    print('CHANGED FOLDER: "%s"' % url + toFolder)
except ftplib.error_perm:
    print('ERROR: cannot CD to "%s"' % url + toFolder)
    ftp.quit()

# dir returns files/folders in current ftp directory
# dir function takes a callable function, which is called once for each line in the server response
# Split ftp directory by space and return last item in list for folder/file name
data = []
ftp.dir(lambda s, c = data.append: c(s.split(' ')[-1]))



# Method to use to download .txt, .htm, .html files
# Must have lambda function to append new line characters
def gettext(ftp, filename, outfile = None):
    if outfile is None:
        outfile = sys.stdout
    ftp.retrlines('RETR' + filename, lambda s, w = outfile.write: w(s+'\n'))
    

# Download binary files (anything not .txt, .htm, .html)
def getbinary(ftp, filename, outfile = None):
    if outfile is None:
        outfile = sys.stdout
    ftp.retrbinary('RETR ' + filename, outfile.write)
    
def upload(ftp, file):
    ext = os.path.splitext(file)[1]
    if ext in ('.txt', '.htm', '.html'):
        ftp.storlines('STOR ' + file, open(file))
    else:
        ftp.storbinary('STOR ' + file, open(file, 'rb', 1024))
    
ftp.quit()
print('FTP CLIENT CLOSED: END PROGRAM')
