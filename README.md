
# AudioVisualizer 

## A simple python application for visualising music on a led strip

This project was developed as part of my seminar work about music visualization and representation. It's a simple program with 
a few effects for visualising the audio output from your device on a led strip.
This project was specifically designed to better understand the concepts of audio processing and visualization 
The code therefore is well documented.

In addition, I want to give some credits to the projects [LedFx](https://github.com/LedFx/LedFx) and [Audio Reactive LED Strip](https://github.com/scottlawsonbc/audio-reactive-led-strip)
who helped me to understand the practical usage of many concepts.

If your wish to read our documentation to the seminar work, you will find it [here](SeminarkursDokumentation.pdf)

## Demo

 https://github.com/user-attachments/assets/7c5c3ad7-c655-46f7-905a-4897d45407ea.mp4

Watch on [YouTube](https://www.youtube.com/watch?v=M1xNktjkvWU)

## How does it work?
The program takes the audio signal from your preferred input device and analyzes it. If your wish to visualize your music output on your pc, enable and set the input device Stereomix as the default device.
Stereomix takes the output from your soundcard and loops it to the input again

When the program rendered the signal, it will be send over the sACN protocol through your LAN to a microcontroller with an led strip connected. If your pc is connected through an ethernet cable with your LAN, the connection is more stable than through WLAN.

With this structure you can place the led light in your apartment wherever you want and can connect to it with your pc to start the visualization 

## Usage 

To use the application on your computer you need: 

- Python 3.1 (Anaconda is preferred) and an IDE 
- Stereomix enabled on your computer (to visualize your music output)
- An led strip: We tested the application with a ws2812b/sk6812 strip
- An ESP32 or ESP8266 with a led software to receive the transmitted signals from the computer. Note that the ESP8266 could be to weak for WLAN.
  We used an ESP32 and 
  [WLED](https://github.com/Aircoookie/WLED) for this


- Recommended but optional: Extra power supply to prevent the current from flowing through the whole esp. Without this, the esp doesn't deliver the maximum 5V (Only 3.3V) and he could get hot.

## Install the dependencies 

### with Anaconda

Create a conda virtual environment (optional but recommended)
```bash
conda create --name visualization-env python=3.1
activate visualization-env
```

Install the dependencies with pip and the conda package manager
```bash
conda install numpy scipy pyqtgraph
pip install pyaudio
pip install sacn
pip install PySide2
pip install customtkinter
```

### Without Anaconda

Use the pip packet manager to install all necessary packages
```bash
pip install numpy
pip install scipy
pip install pyaudio
pip install sacn
pip install PySide2
pip install pyqtgraph
pip install customtkinter
```

If `pip` is not found try to use `python -m pip install` instead

When you are finished you can start the program with the `gui.py` file.
A little window is popping up where you can switch between all effects
If you wish to create an own gui use the main interface `program.py`

Make sure your microcontroller has sACN over multicast enabled. If your wish to use unicast for sending, change the sACN configuration in `sender.py`

## Issues and Future

As mentioned at the beginning, this project was developed as part of my seminar work in order to better understand the world of audio processing and music visualization.
For this reason, no regular updates are planned. 

If this project can help anyone to get a better understanding about audio processing, I would be very grateful. If your wish to extend this project or build a new one, feel free to create a fork or use my code for your next project.






