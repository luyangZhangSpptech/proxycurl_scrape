import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/fetch-linkedin-profiles', methods=['POST'])
def fetch_linkedin_profiles():
    data = request.json
    api_key = ''  # Store your API key here or use environment variables for security
    headers = {'Authorization': 'Bearer ' + api_key}
    api_endpoint = 'https://nubela.co/proxycurl/api/v2/linkedin'
    linkedin_base_url = 'https://www.linkedin.com/in/'
    
    profiles_data = []

    for username in data['usernames']:
        profile_url = linkedin_base_url + username  # Construct the full URL
        response = requests.get(api_endpoint,
                                params={'url': profile_url, 'skills': 'include'},
                                headers=headers)
        if response.status_code == 200:
            profile = response.json()
            # Extract desired fields
            profile_data = {
                'full_name': profile.get('full_name', ''),
                'occupation': profile.get('occupation', ''),
                'headline': profile.get('headline', ''),
                'summary': profile.get('summary', ''),
                'country_full_name': profile.get('country_full_name', ''),
                'city': profile.get('city', ''),
                'state': profile.get('state', ''),
                'experiences': profile.get('experiences', []),
                'education': profile.get('education', []),
                'languages': profile.get('languages', []),
                'certifications': profile.get('certifications', []),
                'gender': profile.get('gender', '')
            }
            profiles_data.append(profile_data)
        else:
            profiles_data.append({"error": "Failed to fetch data for " + username, "status_code": response.status_code})

    return jsonify(profiles_data)

if __name__ == '__main__':
    app.run(debug=True)  # Run the server
