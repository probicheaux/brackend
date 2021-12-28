from firebase_admin.auth import list_users, delete_users
import brackend

if __name__ == '__main__':
    users = list_users().iterate_all()
    delete_users([u.uid for u in users])
