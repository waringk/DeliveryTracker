# from django.contrib.auth.models import User
# from django.core.exceptions import ObjectDoesNotExist
#
# from .models import Event
# from django.core.files.base import ContentFile
#
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt, csrf_protect
# from datetime import datetime
#
# import json
# import cv2
# import numpy as np
#
#
# @csrf_exempt
# def upload_frame(request):
#     if request.method == 'POST':
#
#         # convert image
#         data = json.loads(request.body)
#         arrayFrame = np.asarray(data['arr'])
#         ret, jpg_frame = cv2.imencode('.jpg', arrayFrame)
#         content = ContentFile(jpg_frame.tobytes())
#
#         # get user
#         try:
#             # passing the pk is temporary, will update in later iteration
#             user = User.objects.get(pk=data['param'])
#         except ObjectDoesNotExist:
#             HttpResponse.status_code = 404
#             HttpResponse.reason_phrase = 'User not found. Register device'
#             return HttpResponse()
#
#         # create new image instance and save in db
#         eventInstance = Event(user=user)
#         photoName = str(datetime.now()) + '.jpg'
#         photoName = photoName.replace(" ", "_")
#         photoName = photoName.replace(":", ".")
#         eventInstance.photo.save(photoName, content, save=False)
#         eventInstance.save()
#
#     return HttpResponse('Upload successful')
#
