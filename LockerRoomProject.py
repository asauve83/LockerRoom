#!/usr/bin/env python2

import json
from flask import Flask, render_template, request, redirect,\
    jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from LockerRoomDbSetup import Base, Players, Teams, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import requests
from flask import make_response

app = Flask(__name__)

# get the google security information from the local file
CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "LockerRoomProject"

# Connect to the Database and create a database session
engine = create_engine('postgresql://lockerroom:postgress@localhost/LockerRoom')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# show list of teams to any user
@app.route('/')
@app.route('/teams/')
def showTeams():
    teams = session.query(Teams).order_by(asc(Teams.name))
    return render_template('teams.html', teams=teams)


# create Team
@app.route('/teams/new/', methods=['GET', 'POST'])
def newTeam():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newTeam = Teams(
            name=request.form['name'], user_id=login_session['user_id'])
        session.add(newTeam)
        flash('New Team %s Successfully Created' % newTeam.name)
        session.commit()
        return redirect(url_for('showTeams'))
    else:
        return render_template('newTeam.html')


# edit Team
@app.route('/teams/<int:team_id>/edit/', methods=['GET', 'POST'])
def editTeam(team_id):
    editedTeam = session.query(
        Teams).filter_by(id=team_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedteam.user_id != login_session['user_id']:
        flash('You are not authorized to edit this team.\
        Please create your own team')
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        if request.form['name']:
            editedTeam.name = request.form['name']
            flash('Successfully Edited %s' % editedTeam.name)
            return redirect(url_for('showTeams'))
    else:
        return render_template('editTeam.html', team=editedTeam)


# delete Team
@app.route('/teams/<int:team_id>/delete/', methods=['GET', 'POST'])
def deleteTeam(team_id):
    teamToDelete = session.query(
        Teams).filter_by(id=team_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if teamToDelete.user_id != login_session['user_id']:
        flash('You are not authorized to delete this team.')
        return redirect(url_for('showCategories'))
    if request.method == 'POST':
        session.delete(teamToDelete)
        flash('%s Successfully Deleted' % teamToDelete.name)
        session.commit()
        return redirect(url_for('showTeams'))
    else:
        return render_template('deleteTeam.html',
                               team=teamToDelete)


# Show players on a team
@app.route('/teams/<int:team_id>/')
def showPlayers(team_id):
    team = session.query(Teams).filter_by(id=team_id).one()
    players = session.query(Players).filter_by(team_id=team_id).all()
    creator = getUserInfo(team.user_id)
    return render_template('players.html', players=players,
                           team=team, creator=creator)


# Create a player
@app.route('/teams/<int:team_id>/player/new/', methods=['GET', 'POST'])
def newPlayer(team_id):
    if 'username' not in login_session:
        return redirect('/login')
    team = session.query(Teams).filter_by(id=team_id).one()
    if login_session['user_id'] != team.user_id:
        flash('You are not authorized to add players to this team.\
        Please create your own team')
        return redirect(url_for('showTeams', team_id=cteam_id))
    if request.method == 'POST':
            newPlayer = Players(name=request.form['name'], team_id=team_id,
                                user_id=team.user_id)
            session.add(newPlayer)
            session.commit()
            flash(' %s Player Successfully Created' % (newPlayer.name))
            return redirect(url_for('showPlayer', team_id=team_id))
    else:
        return render_template('newPlayer.html', team_id=team_id)


# Edit a Player
@app.route('/teams/<int:team_id>/player/<int:player_id>/edit',
           methods=['GET', 'POST'])
def editPlayer(team_id, player_id):
    if 'username' not in login_session:
        return redirect('/login')
    editedPlayer = session.query(Players).filter_by(id=player_id).one()
    team = session.query(Teams).filter_by(id=team_id).one()
    if login_session['user_id'] != team.user_id:
        return "<script>function myFunction() {alert('You are not authorized\
        to edit players on this team. Please create your own team in\
        order to edit players.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            editedPlayer.name = request.form['name']
        session.add(editedPlayer)
        session.commit()
        flash(' %s Player Successfully Edited' % (editedPlayer.name))
        return redirect(url_for('showPlayers', team_id=team_id))
    else:
        return render_template('editPlayer.html', team_id=team_id,
                               player_id=player_id, player=editedPlayer)


# Delete a Player
@app.route('/teams/<int:team_id>/player/<int:player_id>/delete',
           methods=['GET', 'POST'])
def deletePlayer(team_id, player_id):
    if 'username' not in login_session:
        return redirect('/login')
    team = session.query(Teams).filter_by(id=team_id).one()
    playerToDelete = session.query(Players).filter_by(id=player_id).one()
    if login_session['user_id'] != team.user_id:
        return "<script> function myFunction() {alert('You are not authorized \
        to delete players on this team. Please create your own team in\
        order to delete players.');} </script><body onload = 'myFunction()'>"
    if request.method == 'POST':
        session.delete(playerToDelete)
        session.commit()
        flash('Player Successfully Deleted')
        return redirect(url_for('showPlayers', team_id=team_id))
    else:
        return render_template('deletePlayer.html', player=playerToDelete)


# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']
    # ADD PROVIDER TO LOGIN SESSION
    login_session['provider'] = 'google'

    # see if user exists, if it doesn't make a new one
    user_id = getUserID(data["email"])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius:\
        150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print("done!")
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = 'https://accounts.google.com/o/oauth2/revoke?token = %s' %\
          access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to \
                                 revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# User Helper Functions
def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showTeams'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showTeams'))


@app.route('/clearSession')
def clear_session():
    login_session.clear()
    return "session cleared"


# JSON APIs to view team Information
@app.route('/teams/JSON')
def teamsJSON():
    teams = session.query(Teams).all()
    return jsonify(teams=[r.serialize for r in teams])


@app.route('/players/JSON')
def playersJSON():
    players = session.query(Players).all()
    return jsonify(players=[r.serialize for r in players])


@app.route('/teams/<int:team_id>/players/JSON')
def playersOnTeamJSON(team_id):
    team = session.query(Teams).filter_by(id=team_id).one()
    players = session.query(Players).filter_by(
        team_id=team_id).all()
    return jsonify(players=[i.serialize for i in players])


@app.route('/teams/<int:team_id>/players/<int:player_id>/JSON')
def playerJSON(team_id, player_id):
    players = session.query(Players).filter_by(id=player_id).one()
    return jsonify(players=players.serialize)


@app.route('/users/JSON')
def usersJSON():
    users = session.query(User).all()
    return jsonify(users=[x.serialize for x in users])

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8080, threaded=False)
