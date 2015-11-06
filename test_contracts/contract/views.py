from datetime import datetime as dt
from flask import Blueprint, render_template, flash, url_for, redirect, request, g
from flask_security import login_required, current_user, roles_accepted
from test_contracts.utils import flash_errors, add_event, add_note
from test_contracts.contract.forms import Support, Crew, Combat, ChangeTime, AddNote
from test_contracts.message.forms import ModalMessage
from test_contracts.models import Contract, Services, Messages
from test_contracts.zones import temporary as zones
from sqlalchemy import or_


blueprint = Blueprint("contract", __name__, url_prefix='/contract',
                      static_folder="../static")


@blueprint.before_request
def before_request():
    if current_user.is_authenticated():
        g.new = Messages.query.filter(Messages.recipient_id == current_user.id,
                                      Messages.user_for_id == current_user.id,
                                      Messages.unread == True).count()
    else:
        g.new = None


# New
@blueprint.route("/new/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def new():
    return render_template("contract/new.html")


# Support
@blueprint.route("/support/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def support():
    _order = Support()
    if request.method == 'POST':
        if _order.validate_on_submit():
            service_name = _order.service.data
            _ship_name = _order.ship.data
            _contract = Contract.create(user_id=current_user.id, description=_order.description.data,
                                        passengers=_order.passengers.data,
                                        start_location=_order.start_location.data,
                                        end_location=_order.end_location.data, time=_order.time.data,
                                        scu=_order.scu.data, fuel=_order.fuel.data,
                                        service_id=service_name.id, ship_id=_ship_name.id)
            add_event(event="Contract created.", user=current_user.id, invoice=_contract.invoice)
            flash('Contract has been created.', 'success')
            return redirect(url_for('contract.your'))
        else:
            flash_errors(_order)
    return render_template("contract/support.html", order=_order, zones=zones)


# Crew
@blueprint.route("/crew/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def crew():
    _order = Crew()
    if request.method == 'POST':
        if _order.validate_on_submit():
            ship_name = _order.ship.data
            service_data = Services.query.filter_by(name='Crew Members').first()
            job = Contract.create(user_id=current_user.id, description=_order.description.data,
                                  start_location=_order.start_location.data,
                                  end_location=_order.end_location.data, time=_order.time.data,
                                  pilot=_order.pilot.data, radar=_order.radar.data, weapons=_order.weapons.data,
                                  gunner=_order.gunner.data, engineer=_order.engineer.data,
                                  navigation=_order.navigation.data, communications=_order.communications.data,
                                  security=_order.security.data, science=_order.science.data,
                                  medical=_order.medical.data, ship_id=ship_name.id, service_id=service_data.id)
            add_event(event="Contract created.", user=current_user.id, invoice=job.invoice)
            flash('Contract has been created.', 'success')
            return redirect(url_for('contract.your'))
        else:
            flash_errors(_order)
    return render_template("contract/crew.html", order=_order, zones=zones)


# Combat
@blueprint.route("/combat/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def combat():
    _order = Combat()
    if request.method == 'POST':
        if _order.validate_on_submit():
            service_name = _order.service.data
            ship_name = _order.ship.data
            job = Contract.create(user_id=current_user.id, service_id=service_name.id,
                                  time=_order.time.data, ship_id=ship_name.id,
                                  scu=_order.scu.data, fuel=_order.fuel.data,
                                  passengers=_order.passengers.data, start_location=_order.start_location.data,
                                  end_location=_order.end_location.data,
                                  description=_order.description.data)
            add_event(event="Contract created.", user=current_user.id, invoice=job.invoice)
            flash('Contract has been created.', 'success')
            return redirect(url_for('contract.your'))
        else:
            flash_errors(_order)
    return render_template("contract/combat.html", order=_order, zones=zones)


# Current contracts
@blueprint.route("/current/", defaults={'page': 1}, methods=["GET", "POST"])
@blueprint.route("/current/<int:page>/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def current(page):
    _time = dt.utcnow()
    _current_contracts = Contract.query.filter(Contract.status >= 3) \
        .filter(or_(Contract.user_id == current_user.id, Contract.assigned_to == current_user.id)) \
        .paginate(page, 10, True)
    return render_template("contract/current.html", current_contracts=_current_contracts, time=_time)


# History
@blueprint.route("/history/", defaults={'page': 1}, methods=["GET", "POST"])
@blueprint.route("/history/<int:page>/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def history(page):
    _time = dt.utcnow()

    _your_history = Contract.query.filter(Contract.status <= 2) \
        .filter(or_(Contract.user_id == current_user.id, Contract.assigned_to == current_user.id)) \
        .paginate(page, 10, True)
    return render_template("contract/history.html", time=_time,
                           your_history=_your_history)


# Available
@blueprint.route("/available/", defaults={'page': 1}, methods=["GET", "POST"])
@blueprint.route("/available/<int:page>/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def available(page):
    _time = dt.utcnow()
    _available_contracts = Contract.query.filter(Contract.user_id != current_user.id,
                                                 Contract.status == 6,
                                                 Contract.assigned_to == None).paginate(
        page, 10, True)
    return render_template("contract/available.html", time=_time,
                           available_contracts=_available_contracts)


# Detail
@blueprint.route("/detail/", defaults={'invoice': None}, methods=["GET"])
@blueprint.route("/detail/<invoice>/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def detail(invoice):
    # Add forms
    _message = ModalMessage()
    _change_time = ChangeTime()
    _note = AddNote()
    # Get contract object and assign current time variable
    _contract = Contract.query.filter_by(invoice=invoice).first()
    if _contract is None:
        return redirect(url_for('public.overview'))
    _time = dt.utcnow()
    # Confirm the user
    _user = current_user.id
    _owner = None
    _assigned = None
    if _contract is not None:
        _owner = _contract.user_id
        _assigned = _contract.assigned_to
    # If contract is new, display detail and allow time change?
    if int(_contract.status) == 6:
        _change_time.time.data = _contract.time
        return render_template("contract/detail.html",
                               contract=_contract, time=_time, _change_time=_change_time, invoice=invoice,
                               _note=_note, _message=_message)
    elif int(_contract.status) <= 5 or int(_contract.status) >= 7 and _user == _owner or _user == _assigned:
        return render_template("contract/detail.html",
                               contract=_contract, time=_time, _change_time=_change_time, invoice=invoice,
                               _note=_note, _message=_message)
    else:
        flash("Your authority is not recognized in Fort Kickass.", 'danger')
        return redirect(url_for('public.overview'))


# _add_note
@blueprint.route("/detail/<invoice>/note/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def note(invoice):
    _note = AddNote()
    # Get contract object by owner, and if not use contractor or fail.
    _contract = Contract.query.filter(Contract.invoice == invoice,
                                      Contract.user_id == current_user.id).first()
    if _contract is None:
        _contract = Contract.query.filter(Contract.invoice == invoice,
                                          Contract.assigned_to == current_user.id).first()
        if _contract is None:
            flash("Your authority is not recognized in Fort Kickass.", 'danger')
            return redirect(url_for('public.overview'))

    # If request is GET go back to details.
    if request.method == 'GET':
        return redirect('contract.detail', invoice=invoice)

    # Adding the note.
    if _note.validate_on_submit():
        _contractor = 1
        _client = 1
        if current_user.id == _contract.user_id and _note.private.data:
            _contractor = 0
        elif current_user.id == _contract.assigned_to and _note.private.data:
            _client = 0

        # Add note
        add_note(note=_note.note.data, invoice=invoice, user=current_user.id,
                 client=_client,
                 contractor=_contractor)
        # Add Event
        add_event(event="Note added.", invoice=invoice, user=current_user.id, client=_client, contractor=_contractor)
        # Update contract last updated
        _contract.update(last_updated=dt.utcnow())
        flash('The note has been added.', 'success')
        return redirect(url_for('contract.detail', invoice=invoice))
    else:
        flash_errors(_note)
        return redirect(url_for('contract.detail', invoice=invoice))


# _change Time
@blueprint.route("/detail/<invoice>/time/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def time(invoice):
    _change_time = ChangeTime()

    # Get contract object if user is owner or fail.
    _contract = Contract.query.filter(Contract.invoice == invoice,
                                      Contract.user_id == current_user.id).first()
    if _contract is None:
        flash("Your authority is not recognized in Fort Kickass.", 'danger')
        return redirect(url_for('public.overview'))

    if request.method == 'GET':
        return redirect('contract.detail', invoice=invoice)

    if _change_time.validate_on_submit():
        # Changing time and updating contract last updated.
        _contract.update(time=_change_time.time.data, last_updated=dt.utcnow())
        # Creating event
        add_event(event="Estimated time changed.", invoice=invoice, user=current_user.id)
        flash('Estimated time has been updated.', 'success')
        return redirect(url_for('contract.detail', invoice=invoice))
    else:
        flash_errors(_change_time)
        return redirect(url_for('contract.detail', invoice=invoice))


# _cancel
@blueprint.route("/detail/<invoice>/cancel/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def cancel(invoice):
    # Get contract object if user is owner or fail.
    _contract = Contract.query.filter(Contract.invoice == invoice,
                                      Contract.user_id == current_user.id).first()
    if _contract is None:
        flash("Your authority is not recognized in Fort Kickass.", 'danger')
        return redirect(url_for('public.overview'))

    # Cancel the contract.
    _contract.update(status=1, last_updated=dt.utcnow())
    # Creating event.
    add_event(event="Contract cancelled by client.", invoice=invoice, user=current_user.id)
    flash("Contract has been cancelled.", 'danger')
    return redirect(url_for('contract.your'))


# accept job
@blueprint.route("/detail/<invoice>/accept/", methods=["GET", "POST"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def accept(invoice):
    _contract = Contract.query.filter(Contract.invoice == invoice).first_or_404()

    if _contract.assigned_to is not None and _contract.user_id == current_user.id:
        return redirect(url_for('contract.detail', invoice=invoice))

    else:
        # Updating contract
        _contract.update(status=4, assigned_to=current_user.id, last_updated=dt.utcnow())
        # Creating event.
        add_event(event='Contractor {user} assigned to contract.'.format(user=current_user.username), invoice=invoice, user=current_user.id)
        flash("You have successfully accepted contract #{inv}".format(inv=invoice), 'success')
        return redirect(url_for('contract.detail', invoice=invoice))


# Bad
@blueprint.route("/detail/note/", methods=["GET"])
@blueprint.route("/detail/time/", methods=["GET"])
@blueprint.route("/detail/cancel/", methods=["GET"])
@login_required
@roles_accepted('Contractor', 'Employee', 'Arbiter', 'Staff', 'Admin')
def bad():
    flash("Nothing to see here.", 'warning')
    return redirect(url_for('public.overview'))