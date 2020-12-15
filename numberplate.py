
import json
from openalpr import Alpr

alpr = Alpr("eu", "/etc/openalpr/openalpr.conf", "/usr/share/openalpr/runtime_data/")

if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)
results = alpr.recognize_file("car2.jpg")
print(json.dumps(results, indent=4))
alpr.unload()
