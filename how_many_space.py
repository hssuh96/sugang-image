from PIL import Image
import numpy as np
import classifyImage

color_saved = [192, 128, 64]


def show_img_from_np_array(arr):
    arr_uint8 = np.asarray(arr, dtype='uint8')
    # print(arr_bool)
    img = Image.fromarray(arr_uint8, 'L')
    img.show()


def find_white_tile(arr):
    for i in range(0, arr.shape[0]):
        for j in range(0, arr.shape[1]):
            if arr[i, j] == 255:
                return (i, j)

    return (-1, -1)


def color_of_tile(arr, index):
    if index[0] < 0 or index[0] >= arr.shape[0] or index[1] < 0 or index[1] >= arr.shape[1]:
        return 192
    else:
        return arr[index]


def have_to_fill(arr, index, step_num):
    index_diff_list = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    for index_diff in index_diff_list:
        color_tmp = color_of_tile(arr, (index[0] + index_diff[0], index[1] + index_diff[1]))
        if color_tmp == color_saved[step_num] and arr[index] != color_saved[step_num]:
            return True

    return False


def filling_step(arr, step_num):
    fill_num = 0
    fill_x_min = arr.shape[0]
    fill_x_max = -1

    for i in range(0, arr.shape[0]):
        for j in range(0, arr.shape[1]):
            if arr[i, j] != 0:
                if have_to_fill(arr, (i, j), step_num):
                    fill_num += 1
                    arr[i, j] = color_saved[step_num]

                    if i > fill_x_max:
                        fill_x_max = i

                    if i < fill_x_min:
                        fill_x_min = i

    return fill_num, fill_x_min, fill_x_max


def cal_hole(arr):
    fill_num = -1
    hole_num = 0
    hole1_total_fill_num = 0
    hole2_total_fill_num = 0
    hole1_x_min = hole2_x_min = arr.shape[0]
    hole1_x_max = hole2_x_max = -1
    hole1_x_avg = hole2_x_avg = -1
    hole1_len = hole2_len = 0

    # fill empty space
    while fill_num != 0:
        fill_num = filling_step(arr, 0)[0]
        # show_img_from_np_array(arr)
    fill_num = -1

    # fill color_1
    white_tile_index = find_white_tile(arr)

    if white_tile_index != (-1, -1):
        while fill_num != 0:
            arr[white_tile_index] = color_saved[1]
            fill_num, hole1_x_min_tmp, hole1_x_max_tmp = filling_step(arr, 1)
            hole1_total_fill_num += fill_num

            if hole1_x_min_tmp < hole1_x_min:
                hole1_x_min = hole1_x_min_tmp

            if hole1_x_max_tmp > hole1_x_max:
                hole1_x_max = hole1_x_max_tmp

            # show_img_from_np_array(arr)
    fill_num = -1

    # fill color_2
    white_tile_index = find_white_tile(arr)

    if white_tile_index != (-1, -1):
        while fill_num != 0:
            arr[white_tile_index] = color_saved[2]
            fill_num, hole2_x_min_tmp, hole2_x_max_tmp = filling_step(arr, 2)
            hole2_total_fill_num += fill_num

            if hole2_x_min_tmp < hole2_x_min:
                hole2_x_min = hole2_x_min_tmp

            if hole2_x_max_tmp > hole2_x_max:
                hole2_x_max = hole2_x_max_tmp

            # show_img_from_np_array(arr)

    if hole1_total_fill_num > 2:
        hole_num += 1
        hole1_x_avg = ((hole1_x_min+hole1_x_max)/2)/arr.shape[0]
        hole1_len = (hole1_x_max - hole1_x_min + 1)/arr.shape[0]

    if hole2_total_fill_num > 2:
        hole_num += 1
        hole2_x_avg = ((hole2_x_min+hole2_x_max)/2)/arr.shape[0]
        hole2_len = (hole2_x_max - hole2_x_min + 1)/arr.shape[0]

    if hole_num == 1 and hole1_x_avg == -1:
        hole1_x_avg = hole2_x_avg
        hole1_len = hole2_len

    return hole_num, hole1_x_avg, hole1_len , hole2_x_avg, hole2_len


def classify_image_method2(img):
    arr = np.array(img)

    hole_num, hole1_x_avg, hole1_len, hole2_x_avg, hole2_len = cal_hole(arr)

    # print("hole num: ", hole_num, " hole1 x: ", hole1_x_avg, " hole1 len: ", hole1_len, " hole2 x: ", hole2_x_avg, " hole2 len: ", hole2_len)

    if hole_num == 2:
        return 8
    elif hole_num == 1:
        if hole1_x_avg < 0.3:
            return 9
        elif hole1_x_avg > 0.55:
            return 6
        elif hole1_len > 0.5:
            return 0
        else:
            return 4
    else:
        return -1


for index in range(1, 2001):
    file_name = "image_data_processed/image_{0}.png".format(str(index))
    img = Image.open(file_name).convert('L')
    estimate_digit = classify_image_method2(img)

    save_file_name = "image_data_result/{0}/image_{1}.png".format(str(estimate_digit), str(index))
    img.save(save_file_name)


"""
for digit in range(0, 10):
    print("---------------------------------------------------------------")
    print("digit: ", digit)

    for index in range(1, 6):
        # file_name = "image_data_processed/image_{0}.png".format(str(index))
        file_name = "image_data_labeled_3/{0}/image_{1}.png".format(str(digit), str(index))

        img = Image.open(file_name).convert('L')
        classify_image_method2(img)
"""