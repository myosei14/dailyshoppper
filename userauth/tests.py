from django.test import TestCase
from django.contrib.auth import get_user_model



class CustomerTests(TestCase):
    def test_create_user(self):
        db = get_user_model()
        user = db.objects.create_user('test@user.com', 'name', 'password')
        self.assertEqual(user.email, 'test@user.com')
        self.assertEqual(user.name, 'name')
        self.assertTrue(user.password, user.check_password('password'))
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_staff)

        with self.assertRaises(ValueError):
            db.objects.create_user(email='', name='name', password='password')

    def test_create_superuser(self): 
        db = get_user_model()
        super_user = db.objects.create_superuser('test@super.com', 'name', 'password')
        self.assertEqual(super_user.email, 'test@super.com')
        self.assertEqual(super_user.name, 'name')
        self.assertTrue(super_user.is_superuser)
        self.assertTrue(super_user.is_staff)
        self.assertTrue(super_user.is_active)
        self.assertEqual(str(super_user), 'test@super.com')

        with self.assertRaises(ValueError):
            db.objects.create_superuser(name='name', email='test@super.com', password='password', is_superuser=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser( name='name', email='test@super.com', password='password', is_staff=False)

        with self.assertRaises(ValueError):
            db.objects.create_superuser(name='name',email='', password='password', is_superuser=True)
