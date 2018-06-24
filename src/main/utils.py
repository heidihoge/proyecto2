from django import forms

class CurrencyIntegerField(forms.IntegerField):
    def to_python(self, value):
        return super(CurrencyIntegerField, self).to_python(clean_stringnumber(value))

def clean_stringnumber(number):
    if type(number) == str:
        return int(number.replace('.','').replace('₲', '').strip())
    return number