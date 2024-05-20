from PIL import Image

def save_image(instance, output_size=(500, 500)):
    """
    Saves a thumbnail version of the image associated with the instance.
    
    Args:
        instance: The instance of the model containing the image field.
        output_size: A tuple representing the size of the thumbnail. Default is (500, 500).
    """
    img = Image.open(instance.image.path)
    img = img.resize(output_size)
    img.save(instance.image.path)