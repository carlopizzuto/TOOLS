from PIL import Image
import os
import sys

def resize_image(input_image_path, output_dir, sizes=((32, 32), (192, 192), (512, 512))):
    """
    Resize an image (including .webp files) into multiple sizes and save them to the specified output directory.

    Args:
    - input_image_path: Path to the input image.
    - output_dir: Directory to save the resized images.
    - sizes: A tuple of tuples, each containing the width and height to resize to.

    Returns:
    - List of paths to the resized images.
    """
    # Verify the file format is supported
    valid_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    if not input_image_path.lower().endswith(valid_extensions):
        raise ValueError(f"Unsupported file format. Supported formats are: {valid_extensions}")

    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    resized_image_paths = []
    with Image.open(input_image_path) as img:
        for size in sizes:
            # Resize the image using the LANCZOS filter
            resized_img = img.resize(size, Image.LANCZOS)
            
            # Get the original filename with extension
            original_filename = os.path.basename(input_image_path)
            
            # Construct the output image path
            output_image_path = os.path.join(output_dir, f"{os.path.splitext(original_filename)[0]}_{size[0]}x{size[1]}{os.path.splitext(original_filename)[1]}")
            
            # Save the resized image
            resized_img.save(output_image_path)
            
            # Append the path to the list of resized image paths
            resized_image_paths.append(output_image_path)
    
    return resized_image_paths

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <input_image_path>")
        sys.exit(1)
    
    input_image_path = str(sys.argv[1])
    
    output_dir = '../out/imgResizer'
    resized_images = resize_image(input_image_path, output_dir)
    
    print("Resized images saved to:", resized_images)