from django.shortcuts import render
import json
# Create your views here.

def home(request):
    result = ""

    if request.method == "POST":
        raw_json = request.POST.get("json_input")
        action = request.POST.get("action")
        try:
            parsed_json = json.loads(raw_json)

            if action == "validate":
                result = "Valid JSON"
                      
            elif action == "format":
                result = json.dumps(parsed_json, indent=4)            

            elif action == "minify":
                result = json.dumps(parsed_json, separators=(",", ":"))
           
            else:
                result = "Invalid Action Selected"
        except json.JSONDecodeError as error:
            result = f"Invalid JSON: {error}"
            
    return render(request, 'formatter/index.html', {"result": result})


def compare(request):
    return render(request, 'formatter/compare.html')
