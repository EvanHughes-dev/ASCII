from PIL import Image
import os
import argparse
CHAR_SUBSTITUTE= [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']
MODE_COLOR = True

def calculate_intensity(r, g, b):
    return int(r + g + b)//3

def parse_image(file_path: str, chars_wide: int, char_aspect_ratio: float = 0.5):
    """Parse an image from raw pixels to gray values"""
    # Get the image
    image = Image.open(file_path).convert("RGB")
    width, height = image.size
    pixels = image.load()

    # Define how many pixels wide it should be
    pixels_per_square_x = width / chars_wide

    # Derive chars_high from the image aspect ratio, corrected for character shape
    image_aspect = height / width
    chars_high = max(1, round(chars_wide * image_aspect * char_aspect_ratio))

    pixels_per_square_y = height / chars_high

    # Create a jagged array for each row, create the needed columns
    ascii_image_data = [[0] * chars_wide for _ in range(chars_high)]
    
    # For each character we need
    
    for col in range(chars_wide):

        # Find start and end indexes
        x_start = int(col * pixels_per_square_x)
        # Clamp to total width of image
        x_end = min(int((col + 1) * pixels_per_square_x), width)
        x_end = max(x_end, x_start + 1)

        for row in range(chars_high):
            y_start = int(row * pixels_per_square_y)
            y_end = min(int((row + 1) * pixels_per_square_y), height)
            y_end = max(y_end, y_start + 1)

            total_grayscale = 0
            grayscale_count = 0

            for x in range(x_start, x_end):
                for y in range(y_start, y_end):
                    r, g, b = pixels[x, y]
                    total_grayscale += calculate_intensity(r, g, b)
                    grayscale_count += 1

            average = total_grayscale // grayscale_count
            ascii_image_data[row][col] = average

    return ascii_image_data, chars_wide, chars_high


def print_ascii_image(ascii_image_data, chars_wide, chars_high):
    RESET = "\033[0m"
    for row in range(chars_high):
        row_data = ascii_image_data[row]
        row = []
        for col in range(chars_wide):
            grey = row_data[col]

            if MODE_COLOR:
                row.append(f"\033[38;2;{grey};{grey};{grey}m#{RESET}")
            else:
                reduced = int((grey / 256) // 0.1)
                row.append(CHAR_SUBSTITUTE[reduced])

        print("".join(row)+RESET)


if __name__ == "__main__":
    # Get the width of the terminal in characters (terminals are mono spaced)
    CHARS_WIDE = os.get_terminal_size().columns

    parser = argparse.ArgumentParser(
        prog="Image to ASCII Converter",
        description="Take a image or images and convert it to an ASCII interpretation",
    )
    
    parser.add_argument('-d', '--display', help="display the ASCII image created", action="store_true")

    # This kills the program if -h or --help is found (duh)
    args = parser.parse_args()

    data, w, h = parse_image("./test.jpg", CHARS_WIDE)

    if args.display:
        print_ascii_image(data, w, h)




