from icecream import ic
from flask import Flask, request, jsonify
from data_handler import DataHandler
from lib.qs import PAGE, TIER, USER_ID
from lib.emoji_validator import EmojiSizeValidator

FORM_FILE_NAME = "data"

app = Flask(__name__)
data_handler = DataHandler()


@app.route("/api/gallery", methods=["GET"])
def get_gallery_images():
    """
    This route used to retrieve page of blobs of images
    """
    page = request.args.get(PAGE, 1)
    tier = request.args.get(TIER, 1)

    data = data_handler.get_previews_from_gallery(tier, page)
    return jsonify({"images": [image.__str__() for image in data]}), 200


@app.route("/api/gallery/<image_id>", methods=["GET"])
def get_full_size_gallery_image_url(image_id):
    """
    This route used to retrieve a full size emoji url from the db
    You need to have the correct tier access to use the advanced images
    """
    ic(image_id)
    tier = request.args.get(TIER, 1)

    url = data_handler.get_single_image_from_gallery(tier, image_id)
    return jsonify({"asset_url": url}), 200


@app.route("/api/uploads", methods=["GET"])
def get_uploaded_images():
    """
    This route used to retrieve page of blobs of images
    """
    page = request.args.get(PAGE, 1)
    user_id = request.args.get(USER_ID)

    data = data_handler.get_previews_from_user_uploads(user_id, page)
    return jsonify({"images": [image.__str__() for image in data]}), 200


@app.route("/api/uploads/<image_id>", methods=["GET"])
def get_full_size_uploaded_image_url(image_id):
    """
    This route used to retrieve a full size emoji url from the db
    You need to have the correct tier access to use the advanced images
    """
    ic(image_id)
    user_id = request.args.get(USER_ID)
    data = data_handler.get_single_image_from_user_uploads(user_id, image_id)

    return jsonify({"asset_url": data}), 200


@app.route("/api/uploads", methods=["POST"])
def upload_image():
    """
    This route used to upload images to user personal image
        Free users able to add 5 images
        Premium  users able to add 100 images
        No limits for Business user

    """
    user_id = request.args.get(USER_ID)
    tier = request.args.get(TIER, 1)

    if FORM_FILE_NAME not in request.files:
        return jsonify({"error": "no file uploaded"}), 400

    stream = request.files[FORM_FILE_NAME].stream
    validator = EmojiSizeValidator(stream)

    if not validator.is_size_valid():
        return jsonify({"error": "file too big - max size 10Mb"}), 413

    image = request.files[FORM_FILE_NAME].read()
    try:
        data = data_handler.upload_image_to_user_uploads(user_id, tier, image)
        return jsonify({"data": data.__str__()}), 200

    except ValueError as e:
        return jsonify({"error": e}), 400
    except Exception as e:
        print(e)
        return jsonify({"error": "unknown error - check logs"}), 500


if __name__ == "__main__":
    app.run(debug=True)


# @app.route('/api/data', methods=['POST'])
# def handle_data():
#     data = request.get_json()
#     # ic(data)
#     if not data:
#         return jsonify({'error': 'No data provided'}), 400

#     payloads = data.get('payloads', [])
#     if not payloads:
#         return jsonify({'error': 'No payloads provided'}), 400

#     futures = [executor.submit(process_data, payload) for payload in payloads]

#     results = []
#     for future in as_completed(futures):
#         try:
#             result = future.result()
#             results.append(result)
#         except Exception as e:
#             return jsonify({'error': str(e)}), 500

#     return jsonify({'results': results}), 200


# def process_data(payload):
#     # Simulate a long-running task
#     time.sleep(random.randint(1, 5))
#     result = {'payload': payload, 'processed': True}
#     return result
