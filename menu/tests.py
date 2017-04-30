"""Tests for the menu app"""
import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.forms import ValidationError
from django.utils import timezone

from menu import models, forms


class MenuViewsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            username='user1',
            email='user1@gmail.com',
            password='testing'
        )
        ingredient1 = models.Ingredient(name='chocolate')
        ingredient1.save()
        ingredient2 = models.Ingredient(name='vanilla')
        ingredient2.save()
        ingredient3 = models.Ingredient(name='pineapple')
        ingredient3.save()
        self.item1 = models.Item(
            name='Chocolate Vanilla',
            description='very tasty',
            chef=self.user1
        )
        self.item1.save()
        self.item1.ingredients.add(ingredient1, ingredient2)
        self.item2 = models.Item(
            name='Vanilla Pineapple',
            description='quite delicious',
            chef=self.user1
        )
        self.item2.save()
        self.item2.ingredients.add(ingredient2, ingredient3)
        self.menu1 = models.Menu(
            season='Winter 2017',
            expiration_date=
            datetime.datetime.now() -
            datetime.timedelta(days=20)
        )
        self.menu1.save()
        self.menu1.items.add(self.item1, self.item2)
        self.menu2 = models.Menu(
            season='Fall 2017',
            expiration_date=
            datetime.datetime.now() +
            datetime.timedelta(days=220)
        )
        self.menu2.save()
        self.menu2.items.add(self.item1)

    def test_item_detail_view(self):
        resp = self.client.get(
            reverse('item_detail', kwargs={'pk': self.item1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('menu/item_detail.html')

    def test_item_detail_view_notfound(self):
        resp = self.client.get(reverse('item_detail', kwargs={'pk': 100}))
        self.assertEqual(resp.status_code, 404)

    def test_menu_detail_view(self):
        resp = self.client.get(
               reverse('menu_detail', kwargs={'pk': self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('menu/menu_detail.html')

    def test_menu_detail_view_notfound(self):
        resp = self.client.get(reverse('menu_detail', kwargs={'pk': 100}))
        self.assertEqual(resp.status_code, 404)

    def test_menu_list_view_template(self):
        self.client.get(reverse('menu_list'))
        self.assertTemplateUsed('menu/menu_list.html')

    def test_menu_list_view_rc(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertEqual(resp.status_code, 200)

    def test_menu_list_view_content(self):
        resp = self.client.get(reverse('menu_list'))
        self.assertNotIn(self.menu1, resp.context['menus'])
        self.assertIn(self.menu2, resp.context['menus'])

    def test_create_new_menu_view_get_rc(self):
        resp = self.client.get(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)

    def test_create_new_menu_view_get_template(self):
        self.client.get(reverse('menu_new'))
        self.assertTemplateUsed('menu/menu_new.html')

    def test_create_new_menu_view_post_rc(self):
        resp = self.client.post(reverse('menu_new'))
        self.assertEqual(resp.status_code, 200)

    def test_edit_menu_view_rc(self):
        resp = self.client.get(
            reverse('menu_edit', kwargs={'pk': self.menu1.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_edit_menu_view_template(self):
        self.client.get(
            reverse('menu_edit', kwargs={'pk': self.menu1.pk}))
        self.assertTemplateUsed('menu/menu_edit.html')

    def test_edit_menu_view_post_rc(self):
        resp = self.client.post(
            reverse('menu_edit', kwargs={'pk': self.menu1.pk})
        )
        self.assertEqual(resp.status_code, 200)


class MenuFormsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(
            username='user1',
            email='user1@gmail.com',
            password='testing'
        )
        ingredient1 = models.Ingredient(name='chocolate')
        ingredient1.save()
        ingredient2 = models.Ingredient(name='vanilla')
        ingredient2.save()
        ingredient3 = models.Ingredient(name='pineapple')
        ingredient3.save()
        self.item1 = models.Item(
            name='Chocolate Vanilla',
            description='very tasty',
            chef=self.user1
        )
        self.item1.save()
        self.item1.ingredients.add(ingredient1, ingredient2)
        self.item2 = models.Item(
            name='Vanilla Pineapple',
            description='quite delicious',
            chef=self.user1
        )
        self.item2.save()
        self.item2.ingredients.add(ingredient2, ingredient3)

    def test_menu_create_form_valid(self):
        expiration_date = datetime.date(2018, 4, 3)
        data = {'season': 'Spring 2018',
                'items': [self.item1.pk],
                'expiration_date': expiration_date
                }
        form = forms.MenuForm(data=data)
        self.assertTrue(form.is_valid())
        menu = form.save()
        self.assertEqual(menu.season, 'Spring 2018')
        self.assertEqual(menu.expiration_date, expiration_date)

    def test_menu_create_form_blank_data(self):
        form = forms.MenuForm(data={})
        self.assertFalse(form.is_valid())

    def test_menu_create_form_season_error(self):
        expiration_date = datetime.date(2017, 4, 3)
        data = {'season': 'Spring 2018',
                'items': [self.item1.pk],
                'expiration_date': expiration_date}
        form = forms.MenuForm(data=data)
        self.assertRaises(ValidationError, form.full_clean())


class MenuModelsTest(TestCase):
    def test_get_season_from_date(self):
        self.assertEqual(
            models.get_season_from_date(
                datetime.date(2017, 4, 3)),
            "Spring 2017")
        self.assertEqual(
            models.get_season_from_date(
                datetime.date(2017, 8, 20)),
            "Summer 2017")
        self.assertEqual(
            models.get_season_from_date(
                datetime.date(2018, 9, 8)),
            "Autumn 2018")
        self.assertEqual(
            models.get_season_from_date(
                datetime.date(2015, 1, 10)),
            "Winter 2015")

    def test_validate_not_in_the_past_valid(self):
        future_date = (timezone.now() + datetime.timedelta(days=12)).date()
        self.assertIsNone(
            models.validate_not_in_the_past(future_date))

    def test_validate_not_in_the_past_error(self):
        past_date = (timezone.now() - datetime.timedelta(days=12)).date()
        with self.assertRaises(ValidationError):
            models.validate_not_in_the_past(past_date)

    def test_validate_season_valid(self):
        future_date = (timezone.now() + datetime.timedelta(days=12)).date()
        self.assertIsNone(
            models.validate_not_in_the_past(future_date))

    def test_validate_season_error_empty(self):
        season = ""
        with self.assertRaises(ValidationError):
            models.validate_season(season)

    def test_validate_season_error_not_season_year(self):
        season = "Autumn xx"
        with self.assertRaises(ValidationError):
            models.validate_season(season)

    def test_menu__str__(self):
        menu = models.Menu(
            season='Winter 2017')
        self.assertEqual(str(menu), 'Winter 2017')
