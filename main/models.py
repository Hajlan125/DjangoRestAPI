from django.db import models
from mptt.models import MPTTModel


class ParallelBlock(models.Model):
    p_b_id = models.BigAutoField(primary_key=True)
    p_b_name = models.TextField(
        default='Parallel Block',
        db_column='p_b_name'
    )
    p_b_test_id = models.ForeignKey(
        to="Test",
        on_delete=models.CASCADE,
        db_column="p_b_test_id"
    )
    class Meta:
        managed=False
        db_table='parallel_block'


class UserType(models.Model):
    type_u_id = models.BigAutoField(primary_key=True)
    type_user = models.TextField(
        db_column="type_user",
        verbose_name="Тип пользователя"
    )
    access_level = models.IntegerField(
        db_column="access_level",
        verbose_name="Уровень доступа"
    )
    class Meta:
        managed=False
        db_table = 'type_u'


class TestType(models.Model):
    type_t_id = models.BigAutoField(primary_key=True)
    type_test = models.TextField(
        db_column='type_test',
        verbose_name='Тип теста'
    )
    class Meta:
        managed = False
        db_table = 'type_test'


class QuestionType(models.Model):
    type_q_id = models.BigAutoField(primary_key=True)
    type_q = models.TextField(
        db_column="type_q",
        verbose_name="Тип вопроса"
    )
    class Meta:
        managed=False
        db_table = 'type_q'


class User(models.Model):
    user_id = models.BigAutoField(primary_key=True)
    user_name = models.TextField(
        db_column="user_name",
        verbose_name="Имя")
    login = models.TextField(
        db_column="login",
        verbose_name="Логин")
    password = models.TextField(
        db_column="password",
        verbose_name="Пароль")
    user_type = models.ForeignKey(
        related_name="user_type",
        to="UserType",
        default=2,
        on_delete=models.SET_DEFAULT,
        db_column="user_type"
    )

    class Meta:
        managed = False
        db_table = "user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Answer(models.Model):
    answ_id  = models.BigAutoField(primary_key = True)

    answ_text = models.TextField(
        db_column="answ_text",
        verbose_name="Вопрос"
    )
    answ_question_id = models.ForeignKey(
        related_name="answers",
        to='Question',
        on_delete=models.CASCADE,
        db_column="answ_question_id"
    )
    is_correct = models.BooleanField(
        db_column="is_correct"
    )
    answ_comparison_text = models.TextField(
        db_column='answ_comparison_text',
        default=None,
        null=True
    )
    class Meta:
        managed = False
        db_table = 'answer'


class Question(models.Model):
    q_id = models.BigAutoField(primary_key = True)

    q_title = models.TextField(
        db_column="q_title",
        verbose_name="Вопрос"
    )
    q_test_id =  models.ForeignKey(
        related_name="questions",
        to='Test',
        on_delete=models.CASCADE,
        db_column='q_test_id'
    )
    q_parent_id = models.ForeignKey(
        to='self',
        related_name="children",
        null=models.SET_DEFAULT,
        blank=True,
        default=0,
        db_column="q_parent_id",
        on_delete=models.CASCADE,
        verbose_name="Предыдущий вопрос"
    )
    q_exact_match = models.BooleanField(
        default=None,
        null=True,
        db_column='q_exact_match'
    )
    q_type = models.ForeignKey(
        to='QuestionType',
        default=1,
        db_column='q_type',
        on_delete=models.CASCADE
    )
    q_parallel_block_id = models.ForeignKey(
        to='ParallelBlock',
        on_delete=models.CASCADE,
        default=None,
        blank=True,
        null=True,
        db_column='q_parallel_block_id'
    )
    class Meta:
        managed=False
        db_table='question'


class Test(models.Model):
    test_id = models.BigAutoField(primary_key=True)

    test_creator = models.ForeignKey(
        to = 'user',
        related_name='created_tests',
        on_delete=models.CASCADE,
        db_column='test_creator',
        verbose_name="Создатель теста"
    )
    test_name = models.TextField(
        db_column="test_name",
        verbose_name="Название"
    )
    test_create_date = models.DateTimeField(
        db_column="test_create_date",
        verbose_name="Дата создания теста"
    )
    test_subject = models.TextField(
        db_column="test_subject",
        verbose_name="Предмет"
    )
    test_learning_material = models.TextField(
        db_column="test_learning_material",
        verbose_name="Учебный материал",
        null=True,
        blank=True
    )
    test_type = models.ForeignKey(
        to='TestType',
        # related_name='test_type',
        db_column="test_type",
        default=1,
        verbose_name="Тип теста",
        on_delete=models.SET_DEFAULT
    )
    test_random_sort = models.BooleanField(
        db_column="test_random_sort",
        default=False,
        null=models.SET_DEFAULT
    )
    class Meta:
        managed = False
        db_table = 'test'


class TestingSystem(models.Model):
    ts_id = models.BigAutoField(primary_key = True)

    ts_user_id = models.ForeignKey(
        related_name="passed_tests",
        to='User',
        on_delete=models.CASCADE,
        db_column="ts_user_id"
    )
    ts_test_id = models.ForeignKey(
        Test,
        models.CASCADE,
        db_column="ts_test_id"
    )
    ts_start_time = models.DateTimeField(
        db_column="ts_start_time",
        verbose_name="Дата начала"
    )
    ts_end_time = models.DateTimeField(
        db_column="ts_end_time",
        verbose_name="Дата окончания"
    )
    ts_score_percent = models.IntegerField(
        db_column="ts_score_percent",
        verbose_name="Процент правильных ответов"
    )

    class Meta:
        managed = False
        db_table = 'testing_system'

