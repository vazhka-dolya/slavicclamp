# SlavicClamp
Small & simple video compressor, nothing much.\
Just insert the path to the video that you want to compress, then insert the path and name & extension you want the result to have, write the desired size in megabytes, and click Compress.\
DO NOT ask about the name.\
<img src="https://github.com/vazhka-dolya/slavicclamp/blob/main/img/screenshot1_4.png?raw=true">
# Features
- Extremely simple.
- Translated to English, Latvian, Russian, and Ukrainian.
- Decimals are supported, so you can compress videos to sizes like 0.50 megabytes.
- A setting to configure a new file size to be set by default upon launch.
- Works starting from Windows 7 (maybe even Vista, but that has not been tested). It should also work on Linux using [Wine](https://www.winehq.org/). Not sure about Mac.
# Compiling
## Windows
<details>
  <summary>Click here to view</summary>

To compile SlavicClamp the same way I do:
1. Install [Python 3.8.20](https://github.com/adang1345/PythonWindows/tree/master/3.8.20).[^1]
2. Install dependencies by running `py -3.8 -m pip install PyQt5, ffmpeg-python, Nuitka`.
3. Open SlavicClamp's source code's path in the terminal and run `py -3.8 -m nuitka --onefile --windows-icon-from-ico=img\icon_app.ico --enable-plugin=pyqt5 --windows-console-mode=disable .\main.pyw`.
4. Create an `ffmpeg` folder in the compiled program's root directory and place [FFmpeg binaries](https://www.ffmpeg.org/download.html#build-windows) there.[^2]
5. Done.

Note that this is the way I do it. You don't have to use Python 3.8.20 or Nuitka specifically.

</details>

# Plans
All the main goals I had for this tool have been finished, but there are a few other additions that would be good and I could add if I really wanted to:
- Option to configure the path to open by default in the file select dialog (already partly implemented but hidden).
- More options for compression, like:
- - Changing the resolution
- - Removing audio
- Support for compressing other formats, such as:
- - Images
- - Audio
# Credits
- Some person on Stack Overflow – code for actually compressing the video.
- FFmpeg – used for compression.
- SMO14O7 – came up with the name for this program.

[^1]: Last version of Python 3.8. Used for Windows 7 support.
[^2]: You don't need `ffplay.exe`, by the way.
