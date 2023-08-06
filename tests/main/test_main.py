import re
from contextlib import contextmanager
from unittest.mock import patch

from fastapi.testclient import TestClient
from loguru import logger

from src.main import (
    AudioConstants,
    AudioFrame,
    TranscriptionContext,
    TranscriptionService,
    app,
)


def create_test_audio_data():
    return bytes([0] * (AudioConstants.SAMPLE_RATE * AudioConstants.BIT // 8))


# AudioFrame Class Tests
def test_audio_frame():
    """测试 AudioFrame 类的持续时间是否正确计算"""
    data = create_test_audio_data()
    frame = AudioFrame(data)
    assert frame.duration_seconds == 1.0


# TranscriptionContext Class Tests
def test_transcription_context():
    """测试 TranscriptionContext 类是否正确添加和获取音频帧"""
    context = TranscriptionContext()
    data = create_test_audio_data()
    frame = AudioFrame(data)
    context.add_frame(frame)
    assert context.get_full_audio() == data


# TranscriptionService Class Tests
@patch("src.main.transcribe_full")
def test_transcription_service(mock_transcribe_full):
    """测试 TranscriptionService 类是否正确调用转录功能并返回转录内容"""
    mock_transcribe_full.return_value = "Test transcription"
    context = TranscriptionContext()
    data = create_test_audio_data()
    frame = AudioFrame(data)
    context.add_frame(frame)
    service = TranscriptionService()
    transcription = service.transcribe(context)
    assert transcription == "Test transcription"


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
    with capture_logs() as logs:
        with patch("src.main.transcribe_full") as mock_transcribe_full:
            # 设定转录的模拟返回值
            mock_transcribe_full.return_value = "Test transcription"

            client = TestClient(app)
            with client.websocket_connect("/audio") as websocket:
                audio_data = b"test_audio_data"
                websocket.send_bytes(audio_data)
                # 关闭连接以触发转录过程
                websocket.close()

            # 验证转录函数是否被正确调用
            mock_transcribe_full.assert_called_once()

            # 从日志中验证转录内容
            transcription_log = next(
                log for log in logs if "Transcription complete" in log
            )
            assert (
                re.search(r"Transcription complete: (.+)", transcription_log).group(1)
                == "Test transcription"
            )
