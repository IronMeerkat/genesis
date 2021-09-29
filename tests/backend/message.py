import test_agent

print('Logging in')
Meerkat = test_agent.TestAgent(username='meerkat', password='12345678', endpoint='/messages/')
Pangolin = test_agent.TestAgent(username='pangolin', password='12345678', endpoint='/messages/')
Badger = test_agent.TestAgent(username='badger', password='12345678', endpoint='/messages/')
Anon = test_agent.TestAgent(endpoint='/messages/')

print("Meerkat sending message to Pangolin")
meerkat_sent_message = Meerkat.post(recepient='pangolin', title="Hello Pangolin", body="It's me, Meerkat")
assert meerkat_sent_message.status_code == 201, f'Failed to send message. code: {meerkat_sent_message.status_code}'
print("Checking meerkat's mailboxes")
meerkat_mailbox = Meerkat.get()
assert meerkat_mailbox.json() == [], "Meerkat can see a message"
meerkat_outgoing = Meerkat.get('sender')
assert len(meerkat_outgoing.json()) == 1, "Meerkat can's see an outgoing message'"
msg_id = meerkat_outgoing.json()[0]['id']
print("Meerkat's mailboxes passed the initial message test")


print("Checking Pangolin's mailboxes")
pangolin_read_mailbox = Pangolin.get('read')
assert pangolin_read_mailbox.json() == [], "read messages showed up in Pangolin's mailbox"
pangolin_outgoing = Pangolin.get('sender')
assert pangolin_outgoing.json() == [], "Pangolin appears to have an outgoing message"
pangoling_mailbox = Pangolin.get()
assert int(pangoling_mailbox.json()[0]['id']) == msg_id, "No matching message in pangolin's inbox"
message = Pangolin.get(f'{msg_id}').json()
assert message['title'] == "Hello Pangolin" and message['body'] == "It's me, Meerkat", 'Wrong message found'
pangolin_read_mailbox = Pangolin.get('read')
assert len(pangolin_read_mailbox.json()) == 1, "Message not found in read"
print("Pangolin succesfully passed the initial message test")

print("Ensuring Badger is unable to access message")
badger_mail = Badger.get('all')
assert badger_mail.json() == [], "Badger has mail"
badger_message = Badger.get(f'{msg_id}')
assert badger_message.status_code >= 400, 'Badger gained unauthorozed access'
print("Badger succesfully passed the initial message test")

print("Ensuring Anon is unable to access message")
anon_mail = Anon.get()
assert anon_mail.status_code >= 400, "Anon can see a mailbox"
anon_message = Anon.get(f'{msg_id}')
assert anon_message.status_code >= 400, "Anon can see meerkat's message"
print("Anon passed test")


print('Pangolin deleting message')
deletion = Pangolin.delete(f'{msg_id}')
assert deletion.status_code == 204, "failed to delete"
pangolin_read_mailbox = Pangolin.get('read')
print(pangolin_read_mailbox.json())
assert pangolin_read_mailbox.json() == [], "read messages showed up in Pangolin's mailbox"
pangolin_deleted = Pangolin.get('deleted')
assert len(pangolin_deleted.json()) == 1, "Deleted message does not show up"
print('Pangolin succesfully deleted messages')

print("Ensuring meerkat can still see message")
meerkat_outgoing = Meerkat.get('sender')
assert len(meerkat_outgoing.json()) == 1, "Meerkat can's see an outgoing message'"
meerkat_outgoing = Meerkat.get('deleted')
assert meerkat_outgoing.json() == [], "Meerkat sees deleted message"
print('Meerkat can succesfully see message pangolin deleted as non-deleted')