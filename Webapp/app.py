import streamlit as st
import os
import tensorflow as tf
import IPython.display as display

import matplotlib.pyplot as plt
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (12, 12)
mpl.rcParams['axes.grid'] = False

import numpy as np
import PIL.Image
import time
import functools

# Convertir le tenseur en image
def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return PIL.Image.fromarray(tensor)

# Définir les fonctions de chargement et d'affichage des images
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

def main():
    content_folder_path = './content_images'
    style_folder_path = './style_images'

    content_images = os.listdir(content_folder_path)
    style_images = os.listdir(style_folder_path)

    selected_content_image = st.sidebar.selectbox("Select a content image:", content_images)
    selected_style_image = st.sidebar.selectbox("Select a style image:", style_images)

    content_path = os.path.join(content_folder_path, selected_content_image)
    style_path = os.path.join(style_folder_path, selected_style_image)

    content_image = load_img(content_path)
    style_image = load_img(style_path)

    return content_image, style_image

if __name__ == "__main__":
    content_image, style_image = main()

    # Convertir les images TensorFlow en tableaux NumPy
    content_image_np = content_image.numpy()
    style_image_np = style_image.numpy()

    # Afficher les images sélectionnées
    st.image(content_image_np, caption="Selected Content Image")
    st.image(style_image_np, caption="Selected Style Image")

    if st.button('Lancer le modèle'):
        # Définir les fonctions pour les couches VGG et l'extraction de caractéristiques
        def vgg_layers(layer_names):
            vgg = tf.keras.applications.VGG19(include_top=False, weights='imagenet')
            vgg.trainable = False
            outputs = [vgg.get_layer(name).output for name in layer_names]
            model = tf.keras.Model([vgg.input], outputs)
            return model

        # Les couches intérmédiaires:
        content_layers = ['block5_conv2']

        style_layers = ['block1_conv1',
                        'block2_conv1',
                        'block3_conv1',
                        'block4_conv1',
                        'block5_conv1']

        # Extraire les caractéristiques de style:
        style_extractor = vgg_layers(style_layers)
        style_outputs = style_extractor(style_image*255)

        def gram_matrix(input_tensor):
            result = tf.linalg.einsum('bijc,bijd->bcd', input_tensor, input_tensor)
            input_shape = tf.shape(input_tensor)
            num_locations = tf.cast(input_shape[1] * input_shape[2], tf.float32)
            return result / (num_locations)

        # Définir la classe de modèle StyleContentModel
        class StyleContentModel(tf.keras.models.Model):
            def __init__(self, style_layers, content_layers):
                super(StyleContentModel, self).__init__()
                self.vgg = vgg_layers(style_layers + content_layers)
                self.style_layers = style_layers
                self.content_layers = content_layers
                self.num_style_layers = len(style_layers)
                self.vgg.trainable = False

            def call(self, inputs):
                inputs = inputs * 255.0
                preprocessed_input = tf.keras.applications.vgg19.preprocess_input(inputs)
                outputs = self.vgg(preprocessed_input)
                style_outputs, content_outputs = (outputs[:self.num_style_layers],
                                                  outputs[self.num_style_layers:])

                style_outputs = [gram_matrix(style_output) for style_output in style_outputs]

                content_dict = {content_name: value for content_name, value in zip(self.content_layers, content_outputs)}
                style_dict = {style_name: value for style_name, value in zip(self.style_layers, style_outputs)}

                return {'content': content_dict, 'style': style_dict}

        extractor = StyleContentModel(style_layers, content_layers)
        style_targets = extractor(style_image)['style']
        content_targets = extractor(content_image)['content']

        # Définir la fonction de perte de style et de contenu
        def style_content_loss(outputs):
            style_outputs = outputs['style']
            content_outputs = outputs['content']
            style_loss = tf.add_n([tf.reduce_mean((style_outputs[name] - style_targets[name]) ** 2)
                                   for name in style_outputs.keys()])
            style_loss *= 1e-2 / len(style_layers)

            content_loss = tf.add_n([tf.reduce_mean((content_outputs[name] - content_targets[name]) ** 2)
                                     for name in content_outputs.keys()])
            content_loss *= 1e4 / len(content_layers)
            loss = style_loss + content_loss
            return loss

        def clip_0_1(image):
            return tf.clip_by_value(image, clip_value_min=0.0, clip_value_max=1.0)

        @tf.function()
        def train_step(image):
            with tf.GradientTape() as tape:
                outputs = extractor(image)
                loss = style_content_loss(outputs)
                loss += 30 * tf.image.total_variation(image)

            grad = tape.gradient(loss, image)
            opt.apply_gradients([(grad, image)])
            image.assign(clip_0_1(image))

        # Convertir l'image de contenu en variable tensor
        image = tf.Variable(content_image)

        # Définir l'optimisateur
        opt = tf.keras.optimizers.Adam(learning_rate=0.02, beta_1=0.99, epsilon=1e-1)

        # Entrainement du modèle
        start = time.time()

        epochs = 3
        steps_per_epoch = 100

        step = 0
        for n in range(epochs):
            for m in range(steps_per_epoch):
                step += 1
                train_step(image)
                print(".", end='', flush=True)
            st.image(tensor_to_image(image), caption=f"Train step: {step}")

        # Enregistrer l'image résultante sur le disque
        result_image = tensor_to_image(image)
        st.image(result_image, caption="Resulting Image")
