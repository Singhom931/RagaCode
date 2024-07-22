from PIL import Image

color_mapping = ['White', 'Red', 'Blue', 'Green', 'Black', 'None']

def split_into_chunks(s, chunk_size):
    return [s[i:i + chunk_size] for i in range(0, len(s), chunk_size)]

def convert_chunks_to_int(chunks):
    return [int(chunk) for chunk in chunks]

def convert_from_base(digits, base):
    number = 0
    for digit in digits:
        number = number * base + int(digit)
    return number

def decode_ids(mapped_digits, base):
    # Assuming you have a way to split the digits correctly
    ids = []
    temp_digits = []
    
    for digit in mapped_digits:
        temp_digits.append(digit)
        if len(temp_digits) >= 8:  # Example length, adjust as needed
            ids.append(convert_from_base(temp_digits, base))
            temp_digits = []
    
    return ids

def get_pixel_value(image_path):
    # Open the image
    image = Image.open(image_path)
    pixels = image.load()
    width, height = image.size

    grid_size = 8
    pixel_position = (6, 6)

    # List to store pixel values and their classifications
    pixel_values = []

    def classify_color(r, g, b):
        # Define thresholds for color classification
        if   r > 180 and g < 180 and b < 180:
            return '1'
        elif g > 180 and r < 180 and b < 180:
            return '3'
        elif b > 180 and r < 180 and g < 180:
            return '2'
        elif r < 120 and g < 120 and b < 120:
            return '4'
        elif r > 100 and g > 100 and b > 100:
            return '0'
        else:
            return '-1'

    # Iterate over the image in 8x8 grids
    for y in range(0, height, grid_size):
        for x in range(0, width, grid_size):
        
            # Check if the grid fits within the image
            if x + grid_size <= width and y + grid_size <= height:
                # Get the value of the (4,4) pixel in the current grid
                px = x + pixel_position[0]
                py = y + pixel_position[1]
                pixel_value = pixels[px, py]
                
                # Classify the pixel color
                r, g, b = pixel_value[:3]
                color_class = classify_color(r, g, b)
                
                pixel_values.append((x//8, y//8, pixel_value, color_class))
    
    return pixel_values

# Usage example
image_path = 'resized_image.png'
pixel_values = get_pixel_value(image_path)
base5 = ''
for x, y, value, color in pixel_values:
    if (x<8 and y<8) or (x>38 and y<8) or (x<8 and y>38) or (x>21 and x<25 and y>5 and y<9) or (x>5 and x<9 and y>21 and y<25) or (x>21 and x<25 and y>21 and y<25) or (x>21 and x<25 and y>37 and y<41) or (x>37 and x<41 and y>21 and y<25) or (x>37 and x<41 and y>37 and y<41)  : pass#or y==7 or x==7
    else: 
        base5 = base5 + color
        print(f"Pixel at ({x}, {y}) has value {value} and is classified as {color_mapping[int(color)]}({color})")
        # if x == 5 : exit()
        # if color == "-1": exit()
# base5 = convert_chunks_to_int(split_into_chunks(str(convert_from_base(base5, 5)),3))
base5 = split_into_chunks(base5, 3)
base5 = convert_chunks_to_int(base5)
# base5 = [convert_from_base(b5, 5) for b5 in base5]

print(base5)
string = ''
for i in base5:
    string = string + chr(i)
print(string)

