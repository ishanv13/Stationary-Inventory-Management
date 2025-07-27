import io
import csv
from flask import send_file
from ..models import Item, Category
from .. import db

def export_items_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Category', 'Quantity', 'Price'])
    items = Item.query.all()
    for item in items:
        writer.writerow([
            item.id,
            item.name,
            item.category.name if item.category else '',
            item.quantity,
            item.price
        ])
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='inventory.csv'
    ) 