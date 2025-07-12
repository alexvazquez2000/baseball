from flask import Blueprint, render_template, request, Response, redirect, url_for, session

from models import db, Parents


parents_bp = Blueprint('parents', __name__, template_folder='templates')

# -- Parents --
@parents_bp.route('/')
#@login_required
def list_parents():
    parents = Parents.query.all()
    return render_template('parents.html', parents=parents)

@parents_bp.route('/parent', methods=['GET', 'POST'])
#@login_required
def edit_parent():
    parent = {}
    parent_id = request.args.get('parent_id')
    if request.method == 'POST':
        #get the ID from the post data if present
        parent_id = request.form['id'] 
        if parent_id:
            #update existing entry
            parent = Parents.query.get_or_404(parent_id)
            parent.first_name = request.form['first_name']
            parent.last_name = request.form['last_name']
            parent.email = request.form['email']
            parent.phone = request.form['phone']
        else :
            #add new parent / parent_id is empty
            parent = Parents(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                phone=request.form['phone']
            )
            db.session.add(parent)
        db.session.commit()
        #TODO: stay on page to continue editing or redirect to list all parents?
        #return redirect(url_for('parents.list_parents'))

    if parent_id :
        parent = Parents.query.get_or_404(parent_id)
    return render_template('edit_parent.html', parent=parent)


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


