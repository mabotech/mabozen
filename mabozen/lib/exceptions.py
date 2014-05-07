# -*- coding: utf-8 -*-

"""Exceptions"""

class MTPError(Exception):
    """Base MTP exception"""
    
    def __init__( self, msg ):
        Exception.__init__( self, msg )
        
class BadCommand(MTPError):
    """Raised when bad command"""
    
    def __init__( self, msg ):
        MTPError.__init__( self, msg )
        

class PgError(MTPError):
    """Raised when PostgreSQL returns error"""