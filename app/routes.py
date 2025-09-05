from flask import Blueprint, jsonify, request
from sqlalchemy import asc, desc
from . import db
from .models import Order, OrderItem

bp = Blueprint('api', __name__)

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

def _calc_total(items):
    return round(sum(float(i.get('price', 0)) * int(i.get('quantity', 1)) for i in items), 2)

# ----------------- ORDERS CRUD -----------------
@bp.route('/orders', methods=['GET'])
def list_orders():
    status = request.args.get('status')
    sort = request.args.get('sort', 'created_at')
    order = request.args.get('order', 'desc')
    page = int(request.args.get('page', 1))
    per_page = min(int(request.args.get('per_page', 10)), 50)

    query = Order.query
    if status:
        query = query.filter(Order.status == status)

    sort_col = getattr(Order, sort, Order.created_at)
    query = query.order_by(desc(sort_col) if order == 'desc' else asc(sort_col))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    orders = [o.to_dict() for o in pagination.items]
    return jsonify({
        'items': orders,
        'page': page,
        'per_page': per_page,
        'total': pagination.total,
        'pages': pagination.pages
    }), 200

@bp.route('/orders/<int:oid>', methods=['GET'])
def get_order(oid):
    order = Order.query.get_or_404(oid)
    return jsonify(order.to_dict()), 200

@bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json(force=True) or {}
    customer = data.get('customer', {})
    items = data.get('items', [])

    if not items:
        return jsonify({'error': 'items is required'}), 400
    if not customer.get('name') or not customer.get('email'):
        return jsonify({'error': 'customer.name and customer.email are required'}), 400

    order = Order(
        customer_name=customer.get('name'),
        customer_email=customer.get('email'),
        cep=customer.get('cep'),
        address=customer.get('address'),
        status=data.get('status', 'pending'),
        total=_calc_total(items)
    )
    db.session.add(order)
    db.session.flush()

    for it in items:
        item = OrderItem(
            order_id=order.id,
            product_id=int(it.get('productId', 0)),
            title=it.get('title', ''),
            price=float(it.get('price', 0.0)),
            quantity=int(it.get('quantity', 1)),
        )
        db.session.add(item)

    db.session.commit()
    return jsonify({'message': 'order created', 'order': order.to_dict()}), 201

@bp.route('/orders/<int:oid>', methods=['PUT'])
def update_order(oid):
    order = Order.query.get_or_404(oid)
    data = request.get_json(force=True) or {}

    if 'status' in data:
        order.status = data['status']

    if 'customer' in data:
        c = data['customer'] or {}
        if 'name' in c: order.customer_name = c['name']
        if 'email' in c: order.customer_email = c['email']
        if 'cep' in c: order.cep = c['cep']
        if 'address' in c: order.address = c['address']

    if 'items' in data:
        for itm in list(order.items):
            db.session.delete(itm)
        db.session.flush()
        for it in data['items'] or []:
            item = OrderItem(
                order_id=order.id,
                product_id=int(it.get('productId', 0)),
                title=it.get('title', ''),
                price=float(it.get('price', 0.0)),
                quantity=int(it.get('quantity', 1)),
            )
            db.session.add(item)
        order.total = _calc_total(data['items'] or [])

    db.session.commit()
    return jsonify({'message': 'order updated', 'order': order.to_dict()}), 200

@bp.route('/orders/<int:oid>', methods=['DELETE'])
def delete_order(oid):
    order = Order.query.get_or_404(oid)
    db.session.delete(order)
    db.session.commit()
    return jsonify({'message': 'order deleted'}), 200

# ----------------- REPORT -----------------
@bp.route('/reports/sales', methods=['GET'])
def sales_report():
    from sqlalchemy import func
    rows = db.session.query(Order.status, func.count(Order.id), func.sum(Order.total)).group_by(Order.status).all()
    report = [{'status': r[0], 'count': int(r[1]), 'amount': float(r[2] or 0.0)} for r in rows]
    return jsonify({'report': report}), 200
