from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import FlaggedContent, Dispute, Notification, StudyMaterial, BlockedUser
from rest_framework import serializers


# Simple serializers for safety features
class FlaggedContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FlaggedContent
        fields = ['id', 'content_type', 'content_id', 'reason', 'description', 'status', 'created_at']
        read_only_fields = ['id', 'status', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'notification_type', 'title', 'message', 'reference_id', 
                  'reference_type', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']


class StudyMaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyMaterial
        fields = ['id', 'title', 'description', 'course_code', 'course_name', 
                  'material_type', 'file_url', 'download_count', 'rating', 
                  'is_approved', 'created_at']
        read_only_fields = ['id', 'download_count', 'rating', 'is_approved', 'created_at']


class FlaggedContentViewSet(viewsets.ModelViewSet):
    """ViewSet for flagged content"""
    serializer_class = FlaggedContentSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return FlaggedContent.objects.filter(reporter=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for notifications"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark notification as read"""
        notification = self.get_object()
        notification.mark_as_read()
        return Response({'status': 'Notification marked as read'})
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read"""
        self.get_queryset().filter(is_read=False).update(is_read=True)
        return Response({'status': 'All notifications marked as read'})
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get unread notification count"""
        count = self.get_queryset().filter(is_read=False).count()
        return Response({'unread_count': count})


class StudyMaterialViewSet(viewsets.ModelViewSet):
    """ViewSet for study materials"""
    serializer_class = StudyMaterialSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = StudyMaterial.objects.filter(is_approved=True)
        
        course_code = self.request.query_params.get('course_code')
        if course_code:
            queryset = queryset.filter(course_code__icontains=course_code)
        
        material_type = self.request.query_params.get('material_type')
        if material_type:
            queryset = queryset.filter(material_type=material_type)
        
        return queryset.order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(
            uploader=self.request.user,
            campus=self.request.user.campus
        )
    
    @action(detail=True, methods=['post'])
    def download(self, request, pk=None):
        """Track download"""
        material = self.get_object()
        material.increment_download_count()
        return Response({'status': 'Download tracked'})