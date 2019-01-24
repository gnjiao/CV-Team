import cv2
from enum import Enum


class State(Enum):
    Fail=0
    Success=1
    Idle=2
    Running=3
print(State.Fail.value)
