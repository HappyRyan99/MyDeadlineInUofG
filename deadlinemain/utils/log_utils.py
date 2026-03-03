class LogUtils:
    DEBUG = True  # Global switch to enable/disable logging

    @staticmethod
    def d(TAG: str, context: str):
        """
        Prints debug information if DEBUG is True.
        
        Args:
            TAG (str): The tag identifying the source of the log.
            context (str): The message or context to log.
        """
        if LogUtils.DEBUG:
            print(f"[{TAG}] {context}")
