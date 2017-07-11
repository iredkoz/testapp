from flask import redirect, render_template, url_for, flash, abort

from . import finance

@finance.route('/finances')
def finance_main():
    return render_template('financeapp/financeapp.html')
