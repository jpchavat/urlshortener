import os
import sys

# add the parent directory to the sys.path
sys.path = [os.path.join(os.path.dirname(__file__), "..")] + sys.path

try:
    from redirector.app import create_app
except ImportError:
    from admin.app import create_app

app = create_app(load_redis=False, load_views=False, load_db=True)
with app.app_context():
    print("Creating tables...")
    print(app.config)
    from common.models.urlobject import URLObject
    from common.models.analytic import AnalyticRecord

    URLObject.exists() or URLObject.create_table()
    AnalyticRecord.exists() or AnalyticRecord.create_table()
    print("Created.2")
