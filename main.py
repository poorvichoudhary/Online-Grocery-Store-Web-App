from sqlite3 import Connection
from typing import List, Any
from flask import Flask, render_template, request,jsonify, redirect
import sqlite3
app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():   #log in if credentials are correct else stay on the same page
    if request.method == 'POST':
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        username = request.form['username']
        password = request.form['password']
        query = "SELECT username, password FROM userdata where username='" + username + "' and password='" + password + "'"
        cursor.execute(query)
        result = cursor.fetchall()
        if len(result) == 0:
            return "incorrect"
        else:
            return render_template('home.html')
    return render_template('login.html')


@app.route('/register', methods=['GET','POST']) #registration for new users and directly log them in dashboard
def register():
    flag = False
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            address=request.form['address']
            if not username or not password:
                return render_template('login.html')
            else:
                with sqlite3.connect("users.db") as con:  #insert new data into userdata table
                    cur = con.cursor()
                    cur.execute("INSERT INTO userdata (username, password,address) VALUES (?,?,?)",(username, password,address))
                    flag = True
                    con.commit()
        except:
            con.rollback()
        finally:
            if flag == True:
                return render_template('login.html')
            else:
                return render_template('register.html')
    return render_template('register.html')


@app.route('/adminlogin', methods=['GET', 'POST']) #login for admin using predefined credentials
def adminlogin():
    if request.method == 'POST':
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        adname = request.form['adname']
        password = request.form['password']
        cursor = connection.execute('select * from admin where adname="%s" and password="%s"'% (adname, password))
        if cursor.fetchone():
            return render_template('adminhome.html')  #if password is correct they are directed to home page else login only
        else:
            return render_template('adminlogin.html')
        connection.commit()
    return render_template('adminlogin.html')


@app.route('/managecategory', methods=['GET','POST'])
def categorymanage():  #redirects to the page where admin can perform CRUD on categories
    return render_template('managecategory.html')


@app.route('/adminhome')
def adminhome(): #redirect to admin dashboard
    return render_template('adminhome.html')


@app.route('/addcategory',methods=['GET','POST']) #redirects to page where you can add new categories
def addcategories():
    if request.method=='POST':
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cname=request.form.get('cname')
        cid=request.form.get('cid')
        cursor.execute("INSERT INTO category VALUES (?,?)",(cname,cid))
        connection.commit()
        return render_template('managecategory.html')
    return render_template('addcategory.html')


@app.route('/deletecategory',methods=["GET","POST"])
def deletecategory():
    if request.method == 'POST':
        cid = request.form['cid']
        confirmation = request.form.get('confirmation')

        if confirmation == 'yes':  # If the admin confirmed the deletion
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM category WHERE cid=?", (cid,))
            connection.commit()
            connection.close()
            return render_template('managecategory.html', deleted=True)  # Pass a flag to indicate that product is deleted
        else:
            # If the admin didn't confirm, redirect back to the "manageproduct.html" page
            return render_template('managecategory.html')

    return render_template('deletecategory.html')

@app.route('/updatecategory',methods=["GET","POST"])
def updatecategory(): #update name of an existing category which has the cid entered by admin in form along with new name
    if request.method=='POST':
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cid=request.form.get('cid')
        cname=request.form.get('cname')
        cursor.execute("update category set cname=? where cid=?",(cname,cid))
        connection.commit()
        return render_template('managecategory.html')
    return render_template('updatecategory.html')


@app.route('/readcategory',methods=["GET","POST"])
def readcategory(): #all values from table category
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("select * from category")
    rows=cursor.fetchall()
    l=[]
    for row in rows:
        l.append(row)
    return(l)
    return render_template('readcategory.html')


@app.route('/addproduct',methods=["GET","POST"])
def addproduct(): #add a new product with all its values as provided by admin in form
    if request.method == 'POST':
        pname=request.form.get('pname')
        pid=request.form.get('pid')
        price=request.form.get('price')
        cid=request.form.get('cid')
        quantity=request.form.get('quantity')
        max_quantity=request.form.get('max_quantity')
        manufacturing_date=request.form.get('manufacturing_date')
        with sqlite3.connect('users.db') as con:
            cursor=con.cursor()
            cursor.execute("INSERT INTO product VALUES (?,?,?,?,?,?,?)",(pname,pid,price,cid,quantity,max_quantity,manufacturing_date))
            con.commit()
            return render_template('manageproduct.html')
    return render_template('addproduct.html')

