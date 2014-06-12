import datetime

from django.utils import timezone
from django.test import TestCase
from django.core.urlresolvers import reverse

from schedules.models import schedule

# Create your tests here.


class scheduleMethodTests(TestCase):

    def test_was_published_recently_with_future_schedule(self):
        """
        was_published_recently() should return False for schedules whose
        pub_date is in the future
        """
        future_schedule = schedule(pub_date=timezone.now() + datetime.timedelta(days=30))
        self.assertEqual(future_schedule.was_published_recently(), False)

    def test_was_published_recently_with_old_schedule(self):
        """
        was_published_recently() should return False for schedules whose pub_date
        is older than 1 day
        """
        old_schedule = schedule(pub_date=timezone.now() - datetime.timedelta(days=30))
        self.assertEqual(old_schedule.was_published_recently(), False)

    def test_was_published_recently_with_recent_schedule(self):
        """
        was_published_recently() should return True for schedules whose pub_date
        is within the last day
        """
        recent_schedule = schedule(pub_date=timezone.now() - datetime.timedelta(hours=1))
        self.assertEqual(recent_schedule.was_published_recently(), True)


def create_schedule(question, days):
    """
    Creates a schedule with the given `question` published the given number of
    `days` offset to now (negative for schedules published in the past,
    positive for schedules that have yet to be published).
    """
    return schedule.objects.create(question=question,
        pub_date=timezone.now() + datetime.timedelta(days=days))


class scheduleViewTests(TestCase):
    def test_index_view_with_no_schedules(self):
        """
        If no schedules exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('schedules:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No schedules are available.")
        self.assertQuerysetEqual(response.context['latest_schedule_list'], [])

    def test_index_view_with_a_past_schedule(self):
        """
        schedules with a pub_date in the past should be displayed on the index page.
        """
        create_schedule(question="Past schedule.", days=-30)
        response = self.client.get(reverse('schedules:index'))
        self.assertQuerysetEqual(
            response.context['latest_schedule_list'],
            ['<schedule: Past schedule.>']
        )

    def test_index_view_with_a_future_schedule(self):
        """
        schedules with a pub_date in the future should not be displayed on the
        index page.
        """
        create_schedule(question="Future schedule.", days=30)
        response = self.client.get(reverse('schedules:index'))
        self.assertContains(response, "No schedules are available.", status_code=200)
        self.assertQuerysetEqual(response.context['latest_schedule_list'], [])

    def test_index_view_with_future_schedule_and_past_schedule(self):
        """
        Even if both past and future schedules exist, only past schedules should be
        displayed.
        """
        create_schedule(question="Past schedule.", days=-30)
        create_schedule(question="Future schedule.", days=30)
        response = self.client.get(reverse('schedules:index'))
        self.assertQuerysetEqual(
            response.context['latest_schedule_list'],
            ['<schedule: Past schedule.>']
        )

    def test_index_view_with_two_past_schedules(self):
        """
        The schedules index page may display multiple schedules.
        """
        create_schedule(question="Past schedule 1.", days=-30)
        create_schedule(question="Past schedule 2.", days=-5)
        response = self.client.get(reverse('schedules:index'))
        self.assertQuerysetEqual(
            response.context['latest_schedule_list'],
             ['<schedule: Past schedule 2.>', '<schedule: Past schedule 1.>']
        )


class scheduleIndexDetailTests(TestCase):
    def test_detail_view_with_a_future_schedule(self):
        """
        The detail view of a schedule with a pub_date in the future should
        return a 404 not found.
        """
        future_schedule = create_schedule(question='Future schedule.', days=5)
        response = self.client.get(reverse('schedules:detail', args=(future_schedule.id,)))
        self.assertEqual(response.status_code, 404)

    def test_detail_view_with_a_past_schedule(self):
        """
        The detail view of a schedule with a pub_date in the past should display
        the schedule's question.
        """
        past_schedule = create_schedule(question='Past schedule.', days=-5)
        response = self.client.get(reverse('schedules:detail', args=(past_schedule.id,)))
        self.assertContains(response, past_schedule.question, status_code=200)