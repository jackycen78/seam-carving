# seam-carving

Conventional methods of resizing images, like cropping or scaling, results in loss of information. This is because these methods assume all pixels of the image provide the same value. For example, in an image of a human face, the background content does not provide much significance. One way to fix this is to take the least significant details of the image and remove it to resize the image. This can be done by seam carving, which uses the gradients map to find seams in the image that have the least significance. The algorithm goes as follows,

1. Calculate gradient map
2. Find the lowest seam from the top of image to bottom
3. Remove all pixels in this seam
4. Repeat 1-3, until the appropiate dimensions are met

The lowest seam is defined as the lowest sum of gradients of a valid seam.
A valid seam is such that the all pixels proceed directly below, below to the right or below to the left of the pixel above it.
To resize the image's height, simply rotate the image.

Original Image:

![image](https://user-images.githubusercontent.com/24669054/111707683-e6f0cc80-881a-11eb-8a3a-d03bf992e124.png)

Cropped Image:

![image](https://user-images.githubusercontent.com/24669054/111715766-f37d2100-882a-11eb-9b5c-124a15188b08.png)

Scaled Image:

![image](https://user-images.githubusercontent.com/24669054/111715783-fbd55c00-882a-11eb-96ad-d6e3c055572e.png)

Seam-Carved Image:

![image](https://user-images.githubusercontent.com/24669054/111715823-17d8fd80-882b-11eb-9393-0ff0b22fcd74.png)
