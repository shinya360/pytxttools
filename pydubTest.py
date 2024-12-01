from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_file("sample.wav", format="wav")
play(sound)