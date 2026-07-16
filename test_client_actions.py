import os
import sys
import importlib.util

spec = importlib.util.spec_from_file_location("root_app", os.path.join(os.path.dirname(__file__), "app.py"))
root_app = importlib.util.module_from_spec(spec)
spec.loader.exec_module(root_app)
create_app = root_app.create_app

app = create_app()
client = app.test_client()

def test_view_project_no_build_error():
    print("Testing client view_project routing and content...")
    with client.session_transaction() as sess:
        sess['user_id'] = 101  # Client Arjun Sharma
        sess['role'] = 'client'
        sess['email'] = 'arjun.sharma@nexatech.in'
        sess['first_name'] = 'Arjun'
        sess['last_name'] = 'Sharma'

    # Project 2
    response = client.get('/client/projects/2')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    html = response.data.decode('utf-8')
    assert 'Manage Project' in html, "Page should contain 'Manage Project' title"
    # Check that it uses the unified proposal_action endpoint
    assert '/client/proposals/' in html, "Page should link to /client/proposals/"
    assert '/action' in html
    assert 'shortlist' in html
    print("view_project routing and content test passed!")

def test_compare_proposals_no_build_error():
    print("Testing compare_proposals routing and content...")
    with client.session_transaction() as sess:
        sess['user_id'] = 101
        sess['role'] = 'client'
        sess['email'] = 'arjun.sharma@nexatech.in'
        sess['first_name'] = 'Arjun'
        sess['last_name'] = 'Sharma'

    # Project 2 compare
    response = client.get('/client/proposals/compare/2')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    html = response.data.decode('utf-8')
    assert 'Compare Proposals' in html
    assert '/client/proposals/' in html
    assert '/action' in html
    print("compare_proposals routing and content test passed!")

def test_proposal_action_execution():
    print("Testing client proposal action execution (shortlist)...")
    with app.app_context():
        with client.session_transaction() as sess:
            sess['user_id'] = 101
            sess['role'] = 'client'
            sess['email'] = 'arjun.sharma@nexatech.in'
            sess['first_name'] = 'Arjun'
            sess['last_name'] = 'Sharma'

        # Retrieve proposal 3 status before action
        from app.models.proposal import ProposalModel
        prop_before = ProposalModel.get_by_id(3)
        print(f"Proposal 3 status before: {prop_before['status']}")

        # Form post to shortlist proposal 3
        response = client.post(
            f'/client/proposals/3/action',
            data={'action': 'shortlist', 'client_note': 'Looks good!'}
        )
        # Redirects back to client.view_project for project 2
        assert response.status_code == 302, f"Expected redirect, got {response.status_code}"
        
        prop_after = ProposalModel.get_by_id(3)
        print(f"Proposal 3 status after: {prop_after['status']}")
        assert prop_after['status'] == 'shortlisted', "Proposal 3 status should be shortlisted"
        print("Proposal action execution test passed!")

if __name__ == '__main__':
    try:
        test_view_project_no_build_error()
        test_compare_proposals_no_build_error()
        test_proposal_action_execution()
        print("All Client Action BuildError tests verified successfully!")
        sys.exit(0)
    except AssertionError as e:
        print("TEST FAILED:", str(e))
        sys.exit(1)
    except Exception as ex:
        print("UNEXPECTED ERROR:", str(ex))
        sys.exit(1)
