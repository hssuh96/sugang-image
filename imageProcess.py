from PIL import Image
import numpy as np

padding = np.array([0, 0])

def image_save(index):
    file_name = "image_data/image_{0}.png".format(str(index))
    file_name1 = "image_data_processed/image_{0}.png".format(str(2 * index - 1))
    file_name2 = "image_data_processed/image_{0}.png".format(str(2 * index))

    im = Image.open(file_name)
    pix = im.load()

    color1 = color2 = (192, 192, 192)

    im1Arr = []
    im2Arr = []

    for i in range(0, 52):
        for j in range(0, 26):
            pixVal = pix[i, j]

            if pixVal != (192, 192, 192):
                if pixVal == color1:
                    im1Arr.append([i, j])
                elif pixVal == color2:
                    im2Arr.append([i, j])
                else:
                    if color1 == (192, 192, 192):
                        color1 = pixVal
                        im1Arr.append([i, j])
                    else:
                        color2 = pixVal
                        im2Arr.append([i, j])

    im1Arr = np.array(im1Arr, dtype=int)
    im2Arr = np.array(im2Arr, dtype=int)


    im1_min = im1Arr.min(axis=0)
    im1_max = im1Arr.max(axis=0)
    im1_mid = (im1_min + im1_max)/2
    im1_size = im1_max - im1_min + [1,1] + 2*padding
    im1_size = np.array([im1_size.max(), im1_size.max()])
    im1Arr = im1Arr - im1_mid + im1_size/2

    im2_min = im2Arr.min(axis=0)
    im2_max = im2Arr.max(axis=0)
    im2_mid = (im2_min + im2_max)/2
    im2_size = im2_max - im2_min + [1,1] + 2*padding
    im2_size = np.array([im2_size.max(), im2_size.max()])
    im2Arr = im2Arr - im2_mid + im2_size / 2

    im1 = Image.new('1', im1_size, color=1)
    im2 = Image.new('1', im2_size, color=1)

    pix1 = im1.load()
    pix2 = im2.load()

    for i in range(0, im1Arr.shape[0]):
        pix1[int(im1Arr[i, 0]), int(im1Arr[i, 1])] = 0

    for i in range(0, im2Arr.shape[0]):
        pix2[int(im2Arr[i, 0]), int(im2Arr[i, 1])] = 0

    im1.save(file_name1)
    im2.save(file_name2)


for i in range(1, 1001):
    image_save(i)
