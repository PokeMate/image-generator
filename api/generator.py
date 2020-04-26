import tensorflow as tf
import matplotlib as mpl
import numpy as np
import PIL.Image
import tensorflow_hub as hub
import os

mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False

IMAGE_DIR = "{}/api/static/cleaned-images".format(os.getcwd())


class ImageGenerator:
    def __init__(self):
        self.hub_module = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/1')
        self.num_pokemons = count_files(IMAGE_DIR)

    def generate_image(self, id1, id2):
        print(self.num_pokemons)

        path1 = "{}/{}.png".format(IMAGE_DIR, id1)
        path2 = "{}/{}.png".format(IMAGE_DIR, id2)
        path3 = "{}/{}.png".format(IMAGE_DIR, self.num_pokemons + 1)

        print("generating image for {} and {}".format(path1, path2))

        content_path = path1
        style_path = path2

        content_image = load_img(content_path)
        style_image = load_img(style_path)

        stylized_image = self.hub_module(tf.constant(content_image), tf.constant(style_image))[0]
        new_image = tensor_to_image(stylized_image)
        new_image.save(path3)
        self.num_pokemons = count_files(IMAGE_DIR)
        print(self.num_pokemons)
        return self.num_pokemons


def tensor_to_image(tensor):
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)


def load_img(path_to_img):
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img


def count_files(dir):
    return len([1 for x in list(os.scandir(dir)) if x.is_file()])
