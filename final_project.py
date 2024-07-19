import cv2
import os
import hashlib
import numpy as np

# Create dictionaries for character to ASCII and vice versa mapping
char_to_ascii = {chr(i): i for i in range(256)}
ascii_to_char = {i: chr(i) for i in range(256)}

# Function to load an image
def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at {image_path}. Please check the file path.")
    return image

# Function to save and open the modified image
def save_and_open_image(image, output_path):
    cv2.imwrite(output_path, image)
    print(f"Data hiding in image completed successfully. Image saved as {output_path}.")
    os.startfile(output_path)

# Hash the key for better security
def hash_key(key):
    return hashlib.sha256(key.encode()).digest()

# Function to encode text into the image
def encode_text_in_image(image, text, key):
    rows, cols, _ = image.shape
    key = hash_key(key)
    key_length = len(key)
    text_length = len(text)
    key_index = 0
    color_channel = 0  # BGR plane

    # Embed the length of the text
    length_str = str(text_length).zfill(8)  # Ensure it's 8 digits long
    text = length_str + text

    for char in text:
        row = (key_index // cols) % rows
        col = key_index % cols
        image[row, col, color_channel] = char_to_ascii[char] ^ key[key_index % key_length]
        color_channel = (color_channel + 1) % 3
        key_index += 1

    return image

# Function to decode text from the image
def decode_text_from_image(image, key):
    rows, cols, _ = image.shape
    key = hash_key(key)
    key_length = len(key)
    key_index = 0
    color_channel = 0  # BGR plane
    decrypted_text = ""
    length_str = ""

    # Extract the length of the text first
    for _ in range(8):
        row = (key_index // cols) % rows
        col = key_index % cols
        decrypted_char = ascii_to_char[image[row, col, color_channel] ^ key[key_index % key_length]]
        length_str += decrypted_char
        color_channel = (color_channel + 1) % 3
        key_index += 1
    
    text_length = int(length_str)

    # Extract the actual text
    for _ in range(text_length):
        row = (key_index // cols) % rows
        col = key_index % cols
        decrypted_char = ascii_to_char[image[row, col, color_channel] ^ key[key_index % key_length]]
        decrypted_text += decrypted_char
        color_channel = (color_channel + 1) % 3
        key_index += 1

    return decrypted_text

def main():
    try:
        image_path = input("Enter the path of the image to use: ")
        image = load_image(image_path)

        key = input("Enter the security key: ")
        text_to_hide = input("Enter the text to hide: ")

        # Encode the text in the image
        encoded_image = encode_text_in_image(image, text_to_hide, key)
        output_path = "encoded_image.png"
        save_and_open_image(encoded_image, output_path)

        # Prompt user to decode the text
        if input("\nEnter 1 to extract data from the image: ") == '1':
            reentered_key = input("\nRe-enter the key to extract the text: ")
            if key == reentered_key:
                try:
                    decrypted_text = decode_text_from_image(encoded_image, reentered_key)
                    print(f"\nEncrypted text was:\n{decrypted_text}")
                except Exception as decode_error:
                    print(f"An error occurred during decoding: {decode_error}")
            else:
                print("Keys do not match. Unable to decode the text.")
        else:
            print("Exiting.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
