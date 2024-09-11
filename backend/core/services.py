# services.py
from .repositories import UserRepo
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
        
        if self.user_repo.user_exists(username):
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
    
class ListService:
    def __init__(self):
        self.list_repo = ShoppingListRepo()

    def create_list(self, listname: str, lid: int): #create
        if not listname or not lid:
            raise ValueError("All fields are required")
        
        if self.list_repo.list_exists(listname, lid):
            raise ValueError("User already exists")

        self.list_repo.create(listname, lid)
        
    def get_list_info(self, listname: str):
        list = self.list_repo.get(listname)
        return {
            'listname': list.listname,
            'lid': list.lid,
        }

    def change_listname(self, listname: str, newname: str):
        list = self.list_repo.get(listname)
        keys = self.list_repo.get_names()
        
        if newname in keys:
            raise ValueError("List Already Exist")
        
        self.list_repo.change_name(list.lid, newname)

        return {
            'listname': list.listname,
            'lid': list.lid,
        }
        
    def delete_list(self, listname: str):
        list = self.list_repo.get(listname)
        self.list.remove(list)
    