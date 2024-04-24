import os

# Signal handler to delete the associated file when a model instance is deleted.
def delete_file_on_post_delete(sender, instance, field_name, **kwargs):
    file_field = getattr(instance, field_name, None)
    if file_field:
        # Get the path of the file
        file_path = file_field.path
        # Check if the file exists
        if os.path.exists(file_path):
            # Delete the file
            os.remove(file_path)