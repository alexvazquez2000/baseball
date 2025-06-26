from PIL import Image
import io
 
class Thumbnail:
    def __init__(self, instance_attribute):
        self.instance_attribute = instance_attribute

    @classmethod
    def create_thumbnail(cls, image_data, size=(100, 100)):
        """Create a thumbnail from raw image data."""
        img = Image.open(io.BytesIO(image_data))
        img.thumbnail(size)
        if img.mode != "RGB":
            # Ensure RGB mode for JPEG
            #This will work for: JPEG, PNG and Images with transparency (RGBA)
            img = img.convert("RGB")
        thumb_io = io.BytesIO()
        img.save(thumb_io, format="JPEG")
        return thumb_io.getvalue()
