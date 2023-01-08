"""

# Name: Ana Camba Gomes

"""

from PIL import Image, ImageFont, ImageDraw
import numpy


def make_matrix(color):
    """
    Generates a transformation matrix for the specified color.
    Inputs:
        color: string with exactly one of the following values:
               'red', 'blue', 'green', or 'none'
    Returns:
        matrix: a transformation matrix corresponding to
                deficiency in that color
    """

    if color == 'red':
        c = [[.567, .433, 0], [.558, .442, 0], [0, .242, .758]]
    elif color == 'green':
        c = [[0.625, 0.375, 0], [0.7, 0.3, 0], [0, 0.142, 0.858]]
    elif color == 'blue':
        c = [[.95, 0.05, 0], [0, 0.433, 0.567], [0, 0.475, .525]]
    elif color == 'none':
        c = [[1, 0., 0], [0, 1, 0.], [0, 0., 1]]
    return c


def matrix_multiply(m1, m2):
    """
    Multiplies the input matrices.
    Inputs:
        m1,m2: the input matrices
    Returns:
        result: matrix product of m1 and m2
        in a list of floats
    """

    product = numpy.matmul(m1, m2)
    if type(product) == numpy.int64:
        return float(product)
    else:
        result = list(product)
        return result


def img_to_pix(filename):
    """
    Takes a filename (must be inputted as a string
    with proper file attachment ex: .jpg, .png)
    and converts to a list of representing pixels.

    For RGB images, each pixel is a tuple containing (R,G,B) values.
    For BW images, each pixel is an integer.

    # Note: Don't worry about determining if an image is RGB or BW.
            The PIL library functions you use will return the 
            correct pixel values for either image mode.

    Returns the list of pixels.

    Inputs:
        filename: string representing an image file, such as 'lenna.jpg'
        returns: list of pixel values 
                 in form (R,G,B) such as [(0,0,0),(255,255,255),(38,29,58)...] for RGB image
                 in form L such as [60,66,72...] for BW image
    """
    
    pixels = []
    open_file = Image.open(filename, mode='r', formats=None) #we open the file with given function in library
    
    for i in range (open_file.height): #we iterate through Image height, in pixels
        for p in range(open_file.width): #Image height, in pixels
            each_pixel = open_file.getpixel((p,i)) #Returns the pixel value at a given position (height, width).
            pixels.append(each_pixel) #we create our list of pixels values
            
    return pixels 
   
    
    


def pix_to_img(pixels_list, size, mode):
    """
    Creates an Image object from a inputted set of RGB tuples.

    Inputs:
        pixels_list: a list of pixels such as the output of
                img_to_pixels.
        size: a tuple of (width,height) representing
              the dimensions of the desired image. Assume
              that size is a valid input such that
              size[0] * size[1] == len(pixels).
        mode: 'RGB' or 'L' to indicate an RGB image or a 
              BW image, respectively
    returns:
        img: Image object made from list of pixels
    """
    new_image = Image.new(mode, size) # .new function helps use create a new image with the given mode and size
    new_image.putdata(pixels_list) # .putdata copies pixel data from a flattered sequence object into the image
    return new_image # image object made from list of pixels


def filter(pixels_list, color):
    """
    pixels_list: a list of pixels in RGB form, such as
            [(0,0,0),(255,255,255),(38,29,58)...]
    color: 'red', 'blue', 'green', or 'none', must be a string representing 
           the color deficiency that is being simulated.
    returns: list of pixels in same format as earlier functions,
    transformed by matrix multiplication
    """
    
    pixels_transformed = []
    
    for char in pixels_list: #we are evaluating each pixel in the pixels of list provided
        colors = matrix_multiply(make_matrix(color), char) #we create a new matrix by multiplying the given color string in matrix with a pixel in the list
        pixels_transformed.append((int(colors[0]),int(colors[1]), int(colors[2]))) #we iterate through the matrix given from colors. we append as a tuple the pixels edited
        
       
    return pixels_transformed


