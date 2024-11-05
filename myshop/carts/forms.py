from django import forms

PRODUCT_QUANTITY_CHOICES = [(num, str(num)) for num in range(1, 21)]

class CartAddProductForm(forms.Form):
    qunatity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES,
                                      coerce=int)
    
    override = forms.BooleanField(required=False,
                                  initial=False,
                                  widget=forms.HiddenInput)
