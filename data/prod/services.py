from test_contracts.models import Services

# Services.create(name='', description='', active=1, category=1)
# Category should be 1 = Support, 2 = Crew, 3 = Combat

# REQUIRED
# #### crew handler ##### REQUIRED ####
Services.create(name='Crew Members', description='This should never be set to active.', active=0, category=2)
# #####################################

# support
Services.create(name='Transport - Cargo', description='This is a description.', active=1, category=1)
Services.create(name='Transport - Fuel', description='This is a description.', active=1, category=1)
Services.create(name='Transport - Personnel', description='This is a description.', active=1, category=1)
Services.create(name='Salvage', description='This is a description.', active=1, category=1)
Services.create(name='Repair', description='This is a description.', active=1, category=1)
Services.create(name='Refueling', description='This is a description.', active=1, category=1)
Services.create(name='Mining', description='This is a description.', active=1, category=1)

# crew
Services.create(name='Pilot', description='This is a description.', active=1, category=2)
Services.create(name='Radar', description='This is a description.', active=1, category=2)
Services.create(name='Weapons', description='This is a description.', active=1, category=2)
Services.create(name='Gunner', description='This is a description.', active=1, category=2)
Services.create(name='Engineer', description='This is a description.', active=1, category=2)
Services.create(name='Navigation', description='This is a description.', active=1, category=2)
Services.create(name='Communications', description='This is a description.', active=1, category=2)
Services.create(name='Security', description='This is a description.', active=1, category=2)
Services.create(name='Science', description='This is a description.', active=1, category=2)
Services.create(name='Medical', description='This is a description.', active=1, category=2)

# combat
Services.create(name='Bombing', description='This is a description.', active=1, category=3)
Services.create(name='Escort', description='This is a description.', active=1, category=3)
Services.create(name='Bounty Hunting', description='This is a description.', active=1, category=3)
Services.create(name='Combat Medic', description='This is a description.', active=1, category=3)
Services.create(name='Combat Drop - Personnel', description='This is a description.', active=1, category=3)
Services.create(name='Combat Drop - Supplies', description='This is a description.', active=1, category=3)
Services.create(name='Electronic Warfare', description='This is a description.', active=1, category=3)
