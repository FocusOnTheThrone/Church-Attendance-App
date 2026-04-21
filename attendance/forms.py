from django import forms

from .models import Person, Service, Attendance, Fellowship


class VisitorForm(forms.ModelForm):
    """Form for adding a visitor (title=Visitor, first_visit_date set in view)."""

    gender = forms.ChoiceField(
        choices=[("", "—")] + list(Person.GENDER_CHOICES),
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    class Meta:
        model = Person
        fields = ["full_name", "gender", "date_of_birth", "phone", "email", "notes"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name", "required": True}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Optional notes"}),
        }


class PersonForm(forms.ModelForm):
    """Form for adding a new person."""

    gender = forms.ChoiceField(
        choices=[("", "—")] + list(Person.GENDER_CHOICES),
        required=True,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    fellowship = forms.ModelChoiceField(
        queryset=Fellowship.objects.filter(is_active=True).order_by('name'),
        empty_label="—",
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )

    department = forms.ChoiceField(
        choices=[("", "—")] + list(Person.DEPARTMENT_CHOICES),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Department of Service"
    )

    class Meta:
        model = Person
        fields = [
            "full_name",
            "gender",
            "date_of_birth",
            "phone",
            "email",
            "title",
            "occupation",
            "fellowship",
            "department",
            "residence",
            "first_visit_date",
            "notes",
        ]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Full name"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
            "title": forms.Select(attrs={"class": "form-select"}),
            "occupation": forms.TextInput(attrs={"class": "form-control", "placeholder": "e.g. Teacher, Nurse"}),
            "residence": forms.TextInput(attrs={"class": "form-control", "placeholder": "Area / district"}),
            "first_visit_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Optional notes"}),
        }


class ServiceForm(forms.ModelForm):
    """Form for adding a new service."""

    class Meta:
        model = Service
        fields = [
            "date",
            "start_time",
            "service_type",
            "title",
            "location",
            "notes",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "start_time": forms.TimeInput(attrs={"class": "form-control", "type": "time"}),
            "service_type": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Optional title"}),
            "location": forms.TextInput(attrs={"class": "form-control", "placeholder": "Location"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Optional notes"}),
        }


class AttendanceForm(forms.ModelForm):
    """Form for recording attendance."""

    class Meta:
        model = Attendance
        fields = [
            "service",
            "person",
            "category",
            "present",
            "is_first_time_visitor",
            "is_healed_this_service",
            "notes",
        ]
        widgets = {
            "service": forms.Select(attrs={"class": "form-select"}),
            "person": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "present": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_first_time_visitor": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "is_healed_this_service": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Optional notes"}),
        }
