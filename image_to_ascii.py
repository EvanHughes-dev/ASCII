from PIL import Image
import os
from sys import argv

CHAR_SUBSTITUTE= [' ', '.', ':', '-', '=', '+', '*', '#', '%', '@']
MODE_COLOR = True

def calculate_intensity(r, g, b):
    return int(r + g + b)//3

def parse_image(file_path: str, chars_wide: int, char_aspect_ratio: float = 0.5):
    """
    char_aspect_ratio: width-to-height ratio of a single terminal character cell.
    Most monospace terminal fonts are roughly twice as tall as they are wide,
    so 0.5 is a reasonable default. Set to 1.0 if your terminal/font is square,
    or tweak until circles look like circles.
    """
    im = Image.open(file_path).convert("RGB")
    width, height = im.size
    pixels = im.load()

    pixels_per_square_x = width / chars_wide

    # Derive chars_high from the image aspect ratio, corrected for character shape
    image_aspect = height / width
    chars_high = max(1, round(chars_wide * image_aspect * char_aspect_ratio))

    pixels_per_square_y = height / chars_high

    ascii_image_data = [[0] * chars_high for _ in range(chars_wide)]

    for col in range(chars_wide):
        x_start = int(col * pixels_per_square_x)
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
            ascii_image_data[col][row] = average

    return ascii_image_data, chars_wide, chars_high


def print_ascii_image(ascii_image_data, chars_wide, chars_high):
    RESET = "\033[0m"
    for y in range(chars_high):
        row = []
        for x in range(chars_wide):
            grey = ascii_image_data[x][y]

            if MODE_COLOR:
                row.append(f"\033[38;2;{grey};{grey};{grey}m#{RESET}")
            else:
                reduced = int((grey / 256) // 0.1)
                row.append(CHAR_SUBSTITUTE[reduced])

        print("".join(row)+RESET)


if __name__ == "__main__":
    CHARS_WIDE = os.get_terminal_size().columns
    if len(argv)>1 and (argv[1] == "ASCII" or argv[1]=="-a"):
        MODE_COLOR = False
        
    data, w, h = parse_image("./TestPhoto.jpg", CHARS_WIDE)
    print(f"Grid size: {w}x{h}")
    print_ascii_image(data, w, h)




