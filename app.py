import cv2
from PIL import Image
import numpy as np
import argparse
import mimetypes
from vortex.runtime.helper import InferenceHelper


source_img = "./test_images/weapon0.jpg"
size = (480, 640)

# Set Argument Parse
parser = argparse.ArgumentParser()
parser.add_argument(
    "-s",
    "--source-img",
    default=source_img,
    help="Input your image source to detect the object",
)
value_parser = parser.parse_args()
source_img = value_parser.source_img

# Check Source Img
mimestart = mimetypes.guess_type(value_parser.source_img)[0]
if mimestart != None:
    mimestart = mimestart.split("/")[0]
    if mimestart not in ["image"]:
        raise "Input image source correctly!"

# Run Open cv
img = Image.open(source_img)
img = np.array(img)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
img = np.flip(img, -1)
img = np.expand_dims(img,0)
img = cv2.resize(img[0], size[::-1])[None,...]

kwargs = dict(
    model_path="./saved_model_onnx.onnx",
    runtime="cpu",
)
rt = InferenceHelper.create_runtime_model(**kwargs)

kwargs = dict(
    score_threshold=0.5,
    visualize=True,
)
result = rt(img, **kwargs)
visual = result["visualization"][0]
visual = np.flip(visual, 2)

cv2.imshow("Weapon", visual)
cv2.waitKey(0)

cv2.destroyAllWindows()
