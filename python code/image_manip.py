from PIL import Image


def double_image_size(img_path, file_name):
    # Open the image using PIL
    original_image = Image.open(img_path)

    # Get dimensions of the original image
    width, height = original_image.size

    # Create a new image with double the dimensions
    new_width = width * 2
    new_height = height * 2
    new_image = Image.new("RGB", (new_width, new_height), "WHITE")

    # Iterate through each pixel of the original image
    for y in range(height):
        for x in range(width):
            # Get the pixel value at (x, y) in the original image
            pixel = original_image.getpixel((x, y))

            # Assign this pixel value to a 2x2 block in the new image
            new_image.putpixel((2 * x, 2 * y), pixel)
            new_image.putpixel((2 * x + 1, 2 * y), pixel)
            new_image.putpixel((2 * x, 2 * y + 1), pixel)
            new_image.putpixel((2 * x + 1, 2 * y + 1), pixel)

    new_image.show()
    new_image.save(f"images/{file_name}")


def split_image(input_image_path, output_path, num_splits):
    """
    Splits the input image into num_splits x num_splits smaller square images.
    Args:
    - input_image_path (str): File path to the input image.
    - output_path (str): Directory where the smaller images will be saved.
    - num_splits (int): Number of splits along each dimension (e.g., 4 means 4x4 grid).
    """
    img = Image.open(input_image_path)
    width, height = img.size
    split_width = width // num_splits
    split_height = height // num_splits

    for i in range(num_splits):
        for j in range(num_splits):
            left = j * split_width
            upper = i * split_height
            right = (j + 1) * split_width
            lower = (i + 1) * split_height
            box = (left, upper, right, lower)
            split_img = img.crop(box)
            split_img.save(f"{output_path}/split_{i * num_splits + j + 1}.png")


if __name__ == "__main__":
    image_path = "canvas-2025.png"  # Replace with your image file path
    # split_image(image_path, 'slices/3', 8)
    double_image_size(image_path, "canvas2025.png")
