import numpy as np
import wave


def read_wav_file(file_name, tsh):
    spf = wave.open(file_name, "r")

    # Extract Raw Audio from Wav File
    signal = spf.readframes(-1)
    signal = np.frombuffer(signal, np.int16)
    fs = spf.getframerate()

    signal = signal / np.max(signal)
    Time = np.linspace(0, len(signal) / fs, num=len(signal))

    signal = signal[10000:40000]
    Time = Time[10000:40000]

    mask = ((signal < tsh) & (signal > 0)) | (signal > -tsh) & (signal < 0)
    filtered = signal.copy()
    filtered[mask] = 0

    return signal, Time, fs, filtered


def get_second_peak_position(signal):
    def get_second_peak(filtered):
        maxa = 0
        max2 = 0
        for i, x in enumerate(filtered):
            if x < 0.1:
                continue

            else:
                maxa = max(maxa, x)

            if x < maxa:
                break

        for j, x in enumerate(filtered[i:]):
            if x < maxa:
                continue
            else:
                max2 = max(max2, x)

            if x < max2:
                break
        return max2, j + i - 1

    maxa, la = get_second_peak(signal)
    maxb, lb = get_second_peak(signal[20000:])
    lb += 20000

    return la, lb, maxa, maxb


tsh = 0.1
_, Time_1, _, filtered_1 = read_wav_file("output_1.wav", tsh)
_, Time_2, _, filtered_2 = read_wav_file("output_2.wav", tsh)


la, lb, _, _ = get_second_peak_position(filtered_1)
delay_1 = (Time_1[lb] - Time_1[la]) * 1000

la, lb, _, _ = get_second_peak_position(filtered_2)
delay_2 = (Time_2[lb] - Time_2[la]) * 1000

print("The distance between the two peaks is:", round(delay_1, 2))
print("The distance between the two peaks is:", round(delay_2, 2))

# average
print(
    "The average distance between the two peaks is:", round((delay_1 + delay_2) / 2, 2)
)
