from PIL import Image
import numpy as np

"""
식이 굉장히 더러워짐. 아이디어는 k-nearest clustering과 비슷
"""


def cal_diff(digit, img):
    avg_file_name = "image_data_labeled/{0}/avg_image.png".format(str(digit))
    img_avg = Image.open(avg_file_name)
    img_avg_arr = np.array(img_avg)
    img_avg_arr_float = np.asarray(img_avg_arr, dtype ='float32')

    img_arr = np.array(img)
    img_arr_float = np.asarray(img_arr, dtype ='float32')
    diff = img_avg_arr_float - img_arr_float
    return np.linalg.norm(diff)


def classify_image(img, digit_find_list):
    digit_array = {1:-1, 2:-1, 3:-1, 4:-1, 5:-1, 6:-1, 7:-1, 8:-1, 9:-1}

    for i in digit_find_list:
        # print(i)
        digit_array[i] = cal_diff(i, img)

    # print(index, ": ", diff_array)
    estimate_digit = digit_array.argmin()
    # save_file_name = "image_data_result/{0}/image_{1}.png".format(str(estimate_digit), str(index))
    # img.save(save_file_name)

    return estimate_digit


# for i in range(1, 2001):
#     classify_image(i)