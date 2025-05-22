import rasterio
import numpy as np
import matplotlib.pyplot as plt
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

# Cargar las bandas necesarias para el NDVI (NIR y Red)
nir_band = load_band("T18NYN_20240123T152649_B08_10m.jp2", extract_path)  # NIR
red_band = load_band("T18NYN_20240123T152649_B04_10m.jp2", extract_path)  # Red

# Definir las coordenadas del parche
x_center, y_center = 2363, 1223
half_patch_size = 156

x_start, x_end = x_center - half_patch_size, x_center + half_patch_size
y_start, y_end = y_center - half_patch_size, y_center + half_patch_size

# Extraer el parche de las bandas NIR y Red
nir_patch = nir_band[y_start:y_end, x_start:x_end]
red_patch = red_band[y_start:y_end, x_start:x_end]

# Calcular el NDVI
ndvi = (nir_patch - red_patch) / (nir_patch + red_patch)

# Limitar los valores del NDVI
ndvi[(ndvi < 0)] = 0
ndvi[(ndvi > 0.7)] = 0

# Crear una figura para mostrar el NDVI del parche
fig, ax = plt.subplots(figsize=(8, 8))

# Mostrar el NDVI con la barra de colores
ndvi_image = ax.imshow(ndvi, cmap='RdYlGn')

# Ocultar los números de los ejes
ax.set_xticks([])
ax.set_yticks([])

cbar = plt.colorbar(ndvi_image, ax=ax, fraction=0.046, pad=0.04)

plt.tight_layout()

# Guardar la imagen como PNG
output_path = os.path.join(script_dir, "NDVI_patch.png")
plt.savefig(output_path, dpi=500, bbox_inches='tight')
print(f"Imagen NDVI guardada en {output_path}")

# Mostrar la imagen
plt.show()
