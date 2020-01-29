from typing import List, Optional


class ProtectedAttribute:
    def __init__(self, requires_role=None):
        self.permission_required = requires_role
        self._name = None

    def __set_name__(self, owner, name):
        self._name = name

    def __set__(self, user, value):
        if value is None:
            raise ValueError(f"Cannot set {self._name} None")
        user.__dict__[self._name] = value

    def __delete__(self, user):
        if self.permission_required in user.permissions:
            user.__dict__[self._name] = None
        else:
            raise ValueError(f"User '{user!s}' does not have {self.permission_required} permission")


class User:
    """Only admin user can delete email address."""

    email = ProtectedAttribute(requires_role="admin")

    def __init__(self, username: str, email: str, permission_list: Optional[List] = None):
        self.username = username
        self.email = email
        self.permissions = permission_list if permission_list is not None else []

    def __str__(self):
        return self.username


if __name__ == "__main__":
    admin = User("root", "root@d.com", ["admin"])
    user = User("user", "user@d.com", ["email", "helpdesk"])
    print(admin.email)
    del admin.email
    print(admin.email is None)
    print(user.email)
    # ValueError: Cannot set email None
    user.email = None
    # ValueError: User 'user' does not have admin permission
    del user.email
