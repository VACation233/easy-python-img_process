from PIL import Image, ImageFilter

img = Image.open('img.jpg')
blurred_img = img.filter(ImageFilter.GaussianBlur(radius=5))
blurred_img.show()
