from brackend.db.models import clear_models
from firebase_admin.auth import list_users, delete_users

if __name__ == '__main__':
    clear_models()
    users = list_users().iterate_all()
    delete_users([u.uid for u in users])
