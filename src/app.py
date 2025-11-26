from flask import Flask, render_template, request, redirect, url_for
from varasto import Varasto

app = Flask(__name__)

# Store warehouses in memory with id, name, and Varasto object
warehouses = {}
next_id = 1


def get_next_id():
    global next_id # pylint: disable=global-statement
    current_id = next_id
    next_id += 1
    return current_id


@app.route('/')
def index():
    return render_template('index.html', warehouses=warehouses)


@app.route('/warehouse/create', methods=['GET', 'POST'])
def create_warehouse():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        try:
            capacity = float(request.form.get('capacity', 0))
        except ValueError:
            capacity = 0

        if name and capacity > 0:
            warehouse_id = get_next_id()
            warehouses[warehouse_id] = {
                'id': warehouse_id,
                'name': name,
                'varasto': Varasto(capacity)
            }
            return redirect(url_for('index'))

        return render_template(
            'create.html',
            error='Please provide a valid name and capacity'
        )

    return render_template('create.html')


@app.route('/warehouse/<int:warehouse_id>')
def view_warehouse(warehouse_id):
    warehouse = warehouses.get(warehouse_id)
    if not warehouse:
        return redirect(url_for('index'))
    return render_template('view.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/edit', methods=['GET', 'POST'])
def edit_warehouse(warehouse_id):  # pylint: disable=too-many-statements
    warehouse = warehouses.get(warehouse_id)
    if not warehouse:
        return redirect(url_for('index'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        try:
            capacity = float(request.form.get('capacity', 0))
        except ValueError:
            capacity = 0

        if name and capacity > 0:
            old_saldo = warehouse['varasto'].saldo
            warehouse['name'] = name
            new_saldo = min(old_saldo, capacity)
            warehouse['varasto'] = Varasto(capacity, new_saldo)
            return redirect(
                url_for('view_warehouse', warehouse_id=warehouse_id)
            )

        return render_template(
            'edit.html',
            warehouse=warehouse,
            error='Please provide a valid name and capacity'
        )

    return render_template('edit.html', warehouse=warehouse)


@app.route('/warehouse/<int:warehouse_id>/delete', methods=['POST'])
def delete_warehouse(warehouse_id):
    if warehouse_id in warehouses:
        del warehouses[warehouse_id]
    return redirect(url_for('index'))


@app.route('/warehouse/<int:warehouse_id>/add', methods=['POST'])
def add_to_warehouse(warehouse_id):
    warehouse = warehouses.get(warehouse_id)
    if warehouse:
        try:
            amount = float(request.form.get('amount', 0))
        except ValueError:
            amount = 0

        if amount > 0:
            warehouse['varasto'].lisaa_varastoon(amount)

    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


@app.route('/warehouse/<int:warehouse_id>/remove', methods=['POST'])
def remove_from_warehouse(warehouse_id):
    warehouse = warehouses.get(warehouse_id)
    if warehouse:
        try:
            amount = float(request.form.get('amount', 0))
        except ValueError:
            amount = 0

        if amount > 0:
            warehouse['varasto'].ota_varastosta(amount)

    return redirect(url_for('view_warehouse', warehouse_id=warehouse_id))


if __name__ == '__main__':
    app.run()
