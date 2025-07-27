from flask import Blueprint, render_template, redirect, url_for, flash, request, send_file
from flask_login import login_required
from ..models import Item, Category
from .. import db
from ..utils.csv_export import export_items_csv
from ..utils.barcode import generate_barcode

inventory_bp = Blueprint('inventory', __name__)

@inventory_bp.route('/')
@login_required
def inventory():
    search = request.args.get('search', '')
    category_id = request.args.get('category', type=int)
    query = Item.query
    if search:
        query = query.filter(Item.name.ilike(f'%{search}%'))
    if category_id:
        query = query.filter_by(category_id=category_id)
    items = query.all()
    categories = Category.query.all()
    return render_template('inventory.html', items=items, categories=categories, search=search, category_id=category_id)

@inventory_bp.route('/item/add', methods=['POST'])
@login_required
def add_item():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    category_id = int(request.form['category_id'])
    item = Item(name=name, quantity=quantity, price=price, category_id=category_id)
    db.session.add(item)
    db.session.commit()
    flash('Item added!', 'success')
    return redirect(url_for('inventory.inventory'))

@inventory_bp.route('/item/<int:item_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_item(item_id):
    item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        item.name = request.form['name']
        item.quantity = int(request.form['quantity'])
        item.price = float(request.form['price'])
        item.category_id = int(request.form['category_id'])
        db.session.commit()
        flash('Item updated!', 'success')
        return redirect(url_for('inventory.inventory'))
    categories = Category.query.all()
    return render_template('edit_item.html', item=item, categories=categories)

@inventory_bp.route('/item/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted!', 'info')
    return redirect(url_for('inventory.inventory'))

@inventory_bp.route('/export/csv')
@login_required
def export_csv():
    return export_items_csv()

@inventory_bp.route('/item/<int:item_id>/barcode')
@login_required
def barcode(item_id):
    item = Item.query.get_or_404(item_id)
    return generate_barcode(item) 