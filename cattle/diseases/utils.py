import hashlib


def compare_images(image_data1, image_data2):
    hash_object1 = hashlib.sha256(image_data1.read())
    hash_object2 = hashlib.sha256(image_data2.read())

    return hash_object1.digest() == hash_object2.digest()
