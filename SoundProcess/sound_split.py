import pydub
import silence
import os
from pydub.generators import WhiteNoise

target = ""
output_dir = ".\\result"
threshold = -18


def sound_split(file=target):
    sound = pydub.AudioSegment.from_wav(file)
    audio_chunks = silence.split_on_silence(sound, min_silence_len=500, silence_thresh=threshold * 2)
    for i, chunk in enumerate(audio_chunks, start=0):
        noise = WhiteNoise().to_audio_segment(duration=len(chunk), volume=threshold * 1.5)
        combined = chunk.overlay(noise)
        output_file = "{name}_{number}.wav".format(name=os.path.basename(os.path.splitext(file)[0]), number=i)
        output_file = os.path.join(output_dir, output_file)
        combined.export(output_file, format="wav")


if __name__ == '__main__':
    print("awake")
    sound_split(".\\source\\awake.wav")
    print("light")
    sound_split(".\\source\\light.wav")
    print("shut")
    sound_split(".\\source\\shut.wav")
    print("blink")
    sound_split(".\\source\\blink.wav")
