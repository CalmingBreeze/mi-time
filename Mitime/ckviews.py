import os
from django.conf import settings
from django.core.files.storage import default_storage
from django.http import JsonResponse

def custom_upload_file(request):
    if request.method == "POST" and request.FILES.get("upload"):
        uploaded_file = request.FILES["upload"]
        # Define the upload path (customize as needed)
        upload_path = os.path.join("ckeditor_uploads", uploaded_file.name)

        # Save the file using Django's storage system
        file_path = default_storage.save(upload_path, uploaded_file)
        file_url = default_storage.url(file_path)

        # Return the response CKEditor 5 expects
        return JsonResponse({"url": file_url})

    # If the request is invalid, return an error
    return JsonResponse(
        {"error": {"message": "Invalid request or no file uploaded."}}, status=400
    )