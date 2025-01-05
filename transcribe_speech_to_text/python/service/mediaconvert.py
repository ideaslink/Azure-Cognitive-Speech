"""
    media file conversion
"""

import subprocess

class MediaConv():
    """
        convert media files
    """
    ffmpath = r"G:\VCI\download\tools\ffmpeg-5.0-essentials_build\ffmpeg-5.0-essentials_build\bin/ffmpeg.exe"

    def webm2wav(self, filefrom: str, fileto: str):
        retv = subprocess.run([self.ffmpath, '-i', filefrom, fileto])
        # retv = retv.returncode
        # print(f"returned {retv}")


# file1 = "../../../media/webmt1.webm"
# file2 = "../../../media/webmt1-1.wav"
# x = MediaConv()
# x.webm2wav(file1, file2)
