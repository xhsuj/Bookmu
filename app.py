from flask import Flask, render_template,request,redirect,url_for,jsonify,abort,json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from functools import wraps
#from jose import jwt
from urllib.request import urlopen
import sys

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://yhb@localhost:5432/bookmu'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
migrate=Migrate(app,db)

    



genre_venue=db.Table('genre_venues',db.Column('item_id',db.Integer,db.ForeignKey('venue.id'),primary_key=True),
db.Column('genre_id',db.Integer,db.ForeignKey('genres.id'),primary_key=True)
)
genre_artist=db.Table('genre_artists',db.Column('item_id',db.Integer,db.ForeignKey('artist.id'),primary_key=True),
db.Column('genre_id',db.Integer,db.ForeignKey('genres.id'),primary_key=True)
)
class Genres(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    kind=db.Column(db.String(),nullable=False,default=False)
    def __repr__(self):
        return f'<Genres {self.id} {self.kind}>'

class Artist(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(),nullable=False, default=False)
    city=db.Column(db.String(),nullable=False,default=False)
    state=db.Column(db.String(),nullable=False,default=False)
    phone=db.Column(db.String(), nullable=False,default=False)
    facebook_link=db.Column(db.String(),nullable=False,default=False)
    genres=db.relationship('Genres',secondary=genre_artist,backref=db.backref('artist',lazy=True))
    def __repr__(self):
        return f'<Artist {self.id} {self.name} {self.city} {self.state} {self.phone} {self.facebook_link}>'


class Shows(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    artist_id=db.Column(db.Integer,db.ForeignKey('artist.id'),nullable=False,default=False)
    venue_id=db.Column(db.Integer,db.ForeignKey('venue.id'),nullable=False,default=False)
    start_time=db.Column(db.String(),nullable=False,default=False)
    artist=db.relationship('Artist',backref=db.backref('venues'))
    venue=db.relationship('Venue',backref=db.backref('artists'))



    

class Venue(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(),nullable=False,default=False)
    city=db.Column(db.String(),nullable=False,default=False)
    state=db.Column(db.String(),nullable=False,default=False)
    phone=db.Column(db.String(),nullable=False,default=False)
    address=db.Column(db.String(),nullable=False,default=False)
    genres=db.relationship('Genres',secondary=genre_venue,backref=db.backref('venues',lazy=True))
    facebook_link=db.Column(db.String(),nullable=False,default=False)
    def __repr__(self):
        return f'<Venue {self.id} {self.name} {self.city} {self.state} {self.phone} {self.address} {self.facebook_link}>'
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def requires_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        jwt=get_token_auth_header()
        try:
            payload =verify_decode_jwt(jwt)
        except:
            abort(401)
        return f(jwt,*args, **kwargs)
    return wrapper

AUTH0_DOMAIN = 'elngu.us.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'Image'

@app.route('/main')
def main():
    return render_template('main.html')

@app.route('/')
def index():
    return redirect(url_for('main'))

@app.route('/artist')
def artist():
    return render_template('artist.html')

@app.route('/venues')
def venues():
    return render_template('venues.html')

@app.route('/shows')
def showss():
    return render_template('shows.html')


@app.route('/venue_list')
def venue_list(): 
    return render_template('venue_list.html',
    venues=Venue.query.order_by('city').all()
    ) #specify which html file we will use for the application


@app.route('/artist_list')
def artist_list():
    return render_template('artist_list.html',
    artists=Artist.query.order_by('city').all()
    )
@app.route('/artist_list/<artist_id>')
def get_artist(artist_id):
    return render_template('artist_intro.html',
    art=Artist.query.filter_by(id=artist_id).first(),
    gens=Genres.query.filter_by(artist_id=artist_id).all() 
    )

@app.route('/venue_list/<venue_id>')
def get_venue(venue_id):
    return render_template('venue_intro.html',
    ve=Venue.query.filter_by(id=venue_id).first(),
    gens=Genres.query.filter_by(venue_id=venue_id).all() #use get method instead of query or .first since we get only one object
    )

@app.route('/venue_list/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
    try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return

@app.route('/show_list')
def get_shows():
    return render_template('show_list.html',
    shows=Shows.query.all()
    )

@app.route('/venues/create',methods=['POST'])
def create_venue():
    error=False
    body={}
    body['status']='non-exist'
    try:
        name=request.get_json()['name']
        city=request.get_json()['city']
        state=request.get_json()['state']
        phone=request.get_json()['phone']
        address=request.get_json()['address']
        facebook_link=request.get_json()['facebook_link']
        if (bool(Venue.query.filter_by(name=name,city=city,address=address,state=state,phone=phone,facebook_link=facebook_link).first())==True):
            db.session.commit()
            body['status']=['exist']
        else :
            venue=Venue(name=name,city=city,state=state,phone=phone,address=address,facebook_link=facebook_link)
            genres=request.get_json()['genres']
            for kind in genres:
                    dbgen=Genres.query.filter_by(kind=kind).first()
                    if dbgen != None:
                        venue.genres.append(dbgen)
                    else:
                        gen=Genres(kind=kind)
                        venue.genres.append(gen)
            db.session.add(venue)
            db.session.commit()
            body['name']=venue.name
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (400)
    if not error:
        return jsonify(body)


@app.route('/artist/create',methods=['POST'])
def create_artist():
    error=False
    body={}
    body['status']='non-exist'
    try:
        name=request.get_json()['name']
        city=request.get_json()['city']
        state=request.get_json()['state']
        phone=request.get_json()['phone']
        facebook_link=request.get_json()['facebook_link']
        if (bool(Artist.query.filter_by(name=name,city=city,state=state,phone=phone,facebook_link=facebook_link).first())==True):
            db.session.commit()
            body['status']=['exist']
        else:
            artist=Artist(name=name,city=city,state=state,phone=phone,facebook_link=facebook_link)
            db.session.add(artist)
            db.session.commit()
            artist_id=artist.id
            genres=request.get_json()['genres']
            for genre in genres:
                kind=genre
                gen=Genres(kind=kind,artist_id=artist_id)
                db.session.add(gen)
            db.session.commit()
            body['name']=artist.name   
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (400)
    if not error:
        return jsonify(body)

@app.route('/show/create',methods=['POST'])
def create_show():
    error=False
    body={}
    body['status']='non-exist'
    try:
        artist_id=request.get_json()['artist_id']
        venue_id=request.get_json()['venue_id']
        start_time=request.get_json()['start_time']
        if (bool(Shows.query.filter_by(artist_id=artist_id,venue_id=venue_id,start_time=start_time).first())==True):
            db.session.commit()
            body['status']=['exist']
        else:
            show=Shows(artist_id=artist_id,venue_id=venue_id,start_time=start_time)
            db.session.add(show)
            db.session.commit()
            body['artist_id']=show.artist_id
            body['venue_id']=show.venue_id
            body['start_time']=show.start_time
    except:
        error=True
        db.session.rollback()
        print(sys.exc_info())
    finally:
        db.session.close()
    if error:
        abort (400)
    if not error:
        return jsonify(body)



def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)

    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


@app.route('/headers')
@requires_auth
def headers(payload):
    print(payload)
    return "Access Granted"





