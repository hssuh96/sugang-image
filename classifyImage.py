from PIL import Image
import numpy as np

def cal_diff(digit, img):
    avg_file_name = "image_data_labeled/{0}/avg_image.png".format(str(digit))
    img_avg = Image.open(avg_file_name)
    img_avg_arr = np.array(img_avg)
    img_avg_arr_float = np.asarray(img_avg_arr, dtype ='float32')

    img_arr = np.array(img)
    img_arr_float = np.asarray(img_arr, dtype ='float32')

    return np.linalg.norm(img_avg_arr_float - img_arr_float)


def classify_image(index):
    file_name = "image_data_resize/image_{0}.png".format(str(index))
    img = Image.open(file_name)

    diff_array = np.zeros(shape=10)

    for i in range(0,10):
        diff_array[i] = cal_diff(i, img)

    print(index, ": ", diff_array)
    estimate_digit = diff_array.argmin()
    save_file_name = "image_data_result/{0}/image_{1}.png".format(str(estimate_digit), str(index))
    img.save(save_file_name)

for i in range(1, 2001):
    classify_image(i)