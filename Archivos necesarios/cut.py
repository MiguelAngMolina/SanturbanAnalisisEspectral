import rasterio
import numpy as np
import os
from PIL import Image

def construct_band_file_name(url):
    return url

def load_band(url, extract_path):
    band_file = construct_band_file_name(url)
    band_path = os.path.join(extract_path, band_file)
    with rasterio.open(band_path) as band_data:
        return band_data.read(1), band_data.profile  # Devolver también el perfil del raster

# Obtener la ruta del directorio donde se encuentra el script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Ruta relativa a la carpeta R10m
extract_path = os.path.join(script_dir, "R10m")

# Cargar las bandas para rojo, verde y azul
red_band, profile = load_band("T18NYN_20240123T152649_B04_10m.jp2", extract_path)
green_band, _ = load_band("T18NYN_20240123T152649_B03_10m.jp2", extract_path)
blue_band, _ = load_band("T18NYN_20240123T152649_B02_10m.jp2", extract_path)

# Apilar las bandas en un arreglo de imagen RGB
rgb_image = np.dstack((red_band, green_band, blue_band))

# Definir las coordenadas del parche
x_center, y_center = 2363, 1223  # Estas son las coordenadas que ya tienes
half_patch_size = 156  # Tamaño del parche

x_start, x_end = x_center - half_patch_size, x_center + half_patch_size
y_start, y_end = y_center - half_patch_size, y_center + half_patch_size

# Extraer el parche de la imagen RGB
rgb_patch = rgb_image[y_start:y_end, x_start:x_end, :]

# Mejorar la normalización utilizando un percentil para evitar la pérdida de detalles
rgb_patch_normalized = np.zeros_like(rgb_patch, dtype=np.uint8)

for i in range(3):  # Normalizar cada canal por separado
    min_val = np.percentile(rgb_patch[:, :, i], 2)  # Valor en el percentil 2
    max_val = np.percentile(rgb_patch[:, :, i], 98)  # Valor en el percentil 98
    scaled = np.clip((rgb_patch[:, :, i] - min_val) / (max_val - min_val) * 255, 0, 255)
    rgb_patch_normalized[:, :, i] = scaled.astype(np.uint8)

# Convertir el arreglo normalizado a una imagen de PIL
rgb_image_pil = Image.fromarray(rgb_patch_normalized)

# Guardar el parche como un nuevo archivo .png para evitar la pérdida de calidad
output_path = os.path.join(extract_path, "PARCHERGB.png")
rgb_image_pil.save(output_path, format='PNG')

print(f"Parche RGB guardado como {output_path}")
