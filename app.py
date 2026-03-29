from flask import Flask, render_template, request, redirect
import os, json

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

DATA_FILE = 'data.json'

def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_items(items):
    with open(DATA_FILE, 'w') as f:
        json.dump(items, f)

items = load_items()
def find_matches(new_item, items):
    matches = []

    keywords = new_item['item'].lower().split()

    for i in items:
        item_text = i['item'].lower()

        for word in keywords:
            if word in item_text:
                matches.append(i)
                break

    return matches

# ✅ HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')


# ✅ SEARCH PAGE
@app.route('/search')
def search():
    query = request.args.get('search')
    results = []

    if query:
        for i in items:
            if query.lower() in i['item'].lower():
                results.append(i)

    return render_template('search.html', items=results)


# ✅ POST (UPDATED WITH MATCHING 🔥)
@app.route('/post', methods=['GET', 'POST'])
def post():
    global items

    if request.method == 'POST':
        item = request.form.get('item')
        description = request.form.get('description')
        name = request.form.get('name')
        phone = request.form.get('phone')

        file = request.files.get('image')
        filename = ""

        if file and file.filename != "":
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        new_id = len(items) + 1

        new_data = {
            'id': new_id,
            'item': item,
            'description': description,
            'name': name,
            'phone': phone,
            'image': filename
        }

        # 🔥 FIND MATCHES BEFORE ADD
        matches = find_matches(new_data, items)

        # ADD ITEM
        items.append(new_data)
        save_items(items)

        # 🔥 SHOW MATCH PAGE
        return render_template('match.html', matches=matches, new_item=new_data)

    return render_template('post.html')


# ✅ DELETE
@app.route('/delete/<int:item_id>')
def delete(item_id):
    global items

    items = [i for i in items if i['id'] != item_id]
    save_items(items)

    return redirect('/search')


if __name__ == '__main__':
    app.run(debug=True)