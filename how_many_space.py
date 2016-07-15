from PIL import Image
import numpy as np

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
    for i in range(0, arr.shape[0]):
        for j in range(0, arr.shape[1]):
            if arr[i, j] != 0:

                if have_to_fill(arr, (i, j), step_num):
                    fill_num += 1
                    arr[i, j] = color_saved[step_num]

    return fill_num


def cal_hole_num(arr):
    fill_num = -1
    hole_num = 0

    # fill empty space
    while fill_num != 0:
        fill_num = filling_step(arr, 0)
        # show_img_from_np_array(arr)

    fill_num = -1

    #fill color_1
    white_tile_index = find_white_tile(arr)

    if white_tile_index != (-1, -1):
        hole_num = 1
        while fill_num != 0:
            arr[white_tile_index] = color_saved[1]
            fill_num = filling_step(arr, 1)
            # show_img_from_np_array(arr)

    # fill color_2
    white_tile_index = find_white_tile(arr)

    if white_tile_index != (-1, -1):
        hole_num = 2
        while fill_num != 0:
            arr[white_tile_index] = color_saved[2]
            fill_num = filling_step(arr, 2)
            # show_img_from_np_array(arr)

    return hole_num

"""
for digit in range(0, 10):
    print("---------------------------------------------------------------")
    print("digit: ", digit)

    for index in range(1, 6):
        # file_name = "image_data_processed/image_{0}.png".format(str(index))
        file_name = "image_data_labeled_3/{0}/image_{1}.png".format(str(digit), str(index))

        img = Image.open(file_name).convert('L')
        arr = np.array(img)

        print("hole num: ", cal_hole_num(arr))
"""