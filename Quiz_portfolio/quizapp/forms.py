from django import forms
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.core.cache import cache

from .models import Quiz, Choices

# class CartUpdateForm(forms.ModelForm):
#     quantity = forms.IntegerField(label='数量', min_value=1)
#     id = forms.CharField(widget=forms.HiddenInput())

#     class Meta:
#         model = CartItems
#         fields = ['quantity', 'id']
    
#     def clean(self):
#         cleaned_data = super().clean()
#         quantity = cleaned_data.get('quantity')
#         id = cleaned_data.get('id')
#         cart_item = get_object_or_404(CartItems, pk=id)
#         if quantity > cart_item.product.stock:
#             raise ValidationError(f'在庫数を超えています。{cart_item.product.stock}以下にしてください')


class MakeQuizForm(forms.ModelForm):
    title = forms.CharField(label='タイトル', max_length=20)
    sentence = forms.CharField(label='問題文', max_length=100, widget=forms.Textarea)

    class Meta:
        model = Quiz
        fields = ['title', 'sentence', ]
    
    def save(self):
        quiz = super().save(commit=False)
        quiz.created_by = self.user
        quiz.save()
        return quiz
    
    
class EditQuizForm(forms.ModelForm):
    title = forms.CharField(label='タイトル', max_length=20)
    sentence = forms.CharField(label='問題文', max_length=100, widget=forms.Textarea)

    class Meta:
        model = Quiz
        fields = ['title', 'sentence', ]


class MakeChoiceForm(forms.ModelForm):
    description = forms.CharField(label='解説', widget=forms.Textarea)

    class Meta:
        model = Choices
        fields = ['sentence', 'is_correct', 'description',]
        labels = {
            'sentence':'選択肢',
            'is_correct':'正誤',
        }
        
    

    # def save(self):
    #     address = super().save(commit=False)
    #     address.user = self.user
    #     try:
    #         address.validate_unique()
    #         address.save()
    #     except ValidationError as e:
    #         address = get_object_or_404(
    #             Addresses, 
    #             user = self.user,
    #             prefecture = address.prefecture,
    #             zip_code = address.zip_code,
    #             address = address.address
    #         )
    #     cache.set(f'address_user_{self.user.id}', address)
    #     return address
