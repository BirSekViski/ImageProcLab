import numpy as np
from skimage.io import imread, imshow
from skimage import img_as_float, img_as_ubyte
from skimage import exposure
from scipy.ndimage import convolve, gaussian_filter
import matplotlib.pyplot as plt

class ImageSharpening:
    def __init__(self, path):
        self.image = img_as_float(imread(path))
        
    def box_method(self, s, k):
        # Applies unsharp masking using a box filter of size s and highboost filter of order k
        h = np.ones((s, s)) / (s * s)
        g_mask = self.image - convolve(self.image, h)
        g = self.image + k * g_mask
        return self._finalize(g)

    def gaussian_method(self, sigma, k):
        # Applies unsharp masking using a Gaussian filter of standard deviation sigma and highboost filter of order k
        unsharp_mask = self.image - gaussian_filter(self.image, sigma)
        g = self.image + k * unsharp_mask
        return self._finalize(g)
    
    def _finalize(self, g):
        # Scales the intensity values of the output image to the range [0, 1]
        g += abs(g.min())
        g_rescaled = exposure.rescale_intensity(g, out_range=(0, 1))
        return g_rescaled


path = ' ' # Implement your photo through this path
sharpening = ImageSharpening(path)

method = input("Enter the sharpening method (box or gaussian): ")

if method == 'box':
    s = int(input("Enter the size of the square filter (odd number): "))
    k = float(input("Enter the order of the highboost filter: "))
    result = sharpening.box_method(s, k)
elif method == 'gaussian':
    sigma = float(input("Enter the standard deviation for the Gaussian filter: "))
    k = float(input("Enter the order of the highboost filter: "))
    result = sharpening.gaussian_method(sigma, k)

fig, ax = plt.subplots(1, 2, figsize=(10, 5))
ax[0].imshow(sharpening.image, cmap='gray')
ax[0].set_title('Original Image')
ax[1].imshow(result, cmap='gray')
ax[1].set_title('Sharpened Image')
plt.show()
