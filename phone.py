#!usr/bin/python3



import phonenumbers
ali = 9106710970
phone = phonenumbers.parse(f"+98{ali}")
print(phone)
valid = phonenumbers.is_valid_number(phone)
print(valid)