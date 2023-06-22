from PIL import Image

def extract_blocks_from_image(image,filter):
    img = Image.open(image)
    pixels = img.load()

    filter = Image.open(filter)
    filter = filter.convert('L')
    
    width, height = img.size
    wr = width/45; io = wr/2; iv = io
    hr = height/45; jo = hr/2; jv = jo
    print(wr,hr)
    
    blocks = []
    pixRGB = []
    colors = ["white","red","blue","green","black"]

    for j in range(45):
        for i in range(45):
            pixel = filter.getpixel((i,j))
            print(i,j)
            if pixel > 0:
                print(iv,jv)
                io = i*wr+iv; jo = j*hr+jv
                RGB = img.getpixel((int(io),int(jo)))
                print(int(io),int(jo))
                print(RGB)
                if RGB[0]>200 and RGB[1]>200 and RGB[2]>200:
                    block_value = 0
                elif RGB[0]>200 and RGB[1]<200 and RGB[2]<200:
                    block_value = 1
                elif RGB[0]<200 and RGB[1]<200 and RGB[2]>200:
                    block_value = 2
                elif RGB[0]<200 and RGB[1]>200 and RGB[2]<200:
                    block_value = 3
                elif RGB[0]<200 and RGB[1]<200 and RGB[2]<200:
                    block_value = 4
                #else: block_value = 0
                print(colors[block_value])

                blocks.append(block_value)

    return blocks


def convert_to_base_10(digits, base):
    number = 0
    for digit in digits:
        number = number * base + digit
    
    return number

def decode_color_qr_code(blocks):
    base = 5
    block_digits = [str(block) for block in blocks]
    block_values = [int(''.join(block_digits[i:i+3]), base) for i in range(0, len(block_digits), 3)]
    characters = ''.join(chr(base_10) for base_10 in block_values)
    print([int(''.join(block_digits[i:i+3])) for i in range(0, len(block_digits), 3)])
    print(block_values)
    
    return characters

def b2c(blocks):
    colors = ["white","red","blue","green","black"]
    clist = []
    for block in blocks:
        clist.append(colors[block])
    print(clist)

# Example usage
image_path = "warpedQR.png"
filter = 'QRv7filterout.png'
square_size = 10
blocks = extract_blocks_from_image(image_path,filter)
#b2c(blocks)
original_string = decode_color_qr_code(blocks)
print("Original string:", original_string)
