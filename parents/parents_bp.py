from flask import Blueprint, render_template, request, Response, redirect, url_for, session

from models import db, Parents, Users
from auth.auth_bp import login_required

parents_bp = Blueprint('parents', __name__, template_folder='templates')

# -- Parents --
@parents_bp.route('/')
@login_required
def list_parents():
    #filter(Users.parent.isnot(None)) doesn't work because isnot() is used only on columns of the DB.  Use parent_id
    #parents = Users.query.filter(Users.parent_id.isnot(None)).all()
    #Commented out the filter because we are missing rows if no players are added
    #users = Users.query.all()
    users = db.session.scalars(db.select(Users)).all()
    return render_template('parents.html', users=users)

@parents_bp.route('/parent', methods=['GET', 'POST'])
@login_required
def edit_parent():
    user = {}
    user_id = request.args.get('user_id')
    if request.method == 'POST':
        #get the ID from the post data if present
        user_id = request.form['id'] 
        if user_id:
            #update existing entry
            user = Users.query.get_or_404(user_id)
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.email = request.form['email']
            user.phone = request.form['phone']
        else :
            #add new parent / parent_id is empty
            user = Users(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                phone=request.form['phone'],
                #TODO _ Make sure we have a parent - might need to save before adding
                parent = Parents()
            )
            db.session.add(user)
        #FIXME: user.email must be unique, try/catch the error 
        db.session.commit()
        #TODO: stay on page to continue editing or redirect to list all parents?
        #return redirect(url_for('parents.list_parents'))

    if user_id :
        user = Users.query.get_or_404(user_id)
    return render_template('edit_parent.html', user=user)


#        # Clear current children
#        parent.players.clear()
#        # Add selected children
#        child_ids = request.form.getlist('children')
#        for cid in child_ids:
#            player = Players.query.get(int(cid))
#            if player:
#                parent.players.append(player)
#        db.session.commit()
#        return redirect(url_for('parents.list_parents'))
#    return render_template('edit_parent.html', parent=parent, players=players)


