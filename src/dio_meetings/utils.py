import librosa
import soundfile as sf


def split_audio_librosa(input_file, segment_length_sec=30):
    y, sr = librosa.load(input_file, sr=None)  # Загрузка аудио
    segment_samples = int(segment_length_sec * sr)

    for i in range(0, len(y), segment_samples):
        segment = y[i:i + segment_samples]
        output_file = f"segment_{i // segment_samples}.wav"
        sf.write(output_file, segment, sr)
        print(f"Сохранено: {output_file}")


split_audio_librosa(r"C:\Users\andre\DIOMeetings\5409190724363121400.ogg")
