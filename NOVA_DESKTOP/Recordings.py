#Module used
import datetime
from PIL import ImageGrab
import numpy as np 
import cv2
import pyaudio
import wave
import subprocess
import msvcrt
import pyautogui
import pyscreenrec
import time

def Record_Option(option):
    
    audio = pyaudio.PyAudio()
    time_stamp = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')    
    VideoFile_name = f'VideoFile-{time_stamp}.mp4'
    AudioFile_name = f'AudioFile-{time_stamp}.wav'
    OutputFileName = f'VideoFile-{time_stamp}.mp4'
    frames=[]
    stream = audio.open(format=pyaudio.paInt16,channels=1,rate=44100,input=True,frames_per_buffer=1024)
    if "screen recording" in option:
        screen_recording(OutputFileName)
    elif "voice recording" in option:
        VoiceRecording(stream,frames,AudioFile_name,audio)

def screen_recording(output_filename,fps=12.0):
    # Get the screen resolution
    screen_size = tuple(pyautogui.size())
    print(f"Screen resolution: {screen_size}")

    # Define the codec (XVID) and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out = cv2.VideoWriter(output_filename, fourcc, fps, screen_size)

    # Calculate the number of frames to capture
    start_time = time.time()
    
    while True:
        # Capture the screen as a PIL image
        screenshot = pyautogui.screenshot()
        
        # Convert the screenshot to a numpy array (OpenCV format)
        frame = np.array(screenshot)

        # Convert RGB to BGR (OpenCV uses BGR by default)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Write the frame to the video file
        out.write(frame)

        # Show the live screen recording window (optional)
        cv2.imshow("Screen Recording", frame)

        # Check if 'Q' is pressed to stop the recording
        key = cv2.waitKey(1) & 0xFF
        if msvcrt.kbhit():
            if ord(msvcrt.getch()) == ord('q'):
                break

    # Release the VideoWriter and close OpenCV windows
    out.release()
    cv2.destroyAllWindows()
    print(f"Recording finished. File saved as {output_filename}")

def VoiceCapture(stream,frames):
    date = stream.read(1024) #records the voice
    frames.append(date)

def VoiceEnd(AudioFile_name,audio,frames):
    soundFile = wave.open(AudioFile_name,"wb")
    soundFile.setnchannels(1)
    soundFile.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
    soundFile.setframerate(44100)
    soundFile.writeframes(b''.join(frames))
    soundFile.close()

def VoiceRecording(stream,frames,AudioFile_name,audio):
    print("voice Recording has been started")
    print("press the key 'q' to exit stop voice recording")
    while True:
        VoiceCapture(stream,frames)
        
        if msvcrt.kbhit():
            if ord(msvcrt.getch()) == ord('q'):
                break


    stream.stop_stream()
    stream.close()
    audio.terminate()

    VoiceEnd(AudioFile_name,audio,frames)
    print("voice Recording has been ended")

