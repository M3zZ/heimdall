# -*- coding: utf-8 -*-

"""
Global Heimdall exception and warning classes.
"""


class RuleError(Exception):
    """ Heimdall base class for Rule exceptions."""
    pass


class RuleDoesNotExist(RuleError):
    """ Raised when Rule object doesn't exists.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error
    """

    def __init__(self, message):
        self.help = '\nUse heimdall get rule --type type_name for show all rules from a type'
        self.code = 21
        super(RuleError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class RuleAlreadyExist(RuleError):
    """ Raised when rule object already exists.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nUse heimdall get rule --type type_name for show all rules from a type'
        self.code = 22
        super(RuleError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class RuleDataError(RuleError):
    """ Raised when audit command/script are not a list.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message, type):
        self.help = '\nRule attributes audit or remed must be a list.\nPlease check yml file %s' % type
        self.code = 23
        super(RuleError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class TypeError(Exception):
    """ Heimdall base class for Type exceptions."""
    pass


class TypeDoesNotExist(TypeError):
    """ Raised when Type object doesn't exists.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nUse heimdall get type --type type_name for show all type availables'
        self.code = 31
        super(TypeError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class TypeAlreadyExist(TypeError):
    """ Raised when Type object already exists.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nUse heimdall get Type --type type_name for show all Types from a type'
        self.code = 32
        super(TypeError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class TypeInstanceError(TypeError):
    """ Raised when Type instance is expected but other type is passed.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nMust be a type object passed in parameters'
        self.code = 33
        super(TypeError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class ScriptError(Exception):
    """ Heimdall base class for Scripts errors."""
    pass


class ScriptDoesNotExist(ScriptError):
    """ Raised when a script doesn't exists.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nUse heimdall get script for show all script availables'
        self.code = 61
        super(ScriptError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class ScriptAlreadyExist(ScriptError):
    """ Raised when a script already exist.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nUse heimdall get script for show all script availables'
        self.code = 62
        super(ScriptError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class ScriptTypeError(ScriptError):
    """ Raised when a script is not a .sh file.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nUse heimdall add script for add properly a new script'
        self.code = 63
        super(ScriptError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class ArgumentsError(Exception):
    """
        Heimdall base class for arguments error
    """
    pass


class RuleArgumentsError(ArgumentsError):
    """ Raised when arguments for rule actions are not valid.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nUse heimdall --help for more information'
        self.code = 41
        super(ArgumentsError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class HostArgumentsError(ArgumentsError):
    """ Raised when arguments for host actions are not valid.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nUse heimdall --help for more information'
        self.code = 42
        super(ArgumentsError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class ProfileError(Exception):
    """
      Base exception class for all profile errors.
    """


class ProfileTypeError(ProfileError):
    """ Raised when profile instance is expected but other type is passed.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nArguments passed must be a Profile Object.'
        self.code = 81
        super(ProfileError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class ProfileDoesNotExist(ProfileError):
    """ Raised when data is not a plateform object.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nUse heimdall get profile --profile profile_name for show all profile available.'
        self.code = 81
        super(ProfileError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class HostError(Exception):
    """ Base exception class for all host errors """
    pass


class HostDoesNotExist(HostError):
    """ Raised when Host object doesn't exists.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nUse heimdall get host --name host_name for show all hosts from a plateform'
        self.code = 10
        super(HostError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class HostAlreadyExist(HostError):
    """ Raised when Host object already exists.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nUse heimdall get host --name host_name for show all hosts from a plateform'
        self.code = 11
        super(HostError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class PlateformError(Exception):
    """ Base expection class for Plateform errors."""
    pass


class PlateformDoesNotExist(PlateformError):
    """ Raised when Plateform object doesn't exists.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message, plateform):
        self.help = '\nUse heimdall get plateform --plateform %s for show all plateforms' % plateform
        self.code = 51
        super(PlateformError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class PlateformAlreadyExist(PlateformError):
    """ Raised when plateform object already exists.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message, plateform):
        self.help = '\nUse heimdall get plateform --plateform %s for show all plateforms' % plateform
        self.code = 52
        super(PlateformError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class PlateformTypeError(PlateformError):
    """ Raised when plateform instance is expected but other type is passed.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message):
        self.help = '\nArguments passed must be a Plateform Object.'
        self.code = 53
        super(PlateformError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class EnvironmentDoesNotExist(PlateformError):
    """ Raised when Environment object doesn't exists.
    Attributes:
        message -- explanation of the error
        code -- code id for the error
        help -- help for avoid this error

        :return: Human readable string describing the error.
        :rtype: str
    """

    def __init__(self, message, plateform):
        self.help = '\nUse heimdall get plateform --plateform %s for show all environments' % plateform
        self.code = 54
        super(PlateformError, self).__init__(message)

    def __str__(self):
        return '<%s>: %s%s' % (self.__class__.__name__, self.message, self.help)


class AuditError(Exception):
    """ Base exception class for all audit errors."""
    pass


class FabricCommandError(AuditError):
    """ Raise when a fabric function Failed. """

    def __init__(self, message, fabric_func):
        self.fabric_func = fabric_func
        self.help = 'Check %s in heimdall/core/commands.' % self.fabric_func
        self.code = 70
        super(FabricCommandError, self).__init__(message, fabric_func)

    def __str__(self):
        return '<%s>: %s%s\n<Fabric Function Error>: %s' % (
            self.__class__.__name__, self.message, self.help, self.fabric_func)
