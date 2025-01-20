import numpy as np
import cv2
from scipy import fftpack
import matplotlib.pyplot as plt
from scipy.signal import medfilt

#Function for notch filters
def notch_filters(im_shape, notch_centers):
    trans_func = np.ones(im_shape)
    for center in notch_centers:
        y, x = np.ogrid[:im_shape[0], :im_shape[1]]
        mask = ((y - center[0]) ** 2 + (x - center[1]) ** 2) > 5**2
        trans_func = trans_func * mask
    return trans_func

# File Path
file_path = 'image05.tif'

# Using openCV for read 
im1 = cv2.imread(file_path, 0)

# Median filter
im2 = medfilt(im1)

# Compute the Fourier spectrum
f_im1 = np.fft.fftshift(np.fft.fft2(im1))

# In my case of centers of the notch filters
notch_centers = [(108, 108), (120, 123), (136, 133), (148, 148)] 

# Creating notch filter
im5 = notch_filters(f_im1.shape, notch_centers)

# Remove the noise
im6 = f_im1 * im5

# Reverse transform the notch-filtered image
im3 = np.real(np.fft.ifft2(np.fft.ifftshift(im6)))

# Display images
plt.figure(figsize=(12, 8))
plt.subplot(231),plt.imshow(im1, cmap = 'gray')
plt.title('1. Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(232),plt.imshow(im2, cmap = 'gray')
plt.title('2. Median Filtered Image'), plt.xticks([]), plt.yticks([])
plt.subplot(233),plt.imshow(im3, cmap = 'gray')
plt.title('3. Notch Filtered Image'), plt.xticks([]), plt.yticks([])
plt.subplot(234),plt.imshow(np.log(1+np.abs(f_im1)), cmap = 'gray')
plt.title('4. Shifted Fourier Transform'), plt.xticks([]), plt.yticks([])
plt.subplot(235),plt.imshow(im5, cmap = 'gray')
plt.title('5. Custom Notch Filters'), plt.xticks([]), plt.yticks([])
plt.subplot(236),plt.imshow(np.log(1+np.abs(im6)), cmap = 'gray')
plt.title('6. Filtered Spectrum'), plt.xticks([]), plt.yticks([])
plt.tight_layout()
plt.show()
