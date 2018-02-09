Identicon
=========

.. image:: https://camo.githubusercontent.com/3c4eee845db4fa6af1d93b1c33b30074a9b0333f/68747470733a2f2f662e636c6f75642e6769746875622e636f6d2f6173736574732f363130342f3936313733302f61336334653261302d303464662d313165332d383234632d3733373865363535303730372e706e67
    :width: 2384 px
    :height: 784 px
    :scale: 15 %
    :target: https://camo.githubusercontent.com/3c4eee845db4fa6af1d93b1c33b30074a9b0333f/

A Python library for generating GitHub-like symmetrical 5x5 `identicons <https://github.com/blog/1586-identicons>`_.

.. image:: https://travis-ci.org/flavono123/identicon.svg?branch=master
    :target: https://travis-ci.org/flavono123/identicon

Installation
------------

**Sorry, not yet available.**

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
