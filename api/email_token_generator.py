from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class EmailTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user['email']) + text_type(timestamp)
        )
email_verify_token = EmailTokenGenerator()