import test_agent

Agent = test_agent.TestAgent(endpoint='/users/')

print("Getting current user before logging in")
print(Agent.get().json())

print("Registering a new user")
meerkat = Agent.post(username='meerkat', password='12345678')
badger = Agent.post(username='badger', password='12345678')
pangolin = Agent.post(username='pangolin', password='12345678')
regs = [user.status_code == 201 for user in (meerkat, badger, pangolin)]

assert all(regs), 'Failed to create new users'
faulty_user = Agent.post(username='meerkat', password='12345678')
assert faulty_user.status_code >= 400, f'Status code should be an error, but is {faulty_user.status_code}'  
print('New user has been registered')

print("Entering with the wrong password")
try:
    false_password = test_agent.TestAgent(username='meerkat', password='123', endpoint='/users')
except AssertionError as e:
    print("Wrong password succesfully rejected")
else:
    raise Exception("Entered with wrong password")

print("Entering with nonexisting user")
try:
    false_user = test_agent.TestAgent(username='pikachu', password='12345678', endpoint='/users')
except AssertionError as e:
    print("Nonexisting user succesfully rejected")
else:
    raise Exception("Entered with nonexisting user")

print("Logging in with good credentials")
Meerkat = test_agent.TestAgent(username='meerkat', password='12345678', endpoint='/users/')
assert Meerkat.headers.get('Authorization') is not None, 'Failed to get auth token'

print('Get self\'s details')
get_self = Meerkat.get()
assert get_self.status_code == 200, 'Bad status code'
print(get_self.json())
print('test passed succesfully')
