from PIL import Image
import numpy as np
import tensorflow as tf
import glob

N = 2000

def create_train_data():
    captcha_image = np.zeros([N, 784])
    captcha_label = np.zeros([N, 10])

    for index in range(1, N+1):
        # file to read
        filename = "image_data_processed/image_{0}.png".format(str(index))

        # open image and resize
        img = Image.open(filename).convert('L')
        img = img.resize((28, 28), Image.BILINEAR)

        # image to array
        img_arr = np.array(img)
        img_arr_float = np.asarray(img_arr, dtype='float32')

        # resize array and save it to data
        img_arr_float.resize((1, 784))
        captcha_image[index-1] = img_arr_float

    for digit in range(0,10):
        list = glob.glob("image_data_labeled/{0}/*.png".format(str(digit)))
        list_len = len(list)
        for i in range(0, list_len):
            img_index = int(list[i].split("_")[3].split(".")[0])
            captcha_label[img_index-1, digit] = 1

    return captcha_image, captcha_label, N


"""
def read_my_file_format(filename_queue):
    reader = tf.SomeReader()
    key, record_string = reader.read(filename_queue)
    example, label = tf.some_decoder(record_string)
    processed_example = some_processing(example)
    return processed_example, label


def input_pipeline(filenames, batch_size, num_epochs=None):
    filename_queue = tf.train.string_input_producer(
        filenames, num_epochs=num_epochs, shuffle=True)
    example, label = read_my_file_format(filename_queue)
    # min_after_dequeue defines how big a buffer we will randomly sample
    #   from -- bigger means better shuffling but slower start up and more
    #   memory used.
    # capacity must be larger than min_after_dequeue and the amount larger
    #   determines the maximum we will prefetch.  Recommendation:
    #   min_after_dequeue + (num_threads + a small safety margin) * batch_size
    min_after_dequeue = 10000
    capacity = min_after_dequeue + 3 * batch_size
    example_batch, label_batch = tf.train.shuffle_batch(
        [example, label], batch_size=batch_size, capacity=capacity,
        min_after_dequeue=min_after_dequeue)
    return example_batch, label_batch
"""

if __name__ == "__main__":
    create_train_data()