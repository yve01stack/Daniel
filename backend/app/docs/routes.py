from flask import render_template, url_for
from app.docs import bp


@bp.route('/')
def docs():
    # print(url_for('docs.docs', _external=True))
    return render_template('docs.html', title='API Documentation', year=2024)

@bp.route('/docs/auth')
def docs_auth():
    return render_template('docs_auth.html', title='Auth API Documentation', year=2024)

@bp.route('/docs/product')
def docs_product():
    return render_template('docs_product.html', title='Product API Documentation', year=2024)

@bp.route('/docs/admin')
def docs_admin():
    return render_template('docs_admin.html', title='Admin API Documentation', year=2024)