from PIL import Image

# Tamaño de la imagen
width, height = 8, 8

# Crea una nueva imagen en blanco
image = Image.new("RGB", (width, height))

# Rellena la imagen con el degradado
for x in range(width):
    for y in range(height):
        # Calcula el valor del color en función de la posición
        r = 255  # Componente rojo
        g = int((y / (height - 1)) * 255)  # Componente verde
        b = int((x / (width - 1)) * 255)  # Componente azul constante

        # Establece el color del píxel
        image.putpixel((x, y), (r, g, b))

# Guarda la imagen
image.save("degradado.jpg")

# Muestra la imagen (opcional)
image.show()
