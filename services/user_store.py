from models.user import User

class UserStore:

    def __init__(self):
        self.users = []
        self.next_user_id = 1

    def get_users(self):
        return self.users


    def add_user(self, name, email):
        user = User(id=self.next_user_id, name=name, email=email)
        self.users.append(user)
        self.next_user_id += 1
        return user

    def delete_user(self, index):
        return self.users.pop(index)

user_store = UserStore()