from flask import Flask, render_template
import json
import os

app = Flask(static_folder=os.path.abspath("../data"), import_name=__name__)
IMAGES = os.path.join('../data', 'images')
app.config['UPLOAD_FOLDER'] = IMAGES



@app.route('/')
def main():
    return render_template('main.html')


@app.route('/logs')
def log():
    logs = []
    with open('../.logs', 'r') as reader:
        logs = reader.readlines()
    return render_template('logs.html', logs=logs)


@app.route('/users')
def users():
    names = []
    admins = []
    with open('../configs.json', 'r') as reader:
        configs = json.load(reader)
        admins = configs['admin_users']
    with open('../data/names.json', 'r') as reader:
        names = json.load(reader)

    images_names = []
    dir_path = '../data/images'
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            images_names.append(path)
    data = {}
    for img in images_names:
        _id = img.split('_')[0]
        if _id not in data:
            data[_id] = {'images': []}
        # data[_id]['images'].append(img)
        data[_id]['images'].append(os.path.join(app.config['UPLOAD_FOLDER'], img))
        data[_id]['name'] = names[_id] if _id in names else '-'
        data[_id]['role'] = 'Adminstrator' if _id in admins else 'User'
    return render_template('users.html', users=data)
