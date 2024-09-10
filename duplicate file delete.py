import os
import imagehash
from PIL import Image
from tqdm import tqdm

def find_similar_images(directory, hash_size=8, similarity_threshold=5):
    """
    Finds and deletes similar images in a directory.

    Parameters:
    - directory: str, the directory containing images.
    - hash_size: int, the size of the hash, smaller hash size makes it more sensitive to changes.
    - similarity_threshold: int, the maximum hamming distance between two images to consider them similar.
    """
    image_hashes = {}
    
    for image_name in tqdm(os.listdir(directory)):
        image_path = os.path.join(directory, image_name)
        
        try:
            with Image.open(image_path) as img:
                img_hash = imagehash.average_hash(img, hash_size=hash_size)
                
                # Check if a similar hash exists
                if img_hash in image_hashes:
                    # Remove similar image
                    print(f"Deleting {image_path} - Similar to {image_hashes[img_hash]}")
                    os.remove(image_path)
                else:
                    # Check similarity with existing hashes
                    for existing_hash in image_hashes.keys():
                        if img_hash - existing_hash <= similarity_threshold:
                            print(f"Deleting {image_path} - Similar to {image_hashes[existing_hash]}")
                            os.remove(image_path)
                            break
                    else:
                        # If no similar image found, add to the dictionary
                        image_hashes[img_hash] = image_name
                        
        except Exception as e:
            print(f"Error processing {image_path}: {e}")

# Usage example
directory = "E:\Video\py code"
find_similar_images(directory)
