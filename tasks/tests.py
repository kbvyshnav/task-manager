from django.test import TestCase
from django.urls import reverse
from .models import Task, Category


class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Work', color='#ff0000')

    def test_str(self):
        self.assertEqual(str(self.category), 'Work')

    def test_ordering_alphabetical(self):
        Category.objects.create(name='Personal')
        names = list(Category.objects.values_list('name', flat=True))
        self.assertEqual(names, ['Personal', 'Work'])


class TaskModelTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='Buy groceries', priority='high')

    def test_str(self):
        self.assertEqual(str(self.task), 'Buy groceries')

    def test_defaults(self):
        self.assertFalse(self.task.done)
        self.assertEqual(self.task.priority, 'high')
        self.assertIsNone(self.task.category)
        self.assertIsNone(self.task.due_date)

    def test_get_absolute_url(self):
        url = self.task.get_absolute_url()
        self.assertEqual(url, f'/tasks/{self.task.pk}/')

    def test_category_set_null_on_delete(self):
        category = Category.objects.create(name='Temp')
        task = Task.objects.create(title='With category', category=category)
        category.delete()
        task.refresh_from_db()
        self.assertIsNone(task.category)


class HomeViewTest(TestCase):
    def test_status_200(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_shows_correct_stats(self):
        Task.objects.create(title='Task A', done=True)
        Task.objects.create(title='Task B', done=False)
        response = self.client.get(reverse('home'))
        stats = response.context['stats']
        self.assertEqual(stats['total'], 2)
        self.assertEqual(stats['done'], 1)
        self.assertEqual(stats['pending'], 1)


class TaskListViewTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name='Work')
        Task.objects.create(title='High priority', priority='high', done=False, category=self.cat)
        Task.objects.create(title='Done task', priority='low', done=True)

    def test_status_200(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.status_code, 200)

    def test_shows_all_tasks(self):
        response = self.client.get(reverse('task_list'))
        self.assertEqual(response.context['total'], 2)

    def test_filter_by_status_done(self):
        response = self.client.get(reverse('task_list'), {'status': 'done'})
        self.assertEqual(response.context['tasks'].count(), 1)
        self.assertEqual(response.context['tasks'][0].title, 'Done task')

    def test_filter_by_status_pending(self):
        response = self.client.get(reverse('task_list'), {'status': 'pending'})
        self.assertEqual(response.context['tasks'].count(), 1)

    def test_filter_by_priority(self):
        response = self.client.get(reverse('task_list'), {'priority': 'high'})
        self.assertEqual(response.context['tasks'].count(), 1)
        self.assertEqual(response.context['tasks'][0].title, 'High priority')

    def test_filter_by_category(self):
        response = self.client.get(reverse('task_list'), {'category': self.cat.id})
        self.assertEqual(response.context['tasks'].count(), 1)


class TaskDetailViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='Detail task', priority='low')

    def test_status_200(self):
        response = self.client.get(reverse('task_detail', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 200)

    def test_404_for_missing_task(self):
        response = self.client.get(reverse('task_detail', kwargs={'task_id': 9999}))
        self.assertEqual(response.status_code, 404)

    def test_shows_task_title(self):
        response = self.client.get(reverse('task_detail', kwargs={'task_id': self.task.id}))
        self.assertContains(response, 'Detail task')


class CreateTaskViewTest(TestCase):
    def test_get_renders_form(self):
        response = self.client.get(reverse('create_task'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_post_creates_task(self):
        response = self.client.post(reverse('create_task'), {
            'title': 'New task',
            'description': '',
            'priority': 'low',
        })
        self.assertRedirects(response, reverse('task_list'))
        self.assertTrue(Task.objects.filter(title='New task').exists())

    def test_whitespace_title_rejected(self):
        response = self.client.post(reverse('create_task'), {
            'title': '   ',
            'priority': 'low',
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Task.objects.filter(title='   ').exists())

    def test_empty_title_rejected(self):
        response = self.client.post(reverse('create_task'), {
            'title': '',
            'priority': 'medium',
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Task.objects.count(), 0)


class EditTaskViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='Original', priority='medium')

    def test_get_prepopulates_form(self):
        response = self.client.get(reverse('edit_task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Original')

    def test_post_updates_task(self):
        response = self.client.post(
            reverse('edit_task', kwargs={'task_id': self.task.id}),
            {'title': 'Updated', 'description': '', 'priority': 'high'}
        )
        self.assertRedirects(response, reverse('task_detail', kwargs={'task_id': self.task.id}))
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated')
        self.assertEqual(self.task.priority, 'high')


class DeleteTaskViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='To delete', priority='low')

    def test_get_shows_confirmation(self):
        response = self.client.get(reverse('delete_task', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'To delete')

    def test_post_deletes_task(self):
        response = self.client.post(reverse('delete_task', kwargs={'task_id': self.task.id}))
        self.assertRedirects(response, reverse('task_list'))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())


class ToggleDoneViewTest(TestCase):
    def setUp(self):
        self.task = Task.objects.create(title='Toggle me', done=False)

    def test_post_toggles_to_done(self):
        self.client.post(reverse('toggle_done', kwargs={'task_id': self.task.id}))
        self.task.refresh_from_db()
        self.assertTrue(self.task.done)

    def test_post_toggles_back_to_pending(self):
        self.task.done = True
        self.task.save()
        self.client.post(reverse('toggle_done', kwargs={'task_id': self.task.id}))
        self.task.refresh_from_db()
        self.assertFalse(self.task.done)

    def test_get_returns_405(self):
        response = self.client.get(reverse('toggle_done', kwargs={'task_id': self.task.id}))
        self.assertEqual(response.status_code, 405)
