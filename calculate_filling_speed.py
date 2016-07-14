from PIL import Image
import numpy as np


def show_img_from_np_array(arr):
    arr_uint8 = np.asarray(arr, dtype='uint8')
    # print(arr_bool)
    img = Image.fromarray(arr_uint8, 'L')
    img.show()


def check_tile_filled(arr, index):
    if index[0] < -1 or index[0] >= arr.shape[0] or index[1] < 0 or index[1] >= arr.shape[1]:
        return False
    elif index[0] == -1: # first step
        return True
    elif arr[index] == 128:
        return True
    else:
        return False


def filling_step(arr):
    filled_num = 0
    to_fill_index = []
    # filling_end = False
    for i in range(0, arr.shape[0]):
        for j in range(0, arr.shape[1]):
            if arr[i, j] == 0:
                have_to_fill = False

                for k in range(-1, 2):
                    for l in range(-1, 2):
                        if check_tile_filled(arr, (i + k, j + l)) == True:
                            have_to_fill = True

                if have_to_fill == True:
                    filled_num += 1
                    to_fill_index.append((i, j))
                    """
                    if i == arr.shape[0]-1:
                        filling_end = True
                    """

    for fill_index in to_fill_index:
        arr[fill_index] = 128

    return filled_num


def calculate_filling_speed(arr):
    iteration_max = 20
    filled_num_array = []

    """
    # first step
    for j in range(0, arr.shape[1]):
        if arr[0, j] == 0:
            arr[0, j] = 128
    """
    for iteration in range(0, iteration_max):
        filled_num = filling_step(arr)
        if filled_num != 0:
            filled_num_array.append(filled_num)
        # show_img_from_np_array(arr)

    return filled_num_array

for digit in range(0, 10):
    print("---------------------------------------------------------------")
    print("digit: ", digit)

    for index in range(1, 6):
        # file_name = "image_data_processed/image_{0}.png".format(str(index))
        file_name = "image_data_labeled_3/{0}/image_{1}.png".format(str(digit), str(index))

        img = Image.open(file_name).convert('L')
        arr = np.array(img)

        print(calculate_filling_speed(arr))