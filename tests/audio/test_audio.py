from unittest.mock import patch

from src.audio import AudioConstants
from src.audio.whisper.context import TranscriptionContext
from src.main import (
    AudioFrame,
    TranscriptionService,
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
@patch("src.audio.whisper.server.transcribe_full")
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
