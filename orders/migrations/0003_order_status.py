from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0002_order_delivery_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="status",
            field=models.CharField(
                choices=[
                    ("PENDING", "Pending"),
                    ("SHIPPED", "Shipped"),
                    ("DELIVERED", "Delivered"),
                ],
                default="PENDING",
                max_length=20,
            ),
        ),
    ]
