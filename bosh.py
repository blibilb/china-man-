import os
from PIL import Image

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio  = maxWidth/image.size[0]
    heightRatio = maxHeight/image.size[1]

    newWidth    = int(widthRatio*image.size[0])
    newHeight   = int(heightRatio*image.size[1])

    newImage    = image.resize((newWidth, newHeight))
    return newImage

# Get a list of all the image files in the folder
folder = "gabuk"
image_files = [f for f in os.listdir(folder) if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg")]

# Process the images
for i, image_file in enumerate(image_files):
    # Open the image
    image = Image.open(os.path.join(folder, image_file))

    # Resize the image
    image = changeImageSize(500, 500, image)

    # Make the image transparent
    image.putalpha(1)

    # Composite the image with the previous result
    if i == 0:
        result = image
    else:
      try:
        result = Image.alpha_composite(result, image)
      except:
        continue

# Convert the result to a RGB image and save it
result = result.convert("RGB")
result.save(os.path.join(folder, "result.jpg"))