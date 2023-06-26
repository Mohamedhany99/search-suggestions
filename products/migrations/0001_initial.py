# Generated by Django 4.1.9 on 2023-06-26 10:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(max_length=200)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
            ],
        ),
    ]