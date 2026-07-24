from PIL import Image
import base64
from io import BytesIO

# Open the downloaded 13-frame GIF
gif = Image.open('vietnam_flag.gif')

frames = []
try:
    while True:
        # Convert to RGBA to preserve any transparency and colors, resize to 400x400
        frames.append(gif.convert('RGBA').resize((400, 400)))
        gif.seek(gif.tell() + 1)
except EOFError:
    pass

num_frames = len(frames)
width, height = 400, 400
sheet_width = width * num_frames

# Create a wide canvas for the sprite sheet
sheet = Image.new('RGBA', (sheet_width, height))
for i, frame in enumerate(frames):
    sheet.paste(frame, (i * width, 0))

# Convert the wide image to a base64 string
buffered = BytesIO()
sheet.save(buffered, format="PNG", optimize=True)
b64_img = base64.b64encode(buffered.getvalue()).decode('utf-8')

# Generate the SVG that uses CSS steps() to animate the sprite sheet
svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <style>
    @keyframes play {{
      0% {{ transform: translateX(0); }}
      100% {{ transform: translateX(-{sheet_width}px); }}
    }}
    .sprite {{
      animation: play {num_frames * 0.1}s steps({num_frames}) infinite;
    }}
  </style>
  <image class="sprite" href="data:image/png;base64,{b64_img}" width="{sheet_width}" height="{height}" />
</svg>"""

with open('vietnam_flag.svg', 'w', encoding='utf-8') as f:
    f.write(svg_content)

print(f"Successfully generated vietnam_flag.svg using Sprite Sheet animation! Sheet size: {sheet_width}x{height}")
