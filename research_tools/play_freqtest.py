# /usr/bin/python
# coding: utf-8
import sys
import struct

import pyaudio
import numpy as np


# classとか関数書く

def play(stream, data):  # 再生用関数、ストリームと波形データを引数に

    # チャンク単位でストリームに出力し音声を再生
    chunk = 1024
    sp = 0  # 再生位置ポインタ
    buffer = data[sp:sp + chunk]
    while buffer:
        stream.write(buffer)
        sp = sp + chunk
        buffer = data[sp:sp + chunk]


def create_data(freq_list=[800], start_pos=0):  # オシレーター
    data = []
    amp = 1.0 / len(freq_list)  # 使用時は波形データにampを乗算する

    end_pos = start_pos + 0.05 * 44100
    for n in np.arange(start_pos, end_pos):
        s = 0.0  # 波形データをゼロクリア
        for f in freq_list:
            s += amp * np.sin(2 * np.pi * f * n / 44100)
        # 振幅が大きい時はクリッピング
        if s > 1.0:  s = 1.0
        if s < -1.0: s = -1.0
        data.append(s)  # 末尾に追加
    data = [int(x * 32767.0) for x in data]  # 値を32767～-32767間にする

    # バイナリに変換
    data = struct.pack("h" * len(data), *data)  # listに*をつけると引数展開される

    return data, end_pos


if __name__ == '__main__':

    # ストリームを開く
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, output=1)
    freq_list = []
    for i, freq in enumerate(sys.argv):
        if i == 0:
            continue
        freq_list.append(freq)

    pos = 0
    try:
        while True:
            data, pos = create_data(start_pos=pos, freq_list=freq_list)
            play(stream, data)

    except KeyboardInterrupt:

        stream.close()
        p.terminate()
