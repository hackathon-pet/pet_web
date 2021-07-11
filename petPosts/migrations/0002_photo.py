# Generated by Django 3.2.5 on 2021-07-10 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('petPosts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='petPosts.post')),
            ],
        ),
    ]
