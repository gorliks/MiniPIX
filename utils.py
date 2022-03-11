import time, sys
import logging
import json
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.ndimage as ndi



def parse_command(command):
    # command = "key1=val1 key2=val2"
    try:
        parsed = dict((key, value) for key, value in [i.split('=') for i in command.split()])
    except:
        print('No keywords, using command as a string')
        parsed = str(command)
    return parsed


def convert_dictionary_string_to_dictionary(dictionary_string):
    return json.loads(dictionary_string)


def read_data_file(file_name):
    file_name = file_name.replace('\\', '/')
    if os.path.isfile(file_name):
        data = np.loadtxt(  file_name  )
    else:
        print('file not found')
        data = None
    return data





def plot_sem_image(image, median_smoothing=3, show=True):
    """Display image with matplotlib.pyplot
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    if median_smoothing is not None:
        image = ndi.median_filter(image, size=median_smoothing)
    height, width = image.shape
    #extent_kwargs = [-(width / 2), +(width / 2), -(height / 2), +(height / 2)]
    extent_kwargs = [0,width, height,0]
    ax.set_xlabel("Select starting point")
    ax.set_xlim(extent_kwargs[0], extent_kwargs[1])
    ax.set_ylim(extent_kwargs[2], extent_kwargs[3])
    ax.imshow(image, cmap="gray", extent=extent_kwargs)
    if show is True:
        fig.show()
    return fig, ax


def select_point(image):
    """Return location of interactive user click on image.
    """
    fig, ax = plot_sem_image(image)
    coords = []

    def on_click(event):
        print(event.xdata, event.ydata)
        coords.append(event.ydata)
        coords.append(event.xdata)

    fig.canvas.mpl_connect("button_press_event", on_click)
    plt.show()
    return np.flip(coords[-2:], axis=0)  # coordintes in x, y format