from django.test import TestCase
from django.contrib.auth import get_user_model



class CustomerTests(TestCase):
    def test_create_user(self):
        db = get_user_model()
        user = db.objects.create_user('test@user.com', 'name', 'password')
        self.assertEqual(user.name, 'name')
        self.assertEqual(user.email, 'test@user.com')
        self.assertEqual(user.password, 'password')
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

        with self.assertRaises(ValueError):
            db.objects.create_user(name='name', email='', password='password')

    def test_create_superuser(self):
        db = get_user_model()
        super_user = db.create_superuser('name', 'test@super.com', 'password')
        self.assertEqual(super_user.name, 'name')
        self.assertEqual(super_user.email, 'test@super.com')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), 'test@super.com')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(name='name', email='test@super.com', password='password', is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(name='name', email='test@super.com', password='password', is_staff=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(name='name', email='', password='password', is_superuser=True)
