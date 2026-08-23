import http.server
import json
import os
import urllib.parse

# Load policies dataset from data.json
dir_path = os.path.dirname(os.path.realpath(__file__))
json_path = os.path.join(dir_path, 'data.json')

with open(json_path, 'r', encoding='utf-8') as f:
    policies_list = json.load(f)

class PolicyHubHandler(http.server.SimpleHTTPRequestHandler):
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == '/api/stats':
            self.handle_stats()
        elif path == '/api/schemes':
            self.handle_schemes(parsed_url.query)
        else:
            # Serve static files normally using parent handler
            super().do_GET()

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8')) if post_data else {}
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON"}, 400)
            return

        if path == '/api/eligibility':
            self.handle_eligibility(data)
        elif path == '/api/compare':
            self.handle_compare(data)
        else:
            self.send_response(404)
            self.end_headers()

    def handle_stats(self):
        total_count = len(policies_list)
        central_count = len([p for p in policies_list if p.get('category') != 'state'])
        state_count = len([p for p in policies_list if p.get('category') == 'state'])
        
        states_with_schemes = set()
        for p in policies_list:
            if p.get('category') == 'state' and p.get('stateSpecific'):
                for s in p.get('stateSpecific', []):
                    states_with_schemes.add(s)
        states_with_schemes_count = len(states_with_schemes)
        
        cats = ['agriculture', 'women', 'health', 'education', 'housing', 'livelihood', 'social', 'digital', 'state']
        category_counts = [len([p for p in policies_list if p.get('category') == c]) for c in cats]
        
        budget_top = sorted([p for p in policies_list if p.get('budget', 0) > 0], key=lambda x: x['budget'], reverse=True)[:10]
        benef_top = sorted([p for p in policies_list if p.get('beneficiaries', 0) > 0], key=lambda x: x['beneficiaries'], reverse=True)[:10]
        
        stats = {
            "totalCount": total_count,
            "centralCount": central_count,
            "stateCount": state_count,
            "statesWithSchemes": states_with_schemes_count,
            "totalStates": 28, # standard state list length
            "categoryCounts": category_counts,
            "budgetTop": budget_top,
            "benefTop": benef_top
        }
        self.send_json(stats)

    def handle_schemes(self, query_str):
        params = urllib.parse.parse_qs(query_str)
        category = params.get('category', ['all'])[0]
        query = params.get('q', [''])[0].strip().lower()

        filtered = policies_list
        if category != 'all':
            filtered = [p for p in filtered if p.get('category') == category]
            
        if query:
            filtered = [
                p for p in filtered
                if query in p.get('title', '').lower()
                or query in p.get('subtitle', '').lower()
                or query in p.get('tag', '').lower()
                or query in p.get('description', '').lower()
            ]
            
        self.send_json(filtered)

    def handle_eligibility(self, u):
        age = int(u.get('age', 0))
        income = float(u.get('income', 0))
        gender = u.get('gender', 'any')
        profession = u.get('profession', 'any')
        caste = u.get('caste', 'any')
        state = u.get('state', '')
        bpl = bool(u.get('bpl', False))
        land = bool(u.get('land', False))
        pregnant = bool(u.get('pregnant', False))
        girls = str(u.get('girls', '0'))
        house = bool(u.get('house', False))

        results = []
        for p in policies_list:
            score = 0
            max_score = 0
            blockers = []
            e = p.get('eligibility', {})
            
            # Age check
            max_score += 20
            age_min = e.get('ageMin', 0)
            age_max = e.get('ageMax', 120)
            if age >= age_min and age <= age_max:
                score += 20
            else:
                blockers.append(f"Age {age} outside required range {age_min}-{age_max}")
                
            # Gender check
            max_score += 15
            p_gender = e.get('gender', ['any'])
            if 'any' in p_gender or gender in p_gender:
                score += 15
            else:
                blockers.append(f"Scheme is {'/'.join(p_gender)}-only")
                
            # Income check
            max_score += 20
            income_max = e.get('incomeMax', 999999999)
            if income <= income_max:
                score += 20
            elif income <= income_max * 1.3:
                score += 8
            else:
                blockers.append("Income exceeds scheme limit")
                
            # Profession check
            max_score += 20
            p_profession = e.get('profession', ['any'])
            if 'any' in p_profession or profession in p_profession:
                score += 20
            else:
                score += 5
                
            # Caste check
            max_score += 10
            p_caste = e.get('caste', ['any'])
            if 'any' in p_caste or caste in p_caste:
                score += 10
                
            # BPL check
            max_score += 5
            bpl_req = e.get('bplRequired', False)
            if not bpl_req:
                score += 5
            elif bpl:
                score += 5
            else:
                blockers.append("BPL card required")
                
            # Land check
            max_score += 5
            land_req = e.get('landRequired', False)
            if not land_req:
                score += 5
            elif land:
                score += 5
            else:
                blockers.append("Agricultural land required")
                
            # State-specific check
            p_state = p.get('stateSpecific')
            if p_state:
                state_match = any(s.lower() == state.lower() for s in p_state)
                if not state_match:
                    score = min(score, 30)
                    blockers.append(f"State-specific scheme ({', '.join(p_state)})")
                else:
                    score += 5
                    
            # Special boosts
            p_id = p.get('id')
            if pregnant and p_id == 'janani-suraksha':
                score = min(100, score + 20)
            if girls != '0' and p_id in ['beti-bachao', 'sukanya-samriddhi']:
                score = min(100, score + 15)
            if girls != '0' and p_id in ['ladli-delhi', 'kanyashree-wb']:
                score = min(100, score + 15)
            if not house and p_id in ['pm-awas-gramin', 'pm-awas-urban']:
                score = min(100, score + 10)
                
            pct = round((score / max_score) * 100) if max_score > 0 else 0
            results.append({
                "policy": p,
                "score": pct,
                "blockers": blockers
            })
            
        results.sort(key=lambda x: x['score'], reverse=True)
        self.send_json(results)

    def handle_compare(self, data):
        id_a = data.get('idA')
        id_b = data.get('idB')

        p_a = next((p for p in policies_list if p.get('id') == id_a), None)
        p_b = next((p for p in policies_list if p.get('id') == id_b), None)

        self.send_json({
            "policyA": p_a,
            "policyB": p_b
        })

if __name__ == '__main__':
    server_address = ('', 3456)
    httpd = http.server.HTTPServer(server_address, PolicyHubHandler)
    print("Policy Hub server running at http://localhost:3456 ...")
    httpd.serve_forever()
