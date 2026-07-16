import os
import sys
import importlib.util

spec = importlib.util.spec_from_file_location("root_app", os.path.join(os.path.dirname(__file__), "app.py"))
root_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(root_app)
create_app = root_app.create_app

app = create_app()
client = app.test_client()

def test_view_project():
    print("Testing client view project with proposals...")
    with client.session_transaction() as sess:
        sess['user_id'] = 101 # Client: Arjun Sharma
        sess['role'] = 'client'
        sess['email'] = 'arjun.sharma@nexatech.in'
        sess['first_name'] = 'Arjun'
        sess['last_name'] = 'Sharma'
        
    response = client.get('/client/projects/1')
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    html = response.data.decode('utf-8')
    assert 'Deepak Verma' in html, "Deepak Verma (Freelancer) should be rendered in proposals list"
    assert 'Aditya Bose' in html, "Aditya Bose (Freelancer) should be rendered in proposals list"
    print("Client view project test passed successfully!")

def test_chat_inbox():
    print("Testing chat inbox content...")
    with client.session_transaction() as sess:
        sess['user_id'] = 101 # Client: Arjun Sharma
        sess['role'] = 'client'
        sess['email'] = 'arjun.sharma@nexatech.in'
        sess['first_name'] = 'Arjun'
        sess['last_name'] = 'Sharma'
        
    response = client.get('/chat/')
    assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"
    
    html = response.data.decode('utf-8')
    # According to our sample data, Arjun Sharma (101) has chat conversations with Deepak Verma (106) on project 1
    assert 'Deepak' in html or 'Verma' in html, "Deepak Verma should be present in conversation list"
    print("Chat inbox test passed successfully!")

if __name__ == '__main__':
    try:
        test_view_project()
        test_chat_inbox()
        print("All template fix validation tests completed successfully!")
    except AssertionError as e:
        print("TEMPLATES TEST FAILED:", str(e))
        sys.exit(1)
    except Exception as ex:
        print("UNEXPECTED ERROR DURING TESTING:", str(ex))
        sys.exit(1)
