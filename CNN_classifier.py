import tensorflow as tf
import numpy as np
from PIL import Image
import random

def weight_variable(shape):
    initial = tf.truncated_normal(shape, stddev=0.1)
    return tf.Variable(initial)


def bias_variable(shape):
    initial = tf.constant(0.1, shape=shape)
    return tf.Variable(initial)


def conv2d(x, W):
    return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')


def max_pool_2x2(x):
    return tf.nn.max_pool(x, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')


def create_batch(data, label, data_length, batch_num):
    start_index = random.randrange(0, data_length-batch_num)
    return data[start_index:start_index+batch_num], label[start_index:start_index+batch_num]


if __name__ == "__main__":

    """ Neural Network """
    # session
    sess = tf.InteractiveSession()

    # define input
    x = tf.placeholder(tf.float32, [None, 784])
    y_ = tf.placeholder(tf.float32, [None, 10])

    # reshape image
    x_image = tf.reshape(x, [-1, 28, 28, 1])
    x_image /= 256

    # first convolutional layer
    W_conv1 = weight_variable([5, 5, 1, 32])
    b_conv1 = bias_variable([32])

    h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
    h_pool1 = max_pool_2x2(h_conv1)

    # second convolutional layer
    W_conv2 = weight_variable([5, 5, 32, 64])
    b_conv2 = bias_variable([64])

    h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
    h_pool2 = max_pool_2x2(h_conv2)

    # fully connected layer
    W_fc1 = weight_variable([7 * 7 * 64, 1024])
    b_fc1 = bias_variable([1024])

    h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
    h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, W_fc1) + b_fc1)

    # dropout
    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    # readout layer
    W_fc2 = weight_variable([1024, 10])
    b_fc2 = bias_variable([10])

    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)

    # train step
    cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv + 1e-30), reduction_indices=[1]))
    train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

    # calculate accuracy
    correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y_, 1))
    accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

    # Add ops to save and restore all the variables.
    saver = tf.train.Saver(var_list={"W_conv1": W_conv1, "b_conv1": b_conv1, "W_conv2": W_conv2, "b_conv2": b_conv2,
                                     "W_fc1": W_fc1, "b_fc1": b_fc1, "W_fc2": W_fc2, "b_fc2": b_fc2})

    sess.run(tf.initialize_all_variables())

    saver.restore(sess, "train_result/model.ckpt")

    for index in range(1, 2001):
        # file to read
        filename = "image_data_test_processed/image_{0}.png".format(str(index))

        # open image and resize
        img_raw = Image.open(filename)
        img = img_raw.convert('L')
        img = img.resize((28, 28), Image.BILINEAR)

        # image to array
        img_arr = np.array(img)
        img_arr_float = np.asarray(img_arr, dtype='float32')

        # resize array and save it to data
        img_arr_float.resize((1, 784))

        estimate_digit = sess.run(tf.argmax(y_conv, 1),
                                  feed_dict={x: img_arr_float, y_: [[0, 0, 0, 0, 0, 0, 0, 0, 1, 0]], keep_prob: 1.0})[0]

        # print(estimate_digit)
        save_file_name = "image_data_result/{0}/image_{1}.png".format(str(estimate_digit), str(index))
        img_raw.save(save_file_name)