from django import forms
from django.contrib.admin.widgets import AdminTextInputWidget, AdminTextareaWidget

_EXTRA_CLASSES = ('site-content-editor__control',)


def cms_control_classes(base_classes):
    classes = list(base_classes or [])
    for css_class in _EXTRA_CLASSES:
        if css_class not in classes:
            classes.append(css_class)
    return classes


class CmsAdminTextInputWidget(AdminTextInputWidget):
    def __init__(self, attrs=None):
        attrs = dict(attrs or {})
        attrs['class'] = ' '.join(cms_control_classes(attrs.get('class', '').split()))
        super().__init__(attrs)


class CmsAdminTextareaWidget(AdminTextareaWidget):
    def __init__(self, attrs=None):
        attrs = dict(attrs or {})
        attrs['class'] = ' '.join(cms_control_classes(attrs.get('class', '').split()))
        super().__init__(attrs)


def apply_readable_widget(formfield):
    if formfield is None:
        return formfield
    widget = formfield.widget
    if isinstance(widget, (forms.CheckboxInput, forms.Select, forms.FileInput)):
        return formfield
    if isinstance(widget, AdminTextareaWidget):
        formfield.widget = CmsAdminTextareaWidget(attrs=widget.attrs)
    elif isinstance(widget, AdminTextInputWidget):
        formfield.widget = CmsAdminTextInputWidget(attrs=widget.attrs)
    return formfield
