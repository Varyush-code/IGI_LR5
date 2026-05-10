from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import redirect

from .forms import TicketForm
from .models import PromoCode

def ticket_home(request):

    promocodes = PromoCode.objects.filter(
        active=True
    )

    return render(
        request,'tickets/index.html',{'promocodes': promocodes}
    )

@login_required
def my_tickets(request):

    tickets = request.user.tickets.all()
    return render(request,'tickets/my.html',{'tickets': tickets}
    )

@login_required
def ticket_create(request):

    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            price = 20

            if ticket.day_type == 'weekend':
                price = 30

            if ticket.feeding_show:
                price += 10

            if ticket.active_hours:
                price += 15

            promocode = form.cleaned_data.get('promocode')

            if promocode:
                price = price - (
                    price * promocode.discount_percent / 100
                )

            ticket.final_price = price
            ticket.save()
            return redirect('tickets')

    else:
        form = TicketForm()

    return render(
        request,'tickets/create.html',{'form': form}
    )