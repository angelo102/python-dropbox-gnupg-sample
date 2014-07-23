import pyinotify
import os
import sys
from DropboxFileSigner import DocSigner

'''
Class for handling events taht are watched for changes using
pyinotify
'''
class EventHandler(pyinotify.ProcessEvent):
    def process_IN_ACCESS(self, event):
        print "ACCESS event:", event.pathname

    def process_IN_ATTRIB(self, event):
        print "ATTRIB event:", event.pathname

    def process_IN_CLOSE_WRITE(self, event):
        print "CLOSE_WRITE event:", event.pathname
        #sign file
        docSigner = DocSigner()
        docSigner.getSettings()
        signedFile=docSigner.signFile(event.pathname)
        #delete file from folder
        os.remove(event.pathname)
        #upload signed file to dropbox
        filename = os.path.split(event.pathname)[-1]
        docSigner.uploadToDropbox(filename,signedFile.data)

    def process_IN_CREATE(self, event):
        print "CREATE event:", event.pathname

    def process_IN_ONESHOT(self, event):
        print "ONESHOT event:", event.pathname

    def process_IN_MOVE_SELF(self, event):
        print "MOVE_SELF event:", event.pathname

    def process_IN_DELETE(self, event):
        print "DELETE event:", event.pathname

    def process_IN_MODIFY(self, event):
        print "MODIFY event:", event.pathname

    def process_IN_OPEN(self, event):
        print "OPEN event:", event.pathname
        #print event
        if event.dir == False:
            docSigner = DocSigner()
            docSigner.getSettings()
            docSigner.verifyFile(event.pathname)
            sys.exit(1)

'''
Main class for running the watch on the apllication folder
'''
def main():
    # watch manager
    wm = pyinotify.WatchManager()
    docSigner = DocSigner()
    docSigner.getSettings()
    wm.add_watch(docSigner.dropbox_dir, pyinotify.ALL_EVENTS, rec=True)

    # event handler
    eh = EventHandler()

    # notifier
    notifier = pyinotify.Notifier(wm, eh)
    notifier.loop()

if __name__ == '__main__':
    main()
