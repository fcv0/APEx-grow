Usage
=====

.. _installation:

Installation
------------

To use Lumache, first install it using pip:

.. code-block:: console

   (.venv) $ pip install lumache

Creating recipes
----------------

To retrieve a list of random ingredients,
you can use the ``lumache.get_random_ingredients()`` function:

.. autofunction:: lumache.get_random_ingredients

The ``kind`` parameter should be either ``"meat"``, ``"fish"``,
or ``"veggies"``. Otherwise, :py:func:`lumache.get_random_ingredients`
will raise an exception.

.. autoexception:: lumache.InvalidKindError

For example:

>>> import lumache
>>> lumache.get_random_ingredients()
['shells', 'gorgonzola', 'parsley']

.. Material Requirements:

Material Requirements
---------------------

Assortment of wires -> male to male, male to female, female to female.

Assortment of M3 screws and nuts of varying lengths -> approximately 20.

Arduino Mega x1: https://uk.rs-online.com/web/p/arduino/7154084?gb=s

Multiplexer x1: https://learn.adafruit.com/adafruit-tca9548a-1-to-8-i2c-multiplexer-breakout/overview

Photodiode x3: https://www.mouser.co.uk/ProductDetail/Texas-Instruments/OPT3002DNPT?qs=zEmsApcVOkU5JfY94IcyUw%3D%3D&mgh=1&vip=1&gclid=CjwKCAiAxreqBhAxEiwAfGfndICDwVe5q7AyGCHk7DzQHGdXcSKH3Dxgq5Mo0llkEeWGiyy8MC6SSBoCoxwQAvD_BwE

-> Need to use something such as PCBway to build the custom PCB -> KiCAD in CAD folder.

MOSFET x1 to x3: 

Current driver x1 to x3: 

Temperature sensor x1: https://www.amazon.co.uk/MLX90614-Non-Contact-Infrared-Temperature-Raspberry/dp/B07YKNQQ7P/ref=sr_1_2?crid=2SAZ0TB1FGD27&keywords=mlx90614&qid=1699621618&sprefix=mlx90614%2Caps%2C61&sr=8-2

LEDs: https://www.thorlabs.com/thorproduct.cfm?partnumber=LED750L or https://www.thorlabs.com/thorproduct.cfm?partnumber=LED600L

USB-A to USB-B connector x1: https://www.amazon.co.uk/AmazonBasics-Male-B-Male-Cable-Feet/dp/B00NH13DV2/ref=sr_1_1_ffob_sspa?crid=P6PNE0EVBYO6&keywords=usb%2Ba%2Bto%2Busb%2Bb&qid=1699621045&sprefix=usb%2Ba%2Bto%2Busb%2Bb%2Caps%2C94&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1

Peristaltic pump x1: https://www.amazon.co.uk/peristaltic-Laboratory-Constant-Metering-Controlled/dp/B08JCX6ZS6/ref=sr_1_29?crid=2TXKALNXU9189&keywords=peristaltic%2Bpump&qid=1699620969&sprefix=peristaltic%2Bpump%2Caps%2C89&sr=8-29&th=1

H-Bridge x1: https://www.rapidonline.com/4tronix-l298n-dual-h-bridge-motor-driver-module-75-5013

Heatmat x1: https://uk.rs-online.com/web/p/heater-pads/0245528?gb=s

Relay x1: https://uk.rs-online.com/web/p/power-motor-robotics-development-tools/8430834

Laptop/desktop computer with the ability to run the provided GUIs.

 ** 3D printer with filament or ability to machine the desirable parts. **

