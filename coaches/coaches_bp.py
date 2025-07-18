from flask import Blueprint, render_template, request, Response, redirect, url_for, session, flash
from models import db, Coaches, Users

#Local imports
from thumbnail import Thumbnail

coaches_bp = Blueprint('coaches', __name__, template_folder='templates')
# -- Coaches --

@coaches_bp.route('/')
#@login_required
def list_coaches():
    coaches = Users.query.filter(Users.coach_id.isnot(None)).all()
    return render_template('coaches.html', coaches=coaches)

@coaches_bp.route('/coach', methods=['GET', 'POST'])
#@login_required
def edit_coach():
    user = {}
    user_id = request.args.get('user_id')
    if request.method == 'POST':
        # Handle uploaded or captured photo
        photo_data = None
        thumbnail_data = None
        if "photo" in request.files and request.files["photo"].filename:
            photo_data = request.files["photo"].read()
            thumbnail_data = Thumbnail.create_thumbnail(photo_data)

        #get the coach ID from the post data if present
        user_id = request.form['id'] 
        if user_id:
            #update existing entry
            user = Users.query.get_or_404(user_id)
            user.first_name = request.form['first_name']
            user.last_name = request.form['last_name']
            user.email = request.form['email']
            user.phone = request.form['phone']
            if photo_data:
                # Only overwrite if new photo uploaded
                user.coach.photo = photo_data
                user.coach.thumbnail=thumbnail_data
        else :
            #add new coach / coach_id is empty
            user = Users(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                phone=request.form['phone']
            )
            db.session.add(user)
            coach = Coaches(
                photo=photo_data,
                thumbnail=thumbnail_data)
            db.session.add(coach)
            user.coach = coach
        #TODO: users.email must be unique -Add a try catch block and flash an error or success message
        db.session.commit()
        flash('Coach updated successfully!', 'success')
        return redirect(url_for('coaches.list_coaches'))

    if user_id :
        user = Users.query.get_or_404(user_id)
    return render_template('edit_coach.html', user=user)

@coaches_bp.route("/photo/<int:coach_id>")
def get_photo(coach_id):
    coach = Coaches.query.get_or_404(coach_id)
    if coach and coach.photo:
        return Response(coach.photo, mimetype="image/jpeg")
    return '', 404

@coaches_bp.route("/photo/thumbnail/<int:coach_id>")
def get_thumbnail(coach_id):
    coach = Coaches.query.get_or_404(coach_id)
    if coach and coach.thumbnail:
        return Response(coach.thumbnail, mimetype="image/jpeg")
    return '', 404
