from apps.users.constants import CheckPasswordCts as cts
from apps.users.exceptions import BaseAPIException


class CheckPassword:

    def __init__(self, password, repeat_password=None):
        self.password = password
        self.repeat_password = repeat_password

    def all_validations(self):
        self.is_equal()
        self.len()
        self.has_digit()
        self.has_uppercase()
        self.has_special_sym()

    def is_equal(self):
        if self.password != self.repeat_password:
            raise BaseAPIException(cts.EQUALS)

    def len(self):
        if len(self.password) < 8:
            raise BaseAPIException(cts.LEN)
    
    def has_digit(self):
        if not any(char.isdigit() for char in self.password):
            raise BaseAPIException(cts.HAS_DIGIT)
    
    def has_uppercase(self):
        if not any(char.isupper() for char in self.password):
            raise BaseAPIException(cts.HAS_UPPERCASE)
    
    def has_special_sym(self):
        if not any(char in cts.SPECIAL_SYM for char in self.password):
            raise BaseAPIException(cts.HAS_SPECIAL_SYM.format(sym=cts.SPECIAL_SYM))
    
    def is_different(self):
        if self.password == self.repeat_password:
            raise BaseAPIException(cts.IS_DIFFERENT)
