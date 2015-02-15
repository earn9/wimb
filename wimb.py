#!/usr/bin/python
import sqlite3
from bottle import route, run, debug, template, request

@route('/wimb')
def wimb_list():
    conn = sqlite3.connect('wimb.sqlite')
    c = conn.cursor()
    c.execute("SELECT description, serial_no FROM wimb")
    result = c.fetchall()
    c.close()
    output = template('wimb', rows=result)
    return output

@route('/new', method='GET')
def new_item():
    if request.GET.get('save','').strip():
        item = request.GET.get('item', '').strip()
        serial_no = request.GET.get('serial_no', '').strip()
        conn = sqlite3.connect('wimb.sqlite')
        c = conn.cursor()

        c.execute("INSERT INTO wimb (description,serial_no) VALUES (?,?)", (item,serial_no))
        new_id = c.lastrowid

        conn.commit()
        c.close()

        return '<p>The new item has been added</p>'
    else:
        return template('new_item.tpl')

run(host="0.0.0.0",port=8080, debug=True, reloader=True)