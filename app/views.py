import subprocess
import hashlib
from flask import render_template, redirect, flash, request, url_for
from app import app, models, db, lm
from forms import RuleForm, DeviceForm, GroupForm, LoginForm, ChangePasswordForm
from flask_login import login_user, logout_user, login_required


def get_hash(password):
    md5 = hashlib.md5()
    md5.update(password)
    return md5.hexdigest()


@lm.user_loader
def load_user(userid):
    return models.User.query.get(userid)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(name=form.user.data).first()
        if not user is None:
            if user.password == get_hash(form.password.data):
                login_user(user)
                flash("Logged in successfully.", "success")
                return redirect(url_for("index"))
    return render_template("login.html", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('login')


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(name="Admin").first()
        if user.password == get_hash(form.current_password.data):
            user.password = get_hash(form.new_password.data)
            db.session.commit()
        else:
            flash('Verify your password', 'error')
    return render_template('index.html', form=form)


@app.route('/rules', methods=['GET', 'POST', 'DELETE'])
@login_required
def rules():
    form = RuleForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            rule_id = form.id.data
            if rule_id:
                rule = models.Rule.query.get(rule_id)
                rule.name = form.name.data
                rule.rule = form.rule.data
            else:
                rule = models.Rule(name=form.name.data, rule=form.rule.data)
                db.session.add(rule)
            db.session.commit()
            flash('The rule was successfully saved.', 'success')
        return redirect(url_for('rules'))
    rules = models.Rule.query.all()
    return render_template('rules.html', form=form, rules=rules)


@app.route('/rules/<rule_id>')
@login_required
def edit_rule(rule_id):
    rules = models.Rule.query.all()
    rule = models.Rule.query.get(rule_id)
    form = RuleForm(obj=rule)
    return render_template('rules.html', form=form, rules=rules)


@app.route('/apply', methods=['GET'])
@login_required
def apply_rules():
    rules = models.Rule.query.all()
    groups = models.Group.query.all()
    devices = models.Device.query.all()
    return render_template('apply_rules.html', rules=rules, devices=devices, groups=groups)


@app.route('/apply', methods=['POST'])
@login_required
def applicate_rules():
    rules = []
    devices = []
    for data in request.form:
        if data.find('rule') == 0:
            rules.append(data.replace('rule', ''))
        elif data.find('device') == 0:
            devices.append(data.replace('device', ''))
    rules_generated = generate_rules(rules, devices)
    if insert_rules(rules_generated):
        flash('Rules successfully applied.', 'success')
    else:
        flash('Problem when trying to apply the rules. Check the console messages.', 'error')
    return redirect(url_for('apply_rules', rules_generated=rules_generated))


def insert_rules(rules):
    return_code = 0
    for rule in rules:
        if app.config['DEBUG']:
            return_code = subprocess.call('echo ' + rule + ' >> file', shell=True)
        else:
            return_code = subprocess.call('ipfw -q add ' + rule, shell=True)
    return return_code == 0


def generate_rules(rules, devices):
    result = []
    for rule in rules:
        for device in devices:
            result.append(
                models.Rule.query.get(rule).rule.replace('[MAC]', 'mac ' + models.Device.query.get(device).mac_address))
    return result


@app.route('/devices', methods=['GET', 'POST'])
@login_required
def devices():
    form = DeviceForm()
    form.group.choices = [(str(g.id), g.name) for g in models.Group.query.order_by('id')]
    if form.validate_on_submit():
        device_id = form.id.data
        if device_id:
            device = models.Device.query.get(device_id)
            device.group_id = form.group.data
            device.mac_address = form.mac_address.data
            device.name = form.name.data
        else:
            device = models.Device(name=form.name.data, mac_address=form.mac_address.data.upper(),
                                   group_id=form.group.data)
            db.session.add(device)
        db.session.commit()
        flash('The device was successfully saved.', 'success')
        return redirect(url_for('devices'))
    devices = models.Device.query.all()
    return render_template('devices.html', form=form, devices=devices)


@app.route('/devices/<device_id>', methods=['GET'])
@login_required
def edit_device(device_id):
    devices = models.Device.query.all()
    device = models.Device.query.get(device_id)
    form = DeviceForm(obj=device)
    form.group.choices = [(str(g.id), g.name) for g in models.Group.query.order_by('id')]
    if device.group:
        group_id = str(device.group.id)
    else:
        group_id = '0'
    form.group.data = group_id
    return render_template('devices.html', form=form, devices=devices, device=device)


@app.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    form = GroupForm()
    if form.validate_on_submit():
        group_id = form.id.data
        if group_id:
            group = models.Group.query.get(group_id)
            group.name = form.name.data
        else:
            group = models.Group(name=form.name.data)
            db.session.add(group)
        db.session.commit()
        flash('The group was successffully saved.', 'success')
        return redirect(url_for('groups'))
    groups = models.Group.query.all()
    return render_template('groups.html', form=form, groups=groups)


@app.route('/api/groups/<group_id>', methods=['DELETE'])
@login_required
def delete_group(group_id):
    devices = models.Device.query.filter_by(group_id=group_id).all()
    for device in devices:
        device.clear_group()
    db.session.delete(models.Group.query.get(group_id))
    db.session.commit()
    return 'True', 200


@app.route('/api/devices/<device_id>', methods=['DELETE'])
@login_required
def delete_device(device_id):
    db.session.delete(models.Device.query.get(device_id))
    db.session.commit()
    return 'True', 200


@app.route('/api/rules/<rule_id>', methods=['DELETE'])
@login_required
def delete_rule(rule_id):
    db.session.delete(models.Rule.query.get(rule_id))
    db.session.commit()
    return 'True', 200


@app.route('/api/current', methods=['GET'])
@login_required
def current_config():
    if app.config['DEBUG']:
        result = subprocess.check_output(['cat', 'file'])
    else:
        result = subprocess.check_output(['ipfw', '-t list'])
    return result


@app.route('/groups/<group_id>', methods=['GET'])
@login_required
def edit_group(group_id):
    groups = models.Group.query.all()
    group = models.Group.query.get(group_id)
    form = GroupForm(obj=group)
    return render_template('groups.html', form=form, groups=groups)


@app.errorhandler(404)
@login_required
def page_not_found(e):
    return render_template('404.html'), 404


@lm.unauthorized_handler
def unauthorized():
    return redirect(url_for('login'))