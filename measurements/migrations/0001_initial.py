# Generated by Django 3.1.4 on 2020-12-07 09:05

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Measurements',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('chest', models.FloatField(help_text='in inches', max_length=50)),
                ('shoulder_width', models.FloatField(help_text='in inches', max_length=50)),
                ('waist', models.FloatField(help_text='in inches', max_length=50)),
                ('stomach', models.FloatField(help_text='in inches', max_length=50)),
                ('arms_length', models.FloatField(help_text='in inches', max_length=50)),
                ('biceps', models.FloatField(help_text='in inches', max_length=50)),
                ('hips', models.FloatField(help_text='in inches', max_length=50)),
                ('waist_to_ankle', models.FloatField(help_text='in inches', max_length=50)),
                ('ankle', models.FloatField(help_text='in inches', max_length=50)),
                ('neck', models.FloatField(help_text='in inches', max_length=50)),
                ('thighs', models.FloatField(help_text='in inches', max_length=50)),
                ('extra_comments', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='authentication.customer')),
            ],
        ),
    ]
