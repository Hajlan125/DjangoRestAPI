from django.contrib import admin
from main.models import User, Answer, Question, Test, TestingSystem, UserType, QuestionType, TestType
# Register your models here.

admin.site.register(User)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(Test)
admin.site.register(TestingSystem)
admin.site.register(UserType)
admin.site.register(QuestionType)
admin.site.register(TestType)