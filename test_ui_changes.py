import os
import sys
import importlib.util

spec = importlib.util.spec_from_file_location("root_app", os.path.join(os.path.dirname(__file__), "app.py"))
root_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(root_app)
create_app = root_app.create_app

app = create_app()
client = app.test_client()

def test_navbar_anonymous():
    print("Testing navbar for anonymous user...")
    response = client.get('/')
    html = response.data.decode('utf-8')
    # logo link should go to / (or url_for('main.home') equivalent)
    assert 'href="/"' in html or 'href="http://localhost/"' in html, "Logo link is wrong"
    # both Browse Projects and Find Talent should be visible
    assert 'Browse Projects' in html, "Browse Projects missing"
    assert 'Find Talent' in html, "Find Talent missing"
    print("Anonymous navbar test passed!")

def test_navbar_client():
    print("Testing navbar for client user...")
    with client.session_transaction() as sess:
        sess['user_id'] = 1
        sess['role'] = 'client'
        sess['first_name'] = 'Client'
        sess['last_name'] = 'User'
        
    response = client.get('/')
    html = response.data.decode('utf-8')
    nav_start = html.find('<nav')
    nav_end = html.find('</nav>', nav_start)
    nav_html = html[nav_start:nav_end]
    
    assert 'Browse Projects' not in nav_html, "Browse Projects should be hidden for client"
    assert 'Find Talent' in nav_html, "Find Talent should be visible for client"
    assert 'href="/client/dashboard"' in nav_html, "Logo link should go to /client/dashboard"
    print("Client navbar test passed!")

def test_navbar_freelancer():
    print("Testing navbar for freelancer user...")
    with client.session_transaction() as sess:
        sess['user_id'] = 2
        sess['role'] = 'freelancer'
        sess['first_name'] = 'Freelancer'
        sess['last_name'] = 'User'
        
    response = client.get('/')
    html = response.data.decode('utf-8')
    nav_start = html.find('<nav')
    nav_end = html.find('</nav>', nav_start)
    nav_html = html[nav_start:nav_end]
    
    assert 'Find Talent' not in nav_html, "Find Talent should be hidden for freelancer"
    assert 'Browse Projects' in nav_html, "Browse Projects should be visible for freelancer"
    assert 'href="/freelancer/dashboard"' in nav_html, "Logo link should go to /freelancer/dashboard"
    print("Freelancer navbar test passed!")

if __name__ == '__main__':
    try:
        test_navbar_anonymous()
        test_navbar_client()
        test_navbar_freelancer()
        print("All Flask tests completed successfully!")
    except AssertionError as e:
        print("Test failed:", str(e))
        sys.exit(1)
