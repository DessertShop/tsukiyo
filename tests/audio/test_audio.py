from unittest.mock import patch

from src.audio import AudioConstants
from src.audio.whisper.context import TranscriptionContext
from src.main import (
    AudioFrame,
    TranscriptionService,
)


def create_test_audio_data() -> bytes:
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


def test_faster_whisper():
    """使用真实的音频测试 TranscriptionService 的 faster_whisper 类是否正确调用转录功能并返回转录内容"""
    # TODO: 因为会加载模型, 这个测试用例有点慢.. 要不要想个办法呢
    file = "tests/data/test.mp3"
    service = TranscriptionService()
    res = service.transcribe(file)
    sec = res.info.duration
    assert 10 < sec < 12  # test.mp3 长度大约为 11s
    assert len(res.text) > 0
