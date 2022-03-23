import json
from datetime import datetime,timezone

from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from main.models import User, Answer, Question, Score, Test, TestingSystem

class TestingSystemSerializer(serializers.ModelSerializer):
    ts_start_time = serializers.DateTimeField(required=False, default=datetime.now(timezone.utc).astimezone())
    ts_end_time = serializers.DateTimeField(required=False, default=datetime.now(timezone.utc).astimezone())
    class Meta:
        model = TestingSystem
        fields = ('ts_id', 'ts_user_id', 'ts_test_id',
                  'ts_start_time', 'ts_end_time',
                  'ts_count_right_answers', 'ts_score_id')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('answ_id', 'answ_text',
                  'answ_question_id', 'is_correct')

class QuestionSerializer(serializers.ModelSerializer):
    q_chance = serializers.IntegerField(required=False, default=100)
    class Meta:
        model = Question
        fields = ('q_id', 'q_title', 'q_test_id', 'q_parent_id', 'q_chance')
class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
class QuestionExpandSerializer(serializers.ModelSerializer):
    q_chance = serializers.IntegerField(required=False,default=100)
    answers = AnswerSerializer(many=True,read_only=True)
    children = RecursiveField(many=True, read_only=True, allow_null=True)
    class Meta:
        model = Question
        fields = ['q_id', 'q_title', 'q_test_id','q_parent_id', 'q_chance', 'answers','children']
class QuestionPassingSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['q_id', 'q_title', 'q_test_id','q_parent_id', 'q_chance', 'answers']

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ('score_id', 'score_text')

class TestSerializer(serializers.ModelSerializer):
    test_create_date = serializers.DateTimeField(required=False,
                                                 default=datetime.now(timezone.utc).astimezone())
    class Meta:
        model = Test
        fields = ['test_id', 'test_creator',
                  'test_name', 'test_create_date',
                  'test_subject', 'is_tree']
class TestExpandSerializer(serializers.ModelSerializer):
    test_create_date = serializers.DateTimeField(required=False,
                                                 default=datetime.now(timezone.utc).astimezone())
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Test
        fields = ['test_id', 'test_creator',
                  'test_name', 'test_create_date', 'questions']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'user_name', 'user_type', 'login', 'password', 'create_test_permission']
class UserExpandSerializer(serializers.ModelSerializer):
    created_tests = TestSerializer(many=True, read_only=True)
    passed_tests = TestingSystemSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['user_id', 'user_name', 'user_type', 'login', 'password',
                  'create_test_permission', 'created_tests', 'passed_tests']



