import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.app import create_app

app = create_app()

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5001))
    print(f'Starting Medicinal Plant API on http://localhost:{port}')
    app.run(debug=True, host='0.0.0.0', port=port)
