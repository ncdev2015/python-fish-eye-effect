# Python Fish Eye Effect

## Overview
This project implements a fish-eye effect on a stitched panorama created from multiple images. It utilizes OpenCV for image processing, NumPy for numerical operations, and Matplotlib for displaying the results. The main functionalities include stitching images together to form a panorama, applying a fish-eye lens effect, and visualizing the output.

## Installation
To run this project, you need to have Python installed on your machine. You also need to install the required libraries. You can do this using pip:

```bash
pip install opencv-python numpy matplotlib
```

## Usage
1. Place your image files in the `images` directory. You can use any number of images, but ensure they are suitable for stitching (i.e., overlapping regions).
2. Modify the `image_files` list in `main.py` to include the names of your images. The default example includes:
   - image1.jpg
   - image2.jpg
   - image3.jpg
   - image4.jpg
   - image5.jpg
   - image6.jpg
   - image7.jpg

3. Run the application:

```bash
python main.py
```

4. The program will stitch the images, apply the fish-eye effect, and display the results. The output images will be saved in the `images` directory as `panorama.jpg` and `fisheye_panorama.jpg`.

## Directory Structure
```
python-fish-eye-effect
├── images               # Directory for input images and output results
├── main.py             # Main application file
└── README.md           # Project documentation
```

## Contributing
Feel free to contribute to this project by submitting issues or pull requests. Your feedback and suggestions are welcome!

## License
This project is open-source and available under the MIT License.