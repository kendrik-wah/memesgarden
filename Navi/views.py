from django.shortcuts import render, redirect, reverse
from .models import *
import re
from django.http import *
from django.contrib.sessions.backends.db import SessionStore
from django.db import connection
from datetime import datetime

def index(request):
	
	session = request.session
	sk = session.session_key

	if sk == None:
		return render(request, 'base/index.html')
	else:
		return HttpResponseRedirect('home')


def about(request):
	return render(request, 'base/about.html')





def register(request):

	fname = request.POST.get('fname', '')
	lname = request.POST.get('lname', '')
	gender = request.POST.get('gender', '')
	contact = request.POST.get('contact', '')
	email = request.POST.get('email', '')
	password = request.POST.get('password', '')

	user_results = Users.objects.all()
	fail_dict = dict()

	if not re.match("\w{3}-\w{3}-\w{4}", contact) and not re.match("^[0-9]{8}$", contact):
		fail_dict['invalid_contact'] = 'Invalid phone number.'
	if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
		fail_dict['invalid_email'] = 'Invalid email.'


	if len(fail_dict) and contact:
		return render(request, 'registration/register.html', fail_dict)

	elif not len(fail_dict) and contact:
		pass_dict = {"name": fname,
					 "email": email}
		return render(request, 'registration/validation.html', pass_dict)

	else:
		return render(request, 'registration/register.html')


def authenticate(request):

	email = request.POST.get('email', '')
	password = request.POST.get('password', '')
	rmb = request.POST.get('remember', '')

	if email:
		try:
			user_results = Users.objects.get(email=email)
		except Users.DoesNotExist:
			fail = {'fail': 'User does not exist!'}
			return render(request, 'registration/login.html', fail)
		else:
			
			if password != user_results.password:
				fail = {'fail': 'Incorrect password!'}
				return render(request, 'registration/login.html', fail)
			else:

				request.session['name'] = user_results.first_name + ' ' + user_results.last_name
				request.session['email'] = user_results.email
				request.session['id'] = user_results.user_id

				if not rmb:
					request.session.set_expiry(600)

				return HttpResponseRedirect('home')
	else:

		try:
			name = request.session['name']
		except:
			print('session expired!')
			return render(request, 'registration/login.html')
		else:
			print("session found!")
			return HttpResponseRedirect('home')


def home(request):

	try:
		name = request.session['name'] 
		email = request.session['email']
		points = request.session['points']
	except:
		print("session expired!")
		return HttpResponseRedirect('/memes')
	else:
		print("session found!")

	success = {'name': name,
			   'points': points,
			   'email': email,
			   'is_logged_in': True}
	return render(request, 'home/home.html', success)

def logout(request):

    try:
        del request.session
    except KeyError:
        print("key error has occured!")
    else:
    	print("session deleted")

    result_dict = {'logged_out': True}
    return render(request, 'base/index.html', result_dict)






def tasks(request):

	try:
		user_id = request.session['id']
		email = request.session['email']
	except KeyError:
		return HttpResponseRedirect('index')
	else:
		print("user_id {} obtained".format(user_id))

	task_query = """SELECT DISTINCT t.task_id,
									t.datetime_opened,
									p.plant,
									p.plant_type,
									p.location,
									CONCAT(u1.first_name, ' ', u1.last_name) AS requester,
									(CASE
									WHEN t.assignee_id IS NOT NULL THEN CONCAT(u2.first_name, ' ', u2.last_name)
									ELSE NULL
									END) AS assignee,
									t.points_given,
									t.urgency
									FROM tasks t, pots p, users u1, users u2
									WHERE t.requester_id = u1.user_id
									AND (t.assignee_id = u2.user_id OR
									 	 t.assignee_id isnull)
									AND t.is_done = false
									AND t.target_pot = p.pot_id
									AND u1.user_id != \'%s\'""" % (user_id)

	c = connection.cursor()
	c.execute(task_query)
	results = c.fetchall()

	result_dict = {'tasks': results,
				   'is_logged_in': True}

	return render(request, 'base/tasks.html', result_dict)

def your_tasks(request):

	try:
		user_id = request.session['id']
	except KeyError:
		return HttpResponseRedirect('index')
	else:
		print("user_id {} obtained".format(user_id))

	requested = Tasks.objects.filter(requester_id=user_id, is_done=False)
	requested = [(r.task_id, r.task, r.target_pot, r.assignee_id, r.points_given, r.datetime_opened, r.urgency) for r in requested]

	assigned = Tasks.objects.filter(assignee_id=user_id, is_done=False)
	assigned = [(r.task_id, r.task, r.target_pot, r.requester_id, r.points_given, r.datetime_opened, r.urgency) for r in assigned]

	result_dict = {'requested': requested,
				   'assigned': assigned,
				   'request_length': len(requested),
				   'accept_length': len(assigned)}

	return render(request, 'home/tasks.html', result_dict)

def accept_tasks(request):
	pass

def request_tasks(request):
	return render(request, 'base/request_tasks.html')

