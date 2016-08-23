from PIL import Image

example_image = '000039.jpg'

floyd_steinberg_matrix = [
                          [(-1, 0), (0, 0), (1, 7)],
                          [(-1, 3), (0, 5), (1, 1)]
                         ]
# We calculate the coefficient this way so we can change the matrix easily
coefficient = sum([part[1] for row in floyd_steinberg_matrix for part in row])

image = Image.open(example_image)

def apply_floyd_steinberg(x, y, image):

    # Calculations for current pixel
    old_pixel = image.getpixel((x, y))
    new_pixel = tuple([round(val/256) for val in old_pixel])
    error = tuple([old_pixel[i] - new_pixel[i] for i in range(len(old_pixel))])
    pixel_updates = []
    y_offset = 0

    # Diffusion of error according to matrix
    for row in floyd_steinberg_matrix:
        update_row = []
        for x_offset, value in row:
            current_pos = (curr_x, curr_y) = (x+x_offset, y+y_offset)
            value = float(value) / coefficient
            if curr_x < image.width and curr_y < image.height:
                new_value = image.getpixel(current_pos)
                new_value = tuple([new_value[i] + int((error[i] * value)) for i in \
                        range(len(new_value))])
                image.putpixel(current_pos, new_value)
        y_offset += 1

    # Set the pixel we were given and get out
    image.putpixel((x, y), new_pixel)
    return image


width, height = image.size
for x in range(1, width-1):
    for y in range(1, height-1):
        print((x, y))
        image = apply_floyd_steinberg(x, y, image)
image.show()
