# Generated by Django 4.1.4 on 2022-12-31 12:18

import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import grapp.mymanager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='HeadOffice',
            fields=[
                ('HeadOffice_id', models.AutoField(primary_key=True, serialize=False)),
                ('HeadOffice_name', models.CharField(default='Mizynté', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('Zone_id', models.AutoField(primary_key=True, serialize=False)),
                ('Zone_name', models.CharField(max_length=255)),
                ('head_office', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='related_zones', to='grapp.headoffice')),
            ],
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('Branch_id', models.AutoField(primary_key=True, serialize=False)),
                ('Branch_name', models.CharField(max_length=255)),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='branches', to='grapp.zone')),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('User_id', models.AutoField(primary_key=True, serialize=False)),
                ('Phone_number', models.CharField(max_length=15, unique=True)),
                ('Phone_is_verified', models.BooleanField(default=False)),
                ('otp', models.CharField(max_length=6)),
                ('access_level', models.CharField(choices=[('employee', 'Employee'), ('manager', 'Manager'), ('admin', 'Admin')], max_length=10)),
                ('branch', models.CharField(max_length=22)),
                ('zone', models.CharField(max_length=22)),
                ('head_office', models.CharField(max_length=22)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', grapp.mymanager.UserManager()),
            ],
        ),
    ]
