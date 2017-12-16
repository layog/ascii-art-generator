import argparse
from PIL import Image
import numpy as np


def average(image):
    img = np.array(image)
    width, height = img.shape
    avg = np.average(img.reshape(width*height))
    return avg


def convert(image, columns, scale, output_file):
    gradient_scales = {
        70: "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
        10: '@%#*+=-:. '
    }
    scale_to_use = 10

    # It's easier to work with numpy
    image = np.array(image)
    image = np.transpose(image)

    width, height = image.shape
    rows = int((height/width)*columns*scale)

    stride_width, stride_height = int(width/columns), int(height/rows)

    output = []

    for h_index in range(rows):
        output.append([])
        for w_index in range(columns):
            cut_image = image[w_index*stride_width:(w_index+1)*stride_width, h_index*stride_height:(h_index+1)*stride_height]
            cut_image_average = average(cut_image)
            char_to_choose = int((cut_image_average*(scale_to_use-1))/255.0)
            output[-1].append(gradient_scales[scale_to_use][char_to_choose])

    with open(output_file, "w") as out_file:
        for row in output:
            for char in row:
                out_file.write(char)
            out_file.write("\n")


def main():
    parser = argparse.ArgumentParser(description="Generates ASCII image from the provided image")
    parser.add_argument("input_image", help="Image to be converted", type=str)
    parser.add_argument("-c", "--columns", type=int, help="Number of colums in output image", default=80)
    parser.add_argument("--scale", type=float, help="The height to scale acc. to the width", default=1)
    parser.add_argument("-o", "--output", action="store", type=str,
        help="Provide an output file name (default: out.txt)", default="out.txt")

    args = parser.parse_args()

    try:
        image = Image.open(args.input_image).convert('L')
    except FileNotFoundError:
        print("Please provide a valid path to the file")
        raise

    convert(image, args.columns, args.scale, args.output)


if __name__ == "__main__":
    main()