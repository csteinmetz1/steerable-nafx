import librosa
import soundfile
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
from itertools import cycle


def rt60(h):

    power = h ** 2
    energy = np.cumsum(power[::-1])[::-1]  # Integration according to Schroeder

    # remove the possibly all zero tail
    i_nz = np.max(np.where(energy > 0)[0])
    energy = energy[:i_nz]
    energy_db = 10 * np.log10(energy)
    energy_db -= energy_db[0]

    return energy_db


ir0dB = "docs/audio/reverb/ir.mp3"
ir12dB = "docs/audio/reverb/ir+12dB.mp3"
ir24dB = "docs/audio/reverb/ir+24dB.mp3"

A = [ir0dB, ir12dB, ir24dB]

ir0dB_2 = "docs/audio/reverb/ir+0dB_3_-1.5.mp3"
ir12dB_2 = "docs/audio/reverb/ir+12dB_3_-1.5.mp3"
ir24dB_2 = "docs/audio/reverb/ir+24dB_3_-1.5.mp3"

B = [ir0dB_2, ir12dB_2, ir24dB_2]

ir0dB_3 = "docs/audio/reverb/ir+0dB_3.5_0.mp3"
ir12dB_3 = "docs/audio/reverb/ir+12dB_3.5_0.mp3"
ir24dB_3 = "docs/audio/reverb/ir+24dB_3.5_0.mp3"

C = [ir0dB_3, ir12dB_3, ir24dB_3]

fig, ax = plt.subplots(nrows=1, sharex=True, sharey=True, figsize=(6, 2.5))

ax = [ax]

y_labels = ["0,0", "3,-1.5", "3.5,0"]
gains = ["+0dB", "+12dB", "+24dB"]

for set_idx, ir_set in enumerate([A]):
    lines = ["-", "--", ":"]
    linecycler = cycle(lines)

    for gain_idx, ir in enumerate(ir_set):
        y, sr = librosa.load(ir)
        y = y[int(1.2 * sr) :]

        energy_db = rt60(y)

        t = np.linspace(0, len(energy_db) / sr, num=len(energy_db))
        ax[set_idx].plot(t, energy_db.T, linestyle=next(linecycler), alpha=0.8)

        # y /= np.max(np.abs(y))
        # librosa.display.waveplot(y, sr=sr, ax=ax[idx])
        ax[set_idx].set_ylabel(y_labels[set_idx], rotation=0, labelpad=20)
        ax[set_idx].yaxis.set_label_position("right")
        ax[set_idx].grid(c="lightgray")
        ax[set_idx].set_axisbelow(True)

ax[0].set_title("Energy Decay Curve (dB)")
ax[0].set_xlim([0, 2.25])
ax[0].set_ylim([-60, 3])
ax[-1].set_xlabel("Time (s)")
ax[0].legend(gains, loc="lower left", ncol=3)


# ax[0].label_outer()
plt.tight_layout()
plt.savefig("docs/audio/reverb/edc.png")
plt.savefig("docs/audio/reverb/edc.pdf")
