from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class LoginEndpointTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.user = User.objects.create_user(
            username='normal@example.com',
            password='testpass123',
            email='normal@example.com'
        )
        cls.login_url = reverse('login')
        cls.index_url = reverse('index')
        cls.home_url = reverse('home')

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()
        super().tearDownClass()

    def test_login_success(self):
        """Login de usuario normal correcto"""
        response = self.client.post(self.login_url, {
            'username': 'normal@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)

    def test_login_failure_wrong_password(self):
        """Login de usuario normal incorrecto"""
        response = self.client.post(self.login_url, {
            'username': 'normal@example.com',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nombre de usuario o contraseña incorrectos.')

        response = self.client.post(self.login_url, {
            'username': 'bad@example.com',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nombre de usuario o contraseña incorrectos.')

        response = self.client.post(self.login_url, {
            'username': '',
            'password': ''
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nombre de usuario o contraseña incorrectos.')
    

class StaffEndpointTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.staff_user = User.objects.create_user(
            username='staff@example.com',
            password='testpass123',
            first_name='Staff',
            last_name='User',
            email='staff@example.com',
            is_staff=True
        )
        cls.normal_user = User.objects.create_user(
            username='normal@example.com',
            password='testpass123',
            first_name='Normal',
            last_name='User',
            email='normal@example.com',
            is_staff=False
        )
        cls.login_staff_url = reverse('loginStaff')
        cls.home_url = reverse('home')

    @classmethod
    def tearDownClass(cls):
        cls.staff_user.delete()
        cls.normal_user.delete()
        super().tearDownClass()

    def test_staff_login_success(self):
        """Login de Staff correcto"""
        response = self.client.post(self.login_staff_url, {
            'first_name': 'Staff',
            'last_name': 'User',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.home_url)

    def test_home_access_by_normal_user(self):
        """Usuario normal no debe poder acceder a home"""
        self.client.login(username='normal@example.com', password='testpass123')
        response = self.client.get(self.home_url)

        
        self.assertIn(response.status_code, [302, 403])
        
        if response.status_code == 302:
            self.assertIn(reverse('login'), response.url)
