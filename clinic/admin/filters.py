from django.contrib import admin


class HasPriceFilter(admin.SimpleListFilter):
    title = 'Ціна'
    parameter_name = 'has_price'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'З ціною'),
            ('no', 'Без ціни'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.filter(price__isnull=False)
        if self.value() == 'no':
            return queryset.filter(price__isnull=True)
        return queryset
