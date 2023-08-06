from src.audio import AudioFrame


class TranscriptionContext:

    def __init__(self) -> None:
        self.frames: list[AudioFrame] = []

    def add_frame(self, frame: AudioFrame) -> None:
        self.frames.append(frame)

    def get_full_audio(self) -> bytes:
        return b"".join([frame.data for frame in self.frames])
