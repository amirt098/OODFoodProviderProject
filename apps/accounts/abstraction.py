import abc
from .data_classes import UserInfo, UserRole, AddressList


class AbstractAccountService(abc.ABC):
    @abc.abstractmethod
    def login(self,
              username: str,
              password: str):
        """
        User can log in using this method.
        Args:
            username (str): Username of user
            password (str): <PASSWORD>
        Raise:
            UsernameNotFound: If the username is not found
            PasswordNotFound: If the password is incorrect
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def logout(self):
        """
        User can log out via this method.
        Return:
            None
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def register_user(self, request: UserInfo) -> UserInfo:
        """
        User can register via this method.
        Args:
            request (UserInfo): User registration
        Return:
            UserInfo: registered user information

        """

    @abc.abstractmethod
    def modify_user(self, request: UserInfo) -> UserInfo:
        """
        User can modify his accounts with this method.
            Args:
                request (UserInfo):+9

            Raise:
                UIDNotFound
            Return:
                UserInfo: User modified information

        """

    @abc.abstractmethod
    def get_addresses(self, username: str) -> AddressList:
        """
        Get addresses associated with the user.
        Args:
            username (str): Username of the user
        Raise:
           UIDNotFound : If the user uid is not found
        Return:
            AddressList: List of addresses
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_info(self, username: str) -> UserInfo:
        """
        Get user information.
        Args:
            username (str): Username of the user
        Raise:
            UIDNotFound: If the user uid is not found
        Return:
            UserInfo: User information
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_full_name(self, username: str) -> str:
        """
        Get the full name of the user.
        Args:
            username (str): Username of the user
        Raise:
            UIDNotFound: If the user uid is not found
        Return:
            str: Full name of the user
        """
        raise NotImplementedError()

    @abc.abstractmethod
    def get_role(self, username: str) -> UserRole:
        """
        Get the role of the user.
        Args:
            username (str): Username of the user
        Raise:
            UIDNotFound: If the user uid is not found
        Return:
            UserRole: Role of the user
        """
        raise NotImplementedError()
    
    @abc.abstractmethod
    def get_user_id(self, uid: str) -> int:
        """
        Get database id of the user (only for foreign keys)
        Args:
            uid (int): uid of the user
        Raise:
           UIDNotFound : If the user uid is not found
        Return:
            int : database id of the user
        """
        raise NotImplementedError()
