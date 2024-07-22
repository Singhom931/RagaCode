from PIL import Image
import numpy as np

def main():
    # Load the image
    image_path = 'resized_second.png'  # Update with your image path
    image = Image.open(image_path)

    # Convert image to numpy array
    image_array = np.array(image)

    def split_into_chunks(s, chunk_size):
        return [s[i:i + chunk_size] for i in range(0, len(s), chunk_size)]

    def convert_chunks_to_int(chunks):
        return [int(chunk) for chunk in chunks]

    def convert_from_base(digits, base):
        number = 0
        for digit in digits:
            number = number * base + int(digit)
        return number

    def colour_classification(pixel):
        r,g,b = pixel
        if r>100 and g>100 and b>100 and max(r,g,b)-min(r,g,b)<50:
            return '0'
        elif r<100 and g<100 and b<100: #and max(r,g,b)-min(r,g,b)<75:
            return '4'
        elif r>g and r>b:
            return '1'
        elif g>r and g>b:
            return '3'
        elif b>r and b>g:
            return '2'
        else:
            return '0'

    filter = Image.open('QRv7readfilter.png')
    filter = filter.convert('L')

    base5 = ''
    for y, row in enumerate(image_array):
        for x, pixel in enumerate(row):
            filter_pixel = filter.getpixel((x,y))
            if filter_pixel > 0:
                base5 = base5 + colour_classification(pixel)

    base5 = split_into_chunks(base5, 3)
    intbase5 = convert_chunks_to_int(base5)
    base5 = [convert_from_base(b5, 5) for b5 in base5]

    print(intbase5)

    string = ''
    for i in base5:
        string = string + chr(i)
    print(string)

if __name__ == '__main__':
    main()