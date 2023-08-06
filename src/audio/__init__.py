# 音频配置类
class AudioConstants:
    SAMPLE_RATE = 16000
    BIT = 16


# 音频帧类
class AudioFrame:

    def __init__(self, data: bytes):
        self.data = data
        self.duration_seconds = len(data) / (
            AudioConstants.SAMPLE_RATE * AudioConstants.BIT / 8
        )
