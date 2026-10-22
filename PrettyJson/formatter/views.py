from django.shortcuts import render
import json
# Create your views here.

def home(request):
    if request.method == "POST":
        raw_json = request.POST.get("json_input")
        action = request.POST.get("action")

        if action == "validate":
            try:
                parsed_json = json.loads(raw_json)
                result = "Valid JSON"
            
            except json.JSONDecodeError as error:
                result = f"Invalid JSON: {error}"
                return render(request, 'formatter/index.html', {"result": result})
            
        elif action == "format":
            try:
                parsed_json = json.loads(raw_json)
                result = json.dumps(parsed_json, indent=4)
            
            except json.JSONDecodeError as error:
                result = f"Invalid JSON: {error}"

        elif action == "minify":
            try:
                parsed_json = json.loads(raw_json)
                result = json.dumps(parsed_json, separators=(",", ":"))
           
            except json.JSONDecodeError as error:
                result = f"Invalid JSON: {error}"
        else:
            print("Invalid actions ")
    
    return render(request, 'formatter/index.html', {"result": result})


