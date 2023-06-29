from django.contrib import admin

from .models import Coder, CoderMessage
from .interface import Interface


@admin.register(Coder)
class CoderAdmin(admin.ModelAdmin):
    list_display = ("requirements", "tasks", "user")

    change_form_template = 'admin/coder/change_form.html'

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def get_queryset(self, request):
        qs = super(CoderAdmin, self).get_queryset(request)

        return qs.order_by('-created_at')

    def render_change_form(self, request, context, *args, **kwargs):
        coder = kwargs.get('obj')
        context['adminform'].form.instance = coder
        coder_messages = CoderMessage.objects.filter(coder=coder).order_by("created_at")
        context['coder_messages'] = list(coder_messages.values())
        return super(CoderAdmin, self).render_change_form(request, context, *args, **kwargs)