def extract_end_bits(num_end_bits, pixel):
    """
    Extracts the last num_end_bits of each value of a given pixel.

    example for BW pixel:
        num_end_bits = 5
        pixel = 214

        214 in binary is 11010110. 
        The last 5 bits of 11010110 are 10110.
                              ^^^^^
        The integer representation of 10110 is 22, so we return 22.

    example for RBG pixel:
        num_end_bits = 2
        pixel = (214, 17, 8)

        last 3 bits of 214 = 110 --> 6
        last 3 bits of 17 = 001 --> 1
        last 3 bits of 8 = 000 --> 0

        so we return (6,1,0)

    Inputs:
        num_end_bits: the number of end bits to extract
        pixel: an integer between 0 and 255, or a tuple of RGB values between 0 and 255

    Returns:
        The num_end_bits of pixel, as an integer (BW) or tuple of integers (RGB).
    """
    pixels_list = []
    if type(pixel) == tuple: #checks to see if it is an RGB
        for i in pixel: 
            pixels_list.append(i%2**(num_end_bits))
            binary = tuple(pixels_list)
    elif type(pixel) == int: #checks if it is an int
        binary = pixel%2**(num_end_bits) #gives us the num_end_bist of pixel either as an integer if it is BW or as a tuple if it is RGB
         
    return binary
        
        
            


def reveal_bw_image(filename):
    """
    Extracts the single LSB for each pixel in the BW input image. 
    Inputs:
        filename: string, input BW file to be processed
    Returns:
        result: an Image object containing the hidden image
    """
    bw_file = Image.open(filename) #open the image
    pixel_bw = img_to_pix(filename) #transform it to pixel
    
    pixels_new_list = []
    
    for i in pixel_bw:
        pixels_new_list.append((extract_end_bits(1, i))*255) #since we only have 1 single LBS we directly multiply by 255 which is our range
    
    hidden_image = pix_to_img(pixels_new_list, size = bw_file.size, mode = bw_file.mode) 
    
    return hidden_image


def reveal_color_image(filename):
    """
    Extracts the 3 LSBs for each pixel in the RGB input image. 
    Inputs:
        filename: string, input RGB file to be processed
    Returns:
        result: an Image object containing the hidden image
    """
    color_file = Image.open(filename)
    pixel_color = img_to_pix(filename)
    
    new_color_pixels = []
    
    for i in pixel_color:
        
        color1 = (extract_end_bits(3, i[0]))*255//7 #it is divided by 7 because we have 3 numbers now instead of 1. So in binary 3 will represent 7 and we have to divide 255 by 7.
        color2 = (extract_end_bits(3, i[1]))*255//7
        color3 = (extract_end_bits(3, i[2]))*255//7
        
        new_color_pixels.append((color1, color2, color3)) # append as a tuple because we have now 3 colors
       
    hidden = pix_to_img(new_color_pixels, size = color_file.size, mode = color_file.mode)
    
    return hidden #image object that containts the hidden image



def reveal_image(filename):
    """
    Extracts the single LSB (for a BW image) or the 3 LSBs (for a 
    color image) for each pixel in the input image. Hint: you can
    use a function to determine the mode of the input image (BW or
    RGB) and then use this mode to determine how to process the image.
    Inputs:
        filename: string, input BW or RGB file to be processed
    Returns:
        result: an Image object containing the hidden image
    """
    im = Image.open(filename)
    if im.mode == '1' or im.mode == 'L':
        return(reveal_bw_image(filename))
    elif im.mode == 'RGB':
        return(reveal_color_image(filename))
    else:
        raise Exception("Invalid mode %s" % im.mode)


def draw_kerb(filename, kerb):
    """
    Draws the text "kerb" onto the image located at "filename" and returns a PDF.
    Inputs:
        filename: string, input BW or RGB file
        kerb: string, your kerberos
    Output:
        Saves output image to "filename_kerb.xxx"
    """
    im = Image.open(filename)
    font = ImageFont.truetype("noto-sans-mono.ttf", 40)
    draw = ImageDraw.Draw(im)
    draw.text((0, 0), kerb, "white", font=font)
    idx = filename.find(".")
    new_filename = filename[:idx] + "_kerb" + filename[idx:]
    im.save(new_filename)
    return


def main():
    pass

    # Uncomment the following lines to test part 1

    im = Image.open('image_15.png')
    width, height = im.size
    pixels = img_to_pix('image_15.png')

    non_filtered_pixels = filter(pixels,'none')
    im = pix_to_img(non_filtered_pixels, (width, height), 'RGB')
    im.show()

    red_filtered_pixels = filter(pixels,'red')
    im2 = pix_to_img(red_filtered_pixels,(width,height), 'RGB')
    im2.show()

    # # Uncomment the following lines to test part 2
    # im = reveal_image('hidden1.bmp')
    # im.show()

    # im2 = reveal_image('hidden2.bmp')
    # im2.show()
    
    #print(draw_kerb('image3.png', 'fabianag')) #run this line to download the images in your pc
    

if __name__ == '__main__':
    main()
