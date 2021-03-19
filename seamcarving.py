import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve 
from PIL import Image
import cv2 as cv


def gradientMap(image):
    """
    image: 3d array
        3d array of an image. Each value, image[i][j][k] is the pixel intensity at pixel (i, j)
        with colour channel k.
        
    gradientMap returns the gradient map of the image.    
    
    gradient_image: 2d array
        greyscale gradient map.
        
    """
    
    # Transform image to greyscale
    image = np.dot(image[...,:3], [0.299, 0.587, 0.144])
    
    sobel_x = np.array([[-1,  0,  1],
                      [-2,  0,  2],
                      [-1,  0,  1]])

    
    sobel_y = np.array([[-1, -2, -1],
                      [0 ,  0,  0],
                      [1 ,  2,  1]])
 
    gradient_image = np.sqrt(np.square(convolve(image, sobel_x)) + np.square(convolve(image, sobel_y)))
 
    return gradient_image


def minSeam(image):
    """
    image: 3d array
        3d array of an image. Each value, image[i][j][k] is the pixel intensity at pixel (i, j)
        with colour channel k.
    
    minSeam finds the seam with the lowest total sum of gradients. It returns cost_map and 
    path_map, which are:
    
    cost_map: 2d array
        cost_map is the lowest sum of gradients to reach each pixel.
        i.e cost_map[i, k] is the lowest sum of gradients to reach pixel (i, k).
        
    path_map: 2d array
        path_map is the column index of the pixel that was used to arrive at the current pixel
        i.e path_map[i, k] is the column index of: 
            min(cost_map[i - 1, k - 1], cost_map[i - 1, k], cost_map[i - 1, k + 1]).
            
    gradient_image: 2d array
        greyscale gradient map.        
    """
    
    gradient_image = gradientMap(image)
    
    Y, X = gradient_image.shape[0], gradient_image.shape[1]
    cost_map = np.zeros((Y, X))
    path_map = np.zeros((Y, X))
    cost_map[1, :] = gradient_image[1, :]
    
    
    for row in range(1,Y):
        for pixel in range(0, X):
            if pixel == 0:
                lowest_cost_index = pixel + np.argmin(cost_map[row - 1, pixel:pixel + 2])
                path_map[row, pixel] = lowest_cost_index   
                
            elif pixel == X - 1:
                lowest_cost_index = pixel + np.argmin(cost_map[row - 1, pixel - 1:pixel + 2]) - 1
                path_map[row, pixel] = lowest_cost_index   
                
            else:
                lowest_cost_index = pixel + np.argmin(cost_map[row - 1, pixel - 1:pixel + 1]) - 1
                path_map[row, pixel] = lowest_cost_index
            
            lowest_path_cost = cost_map[row - 1, lowest_cost_index ]
            cost_map[row, pixel] = lowest_path_cost + gradient_image[row, pixel]
            
    return cost_map, path_map, gradient_image


def deleteColumnSeam(image):
    """
    image: 3d array
        3d array of an image. Each value, image[i][j][k] is the pixel intensity at pixel (i, j)
        with colour channel k.
        
    deleteColumnSeam finds deletes the column seam with the lowest sum of gradients, as found by minSeam.
    
    new_image: 3d array
        new_image is image with the column seam deleted. If image had shape of (m, n, 3),
        new_image would have shape of (m, n-1, 3).
    """
    cost_map, path_map, gradient_image = minSeam(image)
    
    Y, X = image.shape[0], image.shape[1]
    
    # find the lowest cost of gradient in the last row.
    remove_pixel = np.argmin(cost_map[-1,:])
    
    new_image = []
    for row in range(Y - 1, 0, -1):
        new_row = np.delete(image[row], remove_pixel, axis=0)
        new_image.insert(0, new_row)
        remove_pixel = int(path_map[row, remove_pixel])      
   
    
    new_row = np.delete(image[row], remove_pixel, axis=0)
    new_image.insert(0, new_row)
    
    new_image = np.array(new_image)
    
    return new_image


def deleteRowSeam(image):
    """
    image: 3d array
        3d array of an image. Each value, image[i][j][k] is the pixel intensity at pixel (i, j)
        with colour channel k.
        
    deleteRowSeam finds deletes the row seam with the lowest sum of gradients, as found by minSeam.
    
    new_image: 3d array
        new_image is image with the row seam deleted. If image had shape of (m, n, 3),
        new_image would have shape of (m, n-1, 3).
    """
    # rotate image
    image = np.rot90(image)
    
    cost_map, path_map, gradient_image = minSeam(image)
    
    Y, X = image.shape[0], image.shape[1]
    
    
    remove_pixel = np.argmin(cost_map[-1,:])
    
    new_image = []
    
    # Create a new image by going through every row and deleting the pixel in the lowest 
    # sum of gradients path. 
    for row in range(Y - 1, 0, -1):
        new_row = np.delete(image[row], remove_pixel, axis=0)
        new_image.insert(0, new_row)
        remove_pixel = int(path_map[row, remove_pixel])      
   
    
    new_row = np.delete(image[row], remove_pixel, axis=0)
    new_image.insert(0, new_row)
    
    # rotate image back to original position
    new_image = np.rot90(np.array(new_image))
    new_image = np.rot90(new_image)
    new_image = np.rot90(new_image)

    return new_image


def resizeImage(image, height, width):
    """
    image: 3d array
        3d array of an image. Each value, image[i][j][k] is the pixel intensity at pixel (i, j)
        with colour channel k.
    height: int
        the desired height of the new image. height must be equal or less to the height of image.
    width: intt
        the desired width of the new image. width must be equal or less to the width of image.
        
    resizeImage returns image that has been resized using seam carving.
    
    resized_image: 3d array
        resized_image is image resized with shape (height, width, 3).
    """
    resized_image = image
    image_height, image_width = image.shape[0], image.shape[1]
    
    if height <= image_height:
        for i in range(0, image_height - height):
            resized_image = deleteRowSeam(resized_image)
    else:
        return("height must be equal or less than image height!")
    
    if width <= image_width:
        for i in range(0, image_width - width):
            resized_image = deleteColumnSeam(resized_image)
    else:
        return("width must be equal or less than image width!")
    
    return resized_image



