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



def get_Nx_Ny_from_indices(files_dir, files):
    N = len(files)
    print('Number of files = ', N)
    files = [file_name.replace(files_dir, '') for file_name in files ]
    X = []
    Y = []
    for file_name in files:
        temp = file_name.split('_')
        x = temp[1]
        y = temp[2]
        X.append(int(x))
        Y.append(int(y))
    X = np.array(X)
    Y = np.array(Y)
    Nx = X.max()
    Ny = Y.max()
    print(Nx, Ny)
    return Nx+1, Ny+1


def get_indices_from_file_name(file_dir, file_name):
    file_name = file_name.replace(file_dir, '')
    temp = file_name.split('_')
    i = temp[1]
    j = temp[2]
    return int(i), int(j)




class BlittedCursor:
    """
    A cross-hair cursor using blitting for faster redraw.
    """

    def __init__(self, ax):
        self.ax = ax
        self.background = None
        self.horizontal_line = ax.axhline(color='y', lw=0.8, ls='--')
        self.vertical_line = ax.axvline(color='y', lw=0.8, ls='--')
        # text location in axes coordinates
        self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)
        self._creating_background = False
        ax.figure.canvas.mpl_connect('draw_event', self.on_draw)

    def on_draw(self, event):
        self.create_new_background()

    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw

    def create_new_background(self):
        if self._creating_background:
            # discard calls triggered from within this function
            return
        self._creating_background = True
        self.set_cross_hair_visible(False)
        self.ax.figure.canvas.draw()
        self.background = self.ax.figure.canvas.copy_from_bbox(self.ax.bbox)
        self.set_cross_hair_visible(True)
        self._creating_background = False

    def on_mouse_move(self, event):
        if self.background is None:
            self.create_new_background()
        if not event.inaxes:
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.restore_region(self.background)
                self.ax.figure.canvas.blit(self.ax.bbox)
        else:
            self.set_cross_hair_visible(True)
            # update the line positions
            x, y = event.xdata, event.ydata
            self.horizontal_line.set_ydata([y])
            self.vertical_line.set_xdata([x])
            #self.text.set_text('x=%1.2f, y=%1.2f' % (x, y))

            self.ax.figure.canvas.restore_region(self.background)
            self.ax.draw_artist(self.horizontal_line)
            self.ax.draw_artist(self.vertical_line)
            self.ax.draw_artist(self.text)
            self.ax.figure.canvas.blit(self.ax.bbox)
