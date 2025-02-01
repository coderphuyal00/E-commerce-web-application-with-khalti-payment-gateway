from django import forms
from .models import Category,Size,Product,ProductVariant,ProductImage
class AddCategoryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set form title dynamically
        self.form_title = "Category"
    class Meta:
        model=Category
        fields='__all__'
        # exclude=['added_on']

class AddSizeForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.form_title="Size"
    class Meta:
        model=Size
        fields='__all__'
        # exclude=['added_on']

class AddProductForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.form_title="Product"
    class Meta:
        model=Product
        form_title="Product"
        fields='__all__'
        # exclude=['added_on']

class AddProductVariantForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.form_title="Product Variant"
    class Meta:
        model=ProductVariant
        form_title="Product Variant"
        fields='__all__'
        # exclude=['added_on']
class AddProductImageForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.form_title="Product Image"
    class Meta:
        model=ProductImage
        form_title="Product Image"
        fields='__all__'
        # exclude=['added_on']