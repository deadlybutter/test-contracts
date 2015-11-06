import os
from test_contracts.models import User
from test_contracts.extensions import db, user_datastore

if os.environ.get("TESTIE_ENV") == 'prod':
    User.create(username='contractor',
                password='$pbkdf2-sha512$25000$QUiJUWqt9d5b6x1jjPG.Vw$hIbPLVxpLq3seWMO1VmgJZmcDA6Vn58IjvoPl6cQq9w6knjApao9VDIDn7z2Ek6d7ujWp3bcaS/BSzPveaCoZg',
                active=1, email='contractor@test.com')
    User.create(username='employee',
                password='$pbkdf2-sha512$25000$QUiJUWqt9d5b6x1jjPG.Vw$hIbPLVxpLq3seWMO1VmgJZmcDA6Vn58IjvoPl6cQq9w6knjApao9VDIDn7z2Ek6d7ujWp3bcaS/BSzPveaCoZg',
                active=1, email='employee@test.com')
    User.create(username='arbiter',
                password='$pbkdf2-sha512$25000$QUiJUWqt9d5b6x1jjPG.Vw$hIbPLVxpLq3seWMO1VmgJZmcDA6Vn58IjvoPl6cQq9w6knjApao9VDIDn7z2Ek6d7ujWp3bcaS/BSzPveaCoZg',
                active=1, email='arbiter@test.com')
    User.create(username='staff',
                password='$pbkdf2-sha512$25000$QUiJUWqt9d5b6x1jjPG.Vw$hIbPLVxpLq3seWMO1VmgJZmcDA6Vn58IjvoPl6cQq9w6knjApao9VDIDn7z2Ek6d7ujWp3bcaS/BSzPveaCoZg',
                active=1, email='staff@test.com')
    User.create(username='admin',
                password='$pbkdf2-sha512$25000$QUiJUWqt9d5b6x1jjPG.Vw$hIbPLVxpLq3seWMO1VmgJZmcDA6Vn58IjvoPl6cQq9w6knjApao9VDIDn7z2Ek6d7ujWp3bcaS/BSzPveaCoZg',
                active=1, email='admin@test.com')
else:
    User.create(username='contractor',
                password='$pbkdf2-sha512$25000$CWGMce7dm9M6h9AaIyRE6A$6MOGbjOZh6kldpUe0Vh5zinpxq1Nre2rjiltb8E6GxVmNC6oWlkU715pH7V8R0ziRAeuQBaxop20atEqvhz5gA',
                active=1, email='contractor@test.com')
    User.create(username='employee',
                password='$pbkdf2-sha512$25000$CWGMce7dm9M6h9AaIyRE6A$6MOGbjOZh6kldpUe0Vh5zinpxq1Nre2rjiltb8E6GxVmNC6oWlkU715pH7V8R0ziRAeuQBaxop20atEqvhz5gA',
                active=1, email='employee@test.com')
    User.create(username='arbiter',
                password='$pbkdf2-sha512$25000$CWGMce7dm9M6h9AaIyRE6A$6MOGbjOZh6kldpUe0Vh5zinpxq1Nre2rjiltb8E6GxVmNC6oWlkU715pH7V8R0ziRAeuQBaxop20atEqvhz5gA',
                active=1, email='arbiter@test.com')
    User.create(username='staff',
                password='$pbkdf2-sha512$25000$CWGMce7dm9M6h9AaIyRE6A$6MOGbjOZh6kldpUe0Vh5zinpxq1Nre2rjiltb8E6GxVmNC6oWlkU715pH7V8R0ziRAeuQBaxop20atEqvhz5gA',
                active=1, email='staff@test.com')
    User.create(username='admin',
                password='$pbkdf2-sha512$25000$CWGMce7dm9M6h9AaIyRE6A$6MOGbjOZh6kldpUe0Vh5zinpxq1Nre2rjiltb8E6GxVmNC6oWlkU715pH7V8R0ziRAeuQBaxop20atEqvhz5gA',
                active=1, email='admin@test.com')

users = User.query.all()

for user in users:
    if user.username == 'contractor':
        role = user_datastore.find_role('Contractor')
        user_datastore.add_role_to_user(user, role)
    elif user.username == 'employee':
        role = user_datastore.find_role('Employee')
        user_datastore.add_role_to_user(user, role)
    elif user.username == 'arbiter':
        role = user_datastore.find_role('Arbiter')
        user_datastore.add_role_to_user(user, role)
    elif user.username == 'staff':
        role = user_datastore.find_role('Staff')
        user_datastore.add_role_to_user(user, role)
    elif user.username == 'admin':
        role = user_datastore.find_role('Admin')
        user_datastore.add_role_to_user(user, role)
    db.session.commit()