class ConversationState:
    def __init__(self):
        self.last_message = None

    def is_new(self, msg):
        if not msg:
            return False
        if msg == self.last_message:
            return False
        self.last_message = msg
        return True
