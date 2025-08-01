# news/management/commands/seed_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.apps import apps


class Command(BaseCommand):
    help = "Create Reader, Editor, Journalist groups and attach model permissions."

    def handle(self, *args, **kwargs):
        # Permission codenames we need
        article_perms    = ['add_article', 'view_article',
                            'change_article', 'delete_article']
        newsletter_perms = ['add_newsletter', 'view_newsletter',
                            'change_newsletter', 'delete_newsletter']

        # Helper to fetch Permission objects
        def perms(codenames):
            return Permission.objects.filter(codename__in=codenames)

        # Reader group
        reader, _ = Group.objects.get_or_create(name='reader')
        reader.permissions.set(perms(['view_article', 'view_newsletter']))

        # Editor group
        editor, _ = Group.objects.get_or_create(name='editor')
        editor.permissions.set(perms(article_perms + newsletter_perms))

        # Journalist group
        journalist, _ = Group.objects.get_or_create(name='journalist')
        journalist.permissions.set(perms(article_perms + newsletter_perms))

        self.stdout.write(self.style.SUCCESS("Groups and permissions seeded successfully"))
