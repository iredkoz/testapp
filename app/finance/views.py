from flask import redirect, render_template, url_for, flash, abort
from calendar import Calendar
from datetime import date

from . import finance

months=["January","February","March","April","May","June",
        "July","August","September","October","November","December"]

@finance.route('/finances')
def finance_main():
    cal = Calendar(0)
    today=date.today()
    return render_template('financeapp/financeapp.html',cal=cal,today=today)
