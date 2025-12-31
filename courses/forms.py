from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} sao') for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={
                'placeholder': 'Chia sẻ trải nghiệm của bạn về khóa học này...',
                'rows': 4,
                'class': 'form-textarea'
            })
        }
        labels = {
            'rating': 'Đánh giá',
            'comment': 'Bình luận'
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].widget.attrs.update({'class': 'star-rating'})