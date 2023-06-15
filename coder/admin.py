from django.contrib import admin

from .models import Coder
from .interface import Interface


@admin.register(Coder)
class CoderAdmin(admin.ModelAdmin):
    list_display = ("requirements", "tasks")

    change_form_template = 'admin/coder/change_form.html'

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request, obj=None):
        return request.user.is_staff

    def render_change_form(self, request, context, *args, **kwargs):
        coder = kwargs.get('obj')
        context['adminform'].form.instance = coder
        messages = Interface(coder.id).messages
        context['coder_messages'] = list(map(lambda x: x.message_content, messages[1:]))
        return super(CoderAdmin, self).render_change_form(request, context, *args, **kwargs)
