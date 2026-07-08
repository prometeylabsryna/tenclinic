from django.contrib import admin

from clinic.admin.crm import (
    AppointmentAdmin,
    CatalogServiceAdmin,
    DirectionAdmin,
    DoctorAdmin,
    HearingAidAdmin,
    PriceListItemAdmin,
    ServiceAutocompleteAdmin,
    ServiceAdmin,
    WorkingHoursAdmin,
)
from clinic.admin.site_content import register_site_content_section_admins
from clinic.admin.site_settings import SiteSettingsAdmin
from clinic.models import (
    Appointment,
    CatalogService,
    Direction,
    Doctor,
    HearingAid,
    PriceListItem,
    Service,
    SiteSettings,
    WorkingHours,
)

admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(Direction, DirectionAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(HearingAid, HearingAidAdmin)
admin.site.register(Service, ServiceAutocompleteAdmin)
admin.site.register(CatalogService, CatalogServiceAdmin)
admin.site.register(PriceListItem, PriceListItemAdmin)
admin.site.register(WorkingHours, WorkingHoursAdmin)
admin.site.register(Appointment, AppointmentAdmin)

register_site_content_section_admins()
