import os
from random import randint
from Dimensions import *
from Controller import *
from time import sleep

if not os.path.exists('temp_images'):
    os.makedirs('temp_images')

print("<---------------------Welcome To Grow-Simplee Tool------------------------->\n\n")

while True:
    print("Please start inserting Similar Items into the tool\n")
    input("Press Enter to continue...")

    items_info = []
    while True:

        if in_config():
            print("Item Detected ...")
            max_height = float('-inf')
            while max_height == float('inf') or not centre_config():
                max_height = max(max_height, get_height())

            # TODO: Add line to indicate stopped conveyer belt
            
            file_path = f"./test_images/{randint(0, 1000000)}.jpg"

            capture_image(file_path)
            length, width = get_length_width(file_path, max_height)
            
            
            # Just because we do not have a Bar Code Scanner
            item_id = input("Please Enter Item ID: ")
            
            item_info = {
                "length": length,
                "breadth": width,
                "height": max_height,
                "weight": get_weight(),
            }
            
            items_info.append(item_info)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                
            # TODO: Add line to indicate start conveyer belt
            
            print("Waiting for item to go out ...")
            while not out_config():
                pass
            print("Item Removed ...")
            yes_no = input("1. Continue with Similar. \n ")
        
        sleep(0.05)
    sleep(0.05)
            