""" Generates 5 example files that are 500px by 500px """

import random
from PIL import Image
import math as m


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)

        This function has no doctests because it has a random element.
    """
    if min_depth <= 1:
        min_depth = 1
    depth = random.randint(min_depth, max_depth)
    if depth > 1:
        func = random.randint(0,5)
        if func == 0:
            return ["prod", build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
        elif func == 1:
            return ["avg", build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
        elif func == 2:
            return ["cos_pi", build_random_function(min_depth-1, max_depth-1)]
        elif func == 3:
            return ["sin_pi", build_random_function(min_depth-1, max_depth-1)]
        elif func == 4:
            return ["pythagorean", build_random_function(min_depth-1, max_depth-1), build_random_function(min_depth-1, max_depth-1)]
        else:
            return ["square_root", build_random_function(min_depth-1, max_depth-1)]
    else:
        func = random.randint(0,1)
        if func == 0:
            return ["x"]
        else:
            return ["y"]



def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value
        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(["prod", ["x"], ["y"]],2, 2)
        4
        >>> evaluate_random_function(["avg", ["x"], ["y"]],2, 4)
        3.0
        >>> evaluate_random_function(["cos_pi", ["x"]],1, 0)
        -1.0
        >>> evaluate_random_function(["sin_pi", ["x"]],1/2, 0)
        1.0
        >>> evaluate_random_function(["pythagorean", ["x"], ["y"]],1,1)
        1.0
        >>> evaluate_random_function(["square_root", ["x"]],9, 0)
        3.0
    """
    if(f[0] == "x"):
        return x
    elif(f[0] == "y"):
        return y
    elif(f[0] == "prod"):
        return evaluate_random_function(f[1], x, y)*evaluate_random_function(f[2], x, y)
    elif(f[0] == "avg"):
        return .5*(evaluate_random_function(f[1], x, y)+evaluate_random_function(f[2], x, y))
    elif(f[0] == "cos_pi"):
        return m.cos(m.pi*evaluate_random_function(f[1], x, y))
    elif(f[0] == "sin_pi"):
        return m.sin(m.pi*evaluate_random_function(f[1], x, y))
    elif(f[0] == "pythagorean"):
        return (1/(2**.5))*abs((evaluate_random_function(f[1], x, y)**2+evaluate_random_function(f[2], x, y)**2))**.5
    elif(f[0] == "square_root"):
        return (abs(evaluate_random_function(f[1], x, y)))**.5

def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    input_var = (val-input_interval_start)/(input_interval_end-input_interval_start)
    output_var = input_var*(output_interval_end-output_interval_start)
    output = output_interval_start + output_var
    return output


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7, 9)
    green_function = build_random_function(7, 9)
    blue_function = build_random_function(7, 9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
    for i in range(5):
        filename = 'example'+str(i)+'.png'
        generate_art(filename, 500, 500)