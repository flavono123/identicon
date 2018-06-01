# -*- coding:utf-8 -*-

import io
import math
import hashlib
import colorsys
from PIL import Image, ImageDraw

DEFAULT_BACKGROUND_COLOR = (244, 244, 244)
DEFAULT_PADDING = 20
DEFAULT_SIZE = 290
DEFAULT_IMAGE_TYPE = 'PNG'
DEFAULT_LIGHTNESS = 0.5
DEFAULT_SATURATION = 0.7

def render(input_str, input_hash_str=None, size=DEFAULT_SIZE, padding=DEFAULT_PADDING, background_color=DEFAULT_BACKGROUND_COLOR, foreground_color=None, lightness=DEFAULT_LIGHTNESS, saturation=DEFAULT_SATURATION, corner_radius=None, image_type=DEFAULT_IMAGE_TYPE):

    # Generate colors
    hex_str = input_hash_str if input_hash_str else _to_hash_hex_str(input_str)
    generated_color = _extract_color(hex_str, lightness, saturation)
    background_color = generated_color if background_color is None else background_color
    foreground_color = generated_color if foreground_color is None else foreground_color

    # Generate blocks
    number_of_blocks = 5 # varying the number of blocks is currently unsupported
    block_size = (size-2*padding)/number_of_blocks

    grid = _build_grid(hex_str, number_of_blocks)
    flatten_grid = _flat_to_list(grid)
    pixels = _set_pixels(flatten_grid, number_of_blocks, block_size, padding)
    identicon_im = _draw_identicon(background_color, foreground_color, size, flatten_grid, pixels)

    # Add radius crop
    if corner_radius is not None:
        identicon_im = _crop_coner_round(identicon_im, corner_radius)

    # Generate byte array
    identicon_byte_arr = io.BytesIO()
    identicon_im.save(identicon_byte_arr, format=image_type)
    identicon_byte_arr = identicon_byte_arr.getvalue()

    return identicon_byte_arr

def _to_hash_hex_str(input_str):
    # TODO: Choose hash scheme
    hash = hashlib.md5(input_str.encode('utf8'))

    return hash.hexdigest()

def _extract_color(hex_str, lightness, saturation):
    hue = (int(hex_str[-7:], 16) / float(0xfffffff))

    r,g,b = (int(v*255) for v in colorsys.hls_to_rgb(hue, lightness, saturation))
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def _build_grid(hex_str, number_of_blocks):
    # Tailing hex_str to rear 15 bytes
    hex_str_tail = hex_str[2:]
    
    # Make 3x5 gird, half of the symmetric grid(left side)
    half_number_of_blocks = int(math.ceil(number_of_blocks/2.0))
    hex_half_grid = [[hex_str_tail[col:col+2] for col in range(row, row+2*half_number_of_blocks, 2)]
            for row in range(0, 2*half_number_of_blocks*number_of_blocks, 2*half_number_of_blocks)]

    hex_grid = _mirror_row(hex_half_grid)

    int_grid = [list(map(lambda e: int(e ,base=16), row)) for row in hex_grid]

    # TODO: Using more entropies, should be deprecated
    filtered_grid = [[byte if byte%2==0 else 0 for byte in row] for row in int_grid]
    
    return filtered_grid

def _mirror_row(half_grid):
    opposite_half_grid = [list(reversed(row)) for row in half_grid] 
    # FIXME: just for odd(5) num column now 
    grid = [row + mirrored_row[1:] for row, mirrored_row in zip(half_grid, opposite_half_grid)]

    return grid

def _flat_to_list(nested_list):
    flatten_list = [e for row in nested_list for e in row]

    return flatten_list

def _set_pixels(flatten_grid, number_of_blocks, block_size, padding):
    # len(list) should be a squared of integer value
    # Caculate pixels
    pixels = []
    for i, val in enumerate(flatten_grid):
        x = int(i%number_of_blocks * block_size) + padding
        y = int(i//number_of_blocks * block_size) + padding

        top_left = (x, y)
        bottom_right = (x + block_size, y + block_size)

        pixels.append([top_left, bottom_right])

    return pixels

def _draw_identicon(background, foreground, size, grid_list, pixels):
    identicon_im = Image.new('RGB', (size, size), background)
    draw = ImageDraw.Draw(identicon_im)
    for grid, pixel in zip(grid_list, pixels):
        if grid != 0: # for not zero
            draw.rectangle(pixel, fill=foreground)

    return identicon_im

def _crop_coner_round(im, rad):
    round_edge = Image.new('L', (rad*2, rad*2), 0)

    draw = ImageDraw.Draw(round_edge)
    draw.ellipse((0, 0, rad*2, rad*2), fill='white')

    alpha = Image.new('L', im.size, 255)

    w, h = im.size

    alpha.paste(round_edge.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(round_edge.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(round_edge.crop((rad, 0, rad*2, rad)), (w - rad, 0))
    alpha.paste(round_edge.crop((rad, rad, rad*2, rad*2)), (w - rad, h - rad))

    im.putalpha(alpha)

    return im
