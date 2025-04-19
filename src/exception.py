# src/exception.py

import sys

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self.get_error_message_detail(error_message, error_detail)

    def get_error_message_detail(self, error_message, error_detail):
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        return f"Error occurred in '{file_name}' at line {line_number}: {str(error_message)}"

    def __str__(self):
        return self.error_message
