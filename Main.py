import urllib2
import sys
import re, os
import base64
from urlparse import urlparse
import requests

regex = '<p><a href="(.+html)">Flash Version</a></p>'
PrettyNameRegex = '<td><div align="center"><b><a href="%s">([^<]+)</a>'
VideoPageRegex = 'file: "(.+mp4)",'

BASE_URL = None
username = None
password = None

def DownloadFile(URL, FileName, username, password):
    try:
        with open(FileName):
            print 'File Already Exists'
    except:
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        # this creates a password manager
        passman.add_password(None, URL, username, password)
        # because we have put None at the start it will always
        # use this username/password combination for  urls
        # for which URL is a super-url

        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        # create the AuthHandler

        opener = urllib2.build_opener(authhandler)

        urllib2.install_opener(opener)
        
        fw = open(FileName, mode='wb')

        fo = urllib2.urlopen(URL)
        data = fo.read(10240)
        l = len(data)
        print 'Starting Download ' + FileName
        while(l != 0 ):
            fw.write(data)
            data = fo.read(10240)
            l = len(data)

        print 'Downloading ' + FileName + ' done'
        fo.close()
        fw.close()

def GetSourceOnPasswordProtectedWebpage(URL, username, password):
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    # this creates a password manager
    passman.add_password(None, URL, username, password)
    # because we have put None at the start it will always
    # use this username/password combination for  urls
    # for which 'URL' is a super-url

    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    # create the AuthHandler

    opener = urllib2.build_opener(authhandler)

    urllib2.install_opener(opener)
    # All calls to urllib2.urlopen will now use our handler
    # Make sure not to include the protocol in with the URL, or
    # HTTPPasswordMgrWithDefaultRealm will be very confused.
    # You must (of course) use it when fetching the page though.
    # authentication is now handled automatically for us

    return urllib2.urlopen(URL).read()

def Main(BASE_URL, TargetDirectory, username, password):
    Main_URL = BASE_URL + 'video.html'
    source = GetSourceOnPasswordProtectedWebpage(Main_URL, username, password)

    for Link in re.findall(regex, source):
        for Name in re.findall(PrettyNameRegex % Link, source):
            PrettyName = Name + '.mp4'
        VideoPageSource = GetSourceOnPasswordProtectedWebpage(BASE_URL + Link, username, password)
        for VideoPageLink in re.findall(VideoPageRegex, VideoPageSource):
            DownloadFile(VideoPageLink, os.path.join(TargetDirectory, PrettyName), username, password)

if __name__ == "__main__":
    BASE_URL = sys.argv[1:]
    TargetDirectory = sys.argv[2:]
    username = sys.argv[3:]
    password = sys.argv[4:]

    if not BASE_URL:
            BASE_URL = raw_input("Base URL: ")
    if not TargetDirectory:
            TargetDirectory = raw_input("Enter Target Directory: ")
    if not username:
            username = raw_input("Enter Username: ")
    if not password:
            password = raw_input("Enter Password: ")
            
    Main.Main(BASE_URL, TargetDirectory, username, password)

