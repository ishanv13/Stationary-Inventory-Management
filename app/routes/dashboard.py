from flask import Blueprint, render_template
from flask_login import login_required
from ..models import Item, Category

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def dashboard():
    items = Item.query.all()
    categories = Category.query.all()
    total_value = sum(item.quantity * item.price for item in items)
    low_stock_items = [item for item in items if item.quantity < 10]
    category_names = [cat.name for cat in categories]
    category_stock_values = [sum(item.quantity * item.price for item in cat.items) for cat in categories]
    return render_template(
        'dashboard.html',
        items=items,
        categories=categories,
        total_value=total_value,
        low_stock_items=low_stock_items,
        category_names=category_names,
        category_stock_values=category_stock_values
    ) 