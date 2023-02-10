from time import sleep
from Devices import conveyor, camera, load_cell, send_data, tof_sensor
import requests

print("<---------------------Welcome To Grow-Simplee Tool------------------------->\n\n")

while True:
    print("Stopping Conveyer Belt ...")
    conveyor.stop()
    print("--------------------------------------------------------------------------\n")
    print("Please start inserting Similar Items into the tool\n")
    input("Press Enter to continue...")
    print("Starting Conveyer Belt ...")
    conveyor.start()
    items_info = []

    if not conveyor.out_config():
        print("Please Clear the Conveyer Belt ...")
        continue

    while True:
        print(
            "--------------------------------------------------------------------------\n")
        print("Waiting for Item ...")
        while not conveyor.in_config():
            pass

        print("Item Detected ...")
        max_height = float('-inf')
        image = None

        while (max_height <= 0) or not conveyor.out_config():
            print(conveyor.centre_config())
            if conveyor.centre_config() and image is None:
                print(conveyor.centre_config())
                print("Stopping Conveyer Belt For Image ...")
                conveyor.stop()
                image = camera.capture_image(brightness=50, contrast=90)
                print("Starting Conveyer Belt after Image ...")
                conveyor.start()
            max_height = max(max_height, tof_sensor.get_height())

        if not image:
            print("Error in Image. Please Check the Object or insert again ...")
            continue

        # if max_height <= 0:
        #     print("Error in Height. Please Check the Object ...")
        #     print("Starting Conveyer Belt ...")
        #     conveyor.start()
        #     continue

        try:
            length, width = camera.get_length_width(image, max_height)
            assert length > 0 and width > 0
        except Exception as e:
            print(e)
            print("Error in dimensions. Please Check the Object ...")
            print("Starting Conveyer Belt ...")
            conveyor.start()
            continue

        # Just because we do not have a Bar Code Scanner
        item_id = input("Please Enter Item ID: ")

        item_info = {
            "item_id": item_id,
            "length": length,
            "breadth": width,
            "height": max_height,
            "weight": load_cell.get_weight(),
        }

        items_info.append(item_info)

        print("Item Removed ...")
        yes_no = input("1. Continue similar objects (y / n). \n ")
        if yes_no == 'n':
            print(items_info)
            print("Sending Data to Server ...")
            response = requests.post(
                "http://192.168.205.139:8000/add-item-details", json=items_info)
            rejected_items = response.json()
            print("Sent info to Server...")
            print("Rejected Items: ", rejected_items)
            break

        sleep(0.05)
    sleep(0.05)
