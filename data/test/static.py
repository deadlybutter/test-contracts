from test_contracts.models import StaticPage

StaticPage.create(name="TOS",
                  content="<p>This is sample data and should not be used in production.</p><p>TODO:  Discussion:  Terms of Service</p>")
StaticPage.create(name="Privacy",
                  content="<p>This is sample data and should not be used in production.</p> <p>TODO:  Discussion:  Privacy Policy</p>")
StaticPage.create(name="Insurance",
                  content="<p>This is sample data and should not be used in production.</p> <p>TODO:  Discussion:  Insurance Policy</p>")