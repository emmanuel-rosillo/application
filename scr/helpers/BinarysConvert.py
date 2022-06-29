def imagesToBinary(filename):
    # Convert digital data to binary format
    try:
        with open(filename, 'rb') as file:
            binaryData = file.read()
        return binaryData
    except:
        return 0


def binaryToImages(user, photo):
    with open('unknow_{}.png'.format(id), 'wb') as f:
        f.write(photo)
