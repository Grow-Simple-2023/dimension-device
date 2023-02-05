import os
from random import randint
from Devices import camera, load_cell, tof_sensor, conveyor, send_data
from time import sleep
import init

print("Stopping Conveyer Belt ...")
conveyor.stop()

print("<---------------------Welcome To Grow-Simplee Tool------------------------->\n\n")

while True:
    print("Please start inserting Similar Items into the tool\n")
    input("Press Enter to continue...")
    print("Starting Conveyer Belt ...")
    conveyor.start()
    items_info = []

    if not conveyor.out_config():
        print("Please Clear the Conveyer Belt ...")
        continue

    while True:

        while not conveyor.in_config():
            pass

        print("Item Detected ...")
        max_height = float('-inf')
        image = None
        while (max_height <= 0) or (not conveyer.out_config()):
            if converyer.centre_config() and image is None:
                print("Stopping Conveyer Belt For Image ...")
                conveyor.stop()
                image = camera.capture_image()
                print("Starting Conveyer Belt after Image ...")
                conveyor.start()
            max_height = max(max_height, get_height())

        # if max_height <= 0:
        #     print("Error in Height. Please Check the Object ...")
        #     print("Starting Conveyer Belt ...")
        #     conveyor.start()
        #     continue

        try:
            length, width = get_length_width(image, max_height)
            assert length > 0 and width > 0
        except:
            print("Error in dimensions. Please Check the Object ...")
            print("Starting Conveyer Belt ...")
            conveyor.start()
            continue

        # Just because we do not have a Bar Code Scanner
        item_id = input("Please Enter Item ID: ")

        item_info = {
            "length": length,
            "breadth": width,
            "height": max_height,
            "weight": load_cell.get_weight(),
        }

        items_info.append(item_info)

        print("Item Removed ...")
        yes_no = input("1. Continue similar objects (y / n). \n ")
        if yes_no == 'n':
            print("Sending Data to Server ...")
            print(items_info)
            print("Sent info to Server...")
            break

        sleep(0.05)
    sleep(0.05)
