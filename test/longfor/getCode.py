import pyotp

totp = pyotp.TOTP("X5NRCWHXTUJMHDIGRZKGE7YM77EXDGVU")
print(totp.now())
