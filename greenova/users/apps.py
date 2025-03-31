from django.apps import AppConfig

<<<<<<< HEAD

=======
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
<<<<<<< HEAD
        pass  # Signal connection is handled at the top level
=======
        import users.signals  # Ensure the signal is connected
>>>>>>> b3f8326 (release(v0.0.4): comprehensive platform enhancements and new features (#6))
