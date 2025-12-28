from sklearn import preprocessing
from sklearn.decomposition import PCA
from astropy.io import fits 
import numpy as np
import matplotlib.pyplot as plt


wavelength = np.arange(336., 1021., 2.) 

hdul = fits.open("my_file.fits")
hdul.info()
my_data = hdul[1].data
print(my_data.columns)

X = my_data['flux']

X = preprocessing.normalize(X)
mu = X.mean(0)
std = X.std(0)
plt.plot(wavelength, mu, color='black')
plt.fill_between(wavelength, mu - std, mu + std, color='#CCCCCC')

pca = PCA(n_components=4)
X_projected = pca.fit_transform(X)
print(X_projected.shape)

plt.figure()
plt.scatter(X_projected[:, 0], X_projected[:, 1])#, c=y, s=4, lw=0, vmin=2, vmax=6, cmap=plt.cm.jet)

plt.xlabel('coefficient 1')
plt.ylabel('coefficient 2')
plt.title('PCA projection of Spectra')

plt.show()