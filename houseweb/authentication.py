import passlib

from passlib.context import CryptContext

#
# create a single global instance for your app...
#
pwd_context = CryptContext(
    schemes=["pbkdf2_sha512"],

    # Automatically mark all but first hasher in list as deprecated.
    # (this will be the default in Passlib 2.0)
    deprecated="auto"
)

