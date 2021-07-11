from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pets', '0004_merge_0002_auto_20210711_1503_0003_alter_pet_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pet',
            name='category',
            field=models.CharField(blank=True, choices=[('p1', '강아지'), ('p2', '고양이'), ('p3', '햄스터'), ('p4', '포유류'), ('p5', '조류'), ('p6', '어류'), ('p7', '파충류'), ('p8', '거미/전갈')], max_length=2, null=True, verbose_name='category'),
        ),
    ]
