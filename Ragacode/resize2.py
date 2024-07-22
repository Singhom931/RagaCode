import cv2
import numpy as np
import matplotlib.pyplot as plt

def main():
    # Load the image
    image_path = 'Warped Image.jpeg'
    image = cv2.imread(image_path)

    # Check if the image is loaded properly
    if image is None:
        raise ValueError("Image not loaded. Please check the file path.")

    # Get the original dimensions
    original_height, original_width = image.shape[:2]

    # Calculate new dimensions
    new_width  = original_width  // 64
    new_height = original_height // 64
    # print(new_width, new_height)

    # Initialize the downscaled image
    downscaled_image = np.zeros((new_height, new_width, 3), dtype=np.uint8)

    # Iterate over 64x64 segments
    for i in range(new_height):
        for j in range(new_width):
            # Extract the 64x64 block
            block = image[i*64:(i+1)*64, j*64:(j+1)*64]
            
            # Extract the 2x2 center of the 64x64 block
            center_2x2 = block[30:35, 30:35]
            
            # Calculate the average color of the 2x2 center
            avg_color = center_2x2.mean(axis=(0, 1)).astype(np.uint8)
            
            # Assign the average color to the corresponding pixel in the downscaled image
            downscaled_image[i, j] = avg_color


    # Save the resized image using matplotlib
    fig, ax = plt.subplots()
    ax.imshow(cv2.cvtColor(downscaled_image, cv2.COLOR_BGR2RGB))
    ax.axis('off')  # Hide the axes
    plt.savefig('resized_image.png', bbox_inches='tight', pad_inches=0)
    plt.close(fig)  # Close the figure after saving


    # Display the original and resized images using matplotlib
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.title('Original Image')
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.title('Resized Image')
    plt.imshow(cv2.cvtColor(downscaled_image, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    # plt.show()

    cv2.imwrite('resized_first.png', downscaled_image, [int(cv2.IMWRITE_JPEG_QUALITY), 1600])
    resized_image = cv2.resize(downscaled_image, (45, 45))
    cv2.imwrite('resized_second.png', resized_image, [int(cv2.IMWRITE_JPEG_QUALITY), 1600])

if __name__ == "__main__":
    main()