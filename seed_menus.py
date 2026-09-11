from app import create_app
from app.models import db, Menu, RoleMenu

app = create_app()


with app.app_context():

    menus = [
        {
            "name": "Dashboard",
            "endpoint": "dashboard.dashboard",
            "active_prefix": "dashboard",
            "icon": "bi-speedometer2",
            "order": 1,
            "roles": ["Admin", "Librarian", "Member"],
        },
        {
            "name": "Books",
            "endpoint": "book.books",
            "active_prefix": "book",
            "icon": "bi-book",
            "order": 2,
            "roles": ["Admin", "Librarian"],
        },
        {
            "name": "Members",
            "endpoint": "member.members",
            "active_prefix": "member",
            "icon": "bi-people",
            "order": 3,
            "roles": ["Admin", "Librarian"],
        },
        {
            "name": "Issued Books",
            "endpoint": "transaction.issued_books",
            "active_prefix": "transaction.issued_books",
            "icon": "bi-journal-check",
            "order": 4,
            "roles": ["Admin", "Librarian"],
        },
        {
            "name": "Issue Book",
            "endpoint": "transaction.issue_book",
            "active_prefix": "transaction.issue_book",
            "icon": "bi-journal-plus",
            "order": 5,
            "roles": ["Admin", "Librarian"],
        },
        {
            "name": "Users",
            "endpoint": "user.users",
            "active_prefix": "user",
            "icon": "bi-person-gear",
            "order": 6,
            "roles": ["Admin"],
        },
        {
            "name": "Categories",
            "endpoint": "book_category.list_categories",
            "active_prefix": "book_category",
            "icon": "bi-tags",
            "order": 7,
            "roles": ["Admin", "Librarian"],
        },
        {
            "name": "My Books",
            "endpoint": "member.my_books",
            "active_prefix": "member.my_books",
            "icon": "bi-book",
            "order": 2,
            "roles": ["Member"],
        },
    ]

    for menu_data in menus:

        menu = Menu.query.filter_by(menu_name=menu_data["name"]).first()

        if not menu:

            menu = Menu(
                menu_name=menu_data["name"],
                endpoint=menu_data["endpoint"],
                active_prefix=menu_data["active_prefix"],
                icon=menu_data["icon"],
                display_order=menu_data["order"],
                is_active=True,
            )

            db.session.add(menu)
            db.session.flush()

        else:

            menu.endpoint = menu_data["endpoint"]
            menu.icon = menu_data["icon"]
            menu.display_order = menu_data["order"]
            menu.is_active = True
            menu.active_prefix = menu_data["active_prefix"]

        for role in menu_data["roles"]:

            role_menu = RoleMenu.query.filter_by(
                role_name=role, menu_id=menu.id
            ).first()

            if not role_menu:

                db.session.add(RoleMenu(role_name=role, menu_id=menu.id))

    db.session.commit()

    print("Menus seeded successfully.")
