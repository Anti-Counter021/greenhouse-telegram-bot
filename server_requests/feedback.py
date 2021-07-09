from .base_request import AbstractRequest


class Feedback(AbstractRequest):

    url = 'feedback'


request_feedback = Feedback()
