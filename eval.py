import tensorflow as tf
import os
import PIL.Image

global generator

def load_model():
    saved_model_dir = 'saved_model_filter'
    global generator
    generator=tf.keras.models.load_model(os.path.join(saved_model_dir, 'generator'))



def expand2square(pil_img, background_color):
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

def run(filename):
    input_folder = 'input'
    output_folder = 'output'
    global generator

    input_image = PIL.Image.open(os.path.join(input_folder, filename))
    if input_image is not None:
        if input_image.mode in ("RGBA", "P"):
            input_image = input_image.convert("RGB")

        input_image = expand2square(input_image, (255, 0, 0))
        input_image = tf.keras.preprocessing.image.img_to_array(input_image)
        input_image = tf.cast(input_image, tf.float32)

        input_image = tf.image.resize(input_image, [512, 512], method=tf.image.ResizeMethod.NEAREST_NEIGHBOR)
        input_image = (input_image / 127.5) - 1

        input_image = input_image[None, :, :, :]
        prediction = generator(input_image, training=True)
        prediction = tf.keras.preprocessing.image.array_to_img(prediction[0])
        save_extension = '.png'
        path = os.path.join(output_folder, filename[:len(filename)-4])
        path = path + save_extension
        prediction.save(path)

    return filename.replace("jpg","png")