import cv2 as cv
import numpy as np
import random

image = cv.imread(r"Data\eagle.jpg")
cv.imshow("Raw Image", image)

# Funktion der tilføjer salt and pepper noise
def spnoise(image, percentage):
    working_image = image.copy()
    height, width = working_image.shape[:2]
    for i in range(height):
        for j in range(width):
            if random.randrange(0, 100) < percentage:
                multiplier = random.choice([1, 0])
                pixel_value = 255 * multiplier
                working_image[i, j] = [pixel_value, pixel_value, pixel_value]
    return working_image

sp_image = spnoise(image, 25)
cv.imshow("Salt and Pepper Noise", sp_image)

# Mean blur kernel
blur_kernel = np.ones((3,3), np.float32)/30
image_mean = cv.filter2D(sp_image, ddepth=-1, kernel=blur_kernel)
cv.imshow("Mean Blurred on SP", image_mean)

# Median blur
image_median = cv.medianBlur(sp_image, 3)
cv.imshow("Median Blurred on SP", image_median)

def gausnoise(image, sigma):
    working_image = image.copy()
    row,col,ch= working_image.shape
    mean = 0
    noise = np.random.normal(mean, sigma, (row,col,ch)).astype(np.int8)
    noise = noise.reshape(row,col,ch).astype("uint8")
    noisy_image = working_image + noise
    return noisy_image

gau_image = gausnoise(image, 25)
cv.imshow("Gaussian Noise", gau_image)

# Mean blur kernel
blur_kernel = np.ones((3,3), np.float32)/30
image_mean = cv.filter2D(gau_image, ddepth=-1, kernel=blur_kernel)
cv.imshow("Mean Blurred on Gaussian", image_mean)

# Median blur
image_median = cv.medianBlur(gau_image, 3)
cv.imshow("Median Blurred on Gaussian", image_median)

# OBS OBS OBS
# Størstedelen af koden efter denne linje er kopiret fra tutorial!!! Jeg har ikke selv skabt det.
# OBS OBS OBS

from sklearn.decomposition import PCA, KernelPCA
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler

X, y = fetch_openml(data_id=41082, as_frame=False, return_X_y=True)
X = MinMaxScaler().fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, stratify=y, random_state=0, train_size=1_000, test_size=100
)

rng = np.random.RandomState(42)
noise = rng.normal(scale=0.25, size=X_test.shape)
X_test_noisy = X_test + noise

noise = rng.normal(scale=0.25, size=X_train.shape)
X_train_noisy = X_train + noise

pca = PCA(n_components=54, random_state=42)
kernel_pca = KernelPCA(
    n_components=400,
    kernel="rbf",
    gamma=1e-3,
    fit_inverse_transform=True,
    alpha=5e-3,
    random_state=42,
)

pca.fit(X_train_noisy)
_ = kernel_pca.fit(X_train_noisy)

import matplotlib.pyplot as plt

def plot_digits(X, title):
    """Small helper function to plot 100 digits."""
    fig, axs = plt.subplots(nrows=10, ncols=10, figsize=(8, 8))
    for img, ax in zip(X, axs.ravel()):
        ax.imshow(img.reshape((16, 16)), cmap="Greys")
        ax.axis("off")
    fig.suptitle(title, fontsize=24)
    
X_reconstructed_kernel_pca = kernel_pca.inverse_transform(
    kernel_pca.transform(X_test_noisy)
)
X_reconstructed_pca = pca.inverse_transform(pca.transform(X_test_noisy))

plot_digits(X_test, "Uncorrupted test images")
plot_digits(
    X_reconstructed_pca,
    f"PCA reconstruction\nMSE: {np.mean((X_test - X_reconstructed_pca) ** 2):.2f}",
)
plot_digits(
    X_reconstructed_kernel_pca,
    (
        "Kernel PCA reconstruction\n"
        f"MSE: {np.mean((X_test - X_reconstructed_kernel_pca) ** 2):.2f}"
    ),
)

plt.show()

cv.waitKey()
cv.destroyAllWindows()