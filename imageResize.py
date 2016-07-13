from PIL import Image


def image_save(index):
    filename = "image_data_processed/image_{0}.png".format(str(index))
    filename2 = "image_data_resize/image_{0}.png".format(str(index))

    im = Image.open(filename).convert('L')

    im2 = im.resize((30,30), Image.LANCZOS)

    im2.save(filename2)


for i in range(1, 1001):
    image_save(i)