def create_tasks(request):

	task = request.POST.get('task', '')
	pot = request.POST.get('pot', '')
	points = request.POST.get('points', '')
	urgency = request.POST.get('urgency', '')

	try:
		requester_id = request.session['id']
	except:
		print("An error has occurred")
	else:
		print("user id {} obtained".format(requester_id))

	datetime_opened = datetime.now()
	c = connection.cursor()

	get_max_id_query = """SELECT MAX(t.id)
						  FROM tasks t """

	c.execute(get_max_id_query)
	max_id = c.fetchall()[0][0]

	get_curr_reqs_query = """ SELECT count(t.task_id)
							  from tasks t
							  WHERE t.requester_id = \'%s\' """ % (requester_id)

	c.execute(get_max_id_query)
	req_count = c.fetchall()[0][0]

	if req_count < 10:

		redemption_query = """ INSERT INTO tasks(task_id, task, target_pot, requester_id, assignee_id, points_given, datetime_opened, is_done, urgency)
							   VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\'); """ % (max_id + 1, task, pot, requester_id, None, points, datetime_opened, False, urgency)
		
		c.execute(redemption_query)
		session['latest_task'] = max_id + 1

	return redirect('your_tasks')





def rewards(request):

	try:
		user_id = request.session['id']
	except:
		print("An error has occurred")
		pass
	else:
		print("user id {} obtained".format(user_id))

	point_query = """ SELECT u.points
					  FROM users u
					  WHERE u.user_id = \'%s\'""" % (user_id)

	c = connection.cursor()
	c.execute(point_query)
	your_points = c.fetchall()[0][0]

	results = Rewards.objects.all()
	results = [(r.reward_id, r.reward, r.img, r.points_required, r.valid_till) for r in results]
	result_dict = {'rewards': results,
				   'points': your_points}
	return render(request, 'base/rewards.html', result_dict)

def your_rewards(request):

	session = request.session
	try:
		email = session['email']
	except:
		print("An error has occurred")
		pass
	else:
		user_results = Users.objects.get(email=email)
		user_id = user_results.user_id

	redemption_query =  """ SELECT *
							FROM rewards rw
							INNER JOIN redemption re ON re.reward_id = rw.reward_id
							WHERE re.user_id = \'%s\'
							AND re.has_been_used = false """ % (user_id)

	c = connection.cursor()
	c.execute(redemption_query)
	your_rewards = c.fetchall()

	point_query = """ SELECT u.points
					  FROM users u
					  WHERE u.user_id = \'%s\'""" % (user_id)

	c = connection.cursor()
	c.execute(point_query)
	your_points = c.fetchall()[0][0]

	result_dict = {'rewards': your_rewards,
				   'points': your_points,
				   'just_redeemed': None}

	try:
		just_redeemed = session['just_redeemed']
	except:
		print("failure!")
	else:
		try:
			new_reward = Rewards.objects.get(reward_id=just_redeemed)
		except:
			result_dict['message'] = 'We cannot verify what you have redeemed. Please contact the administrator.'
		else:
			result_dict['just_redeemed'] = new_reward.reward

	return render(request, 'home/rewards.html', result_dict)

def claim_rewards(request):

	try:
		user_id = request.session['id']
	except:
		print("session does not have points!")
		return HttpResponseRedirect('index')
	else:

		point_query = """ SELECT u.points
						  FROM users u
						  WHERE u.user_id = \'%s\'""" % (user_id)

		c = connection.cursor()
		c.execute(point_query)
		your_points = c.fetchall()[0][0]

		print("checking points for rewards claim, currently has: {} MemPts".format(your_points))

	id_no = request.POST.get('id', '')
	to_claim = Rewards.objects.get(reward_id=id_no)

	if your_points - to_claim.points_required < 0:
		remaining = your_points
	else:
		remaining = your_points - to_claim.points_required

	if your_points != remaining:

		point_query = """ UPDATE users 
						  SET points = \'%s\'
					      WHERE user_id = \'%s\';""" % (remaining, user_id)

		c = connection.cursor()
		c.execute(point_query)

		get_max_id_query = """SELECT MAX(redemption_id)
							  FROM redemption r """

		c.execute(get_max_id_query)
		max_id = c.fetchall()[0][0]

		redemption_query = """ INSERT INTO redemption(redemption_id, reward_id, user_id, redeem_datetime, has_been_used)
							   VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\');""" % (max_id + 1, id_no, user_id, datetime.now(), False)

		c.execute(redemption_query)

		request.session['just_redeemed'] = id_no
		request.session['used'] = to_claim.points_required

	return redirect('your_rewards')





def plants(request):

	pots = Pots.objects.all()
	pots = [(r.pot_id, r.location, r.pot_length, r.pot_width, r.pot_height, r.plant, r.plant_type) for r in pots]
	food = list(filter(lambda x: x[6]=='food', pots))
	deco = list(filter(lambda x: x[6]=='deco', pots))
	result_dict = {'food': food,
				   'deco': deco}
	return render(request, 'base/plants.html', result_dict)

def your_plants(request):

	try:
		user_id = request.session['id']
	except KeyError:
		return HttpResponseRedirect('index')
	else:
		print("user_id {} obtained".format(user_id))

	food_query = '''SELECT *
			   		FROM pots p
			   		WHERE p.plant_type = 'food'
			   		AND p.pot_id IN (
			   		SELECT o.pot_id
			  		FROM ownership o
			   		WHERE o.user_id = \'%s\')''' % (user_id)

	c = connection.cursor()
	c.execute(food_query)
	food = c.fetchall()

	deco_query = '''SELECT *
		   		FROM pots p
		   		WHERE p.plant_type = 'deco'
		   		AND p.pot_id IN (
		   		SELECT o.pot_id
		  		FROM ownership o
		   		WHERE o.user_id = \'%s\')''' % (user_id)

	c = connection.cursor()
	c.execute(deco_query)
	deco = c.fetchall()

	result_dict = {'food': food,
				   'deco': deco}

	return render(request, 'home/plants.html', result_dict)

def request_add_plant(request):
	return render(request, 'base/request_add_plants.html')

def add_plant(request):
	return HttpResponse("nada yada")