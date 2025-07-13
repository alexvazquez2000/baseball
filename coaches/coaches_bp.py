from flask import Blueprint, render_template, request, Response, redirect, url_for, session
from models import db, Coaches

#Local imports
from thumbnail import Thumbnail

coaches_bp = Blueprint('coaches', __name__, template_folder='templates')
# -- Coaches --

@coaches_bp.route('/')
#@login_required
def list_coaches():
    coaches = Coaches.query.all()
    return render_template('coaches.html', coaches=coaches)

@coaches_bp.route('/coach', methods=['GET', 'POST'])
#@login_required
def edit_coach():
    coach = {}
    coach_id = request.args.get('coach_id')
    if request.method == 'POST':
        # Handle uploaded or captured photo
        photo_data = None
        thumbnail_data = None
        if "photo" in request.files and request.files["photo"].filename:
            photo_data = request.files["photo"].read()
            thumbnail_data = Thumbnail.create_thumbnail(photo_data)

        #get the coach ID from the post data if present
        coach_id = request.form['id'] 
        if coach_id:
            #update existing entry
            coach = Coaches.query.get_or_404(coach_id)
            coach.first_name = request.form['first_name']
            coach.last_name = request.form['last_name']
            coach.email = request.form['email']
            coach.phone = request.form['phone']
            if photo_data:
                # Only overwrite if new photo uploaded
                coach.photo = photo_data
                coach.thumbnail=thumbnail_data
        else :
            #add new coach / coach_id is empty
            coach = Coaches(
                first_name=request.form['first_name'],
                last_name=request.form['last_name'],
                email=request.form['email'],
                phone=request.form['phone'],
                photo=photo_data,
                thumbnail=thumbnail_data
            )
            db.session.add(coach)
        db.session.commit()
        return redirect(url_for('coaches.list_coaches'))

    if coach_id :
        coach = Coaches.query.get_or_404(coach_id)
    return render_template('edit_coach.html', coach=coach)

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
