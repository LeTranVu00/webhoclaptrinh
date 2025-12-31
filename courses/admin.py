from django.contrib import admin
from .models import Course, Lesson  # ← Import models từ app courses
from .models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'created_at', 'is_read', 'is_replied']
    list_filter = ['created_at', 'is_read', 'is_replied']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created_at']
    list_editable = ['is_read', 'is_replied']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Thông tin liên hệ', {
            'fields': ('name', 'email', 'phone', 'message')
        }),
        ('Trạng thái', {
            'fields': ('is_read', 'is_replied', 'created_at')
        }),
    )

from .models import Review
# Đăng ký model Review với admin
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['user__username', 'course__title', 'comment']
    readonly_fields = ['created_at']


from .models import ForumPost, PostLike, PostComment
# Đăng ký model ForumPost với admin
@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at', 'is_pinned', 'like_count']
    list_filter = ['created_at', 'is_pinned', 'author']
    search_fields = ['title', 'content', 'author__username']
    list_editable = ['is_pinned']
    
    def like_count(self, obj):
        return obj.postlike_set.count()
# Đăng ký model PostLike với admin
@admin.register(PostComment)
class PostCommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at', 'short_content']
    list_filter = ['created_at', 'author']
    search_fields = ['content', 'author__username', 'post__title']
    
    def short_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content


from .models import LearningPath, WeeklySchedule, DailyTask
# Đăng ký model LearningPath, WeeklySchedule, DailyTask với admin
class DailyTaskInline(admin.TabularInline):
    model = DailyTask
    extra = 1

class WeeklyScheduleInline(admin.TabularInline):
    model = WeeklySchedule
    extra = 1
    inlines = [DailyTaskInline]

@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    list_display = ['course', 'total_weeks', 'hours_per_week', 'difficulty']
    inlines = [WeeklyScheduleInline]
    list_filter = ['difficulty', 'total_weeks']

@admin.register(WeeklySchedule)
class WeeklyScheduleAdmin(admin.ModelAdmin):
    list_display = ['learning_path', 'week_number', 'title', 'total_hours']
    list_filter = ['learning_path']
    inlines = [DailyTaskInline]

@admin.register(DailyTask)
class DailyTaskAdmin(admin.ModelAdmin):
    list_display = ['weekly_schedule', 'day_number', 'title', 'duration_minutes', 'is_completed']
    list_filter = ['weekly_schedule', 'is_completed']
    list_editable = ['is_completed']


# Đăng ký model Course với admin
admin.site.register(Course)

# Đăng ký model Lesson với admin  
admin.site.register(Lesson)
