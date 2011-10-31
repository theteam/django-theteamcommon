import Image


def whitespace_processor(im, size, whitespace=False, **kwargs):
    """Adds whitespace to the image"""
    if not whitespace:
        return im
    WHITESPACE_COLOUR = (255, 255, 255, 0)
    new_image = Image.new('RGBA', size, WHITESPACE_COLOUR)
    source_x, source_y = im.size
    target_x, target_y = size
    paste_position = [0, 0]
    if target_x > source_x:
        # we have whitespace on x
        paste_position[0] = (target_x - source_x) / 2
    if target_y > source_y:
        # we have whitespace on y
        paste_position[1] = (target_y - source_y) / 2
    new_image.paste(im, tuple(paste_position))
    return new_image
