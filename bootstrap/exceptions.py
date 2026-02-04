class TopicBlockedException(Exception):
    def __init__(self, keyword):
        self.keyword = keyword
        # This message mimics a Java stack trace error
        self.message = f"Access to topic '{keyword}' denied due to protocol violation."
        super().__init__(self.message)

    def __str__(self):
        return f"TopicBlockedException: {self.message}"

class ResponseNotAvailableException(Exception):
    def __init__(self):
        self.message = "The system cannot find the answer."
        super().__init__(self.message)

    def __str__(self):
        return f"ResponseNotAvailableException: {self.message}"
