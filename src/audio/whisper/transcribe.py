from dataclasses import dataclass
from typing import Iterable

from faster_whisper.transcribe import Segment, TranscriptionInfo


def to_text(segments: Iterable[Segment]) -> str:
    return " ".join(segment.text for segment in segments)


@dataclass
class TranscriptionResult:
    segments: Iterable[Segment]
    info: TranscriptionInfo

    def __post_init__(self):
        # 防止初始化的 segments 为 generator, 转成 list 使其可以被多次迭代
        self.segments = list(self.segments)

    @property
    def text(self) -> str:
        return to_text(self.segments)
