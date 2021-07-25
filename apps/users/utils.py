from apps.users.exceptions import BaseAPIException


class CheckPassword:
    SPECIAL_SYM = ['$', '@', '#', '%', '.']

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
            raise BaseAPIException('Passwords have to be equals.')

    def len(self):
        if len(self.password) < 8:
            raise BaseAPIException('Length should be at least 8.')
    
    def has_digit(self):
        if not any(char.isdigit() for char in self.password):
            raise BaseAPIException('Password should have at least one numeral')
    
    def has_uppercase(self):
        if not any(char.isupper() for char in self.password):
            raise BaseAPIException('Password should have at least one uppercase letter')
    
    def has_special_sym(self):
        if not any(char in self.SPECIAL_SYM for char in self.password):
            raise BaseAPIException(f'Password should have at least one of the symbols {self.SPECIAL_SYM}')
    
    def is_different(self):
        if self.password == self.repeat_password:
            raise BaseAPIException('Passwords have to be differents.')
