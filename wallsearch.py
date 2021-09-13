#!/usr/bin/env python
from sys import argv
from pathlib import Path
import re, os, webbrowser, tempfile, requests


def init():

    # Checking usage
    if len(argv) != 2:
        print(f"Usage: python {argv[0]} query")
        return 1

    # Querying wallhaven.cc
    else:
        user_query = argv[1]
        r = requests.get(
            f"https://wallhaven.cc/api/v1/search?q={user_query}&sorting=views&order=desc"
        )
        output = r.json()["data"]

        # Error handling
        if not output:
            print("Error : No images found")
            return 1

        else:

            # Prompting user with instructions
            print("")
            print("######################################################")
            print("##################### Wallsearch #####################")
            print("######################################################")
            print("")
            print("Fetching thumbnails from wallhaven.cc, please wait ...")
            print("")
            print("Please delete the thumbnails you don't like.")
            print("")

            file_proc(output)


# Download and save image
def get_img(url, path):

    r = requests.get(url)
    with open(path, "wb") as f:
        f.write(r.content)


# Checking for a 'Pictures' folder in home directory
def pictures():
    pictures = f"{Path.home()}{os.path.sep}Pictures"
    if os.path.exists(pictures):
        return pictures
    else:
        os.mkdir(pictures)
        return pictures


def file_proc(output):

    dict = {}

    # Creating temporary folder
    with tempfile.TemporaryDirectory() as tmp:

        # Looping through json output
        for i in range(len(output)):

            # Saving small thumbnail's url
            url = output[i]["thumbs"]["small"]
            # Saving image id
            image_id = output[i]["id"]
            # Saving full hd image's url link
            image_url = output[i]["path"]
            # Getting file extension
            s = re.search("\..{3}$", image_url)
            ext = s.group(0)

            dict[image_id] = image_url

            # Building full local path to image
            image_path = image_id + ext
            fullpath = tmp + os.path.sep + image_path

            get_img(url, fullpath)

        # Openning tmp folder for user interaction
        webbrowser.open(tmp)
        input("Press Enter key to continue ...")
        print("")

        # For each remaining image in folder
        with os.scandir(tmp) as it:

            # If user deleted every thumbnail
            if not os.listdir(tmp):

                # Display message and exit
                print("Everything was deleted... Terminating now.")
                print("")
                return 0

            else:

                print("Downloading FHD images, please wait...")
                print("")

                for entry in it:

                    # Get image file name & build full local path
                    image_id = os.path.splitext(entry.name)[0]
                    fullpath = pictures() + os.path.sep + entry.name

                    get_img(dict[image_id], fullpath)

    # Openning 'Pictures' folder for final display
    webbrowser.open(pictures())
    print("Enjoy your new wallpapers!")
    return 0


if __name__ == "__main__":
    init()
