from django.db import migrations, models
from django.utils.text import slugify


def populate_slugs(apps, schema_editor):
    Category = apps.get_model('home', 'Category')
    for cat in Category.objects.all():
        base = slugify(cat.name)
        slug = base
        i = 1
        while Category.objects.filter(slug=slug).exclude(pk=cat.pk).exists():
            slug = f"{base}-{i}"
            i += 1
        cat.slug = slug
        cat.save()


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_quiz_end_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=120, null=True, blank=True),
        ),
        migrations.RunPython(populate_slugs, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=120, unique=True, blank=False),
        ),
    ]
