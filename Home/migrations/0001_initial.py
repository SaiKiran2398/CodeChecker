# Generated by Django 4.0.3 on 2022-04-16 06:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=122)),
                ('type', models.CharField(max_length=50)),
                ('difficuilty', models.CharField(max_length=10)),
                ('statement', models.TextField()),
                ('desc', models.TextField()),
                ('task', models.TextField(null=True)),
                ('time_complexity', models.CharField(max_length=50, null=True)),
                ('space_complexity', models.CharField(max_length=50, null=True)),
                ('constraints', models.CharField(max_length=122, null=True)),
                ('example', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=122, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=122)),
                ('email', models.CharField(max_length=122, unique=True)),
                ('password', models.CharField(max_length=32)),
                ('problems_solved', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TestCases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.TextField()),
                ('output', models.TextField()),
                ('problem', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Home.problem')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verdict', models.CharField(max_length=255)),
                ('time', models.DateTimeField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.problem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Home.user')),
            ],
        ),
    ]
