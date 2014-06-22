#! venv/bin/python

import unittest
import benicio
from app import db, views, models

dbs = db.session


class BenicioTestCase(unittest.TestCase):
    def setUp(self):
        benicio.app.config['TESTING'] = True
        benicio.app.config['WTF_CSRF_ENABLED'] = False
        self.client = benicio.app.test_client()
        with self.client.session_transaction() as session:
            session['user_id'] = '1'
        admin = models.User(name='Admin', password='0cc75c328858b5d53f188ccdc0f033c9')
        dbs.add(admin)
        dbs.commit()

    def tearDown(self):
        [dbs.execute(table.delete()) for table in db.metadata.sorted_tables]
        dbs.commit()

    def test_empty_database(self):
        rv = self.client.get('/devices')
        assert 'No entries yet' in rv.data

    def test_add_rule(self):
        self.client.post('/rules', data=dict(name='Johns Rule', rule='deny out'))
        rv = self.client.get('/rules')
        assert 'Johns Rule' in rv.data
        assert 'deny out' in rv.data

    def test_add_group(self):
        self.client.post('/groups', data=dict(name='Johns Group'))
        rv = self.client.get('/groups')
        assert 'Johns Group' in rv.data

    def test_add_device(self):
        self.client.post('/groups', data=dict(name='PC Group'))
        self.client.post('/devices', data=dict(name='Johns PC', mac_address='AA:BB:CC:DD:EE', group=1))
        rv = self.client.get('/devices')
        assert 'Johns PC' in rv.data
        assert 'PC Group' in rv.data
        assert 'AA:BB:CC:DD:EE' in rv.data

    def test_delete_rule(self):
        self.client.post('/rules', data=dict(name='Johns Rule', rule='deny out'))
        self.client.delete('/api/rules/1', data=dict(id='1'))
        rv = self.client.get('/rules')
        assert 'Johns Rule' not in rv.data

    def test_delete_group(self):
        self.client.post('/groups', data=dict(name='Johns Group'))
        self.client.delete('/api/groups/1')
        rv = self.client.get('/groups')
        assert 'Johns Group' not in rv.data

    def test_delete_device(self):
        self.client.post('/groups', data=dict(name='PC Group'))
        self.client.post('/devices', data=dict(name='Johns PC', mac_address='AA:BB:CC:DD:EE', group=1))
        self.client.delete('/api/devices/1')
        rv = self.client.get('/devices')
        assert 'Johns PC' not in rv.data

    def test_edit_device(self):
        self.client.post('/groups', data=dict(name='PC Group'))
        self.client.post('/devices', data=dict(name='Johns PC', mac_address='AA:BB:CC:DD:EE', group=1))
        rv = self.client.get('/devices/1')
        assert 'Johns PC' in rv.data

    def test_edit_group(self):
        self.client.post('/groups', data=dict(name='Johns Group'))
        rv = self.client.get('/groups/1')
        assert 'Johns Group' in rv.data

    def test_edit_rule(self):
        self.client.post('/rules', data=dict(name='Johns Rule', rule='deny out'))
        rv = self.client.get('/rules/1')
        assert 'Johns Rule' in rv.data

    def test_alter_rule(self):
        self.client.post('/rules', data=dict(name='Johns Rule', rule='deny out'))
        self.client.post('/rules', data=dict(id='1', name='Other Rule', rule='deny out'))
        rv = self.client.get('/rules')
        assert 'Other Rule' in rv.data
        assert 'Johns Rule' not in rv.data

    def test_alter_device(self):
        self.client.post('/groups', data=dict(name='PC Group'))
        self.client.post('/devices', data=dict(name='Johns PC', mac_address='AA:BB:CC:DD:EE', group=1))
        self.client.post('/devices', data=dict(id='1', name='Other PC', mac_address='AA:BB:CC:DD:EE', group=1))
        rv = self.client.get('/devices')
        assert 'Other PC' in rv.data
        assert 'Johns PC' not in rv.data

    def test_load_apply_rules(self):
        self.client.post('/groups', data=dict(name='PC Group'))
        self.client.post('/devices', data=dict(name='Johns PC', mac_address='AA:BB:CC:DD:EE', group=1))
        self.client.post('/rules', data=dict(name='Johns Rule', rule='deny out'))
        rv = self.client.get('/apply')
        assert 'PC Group' in rv.data
        assert 'Johns PC' in rv.data
        assert 'Johns Rule' in rv.data

    def test_generate_rules(self):
        self.client.post('/groups', data=dict(name='PC Group'))
        self.client.post('/devices', data=dict(name='Johns PC', mac_address='37:3B:09:FC:5C:1D', group=1))
        self.client.post('/devices', data=dict(name='Johns Phone', mac_address='8E:32:62:F0:5D:38', group=1))
        self.client.post('/devices', data=dict(name='Johns Tablet', mac_address='DE:81:00:E5:32:94', group=1))
        self.client.post('/devices', data=dict(name='Johns Notebook', mac_address='DE:4C:47:55:7B:41', group=1))
        self.client.post('/rules', data=dict(name='Johns Rule', rule='deny out [MAC]'))
        self.client.post('/rules', data=dict(name='Johns Rule Exception', rule='allow in [MAC]'))
        rv = views.generate_rules([1, 2], [1, 2, 3, 4])
        assert 'deny out mac 37:3B:09:FC:5C:1D' in rv
        assert 'deny out mac 8E:32:62:F0:5D:38' in rv
        assert 'deny out mac DE:81:00:E5:32:94' in rv
        assert 'deny out mac DE:4C:47:55:7B:41' in rv
        assert 'allow in mac 37:3B:09:FC:5C:1D' in rv
        assert 'allow in mac 8E:32:62:F0:5D:38' in rv
        assert 'allow in mac DE:81:00:E5:32:94' in rv
        assert 'allow in mac DE:4C:47:55:7B:41' in rv

    def test_apply_rules(self):
        self.client.post('/groups', data=dict(name='PC Group'))
        self.client.post('/devices', data=dict(name='Johns PC', mac_address='37:3B:09:FC:5C:1D', group=1))
        self.client.post('/devices', data=dict(name='Johns Phone', mac_address='8E:32:62:F0:5D:38', group=1))
        self.client.post('/devices', data=dict(name='Johns Tablet', mac_address='DE:81:00:E5:32:94', group=1))
        self.client.post('/rules', data=dict(name='Johns Rule', rule='deny out [MAC]'))
        self.client.post('/rules', data=dict(name='Johns Rule Exception', rule='allow in [MAC]'))
        rv = self.client.post('/apply', data=dict(rule1='a', rule2='b', device1='c', device2='d', device3='e'))
        self.assertTrue('deny+out+mac+37%3A3B%3A09%3AFC%3A5C%3A1D' in rv.data)
        self.assertTrue('deny+out+mac+8E%3A32%3A62%3AF0%3A5D%3A38' in rv.data)
        self.assertTrue('deny+out+mac+DE%3A81%3A00%3AE5%3A32%3A94' in rv.data)
        self.assertTrue('allow+in+mac+37%3A3B%3A09%3AFC%3A5C%3A1D' in rv.data)
        self.assertTrue('allow+in+mac+8E%3A32%3A62%3AF0%3A5D%3A38' in rv.data)
        self.assertTrue('allow+in+mac+DE%3A81%3A00%3AE5%3A32%3A94' in rv.data)

    def test_change_password(self):
        admin = models.User(name='Admin', password='0cc75c328858b5d53f188ccdc0f033c9')
        dbs.add(admin)
        dbs.commit()
        self.client.post('/index', data=dict(current_password='bendmin', new_password='12345', retype_password='12345'))
        user_password = models.User.query.filter_by(name="Admin").first().password
        assert user_password == '827ccb0eea8a706c4c34a16891f84e7b'

    def test_login(self):
        admin = models.User(name='Admin', password='0cc75c328858b5d53f188ccdc0f033c9')
        dbs.add(admin)
        dbs.commit()
        self.client.post('/login', data=dict(user='Admin', password='bendmin'))
        rv = self.client.get('/index')
        assert 'Logged in successfully' in rv.data

    @staticmethod
    def test_gethash():
        passhash = views.get_hash('bendmin')
        assert passhash == '0cc75c328858b5d53f188ccdc0f033c9'

    @staticmethod
    def test_clear_group():
        group = models.Group(id=1, name='Group One')
        dbs.add(group)
        dbs.commit()
        device = models.Device(name='Johns PC', mac_address='37:3B:09:FC:5C:1D', group=1)
        device.clear_group()
        assert device.group_id == 0


if __name__ == '__main__':
    unittest.main()
