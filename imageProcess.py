from PIL import Image
import numpy as np


def image_save(index):
    filename = "image_data/image_{0}.png".format(str(index))
    filename1 = "image_data_processed/image_{0}.png".format(str(2 * index - 1))
    filename2 = "image_data_processed/image_{0}.png".format(str(2 * index))

    im = Image.open(filename)
    pix = im.load()

    im1 = Image.new('1', (26, 26), color=1)
    im2 = Image.new('1', (26, 26), color=1)

    pix1 = im1.load()
    pix2 = im2.load()

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


    im1Arr_min = im1Arr.min(axis=0)
    im1Arr_max = im1Arr.max(axis=0)
    im1Arr = im1Arr - (im1Arr_min + im1Arr_max) / 2 + [13, 13]

    im2Arr_min = im2Arr.min(axis=0)
    im2Arr_max = im2Arr.max(axis=0)
    im2Arr = im2Arr - (im2Arr_min + im2Arr_max) / 2 + [13, 13]


    for i in range(0, im1Arr.shape[0]):
        pix1[int(im1Arr[i, 0]), int(im1Arr[i, 1])] = 0

    for i in range(0, im2Arr.shape[0]):
        pix2[int(im2Arr[i, 0]), int(im2Arr[i, 1])] = 0


    im1.save(filename1)
    im2.save(filename2)

    # print("img1 size: ", im2Arr_max - im2Arr_min)
    # print("img2 size: ", im2Arr_max - im2Arr_min)


for i in range(1, 1001):
    image_save(i)
