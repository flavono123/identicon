Identicon
====================================================

A Python library for generating GitHub-like symmetrical 5x5 identicons.
-------------------------------------------

Installation
------------

::
    pip install Identicon

Usage
-----

Pass a string to :code:`Identicon.render()`. It will return the PNG formatted byte stream:

::

    identicon = Identicon.render('Python')
    # b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\xfa\x00\x00\x00...'

You can write to file:

::

    with open('identicon.png', 'wb') as f:
        f.write(identicon)

or get as :code:`PIL.Image`:

::
    import io
    from PIL import Image

    image = Image.open(io.BytesIO(identicon))
