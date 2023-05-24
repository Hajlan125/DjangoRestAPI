import json
from datetime import datetime,timezone

from rest_framework import serializers

from main.models import User, Answer, Question, Test, TestingSystem, UserType, QuestionType, TestType, ParallelBlock


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
        fields = ('type_u_id', 'type_user', 'access_level')


class QuestionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionType
        fields = ('type_q_id', 'type_q')

class TestingSystemSerializer(serializers.ModelSerializer):
    ts_start_time = serializers.DateTimeField(required=False, default=datetime.now(timezone.utc).astimezone())
    ts_end_time = serializers.DateTimeField(required=False, default=datetime.now(timezone.utc).astimezone())
    class Meta:
        model = TestingSystem
        fields = ('ts_id', 'ts_user_id', 'ts_test_id',
                  'ts_start_time', 'ts_end_time',
                  'ts_score_percent')

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('answ_id', 'answ_text',
                  'answ_question_id', 'is_correct', 'answ_comparison_text')

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ('q_id', 'q_title', 'q_test_id', 'q_parent_id', 'q_type',
                  'q_exact_match', 'q_parallel_block_id')
class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data
class QuestionExpandSerializer(serializers.ModelSerializer):
    # answers = AnswerSerializer(many=True,read_only=True)
    children = RecursiveField(many=True, read_only=True, allow_null=True)
    class Meta:
        model = Question
        fields = ['q_id', 'q_title', 'q_test_id','q_parent_id',
                  'q_type', 'q_exact_match', 'q_parallel_block_id', 'children']
class QuestionPassingSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ['q_id', 'q_title', 'q_test_id','q_parent_id',
                  'q_type', 'q_exact_match', 'q_parallel_block_id', 'answers']


class TestSerializer(serializers.ModelSerializer):
    test_create_date = serializers.DateTimeField(required=False,
                                                 default=datetime.now(timezone.utc).astimezone())
    class Meta:
        model = Test
        fields = ['test_id', 'test_creator',
                  'test_name', 'test_create_date',
                  'test_subject','test_learning_material', 'test_type', 'test_random_sort']
class TestExpandSerializer(serializers.ModelSerializer):
    test_create_date = serializers.DateTimeField(required=False,
                                                 default=datetime.now(timezone.utc).astimezone())
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Test
        fields = ['test_id', 'test_creator',
                  'test_name', 'test_create_date', 'test_random_sort', 'questions']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['user_id', 'user_name', 'user_type', 'login', 'password']


class UserAuthSerializer(serializers.ModelSerializer):
    level = serializers.IntegerField(source='user_type.access_level')

    class Meta:
        model = User
        fields = ['user_id', 'user_name', 'user_type', 'level', 'login', 'password']

class UserExpandSerializer(serializers.ModelSerializer):
    created_tests = TestSerializer(many=True, read_only=True)
    passed_tests = TestingSystemSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ['user_id', 'user_name', 'user_type', 'login', 'password',
                  'create_test_permission', 'created_tests', 'passed_tests']


class TestTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestType
        fields = ['type_t_id', 'type_test']


class ParallelBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParallelBlock
        fields = ['p_b_id', 'p_b_name', 'p_b_test_id']