import nxppy

class Tag():
    id = ''
    new = 0


tag = Tag()

def nfc_server():
    mifare = nxppy.Mifare()
    while True:
        uid=mifare.select()
        if uid is None:
            break
        tag.id = uid
        tag.new = 1
        print(uid)

nfc_server()
