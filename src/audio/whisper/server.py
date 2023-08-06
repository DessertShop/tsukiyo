# 转录服务类
from typing import BinaryIO, Union

import numpy as np
from faster_whisper import WhisperModel
from loguru import logger

from src.audio.whisper.context import TranscriptionContext
from src.audio.whisper.transcribe import TranscriptionResult
from src.utils.singleton import singleton


class TranscriptionService:

    def __init__(self) -> None:
        self.model = WhisperModel(
            model_size_or_path="tiny",
            device="auto",
            download_root=None,  # 暂时设置为None, 模型会下载到 ~/.cache/huggingface...
        )

    def transcribe(
        self, audio: Union[str, BinaryIO, np.ndarray]
    ) -> TranscriptionResult:
        res = TranscriptionResult(*self.model.transcribe(audio, vad_filter=True))
        logger.info(
            f"Transcription complete [{res.info.language}][{res.info.duration:.2f}s]: {res.text}"  # noqa: E501
        )
        return res

    def transcribe_context(self, context: TranscriptionContext) -> TranscriptionResult:
        full_audio = context.get_full_audio()
        return self.transcribe(full_audio)


@singleton
class TranscriptionServiceSingleton:

    def __init__(self) -> None:
        self.instance = TranscriptionService()


# 创建转录服务的依赖项
def get_transcription_service() -> TranscriptionService:
    # TODO: 弄清楚 fastapi.Depends 决定这里是否应该用 单例模式, 在这之前, 先用单例模式
    return TranscriptionServiceSingleton().instance
