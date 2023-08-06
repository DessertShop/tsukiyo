from fastapi import Depends, FastAPI, WebSocket, WebSocketDisconnect
from loguru import logger

from src.audio import AudioFrame
from src.audio.whisper.server import TranscriptionService, get_transcription_service
from src.audio.whisper.context import TranscriptionContext

# 创建应用实例
app = FastAPI()


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
    try:
        while True:
            audio_data = await ws.receive_bytes()
            frame = AudioFrame(audio_data)
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
