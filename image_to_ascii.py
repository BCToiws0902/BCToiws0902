import os
from PIL import Image

def image_to_ascii(image_path, width=42, invert=False):
    if not os.path.exists(image_path):
        print(f"Error: File {image_path} does not exist.")
        return ""
        
    try:
        img = Image.open(image_path)
    except Exception as e:
        print(f"Error opening image: {e}")
        return ""

    # Console characters are taller than they are wide.
    # We adjust the height by a factor of 0.55 to maintain aspect ratio.
    aspect_ratio = img.height / img.width
    height = int(width * aspect_ratio * 0.55)
    
    # Resize image and convert to grayscale
    img = img.resize((width, height), Image.Resampling.LANCZOS)
    img = img.convert("L")
    
    # ASCII characters sorted by density (dark to light)
    # For dark mode (light text on dark background), denser characters represent lighter areas.
    # For light mode (dark text on light background), denser characters represent darker areas.
    ascii_chars = '@%#*+=-:. '
    if invert:
        ascii_chars = ascii_chars[::-1]
        
    num_chars = len(ascii_chars)
    
    ascii_str = []
    for y in range(img.height):
        line = ""
        for x in range(img.width):
            gray = img.getpixel((x, y))
            # Map grayscale (0-255) to character index (0 to num_chars-1)
            char_idx = int(gray * (num_chars - 1) / 255)
            line += ascii_chars[char_idx]
        ascii_str.append(line)
        
    return "\n".join(ascii_str)

if __name__ == "__main__":
    image_file = "logobct.png"
    print("--- Dark Mode ASCII Art Preview (Light text on Dark background) ---")
    # For dark theme, lighter pixels get dense chars (@, %, etc.)
    dark_ascii = image_to_ascii(image_file, width=42, invert=False)
    print(dark_ascii)
    
    print("\n--- Saving previews to text files ---")
    with open("ascii_dark.txt", "w", encoding="utf-8") as f:
        f.write(dark_ascii)
    
    # For light theme, darker pixels get dense chars (@, %, etc.)
    light_ascii = image_to_ascii(image_file, width=42, invert=True)
    with open("ascii_light.txt", "w", encoding="utf-8") as f:
        f.write(light_ascii)
    print("Saved ascii_dark.txt and ascii_light.txt successfully!")
