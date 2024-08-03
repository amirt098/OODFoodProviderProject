from django.test import TestCase
from django.contrib.auth.hashers import make_password
from apps.accounts.models import User
from apps.accounts.data_classes import UserInfo, UserRole
from apps.accounts.exceptions import UsernameNotFound, PasswordNotFound, UIDNotFound
from apps.accounts.services import UserService

class UserServiceTestCase(TestCase):

    def setUp(self):
        # Create a user for testing
        self.test_user = User.objects.create(
            uid='test-uid',
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            phone_number='1234567890',
            role=UserRole.CUSTOMER
        )
        self.test_user.password = make_password('testpassword')
        self.test_user.save()
        self.service = UserService()

    # def test_login_success(self):
    #     user_claim = UserService.login(None, 'testuser', 'testpassword')
    #     self.assertEqual(user_claim.username, 'testuser')
    #
    # def test_login_invalid_username(self):
    #     with self.assertRaises(UsernameNotFound):
    #         self.service.login('', 'invaliduser', 'testpassword')

    def test_login_invalid_password(self):
        with self.assertRaises(PasswordNotFound):
            self.service.login(None, 'testuser', 'wrongpassword')

    def test_register_user_success(self):
        user_info = UserInfo(
            uid='new-uid',
            username='newuser',
            email='new@example.com',
            first_name='New',
            last_name='User',
            phone_number='0987654321',
            role=UserRole.CUSTOMER,
            password='newpassword'
        )
        registered_user_info = self.service.register_user(user_info)
        self.assertEqual(registered_user_info.username, 'newuser')
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_user_username_exists(self):
        user_info = UserInfo(
            uid='new-uid-2',
            username='testuser',  # Existing username
            email='new@example.com',
            first_name='New',
            last_name='User',
            phone_number='0987654321',
            role=UserRole.CUSTOMER,
            password='newpassword'
        )
        with self.assertRaises(ValueError):
            self.service.register_user(user_info)

    def test_modify_user_success(self):
        user_info = UserInfo(
            uid='test-uid',
            username='updateduser',
            email='updated@example.com',
            first_name='Updated',
            last_name='User',
            phone_number='1234567890',
            role=UserRole.CUSTOMER,
            password='updatedpassword'
        )
        updated_info = self.service.modify_user(user_info, 'test-uid')
        self.assertEqual(updated_info.username, 'updateduser')

    def test_modify_user_permission_error(self):
        user_info = UserInfo(
            uid='another-uid',  # Different UID
            username='updateduser',
            email='updated@example.com',
            first_name='Updated',
            last_name='User',
            phone_number='1234567890',
            role=UserRole.CUSTOMER,
            password='updatedpassword'
        )
        with self.assertRaises(PermissionError):
            self.service.modify_user(user_info, 'test-uid')

    def test_get_info_success(self):
        user_info = self.service.get_info('testuser')
        self.assertEqual(user_info.username, 'testuser')

    def test_get_info_uid_not_found(self):
        with self.assertRaises(UIDNotFound):
            self.service.get_info('invaliduser')

    def test_get_full_name_success(self):
        full_name = self.service.get_full_name('testuser')
        self.assertEqual(full_name, 'Test User')

    def test_get_role_success(self):
        role = self.service.get_role('testuser')
        self.assertEqual(role, UserRole.CUSTOMER)
