from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="address",
            field=models.TextField(default=""),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="city",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="full_name",
            field=models.CharField(default="", max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="phone_number",
            field=models.CharField(default="", max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="pincode",
            field=models.CharField(default="", max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="order",
            name="state",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]
