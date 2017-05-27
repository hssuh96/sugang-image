import urllib.request
import time

imageNum = 0
filename = ""

for i in range(1, 1001):
    imageNum += 1
    filename = "image_data_test/image_{0}.png".format(str(imageNum))
    urllib.request.urlretrieve("http://sugang.snu.ac.kr/sugang/ca/number.action?v=0.4610331197216959", filename)

    time.sleep(0.5)
