from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class User(models.Model):
    user_id = models.BigAutoField(primary_key = True)
    user_name = models.TextField(
        db_column="user_name",
        verbose_name="Имя"
    )
    user_type = models.TextField(
        db_column="user_type",
        verbose_name="Тип"
    )
    login = models.TextField(
        db_column="login",
        verbose_name="Логин"
    )
    password = models.TextField(
        db_column="password",
        verbose_name="Пароль"
    )
    create_test_permission = models.BooleanField(
        db_column="create_test_permission",
        verbose_name="Разрешение на создание теста"
    )
    class Meta:
        managed = False
        db_table = "user"
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

class Score(models.Model):

    score_id = models.BigAutoField(primary_key = True)

    score_text = models.TextField(
        db_column="score_text",
        verbose_name="Оценка"
    )
    class Meta:
        managed=False
        db_table = 'score'

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
        to = 'Test',
        on_delete=models.CASCADE,
        db_column='q_test_id'
    )
    q_parent_id = models.ForeignKey(
        to='self',
        related_name="children",
        null=True,
        blank=True,
        default=0,
        db_column="q_parent_id",
        on_delete=models.CASCADE,
        verbose_name= "Предыдущий вопрос"
    )
    q_chance = models.IntegerField(
        db_column="q_chance",
        verbose_name="Шанс"
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
    is_tree = models.BooleanField(
        db_column="is_tree",
        default=False,
        verbose_name="Древовидность"
    )
    class Meta:
        managed = False
        db_table = 'test'

class TestingSystem(models.Model):
    ts_id = models.BigAutoField(primary_key = True)

    ts_user_id = models.ForeignKey(
        related_name="passed_tests",
        to='User',
        on_delete=models.DO_NOTHING,
        db_column="ts_user_id"
    )
    ts_test_id = models.ForeignKey(
        Test,
        models.DO_NOTHING,
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
    ts_count_right_answers = models.IntegerField(
        db_column="ts_count_right_answers",
        verbose_name="Количество правильных ответов"
    )
    ts_score_id = models.ForeignKey(
        Score,
        models.DO_NOTHING,
        db_column="ts_score_id",
        verbose_name="Оценка"
    )
    class Meta:
        managed = False
        db_table = 'testing_system'