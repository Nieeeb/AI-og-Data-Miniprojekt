from urllib.request import urlopen
import re

url = "http://olympus.realpython.org/profiles/poseidon"

page = urlopen(url)

html_bytes = page.read()
html = html_bytes.decode("utf-8")

print(html)

title_index = html.find("<title>")
start_index = title_index + len("<title>")
end_index = html.find("</title>")

title = html[start_index:end_index]
print(title)


import sounddevice as sd
from scipy.io.wavfile import write

fs = 44800  # Sample rate
seconds = 5  # Længde på optagelse

recording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Venter indtil optagelse er færdig
write('Data\sound.wav', fs, recording)  # Gemmer som wav fil

import cv2 as cv

# Forbinder til webcam
webcam = cv.VideoCapture(0)
# Video Codex
video_cod = cv.VideoWriter_fourcc(*'mp4v')
# Placering for gem af video
output = cv.VideoWriter(r"Data\video.mp4", video_cod, 30.0, (640,480))

# Sættter optagelse i gang der gemmer hver frame og viser det
while(True):
    # Gemmer hvert frame
    ret,frame = webcam.read()
    cv.imshow("Live video", frame)
    output.write(frame)
    # Stopper så snart der trykkes q
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
    
# Stopper webcam
webcam.release()
# Lukker fil
output.release()
# Lukker vinduer
cv.destroyAllWindows()