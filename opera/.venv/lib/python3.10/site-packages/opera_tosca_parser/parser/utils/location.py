class Location:
    def __init__(self, stream_name: str, line: int, column: int):
        """
        Construct Location object
        :param stream_name: Stream name
        :param line: Line number
        :param column: Column number
        """
        self.stream_name = stream_name
        self.line = line
        self.column = column

    def __str__(self) -> str:
        """Overridden string representation"""
        return f"{self.stream_name}:{self.line}:{self.column}"