@app.route('/deleteproduct', methods=["GET", "POST"])
def deleteproduct():
    if request.method == 'POST':
        pid = request.form['pid']
        confirmation = request.form.get('confirmation')

        if confirmation == 'yes':  # If the admin confirmed the deletion
            connection = sqlite3.connect('users.db')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM product WHERE pid=?", (pid,))
            connection.commit()
            connection.close()
            return render_template('manageproduct.html', deleted=True)  # Pass a flag to indicate that product is deleted
        else:
            # If the admin didn't confirm, redirect back to the "manageproduct.html" page
            return redirect('/manageproduct')

    return render_template('deleteproduct.html')


@app.route('/updateproduct',methods=["GET","POST"])
def updateproduct(): #update the price of a product by entering its new price and pid
    if request.method=='POST':
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        price=request.form['price']
        pid=request.form['pid']
        cursor.execute("update product set price=? where pid=?",[price,pid])
        connection.commit()
        return render_template('manageproduct.html')
    return render_template('updateproduct.html')


@app.route('/readproduct',methods=["GET","POST"])
def readproduct(): #all values from product
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute("select * from product")
    rows=cursor.fetchall()
    l=[]
    for row in rows:
        l.append(row)
    return(l)
    return render_template('readproduct.html')


@app.route('/manageproduct',methods=['GET','POST']) #manage products page where crud operations are there
def manageproduct():
    return render_template('manageproduct.html')



def preprocess_data(data):
    categories = {}
    for item in data:
        category = item[0]
        product_info = item[1:]

        if category not in categories:
            categories[category] = []
        categories[category].append(product_info)
    return categories.items()


@app.route('/userhome',methods=['GET','POST']) #after correct login by user they will be redirected to this page
def userhome():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    username = request.form['username']
    password = request.form['password']
    query = "SELECT username, password FROM userdata where username='" + username + "' and password='" + password + "'"
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) == 0:
        return "<html><h1>incorrect</h1></html>"
    else:
        with sqlite3.connect('users.db') as conn:
            cursor = conn.cursor()
            cursor.execute('select category.cname,product.pname,product.price from category,product where product.cid=category.cid')
            rows=cursor.fetchall()
            l=[]
            for row in rows:
                l.append(row)
            lp=preprocess_data(l)
            return render_template('home.html', lp=lp, username=username)


@app.route('/addtocart', methods=['POST'])
def addtocart():
    con = sqlite3.connect('users.db')
    cursor = con.cursor()
    # Get the user's name from the form
    username = request.form.get('username')
    total_sum=0
    cursor.execute('delete from order1 where username=?',(username,))
    for key, value in request.form.items():
        if key.startswith('quantity_') and value.isdigit():
            quantity = int(value)
            if quantity > 0 :  # Add to order1 only if quantity is greater than 0
                pname = request.form.get(f'pname_{key[9:]}')
                price = request.form.get(f'price_{key[9:]}')
                cursor.execute('SELECT quantity FROM product WHERE pname = ?', (pname,))
                available_stock = cursor.fetchone()[0]
                if quantity > available_stock:
                # If the entered quantity is greater than available stock, show a message
                    return f"{quantity} quantity is not available. Only {available_stock} units are available for {pname}."

                cursor.execute('insert into order1 (username,pname,price,quantity) values (?, ?, ?, ?)',(username,pname, price,quantity))
                total_sum+=int(price)*quantity
    con.commit()
    cursor.execute('SELECT * FROM order1 WHERE username=?', (username,))
    rows=cursor.fetchall()
    lp=[]
    for row in rows:
        lp.append(row)
    lp=preprocess_data(lp)

    return render_template('view.html', lp=lp, username=username, total_sum=total_sum)


@app.route('/place', methods=['GET','POST'])
def  placeorder():
    return render_template('orderplace.html')

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search_query', '')  # Get the search query from the URL parameter
    search_option = request.args.get('search_option', 'product_name')  # Get the search option from the URL parameter

    # Connect to the database
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    # Perform the search based on the selected search option
    if search_option == 'product_name':
        cursor.execute("SELECT pname, quantity, price FROM product WHERE pname LIKE ?", ('%' + search_query + '%',))
    elif search_option == 'category_name':
        cursor.execute("SELECT product.pname, product.quantity, product.price FROM product INNER JOIN category ON product.cid = category.cid WHERE category.cname LIKE ?", ('%' + search_query + '%',))
    elif search_option == 'price':
        cursor.execute("SELECT pname, quantity, price FROM product WHERE price = ?", (search_query,))
    elif search_option == 'manufacturing_date':
        cursor.execute("SELECT pname, quantity, price FROM product WHERE manufacturing_date = ?", (search_query,))

    search_results = cursor.fetchall()
    connection.close()

    # Render the search results on the separate search template
    return render_template('search.html', search_results=search_results, search_query=search_query, search_option=search_option)


if __name__=='__main__':
    app.run(debug = True)
