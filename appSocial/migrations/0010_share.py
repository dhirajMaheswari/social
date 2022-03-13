# Generated by Django 3.0.2 on 2021-03-09 03:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appSocial', '0009_remove_like_likes_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shared_image', to='appSocial.Tasveer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sharer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
