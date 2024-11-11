# SlavicClamp
Small & simple video compressor, nothing much.\
Just insert the path to the video that you want to compress, then insert the path and name & extension you want the result to have, write the desired size in megabytes, and click Compress.\
DO NOT ask about the name.\
<img src="https://github.com/vazhka-dolya/slavicclamp/blob/main/img/screenshot1_3.png?raw=true">
# FFmpeg
SlavicClamp uses FFmpeg for compression.\
On Windows, if you've downloaded the program from the Releases section, then it's already included in the `ffmpeg` folder.\
If, however, you're using the source, then you need to manually create a folder called `ffmpeg` and put the `ffmpeg.exe` and `ffprobe.exe` executables there.
# Other info
- Should work starting from Windows 7 (maybe even Vista, but it has not been tested yet). It should also work on Linux using [Wine](https://www.winehq.org/). Not sure about Mac.
- Decimals are supported, so you should be able to compress videos to sizes like 0.50 megabytes.
- I made this program for myself because I was tired of having to always use some shady online compressor, so I made this program to compress quicker.
- - I may not respond to any issues, since again, I made this just for myself and I am content with what I have already.
# Plans
All the main goals I had for this tool have been finished, but there are a few other additions that would be good and I could add if I really wanted to:
- Support for other languages. If I add this, then expect translations for the following languages:
- - Russian
- - Ukrainian
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
