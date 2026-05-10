from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect

from .models import Review
from .forms import ReviewForm


def review_list(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request,'reviews/index.html',{'reviews': reviews})


@login_required
def review_create(request):

    if request.method == 'POST':
        form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            return redirect('reviews')

    else:
        form = ReviewForm()
    return render(request,'reviews/create.html',{'form': form})

