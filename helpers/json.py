from flask import make_response, jsonify


def json_response(data=None, status="success", code=200):
    body = {"status": status}
    if status == "success" and data:
        body['data'] = data
    else:
        body['message'] = data

    response = make_response(jsonify(body), code)
    response.headers["Content-Type"] = "application/json"
    return response
