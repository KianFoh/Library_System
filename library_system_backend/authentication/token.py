from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six  

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Generate a hash value for the activation token based on user's primary key,
        # timestamp, and user's active status.
        # This hash value is used to generate the activation token.
        return (
            six.text_type(user.pk) + six.text_type(timestamp)  + six.text_type(user.is_active)
        )

# Create an instance of the custom token generator for account activation
account_activation_token = AccountActivationTokenGenerator()