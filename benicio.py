#! venv/bin/python

import os
from app import app, db, models


def insert_demodata():
    db.session.add(models.User(name='Admin', password='pbkdf2:sha1:1000$0jrJWk7S$15c39bbdff6514dfe3377ea5a7a15b7fd1f31a9b'))
    db.session.add(models.Group(id=0, name='Default Group'))
    db.session.add(models.Group(id=1, name='Group One'))
    db.session.add(models.Group(id=2, name='Group Two'))
    db.session.add(models.Group(id=3, name='Group Four'))
    db.session.add(models.Rule(name='Rule 01', rule='deny ip from any to [MAC]'))
    db.session.add(models.Rule(name='Rule 02', rule='deny tcp from any to [MAC]'))
    db.session.add(models.Rule(name='Rule 03', rule='deny udp from any to [MAC]'))
    db.session.add(models.Rule(name='Rule 04', rule='deny icmp from any to [MAC]'))
    db.session.add(models.Rule(name='Rule 05', rule='deny log from any to [MAC]'))
    db.session.add(models.Rule(name='Rule 11', rule='allow ip from any to [MAC]'))
    db.session.add(models.Rule(name='Rule 12', rule='allow tcp from any to [MAC]'))
    db.session.add(models.Rule(name='Rule 13', rule='allow udp from any to [MAC]'))
    db.session.add(models.Rule(name='Rule 14', rule='allow icmp from any to [MAC]'))
    db.session.add(models.Rule(name='Rule 15', rule='allow log from any to [MAC]'))
    db.session.add(models.Device(name='Device 1', mac_address='39-A0-28-31-7C-00', group_id=1))
    db.session.add(models.Device(name='Device 2', mac_address='D9-33-18-8D-9F-3F', group_id=1))
    db.session.add(models.Device(name='Device 3', mac_address='12-61-77-35-D8-6E', group_id=1))
    db.session.add(models.Device(name='Device 4', mac_address='8F-CF-71-EF-F3-E7', group_id=1))
    db.session.add(models.Device(name='Device 5', mac_address='6E-FB-CC-84-CB-C1', group_id=1))
    db.session.add(models.Device(name='Device 6', mac_address='3F-E3-0E-B0-31-23', group_id=1))
    db.session.add(models.Device(name='Device 7', mac_address='6B-CA-59-83-7B-49', group_id=1))
    db.session.add(models.Device(name='Device 8', mac_address='21-14-C7-16-B8-80', group_id=1))
    db.session.add(models.Device(name='Device 9', mac_address='10-0B-3D-DC-25-D6', group_id=1))
    db.session.add(models.Device(name='Device 10', mac_address='2C-E0-F2-EA-31-C4', group_id=1))
    db.session.add(models.Device(name='Device 11', mac_address='4C-3B-F4-45-F5-88', group_id=1))
    db.session.add(models.Device(name='Device 12', mac_address='D5-64-1F-92-3C-C0', group_id=1))
    db.session.add(models.Device(name='Device 13', mac_address='E1-DF-C8-55-C7-C8', group_id=1))
    db.session.add(models.Device(name='Device 14', mac_address='88-F2-F4-30-39-29', group_id=1))
    db.session.add(models.Device(name='Device 15', mac_address='67-BE-CE-CB-BE-EE', group_id=1))
    db.session.add(models.Device(name='Device 16', mac_address='FD-43-D7-29-CF-51', group_id=1))
    db.session.add(models.Device(name='Device 17', mac_address='91-0D-2F-07-9B-C6', group_id=1))
    db.session.add(models.Device(name='Device 18', mac_address='EC-18-0C-1E-65-81', group_id=2))
    db.session.add(models.Device(name='Device 19', mac_address='81-CA-A6-12-BD-E8', group_id=2))
    db.session.add(models.Device(name='Device 20', mac_address='6E-AA-3B-7F-4B-68', group_id=2))
    db.session.add(models.Device(name='Device 21', mac_address='B0-E6-ED-66-4E-D5', group_id=2))
    db.session.add(models.Device(name='Device 22', mac_address='7E-0D-34-87-87-03', group_id=2))
    db.session.add(models.Device(name='Device 23', mac_address='5D-3C-E0-AA-EE-1C', group_id=2))
    db.session.add(models.Device(name='Device 24', mac_address='75-79-68-81-1D-9F', group_id=2))
    db.session.add(models.Device(name='Device 25', mac_address='C8-AD-DD-92-4D-3F', group_id=2))
    db.session.add(models.Device(name='Device 26', mac_address='D7-4A-85-10-88-E9', group_id=2))
    db.session.add(models.Device(name='Device 27', mac_address='2C-73-6E-62-B8-EA', group_id=2))
    db.session.add(models.Device(name='Device 28', mac_address='42-C8-90-13-5D-E9', group_id=3))
    db.session.add(models.Device(name='Device 29', mac_address='6C-82-D5-ED-12-F9', group_id=3))
    db.session.add(models.Device(name='Device 30', mac_address='04-9D-13-A6-E6-29', group_id=3))
    db.session.commit()


def init_db():
    db_path = app.config['SQLALCHEMY_DATABASE_URI']
    db_path = db_path[10:]
    if not os.path.exists(db_path):
        db.create_all()
        insert_demodata()


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=app.config['DEBUG'])
