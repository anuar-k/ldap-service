from flask import Flask, jsonify

from ldap3 import Server, Connection, SUBTREE

app = Flask(__name__)
port = 5000

LDAP_SERVER = '127.0.0.1:389'
LDAP_BIND_DN = 'cn=admin,dc=example,dc=org'
LDAP_BIND_PASSWORD = 'admin'
LDAP_SEARCH_BASE = 'ou=users,dc=example,dc=org'


def getUserByName(username):
    # try:
    server = Server(LDAP_SERVER)
    conn = Connection(server, user=LDAP_BIND_DN, password=LDAP_BIND_PASSWORD, auto_bind=True)

    # Search for the user by username
    search_filter = f'(uid={username})'
    conn.search(search_base=LDAP_SEARCH_BASE, search_filter=search_filter, search_scope=SUBTREE,
                attributes=['*'])
    # attributes=['uid', 'cn', 'sn', 'homeDirectory'])

    user = {}
    if conn.entries:
        for entry in conn.entries:
            for key, val in entry.entry_attributes_as_dict.items():
                # print(str(key) + ' : ' + str(val))
                if key in user:
                    user[key].extend(val)
                else:
                    user[key] = val
    return str(user)


@app.route('/user/<username>')
def get_user(username):
    try:
        user = getUserByName(username)

        if user:
            return jsonify({'data': user, 'error': ''})
        else:
            return jsonify({'data': {}, 'error': 'User not found'})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({'data': {}, 'error': str(e)})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
