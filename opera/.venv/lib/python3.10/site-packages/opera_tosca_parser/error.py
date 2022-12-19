from opera_tosca_parser.parser.utils.location import Location


class OperaToscaParserError(Exception):
    """Base TOSCA parser exception for catch-all-opera-tosca-parser-errors constructs."""


class ParseError(OperaToscaParserError):
    """Exception that is raised on invalid TOSCA document."""

    def __init__(self, msg: str, loc: Location):
        """
        Construct ParseError object
        :param msg: Error message
        :param loc: Location of the error in TOSCA template
        """
        super().__init__(msg)
        self.loc = loc


class DataError(OperaToscaParserError):
    """Exception that is raised on data errors that occur at runtime."""


class ToscaDeviationError(OperaToscaParserError):
    """Raised when something is compatible with TOSCA standard, but not acceptable for the orchestrator."""
