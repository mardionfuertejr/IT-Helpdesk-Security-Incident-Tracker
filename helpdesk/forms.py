from django import forms
from .models import Ticket

class TicketSubmissionForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'ticket_type', 'priority']

    def clean(self):
        cleaned_data = super().clean()
        ticket_type = cleaned_data.get('ticket_type')
        priority = cleaned_data.get('priority')

        if ticket_type == 'Security Incident' and priority == 'Low':
            self.add_error('priority', "Priority cannot be 'Low' for a Security Incident.")

        return cleaned_data
