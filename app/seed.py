from . import create_app, db
from .models import User, Category, Item

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    # Create categories
    categories = [
        Category(name='Writing Tools'),
        Category(name='Papers'),
        Category(name='Art Supplies'),
        Category(name='Office Essentials')
    ]
    db.session.add_all(categories)
    db.session.commit()

    # Create items
    items = [
        Item(name='Ballpoint Pen', quantity=50, price=0.5, category_id=categories[0].id),
        Item(name='Gel Pen', quantity=30, price=0.8, category_id=categories[0].id),
        Item(name='A4 Paper Pack', quantity=20, price=3.0, category_id=categories[1].id),
        Item(name='Sketchbook', quantity=15, price=5.0, category_id=categories[2].id),
        Item(name='Stapler', quantity=8, price=2.5, category_id=categories[3].id),
        Item(name='Highlighter', quantity=12, price=1.2, category_id=categories[0].id)
    ]
    db.session.add_all(items)
    db.session.commit()

    # Create admin user
    admin = User(username='admin', is_admin=True)
    admin.set_password('admin123')
    db.session.add(admin)
    db.session.commit()

    print('Database seeded with sample data.') 