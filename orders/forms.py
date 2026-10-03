from django import forms

from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "quantity",
            "full_name",
            "phone_number",
            "address",
            "city",
            "state",
            "pincode",
        ]
        widgets = {
            "address": forms.Textarea(
                attrs={"placeholder": "Street address, area, landmark"}
            ),
            "phone_number": forms.TextInput(
                attrs={"placeholder": "Enter contact number"}
            ),
            "pincode": forms.TextInput(attrs={"placeholder": "Postal code"}),
        }


class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
