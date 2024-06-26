from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six  

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )

# Create separate instances of the custom token generator
account_activation_token = TokenGenerator()
reset_password_token = TokenGenerator()