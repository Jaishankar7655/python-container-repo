from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'genre', 'publication_date', 'pages', 'available']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '13-digit ISBN'}),
            'genre': forms.Select(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'pages': forms.NumberInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if isbn and len(isbn) != 13:
            raise forms.ValidationError('ISBN must be exactly 13 digits.')
        return isbn