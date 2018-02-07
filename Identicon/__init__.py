# -*- coding:utf-8 -*-
__version__='0.1'

import io
import hashlib
from PIL import Image, ImageDraw

BACKGROUND_COLOR = '#f4f4f4'

def render(code):
    hex_list = _to_hash_hex_list(code)
    color = _extract_color(hex_list)
    grid = _build_grid(hex_list)
    flatten_grid = _flat_to_list(grid)
    pixels = _set_pixels(flatten_grid)
    identicon_im = _draw_identicon(color, flatten_grid, pixels)

    identicon_byte_arr = io.BytesIO()
    identicon_im.save(identicon_byte_arr, format='PNG')
    identicon_byte_arr = identicon_byte_arr.getvalue()

    return identicon_byte_arr

def _to_hash_hex_list(code):
    # TODO: Choose hash scheme
    hash = hashlib.md5(code.encode('utf8'))

    return hash.hexdigest()

def _extract_color(hex_list):
    r,g,b =tuple(hex_list[i:i+2] 
            for i in range(0, 2*3, 2))

    return f'#{r}{g}{b}'

def _set_pixels(flatten_grid):
    # len(list) should be a squared of integer value
    # Caculate pixels
    pixels = []
    for i, val in enumerate(flatten_grid):
        x = int(i%5 * 50)
        y = int(i//5 * 50)
        
        top_left = (x, y)
        bottom_right = (x + 50, y + 50)
        
        pixels.append([top_left, bottom_right])

    return pixels

def _build_grid(hex_list):
    # Tailing hex_list to rear 15 bytes
    hex_list_tail = hex_list[2:]
    
    # Make 3x5 gird, half of the symmetric grid(left side)
    hex_half_grid = [[hex_list_tail[col:col+2] for col in range(row, row+2*3, 2)] 
            for row in range(0, 2*3*5, 2*3)]

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

def _draw_identicon(color, grid_list, pixels):
    identicon_im = Image.new('RGB', (250, 250), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(identicon_im)
    for grid, pixel in zip(grid_list, pixels):
        if grid != 0: # for not zero
            draw.rectangle(pixel, fill=color)

    return identicon_im

