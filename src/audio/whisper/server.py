# 转录服务类
from src.audio.whisper.transcribe import TranscriptionContext, transcribe_full


class TranscriptionService:

    def __init__(self):
        pass

    def transcribe(self, context: TranscriptionContext):
        full_audio = context.get_full_audio()
        return transcribe_full(full_audio)


# 创建转录服务的依赖项
def get_transcription_service() -> TranscriptionService:
    return TranscriptionService()
