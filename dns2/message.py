from .message_section import Question, Header, Answer
from .domain_storage import MessageDomainStorage
from .datatypes import BitStorage
from bitstring import BitArray, ConstBitStream
import typing


class Message:
    def __init__(self):
        self.answers = {
            'answer': [],
            'authority': [],
            'additional': []
        }

    @classmethod
    def parse(cls, data: typing.Union[bytes, dict]):
        if isinstance(data, bytes):
            message = cls()
            message._edns = None
            message._answers = {
                'answer': [],
                'authority': [],
                'additional': []
            }
            message._data = ConstBitStream(bytes=data)
            message._bitstorage = BitStorage(message)
            # print(message._bitstorage._storage)
            message._domains = MessageDomainStorage(message)
            message.header = Header(message)
            if message.header._qdcount.value:
                message.question = Question(message)
            for an in range(message.header._ancount.value):
                message._answers['answer'].append(Answer.parse(message))
            for ns in range(message.header._nscount.value):
                message._answers['authority'].append(Answer.parse(message))
            for ar in range(message.header._arcount.value):
                answ = Answer.parse(message)
                if answ:
                    message._answers['additional'].append(answ)
            message._domains.reset()
            return message

    def to_bytes(self):
        pass

    def build(self):
        """
        Build message for sending
        :return: None
        """
        self.header.push_to_storage()
        if self.header.qdcount:
            self.question.push_to_storage()
        for a_type in self.answers.values():
            for answer in a_type:
                answer.push_to_storage()
        if self._edns:
            self._edns.push_to_storage()



