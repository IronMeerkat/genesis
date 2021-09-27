import test_agent

Agent = test_agent.TestAgent(endpoint='/users/')

print("Getting current user before logging in")
print(Agent.get().json())

print("Registering a new user")
new_user = Agent.post(username='pikachu', password='12345678')
print(new_user.status_code)
assert new_user.status_code == 201, 'Failed to create new user'
faulty_user = Agent.post(username='pikachu', password='12345678')
assert faulty_user.status_code >= 400, f'Status code should be an error, but is {faulty_user.status_code}'  
print('New user has been registered')

print("Entering with the wrong password")
try:
    false_password = test_agent.TestAgent(username='pikachu', password='123', endpoint='/users')
except AssertionError as e:
    print("Wrong password succesfully rejected")
else:
    raise Exception("Entered with wrong password")

print("Entering with nonexisting user")
try:
    false_user = test_agent.TestAgent(username='raichu', password='12345678', endpoint='/users')
except AssertionError as e:
    print("Nonexisting user succesfully rejected")
else:
    raise Exception("Entered with nonexisting user")

print("Logging in with good credentials")
Agent = test_agent.TestAgent(username='pikachu', password='12345678', endpoint='/users')
assert Agent.headers.get('Authorization') is not None, 'Failed to get auth token'

print('Get self\'s details')
get_self = Agent.get()
assert get_self.status_code == 200, 'Bad status code'
print(get_self.json())
print('test passed succesfully')
