import datetime
from test_contracts.utils import add_event
from test_contracts.models import Contract

# transport cargo sample
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='fuel filler', time=datetime.datetime.utcnow(), fuel=20)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='scu filler', time=datetime.datetime.utcnow(), scu=20)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='passengers filler', time=datetime.datetime.utcnow(), passengers=20)
Contract.create(user_id=2, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='scu and fuel filler.', time=datetime.datetime.utcnow(), scu=20, fuel=20)
Contract.create(user_id=2, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='this is just some filler.', time=datetime.datetime.utcnow(), scu=20)
Contract.create(user_id=2, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='this is just some filler.', time=datetime.datetime.utcnow(), scu=20)
Contract.create(user_id=3, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='this is just some filler.', time=datetime.datetime.utcnow(), scu=20)
Contract.create(user_id=4, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='this is just some filler.', time=datetime.datetime.utcnow(), scu=20)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='this is just some filler.', time=datetime.datetime.utcnow(), scu=20, status=2)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='this is just some filler.', time=datetime.datetime.utcnow(), scu=20, status=2)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='this is just some filler.', time=datetime.datetime.utcnow(), scu=20, status=2)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='status number 6', time=datetime.datetime.utcnow(), scu=20, status=6)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='status number 5', time=datetime.datetime.utcnow(), scu=20, status=5)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='status number 4', time=datetime.datetime.utcnow(), scu=20, status=4)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='status number 3', time=datetime.datetime.utcnow(), scu=20, status=3)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='status number 2', time=datetime.datetime.utcnow(), scu=20, status=2)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='status number 1', time=datetime.datetime.utcnow(), scu=20, status=1)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='status number 0', time=datetime.datetime.utcnow(), scu=20, status=0)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='status number 0 x2', time=datetime.datetime.utcnow(), scu=20, status=0)
Contract.create(user_id=1, start_location="Your mom", end_location="The bedroom", service_id=1, ship_id=54,
                description='unknown status code', time=datetime.datetime.utcnow(), scu=20, status=7)

jobs = Contract.query.all()

for job in jobs:
    add_event(event="Contract Created.", user=1, invoice=job.invoice)