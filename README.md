## csgo-auto-accept
A Python script that automatically presses the "accept" button in CS:GO when a match is found.
### How it works
* With pyautogui, a screenhsot is always made after a certain number of time.
* Then the template matching algorithm of opencv is used to search for the template on the screenshot.
* When a match is found with opencv, pyautogui is used to move the mouse to that location and then a mouse click is triggered.
### Installation
* The `config.ini` file must be in the same folder as the python script.
* Make a screenshot (you can make more than one) of your CS:GO "accept" button and put this screenshot in the same folder as the python script and the config.ini file. 
* Go to the config file and replace `example.jpg` with the filename of your screenshot and save it
##### The following Python packages are required: 
    [PyAutoGui](https://github.com/asweigart/pyautogui)
    [NumPy](https://github.com/numpy/numpy)
    [OpenCV](https://github.com/opencv/opencv-python)
### License
    [Apache License 2.0](https://github.com/tym21/csgo-auto-accept/blob/main/LICENSE)
