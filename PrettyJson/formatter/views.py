import json

from django.shortcuts import render


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

    return render(request, "formatter/index.html", {"result": result})


# --------------------------------------------------------------------------
# Compare
# --------------------------------------------------------------------------

def _show(value):
    """Render a JSON value for display (strings keep quotes, True -> true)."""
    return json.dumps(value, ensure_ascii=False)


def _equal(a, b):
    """Like ==, but True/False never equal 1/0."""
    if isinstance(a, bool) != isinstance(b, bool):
        return False
    return a == b


def _diff(a, b, path, added, removed, modified):
    """Walk two parsed JSON values and collect differences by path."""
    if isinstance(a, dict) and isinstance(b, dict):
        for key in a:
            child = f"{path}.{key}"
            if key in b:
                _diff(a[key], b[key], child, added, removed, modified)
            else:
                removed.append({"path": child, "value": _show(a[key])})

        for key in b:
            if key not in a:
                added.append({"path": f"{path}.{key}", "value": _show(b[key])})

    elif isinstance(a, list) and isinstance(b, list):
        for index in range(max(len(a), len(b))):
            child = f"{path}[{index}]"
            if index >= len(a):
                added.append({"path": child, "value": _show(b[index])})
            elif index >= len(b):
                removed.append({"path": child, "value": _show(a[index])})
            else:
                _diff(a[index], b[index], child, added, removed, modified)

    elif not _equal(a, b):
        modified.append({"path": path, "old": _show(a), "new": _show(b)})


def _parse(raw, label):
    """Return (parsed_value, error_message). Exactly one of them is None."""
    if not raw.strip():
        return None, f"{label} JSON is empty."

    try:
        return json.loads(raw), None
    except json.JSONDecodeError as error:
        return None, f"Invalid JSON: {error.msg} (line {error.lineno}, column {error.colno})"


def compare(request):
    context = {"json_a": "", "json_b": ""}

    if request.method == "POST":
        json_a = request.POST.get("json_a", "")
        json_b = request.POST.get("json_b", "")

        # Keep the text in the editors after submitting.
        context["json_a"] = json_a
        context["json_b"] = json_b

        original, error_a = _parse(json_a, "Original")
        modified, error_b = _parse(json_b, "Modified")

        if error_a or error_b:
            if error_a:
                context["error_a"] = error_a
            if error_b:
                context["error_b"] = error_b
            context["error"] = "Fix the highlighted JSON and try again."
        else:
            added, removed, changed = [], [], []

            try:
                _diff(original, modified, "$", added, removed, changed)
            except RecursionError:
                context["error"] = "These documents are nested too deeply to compare."
            else:
                context["result"] = {
                    "identical": not (added or removed or changed),
                    "added": added,
                    "removed": removed,
                    "modified": changed,
                }

    return render(request, "formatter/compare.html", context)