# services.py
from .repositories import ShoppingListRepo, UserRepo
from datetime import datetime

class UserService:
    def __init__(self):
        self.user_repo = UserRepo()

    def register_user(self, username: str, password: str, email: str, birthday: str):
        if not username or not password or not email or not birthday:
            raise ValueError("All fields are required")

        try:
            datetime.strptime(birthday, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid birthday format. Use YYYY-MM-DD.")
        
        if self.user_repo.username_exists(username):
            raise ValueError("User already exists")

        self.user_repo.create(username, password, email, birthday)

    def login_user(self, username: str, password: str):
        if not username or not password:
            raise ValueError("Username and password are required")

        if not self.user_repo.authenticate_user(username, password):
            raise ValueError("Incorrect username or password")

        # Here, you can add more logic like generating a token or managing sessions
        return True
        
    def get_user_settings(self, username: str):
        user = self.user_repo.get(username)
        return {
            'username': user.username,
            'email': user.email,
            'birthday': user.birthday,
            'allergies': user.allergies,
            'diets': user.diets,
            'intolerances': user.intolerances,
        }

    def update_user_settings(self, username: str, data: dict):
        user = self.user_repo.get(username)
        if 'email' in data:
            user.email = data['email']
        if 'birthday' in data:
            user.birthday = data['birthday']
        if 'allergies' in data:
            user.allergies = data['allergies']
        if 'diets' in data:
            user.diets = data['diets']
        if 'intolerances' in data:
            user.intolerances = data['intolerances']

        return user
    
class ShoppingListService:
    def __init__(self):
        self.list_repo = ShoppingListRepo()

    def create_list(self, userid: str, name: str): #create
        if not userid or not name:
            raise ValueError("All fields are required")

        self.list_repo.create(userid, name)
        
    def get_list_info(self, userid: str, listid: str):
        list = self.list_repo.get(userid, listid)
        return {
            'name': list.name
        }

    def change_listname(self, userid: str, listid: str, newname: str):
        self.list_repo.change_name(userid, listid, newname)

        return {
            'name': newname,
        }
        
    def delete_list(self, userid: str, listid: str):
        self.list_repo.delete(userid, listid)
    