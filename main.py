from flask import Flask, jsonify
import json
from ldap3 import Server, Connection, SUBTREE

app = Flask(__name__)
port = 5000

LDAP_SERVER = '127.0.0.1:389'
LDAP_BIND_DN = 'cn=admin,dc=example,dc=org'
LDAP_BIND_PASSWORD = 'admin'
LDAP_SEARCH_BASE = 'ou=users,dc=example,dc=org'


def getUserByName(username):
    server = Server(LDAP_SERVER)
    conn = Connection(server, user=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD, auto_bind=True)

    search_filter = f'(uid={username})'
    conn.search(search_base=LDAP_SEARCH_BASE, search_filter=search_filter, search_scope=SUBTREE,
                attributes=['*'])
    user = {}
    if conn.entries:
        for entry in conn.entries:
            for key, val in entry.entry_attributes_as_dict.items():
                if key in user:
                    user[key].extend(val)
                else:
                    if key in 'userPassword':
                        user[key] = str(val).split("\'")[1]
                    else:
                        user[key] = val
    if user:
        return user
    else:
        return None


@app.route('/user/<username>')
def get_user(username):
    try:
        user = getUserByName(username)
        json_data = json.loads(json.dumps(user))
        if user:
            return {'data': json_data, 'error': ''}
        else:
            return jsonify({'data': None, 'error': 'User not found'})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'data': None, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
