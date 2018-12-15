"""
    @author         :  Rishabh Dalal
    @description    :  Error object for language Flair
    @since          : 31 Aug. 2018
 
"""

class LexicalError(ValueError):
    pass

class ParseError(ValueError):
    pass

class SemanticError(ValueError):
    pass
class FileNotFound(ValueError):
    pass
