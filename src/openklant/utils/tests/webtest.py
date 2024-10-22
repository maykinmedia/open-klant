from webtest import forms


def add_dynamic_field(form: forms.Form, name: str, value: str) -> None:
    """
    Helper to add fields to a webtest form that is typically done in JS otherwise.
    """
    field = forms.Text(form, "input", name, pos=999, value=value)
    form.fields[name] = [field]
    form.field_order.append((name, field))
