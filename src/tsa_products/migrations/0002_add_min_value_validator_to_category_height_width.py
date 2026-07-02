import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tsa_products", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="height",
            field=models.FloatField(default=5.0, validators=[django.core.validators.MinValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name="category",
            name="width",
            field=models.FloatField(default=5.0, validators=[django.core.validators.MinValueValidator(5)]),
        ),
    ]
