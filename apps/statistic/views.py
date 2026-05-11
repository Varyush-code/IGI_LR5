from statistics import median
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Sum, Count
from django.views.generic import TemplateView
import json
from apps.accounts.models import Profile
from apps.animals.models import Animal
from apps.feeding.models import Feeding
from apps.tickets.models import Ticket

class StatisticsView(LoginRequiredMixin, TemplateView):

    template_name = 'statistic.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        visitors = (
            Profile.objects
            .filter(role='visitor')
            .select_related('user')
            .order_by('user__username')
        )
        sort = self.request.GET.get('sort')

        if sort:
            allowed_sort = [
                'user__username',
                '-user__username',
                'age',
                '-age',
            ]
            if sort in allowed_sort:
                visitors = visitors.order_by(sort)

        context['visitors'] = visitors
        context['average_age'] = (
            visitors.aggregate(
                avg=Avg('age')
            )['avg']
        )
        ages = [
            visitor.age
            for visitor in visitors
            if visitor.age is not None
        ]
        context['median_age'] = (
            median(ages)
            if ages else 0
        )

        animals = Animal.objects.all()
        search = self.request.GET.get('search')
        if search:
            animals = animals.filter(
                name__icontains=search
            )
        family = self.request.GET.get('family')
        if family:
            animals = animals.filter(
                family__icontains=family
            )
        arrival_date = self.request.GET.get(
            'arrival_date'
        )
        if arrival_date:
            animals = animals.filter(arrival_date=arrival_date)
        context['animals'] = animals
        context['animals_count'] = animals.count()
        feedings = Feeding.objects.all()
        food_type = self.request.GET.get(
            'food_type'
        )
        if food_type:
            feedings = feedings.filter(
                food__food_type=food_type
            )
        context['feedings'] = feedings
        context['food_total'] = (
            feedings.aggregate(
                total=Sum('amount')
            )['total']
        )

        tickets = Ticket.objects.all()
        context['tickets_count'] = (
            tickets.count()
        )
        context['average_ticket_price'] = (
            tickets.aggregate(
                avg=Avg('final_price')
            )['avg']
        )

        prices = [
            float(ticket.final_price)
            for ticket in tickets
            if ticket.final_price is not None
        ]

        context['median_ticket_price'] = (
            median(prices)
            if prices else 0
        )

        family_stats = (
            Animal.objects
            .values('family')
            .annotate(total=Count('id'))
            .order_by('family')
        )

        context['family_labels'] = json.dumps([
            item['family']
            for item in family_stats
        ])

        context['family_counts'] = json.dumps([
            item['total']
            for item in family_stats
        ])

        food_stats = (
            Feeding.objects
            .values('food__food_type')
            .annotate(total=Sum('amount'))
        )

        context['food_labels'] = json.dumps([
            item['food__food_type']
            for item in food_stats
        ])

        context['food_amounts'] = json.dumps([
            item['total']
            for item in food_stats
        ])

        return context