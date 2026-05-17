from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from projects.models import Project

User = get_user_model()


class Command(BaseCommand):
    help = 'Создаёт тестовых пользователей и проекты для проверки функционала'

    def handle(self, *args, **options):
        self.stdout.write('🔄 Начинаю создание тестовых данных...')

        # Пользователь 1: Автор проекта
        user1, created1 = User.objects.get_or_create(
            email='dmitry@example.com',
            defaults={
                'name': 'Дмитрий',
                'surname': 'Козлов',
                'about': 'Backend-разработчик, люблю Django и PostgreSQL',
                'phone': '+79991234567',
                'github_url': 'https://github.com/dmitry-kozlov'
            }
        )
        if created1:
            user1.set_password('TestPass123!')
            user1.save()
            self.stdout.write(self.style.SUCCESS('✅ Создан: Дмитрий Козлов (dmitry@example.com)'))

        # Пользователь 2: Участник
        user2, created2 = User.objects.get_or_create(
            email='anna@example.com',
            defaults={
                'name': 'Анна',
                'surname': 'Смирнова',
                'about': 'Frontend-разработчик, React & Vue',
                'phone': '+79997654321',
                'github_url': 'https://github.com/anna-smirnova'
            }
        )
        if created2:
            user2.set_password('TestPass123!')
            user2.save()
            self.stdout.write(self.style.SUCCESS('✅ Создан: Анна Смирнова (anna@example.com)'))

        # Пользователь 3: Ещё один участник
        user3, created3 = User.objects.get_or_create(
            email='maxim@example.com',
            defaults={
                'name': 'Максим',
                'surname': 'Петров',
                'about': 'DevOps & Python энтузиаст',
                'phone': '+79990001122',
                'github_url': 'https://github.com/maxim-petrov'
            }
        )
        if created3:
            user3.set_password('TestPass123!')
            user3.save()
            self.stdout.write(self.style.SUCCESS('✅ Создан: Максим Петров (maxim@example.com)'))

        # Проекты
        project1, created_p1 = Project.objects.get_or_create(
            name='TeamFinder Platform',
            owner=user1,
            defaults={
                'description': 'Платформа для поиска команды и управления проектами. Django + HTMX + PostgreSQL.',
                'status': 'open',
                'github_url': 'https://github.com/dmitry-kozlov/teamfinder'
            }
        )
        if created_p1:
            project1.participants.add(user1, user2)
            self.stdout.write(self.style.SUCCESS('✅ Создан проект: TeamFinder Platform'))

        project2, created_p2 = Project.objects.get_or_create(
            name='E-commerce Dashboard',
            owner=user2,
            defaults={
                'description': 'Админ-панель для интернет-магазина с аналитикой и управлением заказами.',
                'status': 'open',
                'github_url': 'https://github.com/anna-smirnova/ecom-dashboard'
            }
        )
        if created_p2:
            project2.participants.add(user2, user3)
            self.stdout.write(self.style.SUCCESS('✅ Создан проект: E-commerce Dashboard'))

        project3, created_p3 = Project.objects.get_or_create(
            name='Bot Assistant',
            owner=user3,
            defaults={
                'description': 'Telegram-бот для автоматизации рутинных задач и уведомлений.',
                'status': 'closed',
                'github_url': 'https://github.com/maxim-petrov/bot-assistant'
            }
        )
        if created_p3:
            project3.participants.add(user3)
            self.stdout.write(self.style.SUCCESS('✅ Создан проект: Bot Assistant'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Готово! Тестовые данные успешно загружены.'))
        self.stdout.write('🔑 Пароль для всех аккаунтов: TestPass123!')
