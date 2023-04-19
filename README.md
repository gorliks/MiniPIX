# Minipix
A graphical user interface (GUI)-based software has 
been developed to integrate a TPX3 Advacam Minipix 
pixelated detector with a ThermoFisher Nova scanning 
electron microscope (SEM). This setup is primarily used 
for electron-backscatter diffraction (EBSD) measurements 
using the external direct-electron pixelated detector. 
One of the main advantages of using this detector is 
its higher sensitivity to weak EBSD signals. As a result,
lower electron beam currents can be utilised, which is 
particularly beneficial for the characterization of 
beam-sensitive materials.

The ThermoFisher Nova scanning electron microscope 
(SEM) can be controlled using Dynamic Link Library (DLL)
libraries from a third-party software called Bruker 
Espirit GUI. These libraries provide a means to access
the functionality of the SEM and perform various 
operations, such as imaging and analysis. 
The Bruker Espirit GUI offers a graphical user interface
(GUI) that allows users to interact with the SEM and 
control its various settings, such as the electron beam
current, the imaging mode, the magnification, and beam
spot position, among many other functionalities. 
The DLL libraries enable seamless communication between 
the SEM and the software, ensuring that commands are 
transmitted accurately and efficiently. 

In order to control and communicate with Dynamic Link 
Library (DLL) C++ functions, a Python layer has
been implemented using the ctypes library. This allows
for seamless integration between the two programming 
languages, enabling the Python program to access the 
functionality provided by the DLL libraries. The ctypes
library provides a means to call functions and pass
parameters to them, as well as to receive return values
from the functions. 