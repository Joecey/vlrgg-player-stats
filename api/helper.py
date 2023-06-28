"""
Helper functions for text post processing
"""

class HelperFunctions:
    # post processing to remove all special characters (if needed)
    def remove_special(text):
        return ''.join(e for e in text if e.isalnum())
    
    # remove special sequences
    def remove_esc_seq(text):
        escapes = ''.join([chr(char) for char in range(1, 32)])
        translator = str.maketrans('', '', escapes)
        return text.translate(translator)

    # remove empty space after string (allows you to keep spaces in words)
    def remove_last(text):
        final = text[:-1]
        return final