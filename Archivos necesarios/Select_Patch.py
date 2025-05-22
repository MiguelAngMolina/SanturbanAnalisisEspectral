import rasterio
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import os

def construct_band_file_name(url):
    return url

def load_band(url, extract_path):
    band_file = construct_band_file_name(url)
    band_path = os.path.join(extract_path, band_file)
    with rasterio.open(band_path) as band_data:
        return band_data.read(1)

# Obtener la ruta del directorio donde se encuentra el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta relativa a la carpeta R10m
extract_path = os.path.join(script_dir, "R10m")

# Cargar las bandas para rojo, verde y azul
red_band = load_band("T18NYN_20240123T152649_B04_10m.jp2", extract_path)
green_band = load_band("T18NYN_20240123T152649_B03_10m.jp2", extract_path)
blue_band = load_band("T18NYN_20240123T152649_B02_10m.jp2", extract_path)

# Apilar las bandas en un arreglo de imagen RGB
rgb_image = np.dstack((red_band, green_band, blue_band))

# Normalizar la imagen para la visualización
rgb_image_norm = rgb_image / np.max(rgb_image)
rgb_image_norm = ((rgb_image / np.max(rgb_image))**0.55)

# Definir las coordenadas del parche con la imagen ya rotada
# Asumiendo que el centro del parche es (x_center, y_center)
x_center, y_center = 2363, 1223
half_patch_size = 156
x_start, x_end = x_center - half_patch_size, x_center + half_patch_size
y_start, y_end = y_center - half_patch_size, y_center + half_patch_size

# Extraer el parche de la imagen rotada
rgb_patch = rgb_image_norm[y_start:y_end, x_start:x_end]

# Crear una figura con dos subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))

# Mostrar el parche RGB en el primer subplot
ax1.imshow(rgb_patch)
ax1.set_title('RGB Patch')

# Mostrar la imagen completa rotada con el rectángulo resaltado en el segundo subplot
ax2.imshow(rgb_image_norm)
rect = patches.Rectangle((x_start, y_start), 312, 312, linewidth=1, edgecolor='r', facecolor='none')
ax2.add_patch(rect)
ax2.set_title('Rotated Image with Patch')

plt.tight_layout()
plt.show()
