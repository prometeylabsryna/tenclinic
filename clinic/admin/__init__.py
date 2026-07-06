from django.contrib import admin

from clinic.admin.crm import AppointmentAdmin, DirectionAdmin, DoctorAdmin, ServiceAdmin, WorkingHoursAdmin
from clinic.admin.site_content import register_site_content_section_admins
from clinic.admin.site_settings import SiteSettingsAdmin
from clinic.models import Appointment, Direction, Doctor, Service, SiteSettings, WorkingHours

admin.site.register(SiteSettings, SiteSettingsAdmin)
admin.site.register(Direction, DirectionAdmin)
admin.site.register(Doctor, DoctorAdmin)
admin.site.register(Service, ServiceAdmin)
admin.site.register(WorkingHours, WorkingHoursAdmin)
admin.site.register(Appointment, AppointmentAdmin)

register_site_content_section_admins()
