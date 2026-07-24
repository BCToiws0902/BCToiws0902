import base64

with open('vietnam_flag.gif', 'rb') as f:
    b64_data = base64.b64encode(f.read()).decode('utf-8')

svg_content = f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="400">
  <image href="data:image/gif;base64,{b64_data}" width="400" height="400" />
</svg>"""

with open('vietnam_flag.svg', 'w') as f:
    f.write(svg_content)
print('Successfully generated vietnam_flag.svg bypassing GitHub player.')
