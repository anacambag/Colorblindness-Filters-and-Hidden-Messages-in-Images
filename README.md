# Colorblindness-Filters-and-Hidden-Messages-in-Images

## Colorblindness Filters
The objective of the colorblindness filters part is to create filters to simulate the deficiency in one of the cones responsible for color vision. To do this, we will make use of Python’s Image Library or PIL for short. From PIL we will import Image, which is a sublibrary, or a set of functions and methods, related to image processing. With Image, we can convert images to a list of pixels, and manipulate the RGB (red, green, blue) values of these pixels.

We can replicate the effects of colorblindness with a matrix multiplication between a colorblindness transformation matrix and the RGB values of a particular pixel, which are represented as a vector with 3 entries.

## Hidden Images

In an image, it is possible to hide a second (secret) image that can only be recovered by certain mathematical operations. This is known as steganography. In this secytion of the project, I wrote my own steganography module to hide images.
