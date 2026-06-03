from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Ticket, TicketLog
from .serializers import TicketSerializer, LegacyTicketSerializer
import logging

audit_logger = logging.getLogger('ticket_audit')

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'manager' or request.user.is_superuser)

class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = LegacyTicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'manager' or user.is_superuser:
            return Ticket.objects.all()
        return Ticket.objects.filter(created_by=user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsManager()]
        return super().get_permissions()


class APITicketListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role == 'manager' or request.user.is_superuser:
            tickets = Ticket.objects.all()
        else:
            tickets = Ticket.objects.filter(created_by=request.user)
        serializer = TicketSerializer(tickets, many=True)
        return Response(serializer.data)


class APITicketCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        title = request.data.get('title')
        description = request.data.get('description')
        ticket_type = request.data.get('ticket_type')
        priority = request.data.get('priority')

        if not all([title, description, ticket_type, priority]):
            return Response({"error": "All fields (title, description, ticket_type, priority) are required."}, status=status.HTTP_400_BAD_REQUEST)

        if ticket_type == 'Security Incident' and priority == 'Low':
            return Response({"error": "Priority cannot be 'Low' for a Security Incident."}, status=status.HTTP_400_BAD_REQUEST)

        ticket = Ticket.objects.create(
            title=title,
            description=description,
            ticket_type=ticket_type,
            priority=priority,
            nist_stage='detection',
            created_by=request.user
        )

        # Database audit log
        TicketLog.objects.create(
            ticket=ticket,
            changed_by=request.user,
            change_description="Ticket created via JWT API."
        )

        # File-based audit log
        audit_logger.info("", extra={
            'user': request.user.email,
            'action': 'API_CREATE',
            'id': ticket.id,
            'detail': f"Ticket created via JWT API. Type: {ticket_type}, Priority: {priority}"
        })

        return Response({
            "ticket_id": ticket.id,
            "title": ticket.title,
            "nist_stage": ticket.nist_stage,
            "created_at": ticket.created_at
        }, status=status.HTTP_201_CREATED)
