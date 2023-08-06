from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends
from loguru import logger
from typing import List
from src.audio.whisper.transcribe import transcribe_full

# 创建应用实例
app = FastAPI()


# 音频配置类
class AudioConfiguration:
    SAMPLE_RATE = 16000
    BIT = 16


# 音频帧类
class AudioFrame:

    def __init__(self, data: bytes, config: AudioConfiguration):
        self.data = data
        self.duration_seconds = len(data) / (config.SAMPLE_RATE * config.BIT / 8)


# 转录上下文类
class TranscriptionContext:

    def __init__(self):
        self.frames: List[AudioFrame] = []

    def add_frame(self, frame: AudioFrame):
        self.frames.append(frame)

    def get_full_audio(self) -> bytes:
        return b"".join([frame.data for frame in self.frames])


# 转录服务类
class TranscriptionService:

    def __init__(self, config: AudioConfiguration):
        self.config = config

    def transcribe(self, context: TranscriptionContext):
        full_audio = context.get_full_audio()
        return transcribe_full(full_audio)


# 创建转录服务的依赖项
def get_transcription_service() -> TranscriptionService:
    return TranscriptionService(AudioConfiguration())


# WebSocket端点
@app.websocket("/audio")
async def audio_endpoint(
    ws: WebSocket,
    transcription_service: TranscriptionService = Depends(get_transcription_service),
) -> None:
    """接受音频数据并在连接关闭时返回完整的转录"""
    logger.info(f"New connection: {ws.client.host}")
    await ws.accept()

    context = TranscriptionContext()
    config = AudioConfiguration()
    try:
        while True:
            audio_data = await ws.receive_bytes()
            frame = AudioFrame(audio_data, config)
            context.add_frame(frame)
            logger.debug(
                f"Received audio data, duration: {frame.duration_seconds:.2f} s"
            )

    except WebSocketDisconnect:
        transcription = transcription_service.transcribe(context)
        logger.info(f"Transcription complete: {transcription}")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise
