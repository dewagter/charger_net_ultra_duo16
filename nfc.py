import nxppy

class Tag():
    id = ''
    new = 0


tag = Tag()

def nfc_server():

    while True:
        uid=nxppy.read_mifare()
        if uid is not None:
            break
        tag.id = uid
        tag.new = 1
        print uid
