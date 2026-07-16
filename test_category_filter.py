import os
import sys
import importlib.util

spec = importlib.util.spec_from_file_location("root_app", os.path.join(os.path.dirname(__file__), "app.py"))
root_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(root_app)
create_app = root_app.create_app

app = create_app()
client = app.test_client()

def test_public_projects_category_filter():
    print("Testing public project search with category filter...")
    # Clean GET on /projects/
    response = client.get('/projects/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    html = response.data.decode('utf-8')
    assert 'Web Development' in html, "Web Development category option should be rendered inside category select list"
    
    # Test filtering by category: Web Development
    print("Filtering public projects by Web Development...")
    response_filtered = client.get('/projects/?category=Web+Development')
    assert response_filtered.status_code == 200
    html_filtered = response_filtered.data.decode('utf-8')
    assert 'Company Website Redesign' in html_filtered, "Company Website Redesign should show up under Web Development category filter"
    assert 'Google Ads' not in html_filtered, "Google Ads (Digital Marketing) should be filtered out"
    assert 'Logo Design' not in html_filtered, "Logo Design (Design) should be filtered out"
    print("Public projects category filter test passed!")

def test_freelancer_browse_category_filter():
    print("Testing freelancer browse projects page with category filter...")
    with client.session_transaction() as sess:
        sess['user_id'] = 106  # Freelancer
        sess['role'] = 'freelancer'
        sess['email'] = 'deepak.verma@gmail.com'
        sess['first_name'] = 'Deepak'
        sess['last_name'] = 'Verma'

    # Filter browse by category: Web Development
    print("Filtering freelancer browse projects by Web Development...")
    response = client.get('/freelancer/browse?category=Web+Development')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert 'Company Website Redesign' in html, "Company Website Redesign should show up under Web Development category filter"
    assert 'Google Ads' not in html, "Google Ads should be filtered out"
    print("Freelancer browse category filter test passed!")


def test_client_create_project_categories():
    print("Testing client project creation category dropdown options...")
    with client.session_transaction() as sess:
        sess['user_id'] = 101  # Client
        sess['role'] = 'client'
        sess['email'] = 'arjun.sharma@nexatech.in'
        sess['first_name'] = 'Arjun'
        sess['last_name'] = 'Sharma'

    response = client.get('/client/projects/create')
    assert response.status_code == 200
    html = response.data.decode('utf-8')
    assert '<option value="Web Development"' in html, "Web Development should be a valid select option in categories"
    assert '<option value="Design"' in html, "Design should be a valid select option in categories"
    print("Client create project categories test passed!")

if __name__ == '__main__':
    try:
        test_public_projects_category_filter()
        test_freelancer_browse_category_filter()
        test_client_create_project_categories()
        print("All Category Filter tests verified successfully!")
        sys.exit(0)
    except AssertionError as e:
        print("CATEGORY FILTER TEST FAILED:", str(e))
        sys.exit(1)
    except Exception as ex:
        print("UNEXPECTED ERROR:", str(ex))
        sys.exit(1)
