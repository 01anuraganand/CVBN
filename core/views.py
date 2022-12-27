from django.shortcuts import render
from . models import Image
from . forms import ImageForm
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
# Create your views here.
def index(request):
    return render(request, 'core/html/index.html')

def error(request):
    return render(request, 'core/html/error.html')

def architecture(request):
    return render(request, 'core/html/architecture.html')

def upload_photo(request):
    to_delete = Image.objects.all()
    to_delete.delete()
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    form = ImageForm()
    img = Image.objects.all()
    return form, img

def covid_model(request, filename):
    result = None
    model_path = "core/MODELS/model_max_val.h5"
    #filename = img[0][1:]
    
    img = image.load_img(filename, color_mode='rgb',target_size=(150, 150))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    model = tf.keras.models.load_model(model_path)
    print(model)
    classname_mapping = {'0': 'Bacterial Pneumonia', '1': 'Covid Positive', '2': 'Normal', '3': 'Viral Pneumonia'}
    pred = model.predict(x)
    ans = pred.argmax()
    for value in classname_mapping:
        if int(value) == ans:
            result = classname_mapping[value]
    return np.max(pred)*100, result

def render_upload_photo(request):
    form = img = max_pred = pred = model = emoji_path =  None
    form, img = upload_photo(request)
    img_path = [str(x.photo.url) for x in img] 
    return render(request, 'core/html/upload_img.html', {'form' : form, 'img' : img,'pred': pred, 'max_pred': max_pred , 'model': model, 'emoji_path' : emoji_path})


@csrf_exempt
def render_upload_photo_classify(request):
    form = img = result = model =predv =   None
    form, img  = upload_photo(request)
    img_path = [str(x.photo.url) for x in img]

    if(len(img_path)>0):
        try:
            predv, result = covid_model(request, img_path[0][1:])
        except:
            #return HttpResponseRedirect('core/html/error.html')
            print('-------getting errror ------')
    return render(request, 'core/html/upload_img.html', {'form' : form, 'img' : img,'pred': result, 'predv': predv, 'model': model})
