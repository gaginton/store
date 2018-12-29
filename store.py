from bottle import route, run, template, static_file, get, post, delete, request
import bottle
import os
from sys import argv
import json
import pymysql

bottle.TEMPLATE_PATH.insert(0,os.path.dirname(os.path.abspath(__file__)))

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='store',
                             charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)

# LOAD ALL THE PAGES
@get("/admin")
def admin_portal():
	return template("pages/admin.html")

@get("/")
def index():
    return template("index.html")

@get('/js/<filename:re:.*\.js>')
def javascripts(filename):
    return static_file(filename, root='js')

@get('/css/<filename:re:.*\.css>')
def stylesheets(filename):
    return static_file(filename, root='css')

@get('/images/<filename:re:.*\.(jpg|png|gif|ico)>')
def images(filename):
    return static_file(filename, root='images')



# WHERE CODE ADDED BEGINS

# CREATING A CATEGORY
@post("/category")
def create_category():
    new_cat = request.forms.get('name')
    if not new_cat:
        return json.dumps({"STATUS": "ERROR", "MSG": "Category name missing", "cat_id": None, "CODE": 400})
    try:
        with connection.cursor() as cursor:
            search_for_cat = """SELECT cat_name FROM category"""
            cursor.execute(search_for_cat)
            category_list = cursor.fetchall()

            for cat in category_list:
                if new_cat == cat[""]:
                    return json.dumps(
                        {"STATUS": "ERROR", "MSG": "Category already exists. Please enter something unique", "cat_id": cat, "CODE": 200})

                else:
                    add_category = "INSERT INTO category VALUES('{}')".format(new_cat)
                    cursor.execute(add_category)
                    newest_id = cursor.lastrowid
                    connection.commit()         #commits changes so it can be seen in database
                    return json.dumps(
                    {"STATUS": "SUCCESS", "MSG": "Category created successfully", "cat_id": newest_id, "CODE": 201})
                                        #should close connection to database with connection.close()
    except:
        return json.dumps({"STATUS": "ERROR", "MSG": "Internal error", "cat_id": None, "CODE": 500})



# DELETING A CATEGORY
@delete("/category/<catid:int>")
def delete_category(catid):
    try:
        with connection.cursor() as cursor:
            delete_cat = ('DELETE FROM category WHERE cat_id = {}'.format(catid))
            cursor.execute(delete_cat)
            connection.commit()
            return json.dumps({'STATUS': 'SUCCESS', 'MSG': 'The category was deleted successfully'})

    except:
        return json.dumps({'STATUS': 'ERROR', 'MSG': "500: Internal error"})


# LISTING CATEGORIES
@get("/categories")
def list_categories():
    try:
        with connection.cursor() as cursor:
            load_cats = "SELECT * FROM category"
            cursor.execute(load_cats)
            result = cursor.fetchall()          #list of all the categories
            return json.dumps({'STATUS': 'SUCCESS', 'CATEGORIES': result})
    except:
        return json.dumps({'STATUS' : 'ERROR', 'MSG': "500: Internal error"})



# LIST ALL PRODUCTS
@get("/products")
def load_products():
    try:
        with connection.cursor() as cursor:
            sql = ('SELECT * FROM products')
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({'STATUS': 'SUCCESS', 'PRODUCTS': result})
    except:
        return json.dumps({'STATUS': 'ERROR', 'MSG': "500: Internal error"})


# ADD AND EDIT PRODUCTS
@post("/products")
def define_product():
    product_dict = {
        "category": int(request.forms.get('category')) if request.forms.get('category') else None,
        "description": request.forms.get('description') if request.forms.get('description') else None,
        "price": int(request.forms.get('price')),
        "title": request.forms.get('title') if request.forms.get('title') else None,
        "favorite": request.forms.get('favorite') if request.forms.get('favorite') else 0,
        "img_url": request.forms.get('img_url') if request.forms.get('img_url') else None,
        "id": int(request.forms.get('id')) if request.forms.get('id') else None
    }
    if product_dict['id']:  #IF PRODUCT ID EXISTS, EDIT PRODUCT
        return edit_product(product_dict)
    else:       #ADD PRODUCTS THAT DONT EXIST ALREADY
        try:
            with connection.cursor() as cursor:
                sql = 'INSERT INTO products VALUES(id,%s,%s,%s,%s,%s,%s,now())'         #now provides a unique ID based on time of entry
                data = (category, description, price, title, favorite,img_url)
                cursor.execute(sql, data)
                connection.commit()
        except:
            return json.dumps({'STATUS':'ERROR', 'MSG':"500: Error"})

def edit_product(product_dict):
    try:
        with connection.cursor() as cursor:
            sql = ('UPDATE products SET category=%s, description=%s, price=%s, title=%s, favorite=%s, img_url=%s WHERE id=%s')
            data = (category, str(description), price, str(title), favorite, str(img_url), id)
            cursor.execute(sql, data)
            connection.commit()
            return json.dumps({'STATUS': 'SUCCESS', 'MSG': 'Product was edited successfully'})
    except:
        return json.dumps({'STATUS': 'ERROR', 'MSG': "500: Error editing product"})



# GETTING PRODUCTS, GETTING PRODUCTS BY CATEGORY
@get("/product/<id:int>")
def list_all_products(id):
    try:
        with connection.cursor() as cursor:
            sql = ('SELECT * FROM products')
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({'STATUS':'SUCCESS','PRODUCTS': result})
    except:
        return json.dumps({'STATUS' : 'ERROR', 'MSG': "500: Internal error listing product"})

@get('/category/<id:int>/products')
def list_cat_products(id):
    try:
        with connection.cursor() as cursor:
            sql = ('SELECT * FROM products WHERE category = {} ORDER BY favorite DESC, creation_date ASC'.format(id) )
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({'STATUS':'SUCCESS','PRODUCTS': result})
    except:
        return json.dumps({'STATUS':'ERROR', 'MSG': "500: Internal error retrieving products"})


# DELETING PRODUCTS
@delete('/product/<id:int>')
def delete_product(id):
    try:
        with connection.cursor() as cursor:
            sql = ('DELETE FROM products WHERE id = {}'.format(id))
            cursor.execute(sql)
            connection.commit()
            return json.dumps({'STATUS':'SUCCES', 'MSG': "Product was deleted successfully"})
    except:
        return json.dumps({'STATUS' : 'ERROR', 'MSG': "500: Internal error while deleting product"})


# LIST ALL PRODUCTS BY CATEGORY
@get('/category/<catid>/products')
def list_products_cat(id):
    try:
        with connection.cursor() as cursor:
            sql = ('SELECT category, description, price, title, favorite, img_url, id FROM products WHERE category = {} ORDER BY favorite DESC, creation_date ASC'.format(catid) )
            cursor.execute(sql)
            result = cursor.fetchall()
            return json.dumps({'STATUS':'SUCCESS','PRODUCTS': result})
    except:
        return json.dumps({'STATUS':'ERROR', 'MSG': "Internal error"})


if __name__ == "__main__":
    run(host='localhost', port=7000)