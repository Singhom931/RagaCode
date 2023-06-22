from PIL import Image

def convert_to_base(number, base):
    digits = []
    while number > 0:
        digits.insert(0, number % base)
        number //= base
    return digits

def generate_color_qr_code(data, num_colors, template , filter):
    
    unique_ids = [ord(c) for c in data]
    #print(unique_ids)
    base = num_colors
    encoded_ids = [convert_to_base(uid, base) for uid in unique_ids]
    #print(encoded_ids)
    
    color_mapping = [(255, 255, 255), (255, 0, 0), (0, 0, 255), (0, 255, 0), (0, 0, 0)]
    
    k = 0
    pix_color = []
    
    filter = Image.open(filter)
    filter = filter.convert('L')

    template = Image.open(template)

    for encoded_id in encoded_ids:
        for digit in encoded_id:
            pix_color.append(color_mapping[digit])
    pix_color.append((0,0,255))
    #print(pix_color)
    toggleplot = 0
    pixL = filter.load()
    pixT = template.load()
    width, height = template.size
    for j in range(height):
        for i in range(width):
            pixel = filter.getpixel((i,j))
            if pixel > 0:
                if k < len(pix_color):
                    pixT[i,j] = pix_color[k]
                #elif i%2==0 or j%2 == 0:
                # elif toggleplot % 3 == 0:
                #     pixT[i,j] = (255,255,255)
                # else:
                #     pixT[i,j] = (0,0,0)
                else:
                    pass
                k = k + 1
                toggleplot = toggleplot + 1
                
    template.save('color_qr_code.png')

# Example usage
template = 'QRv7-2.png'
filter = 'QRv7filter.png'
data = "Hello, World! , This is Om Singh aka Diablo931, This is testing RAGACODE aka ColorQR"
num_colors = 5

qr_code = generate_color_qr_code(data, num_colors, template , filter)
