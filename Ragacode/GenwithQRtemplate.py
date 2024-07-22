from PIL import Image

def convert_to_base(number, base):
    digits = []
    while number > 0:
        digits.insert(0, number % base)
        number //= base
    if len(digits) < 3:
        digits = [0] + digits
        return digits
    return digits

def generate_color_qr_code(data, num_colors, template , filter):
    
    unique_ids = [ord(c) for c in data]
    # print(unique_ids)
    base = num_colors
    encoded_ids = [convert_to_base(uid, base) for uid in unique_ids]
    # print(encoded_ids)
    
    color_mapping = [(255, 255, 255), (128, 0, 0), (0, 0, 128), (0, 128, 0), (0, 0, 0)]
    
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
template = 'QRv7.png'
filter = 'QRv7filter.png'
# data = "Hello, World! , This is Om Singh aka Diablo931, This is testing RAGACODE aka ColorQR"
data = '''What were the chances? It would have to be a lot more than 100 to 1.
It was likely even more than 1,000 to 1. The more he thought about it,
the odds of it happening had to be more than 10,000 to 1 and even 100,000 to 1.
People often threw around the chances of something happening as being 
1,000,000 to 1 as an exaggeration of an unlikely event,
but he could see that they may actually be accurate in this situation.
Whatever the odds of it happening, he knew they were big.
What he didn't know was whether this happening was lucky or unlucky.'''
num_colors = 5

# Binary QR v6 AlphaNumeric Capacity = 66
# Raga QR v6 AlphaNumeric Capacity = 539
qr_code = generate_color_qr_code(data, num_colors, template , filter)
