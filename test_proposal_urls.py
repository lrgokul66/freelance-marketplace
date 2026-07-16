import os
import sys
import importlib.util

spec = importlib.util.spec_from_file_location("root_app", os.path.join(os.path.dirname(__file__), "app.py"))
root_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(root_app)
create_app = root_app.create_app

app = create_app()
client = app.test_client()

def test_proposal_pages():
    print("Testing freelancer proposal views for BuildErrors...")
    with client.session_transaction() as sess:
        sess['user_id'] = 106  # Freelancer: Deepak Verma
        sess['role'] = 'freelancer'
        sess['email'] = 'deepak.verma@gmail.com'
        sess['first_name'] = 'Deepak'
        sess['last_name'] = 'Verma'
        
    # Test proposal listing page
    print("1. Accessing freelancer proposals list Page...")
    response = client.get('/freelancer/proposals')
    assert response.status_code == 200, f"Expected 200 on proposals list, got {response.status_code}"
    
    # Test proposal detail page (proposal 1 belongs to Deepak Verma 106)
    print("2. Accessing proposal detail Page (proposal 1)...")
    response_detail = client.get('/proposals/1')
    assert response_detail.status_code == 200, f"Expected 200 on proposal detail, got {response_detail.status_code}"
    
    # Test proposal edit page directly (proposal 3 is pending and belongs to Deepak Verma 106)
    print("3. Accessing proposal edit Page directly (proposal 3)...")
    response_edit = client.get('/proposals/3/edit')
    assert response_edit.status_code == 200, f"Expected 200 on proposal edit, got {response_edit.status_code}"
    html = response_edit.data.decode('utf-8')
    assert 'Project budget' in html, "Project budget label should be rendered"
    assert '30000' in html, "Budget min should be rendered"
    assert '80000' in html, "Budget max should be rendered"
    
    print("All proposals url_for routing tests passed successfully!")

if __name__ == '__main__':
    try:
        test_proposal_pages()
        sys.exit(0)
    except AssertionError as e:
        print("PROPOSAL ROUTING TEST FAILED:", str(e))
        sys.exit(1)
    except Exception as ex:
        print("UNEXPECTED ERROR DURING TESTING:", str(ex))
        sys.exit(1)
