import sounddevice as sd
from pydub import AudioSegment
from pydub.generators import Sine
import numpy as np
import time
import pyaudio
import wave


def play_metronome(interval, frequency, duration):
    # def generate_metronome_sound(interval, frequency, duration):
    #     beep = Sine(frequency).to_audio_segment(duration=2)  # 100 ms beep
    #     silence = AudioSegment.silent(
    #         duration=int((interval - 0.1) * 1000)
    #     )  # Silence for the rest of the interval
    #     metronome = beep + silence
    #     total_metronome = metronome * int(duration / interval)
    #     return total_metronome

    # metronome_sound = generate_metronome_sound(interval, frequency, duration)
    # metronome_sound.export("metronome.wav", format="wav")

    # # Start playback and recording
    # sd.play(metronome_sound.get_array_of_samples(), samplerate=sample_rate)

    p = pyaudio.PyAudio()

    volume = 0.5  # range [0.0, 1.0]
    fs = 44100  # sampling rate, Hz, must be integer
    duration = .02  # in seconds, may be float
    f = 1000.0  # sine frequency, Hz, may be float

    # generate samples, note conversion to float32 array
    samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)

    # per @yahweh comment explicitly convert to bytes sequence
    output_bytes = (volume * samples).tobytes()

    # for paFloat32 sample values must be in range [-1.0, 1.0]
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    # play. May repeat with different volume values (if done interactively)
    start_time = time.time()
    stream.write(output_bytes)
    print("Played sound for {:.2f} seconds".format(time.time() - start_time))



    stream.stop_stream()

    # save wav file
    wf = wave.open("metronome.wav", 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paFloat32))
    wf.setframerate(fs)
    wf.writeframes(output_bytes)
    wf.close()

    stream.close()

    p.terminate()






def record_audio(format, channels, sample_rate, chunk, output_name):

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=format,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk,
    )

    frames = []
    print("Recording...")

    time_now = time.time()
    while True:
        data = stream.read(chunk)
        frames.append(data)
        # break if time is 1 sec
        if time.time() - time_now > 1:
            break

    print("Finished recording.")
    stream.stop_stream()
    stream.close()
    audio.terminate()

    waveFile = wave.open(output_name, "wb")
    waveFile.setnchannels(channels)
    waveFile.setsampwidth(audio.get_sample_size(format))
    waveFile.setframerate(sample_rate)
    waveFile.writeframes(b"".join(frames))
    waveFile.close()


# Parameters
duration = 1  # Duration of the recording in seconds
interval = 0.3  # Interval of metronome (seconds)
frequency_1 = 900  # Frequency of the beep (Hz)
frequency_2 = 1000  # Frequency of the beep (Hz)
sample_rate = 44100  # Sample rate for recording and playback

format = pyaudio.paInt16
channels = 1
sample_rate = 44100
chunk = 4096
output_name_1 = "output_1.wav"
output_name_2 = "output_2.wav"

play_metronome(interval, frequency_1, duration)
record_audio(format, channels, sample_rate, chunk, output_name_1)


# play_metronome(interval, frequency_2, duration)
# record_audio(format, channels, sample_rate, chunk, output_name_2)
