import cv2
import numpy as np
import matplotlib.pyplot as plt

def stitch_images(images):
    """
    Stitch multiple images together to create a panorama

    Parameters:
    images (list): List of image file paths to stitch

    Returns:
    numpy.ndarray: Stitched panorama image
    """
    # Read all images
    imgs = []
    for img_path in images:
        print(f"Reading image: {img_path}")
        img = cv2.imread(img_path)
        if img is None:
            raise FileNotFoundError(f"Could not read image: {img_path}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert from BGR to RGB
        imgs.append(img)

    print(f"Stitching {len(imgs)} images...")

    # Create a stitcher object
    stitcher = cv2.Stitcher_create()

    # Perform stitching
    status, panorama = stitcher.stitch(imgs)

    if status != cv2.Stitcher_OK:
        error_messages = {
            cv2.Stitcher_ERR_NEED_MORE_IMGS: "Not enough images for stitching",
            cv2.Stitcher_ERR_HOMOGRAPHY_EST_FAIL: "Homography estimation failed",
            cv2.Stitcher_ERR_CAMERA_PARAMS_ADJUST_FAIL: "Camera parameter adjustment failed"
        }
        error_msg = error_messages.get(status, f"Unknown error (code: {status})")
        raise Exception(f"Stitching failed: {error_msg}")

    return panorama

def apply_fisheye_effect(image):
    """
    Apply a fish-eye lens effect to an image

    Parameters:
    image (numpy.ndarray): Input image

    Returns:
    numpy.ndarray: Image with fish-eye effect
    """
    print("Applying fish-eye effect...")

    # Get image dimensions
    height, width = image.shape[:2]

    # Create map for distortion
    distCoeff = np.zeros((4,1), np.float64)

    # Fish-eye distortion parameters
    # Positive values for barrel distortion, negative for pincushion
    distCoeff[0,0] = 0.5  # k1, primary distortion factor
    distCoeff[1,0] = 0.2  # k2, secondary distortion factor
    distCoeff[2,0] = 0.0  # p1, tangential distortion
    distCoeff[3,0] = 0.0  # p2, tangential distortion

    # Set up camera matrix
    cam = np.eye(3, dtype=np.float32)
    cam[0,0] = width / 2.0  # fx
    cam[1,1] = height / 2.0  # fy
    cam[0,2] = width / 2.0   # cx
    cam[1,2] = height / 2.0  # cy

    # Create undistortion maps
    map1, map2 = cv2.initUndistortRectifyMap(
        cam, distCoeff, None, cam, 
        (width, height), cv2.CV_32FC1)

    # Apply remapping to create the fish-eye effect
    fisheye_img = cv2.remap(image, map1, map2, 
                            interpolation=cv2.INTER_LINEAR, 
                            borderMode=cv2.BORDER_CONSTANT)

    return fisheye_img

def display_result(original_images, panorama, fisheye_panorama):
    """
    Display original images, panorama, and fish-eye panorama
    """
    plt.figure(figsize=(20, 15))

    # Display original images in the first row
    for i, img_path in enumerate(original_images):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.subplot(3, max(len(original_images), 1), i + 1)
        plt.imshow(img)
        plt.title(f"Image {i+1}")
        plt.axis('off')

    # Display original panorama in the second row
    plt.subplot(3, 1, 2)
    plt.imshow(panorama)
    plt.title("Panorama")
    plt.axis('off')

    # Display fish-eye panorama in the third row
    plt.subplot(3, 1, 3)
    plt.imshow(fisheye_panorama)
    plt.title("Fish-eye Panorama")
    plt.axis('off')

    plt.tight_layout()
    plt.show()

def main():
    # Example usage - Make sure these files exist in your working directory
    image_files = [
        "image1.jpg",
        "image2.jpg",
        "image3.jpg",
        "image4.jpg",
        "image5.jpg",
        "image6.jpg",
        "image7.jpg",
    ]

    # Alternatively, you can use command line arguments
    import sys
    if len(sys.argv) > 1:
        image_files = sys.argv[1:]

    try:
        # Stitch images
        panorama = stitch_images(image_files)

        # Apply fish-eye effect
        fisheye_panorama = apply_fisheye_effect(panorama)

        # Display results
        display_result(image_files, panorama, fisheye_panorama)

        # Save the results
        cv2.imwrite("panorama.jpg", cv2.cvtColor(panorama, cv2.COLOR_RGB2BGR))
        cv2.imwrite("fisheye_panorama.jpg", cv2.cvtColor(fisheye_panorama, cv2.COLOR_RGB2BGR))
        print("Panorama saved as 'panorama.jpg'")
        print("Fish-eye panorama saved as 'fisheye_panorama.jpg'")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()