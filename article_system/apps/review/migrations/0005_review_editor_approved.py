# Generated by Django 5.1.7 on 2025-03-28 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_review_created_at_review_rating_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='editor_approved',
            field=models.BooleanField(default=False),
        ),
    ]
