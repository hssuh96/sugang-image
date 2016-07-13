from PIL import Image
import numpy as np

def createAverageImage(digit):
    save_file_name = "image_data_labeled/{0}/avg_image.png".format(str(digit))

    avg = np.zeros(shape = (30, 30), dtype = 'float32')

    for i in range(1,11):
        file_name = "image_data_labeled/{0}/image_{1}.png".format(str(digit), str(i))
        im = Image.open(file_name)
        im_arr = np.array(im)
        im_arr_float = np.asarray(im_arr, dtype = 'float32')
        avg = avg + (im_arr_float - avg) / i

    avg_uint8 = np.asarray(avg, dtype ='uint8')
    im_avg = Image.fromarray(avg_uint8, 'L')
    im_avg.save(save_file_name)

for i in range(0, 10):
    createAverageImage(i)