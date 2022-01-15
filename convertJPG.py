from PIL import Image
img=Image.open("mon_image.ppm")
img.save("JPG/mon_image.jpg")

img=Image.open("mon_image_dest_blur.ppm")
img.save("JPG/mon_image_dest_blur.jpg")

img=Image.open("mon_image_dest_horisobel.ppm")
img.save("JPG/mon_image_dest_horisobel.jpg")

img=Image.open("mon_image_dest_sharpen.ppm")
img.save("JPG/mon_image_dest_sharpen.jpg")

img=Image.open("mon_image_dest_shatter.ppm")
img.save("JPG/mon_image_dest_shatter.jpg")

img=Image.open("mon_image_dest_soften.ppm")
img.save("JPG/mon_image_dest_soften.jpg")

img=Image.open("mon_image_dest_softer.ppm")
img.save("JPG/mon_image_dest_softer.jpg")

img=Image.open("mon_image_dest_versobel.ppm")
img.save("JPG/mon_image_dest_versobel.jpg")
