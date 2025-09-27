from google.protobuf.message import Message

class EchoRequest(Message):
    message: str
    def __init__(self, message: str = "") -> None: ...

class EchoResponse(Message):
    message: str
    def __init__(self, message: str = "") -> None: ...
