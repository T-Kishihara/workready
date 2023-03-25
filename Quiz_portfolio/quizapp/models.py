from django.db import models
from accounts.models import Users

# Create your models here.
class Quiz(models.Model):
    title = models.CharField(max_length=20, verbose_name='タイトル(必須)')
    sentence = models.CharField(max_length=100, verbose_name='問題文(必須)')
    created_by = models.ForeignKey(
        Users, on_delete=models.CASCADE, verbose_name='作成者名'
    )

    class Meta:
        db_table = 'quiz'

    def __str__(self):
        return self.title

class Choices(models.Model):
    sentence = models.CharField(max_length=10, verbose_name='選択肢')
    is_correct = models.BooleanField(default=False, verbose_name='正誤(チェックを入れると正解として扱われます)')
    description = models.CharField(max_length=100, null=True, blank=True, verbose_name='解説文')
    quiz = models.ForeignKey(
        Quiz, on_delete=models.CASCADE, verbose_name='対応するクイズ'
    )

    class Meta:
        db_table = 'choices'

    def __str__(self):
        return self.sentence