import tensorflow as tf
import PIL.Image
import os
from skimage import morphology, color
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

global generator


def load_model():
    saved_model_dir = 'saved_model_filter'
    global generator
    generator = tf.keras.models.load_model(os.path.join(saved_model_dir, 'generator'))


def run(filename):
    for file in filename:
        predicted_image = __prediction__(file)
        __post_processing__(predicted_image, file)


def __expand2square__(pil_img, background_color):
    width, height = pil_img.size
    if width == height:
        return pil_img
    elif width > height:
        result = PIL.Image.new(pil_img.mode, (width, width), background_color)
        result.paste(pil_img, (0, (width - height) // 2))
        return result
    else:
        result = PIL.Image.new(pil_img.mode, (height, height), background_color)
        result.paste(pil_img, ((height - width) // 2, 0))
        return result


def __prediction__(filename):
    input_folder = 'input'
    output_folder = 'output'
    global generator

    input_image = PIL.Image.open(os.path.join(input_folder, filename))
    if input_image is not None:
        if input_image.mode in ("RGBA", "P"):
            input_image = input_image.convert("RGB")

        input_image = __expand2square__(input_image, (255, 0, 0))
        input_image = tf.keras.preprocessing.image.img_to_array(input_image)
        input_image = tf.cast(input_image, tf.float32)

        input_image = tf.image.resize(input_image, [512, 512], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        input_image = (input_image / 127.5) - 1

        input_image = input_image[None, :, :, :]
        prediction = generator(input_image, training=True)
        prediction = tf.keras.preprocessing.image.array_to_img(prediction[0])
        path = os.path.join(output_folder, change_extension(filename))
        prediction.save(path)

        return path


def __post_processing__(path, filename):
    DELTA = 50
    dir_path = 'result'

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    image = plt.imread(path)

    tmp = color.rgb2gray(image)
    tmp = np.where(tmp > 0.1, 1, 0)

    tmp = morphology.binary_closing(tmp, morphology.square(5))
    tmp = morphology.remove_small_objects(tmp.astype(bool), min_size=50, connectivity=2).astype(int)

    last_start = -1
    last_end = -1

    for row in range(tmp.shape[0]):
        first = -1
        last = -1
        right = tmp.shape[1] - 1
        left = 0

        left_border_found = False
        right_border_found = False

        while (left_border_found is False or right_border_found is False) and left <= right:

            if left_border_found is False:
                if tmp[row][left] != 0:
                    if last_start == -1 or (last_start - DELTA <= left <= last_start + DELTA):
                        first = left
                else:
                    if first != -1:
                        left_border_found = True

                left += 1

            if right_border_found is False:
                if tmp[row][right] != 0:
                    if last_end == -1 or (last_end - DELTA <= right <= last_end + DELTA):
                        last = right
                else:
                    if last != -1:
                        right_border_found = True
                right -= 1

        if right_border_found is True and left_border_found is True:
            last_end = last
            last_start = first

        if first != -1 and last != -1:
            for i in range(first + 5, last - 5):
                tmp[row][i] = 0

    tmp = morphology.binary_closing(tmp, morphology.square(20))
    tmp = morphology.remove_small_objects(tmp.astype(bool), min_size=255, connectivity=2).astype(int)

    mask_x, mask_y = np.where(tmp == 0)
    image[mask_x, mask_y, :3] = 0

    final_img = Image.fromarray(np.uint8(image * 255))
    final_img.save(os.path.join(dir_path, change_extension(filename)))


def change_extension(filename):
    extension_to_add = "png"

    if filename.endswith('jpg') or filename.endswith('png'):
        ext_len = 3
    elif filename.endswith('jpeg'):
        ext_len = 4
    else:
        raise ValueError('File format not supported')

    return filename[0: len(filename) - ext_len] + extension_to_add
