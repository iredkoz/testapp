from flask import redirect, render_template, url_for, flash, abort
from calendar import Calendar
from datetime import date

from . import finance

@finance.route('/finances')
def finance_main():
    cal = Calendar(0)
    return render_template('financeapp/financeapp.html')
