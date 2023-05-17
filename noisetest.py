from PIL import Image
import numpy as np

def add_gaussian_noise(image, mean=0, std=50):
    img = np.array(image)
    noise = np.random.normal(mean, std, img.shape)
    noisy_img = img + noise
    noisy_img = np.clip(noisy_img, 0, 255)
    noisy_img = Image.fromarray(noisy_img.astype(np.uint8))
    return noisy_img

img = Image.open('img.jpg')
noisy_img = add_gaussian_noise(img)
noisy_img.show()
