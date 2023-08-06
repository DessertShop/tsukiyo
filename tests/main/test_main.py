import re
from contextlib import contextmanager
from unittest.mock import patch

from fastapi.testclient import TestClient
from loguru import logger
from src.audio.whisper.transcribe import TranscriptionResult
from faster_whisper.transcribe import TranscriptionInfo
from src.main import app


@contextmanager
def capture_logs():
    logs = []

    def sink(message):
        logs.append(message.record["message"])

    handler_id = logger.add(sink)
    try:
        yield logs
    finally:
        logger.remove(handler_id)


# Audio Endpoint Tests


def test_audio_endpoint():
    """测试音频端点的 WebSocket 连接及其行为"""

    class MockTranscriptionService:

        class MockSegment:
            text = "Test transcription Text"

        def transcribe_context(self, context):
            return TranscriptionResult([self.MockSegment()], None)

    with patch(
        "src.audio.whisper.server.TranscriptionService"
    ) as transcription_service:
        transcription_service.return_value = MockTranscriptionService()

        with capture_logs() as logs:
            client = TestClient(app)
            with client.websocket_connect("/audio") as websocket:
                audio_data = b"test_audio_data"
                websocket.send_bytes(audio_data)
                # 关闭连接以触发转录过程
                websocket.close()

            # 从日志中验证转录内容
            transcription_log = next(
                log for log in logs if "Transcription complete" in log
            )
            assert (
                re.search(r"Transcription complete: (.+)", transcription_log).group(1)
                == "Test transcription Text"
            )
