from flask import session

## it gets called from seaons_bp and from app
def get_current_season():
    if 'current_season_id' in session:
         current_season_id = session.get('current_season_id')
         current_season_name = session.get('current_season_name')
    else:
         current_season = Seasons.query.order_by(Seasons.created_at.desc()).limit(1).first()
         current_season_id = current_season.id
         current_season_name = current_season.season_name
    return (current_season_id, current_season_name)
