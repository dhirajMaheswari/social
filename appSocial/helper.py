import os
from PIL import Image
from django.core.files.base import ContentFile

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
abcdpath = BASE_DIR+os.path.sep+"appSocial"+os.path.sep+"abcd"

def convert_list_to_ditc(list_input):
    dict_return = {}
    for l in list_input:
        dict_return[l] = dict_return.get(l,0) + 1
    return dict_return

def get_extension(fn):
    et = os.path.basename(fn)
    ext = et.split(".")[-1]
    return ext

def upload_to_disk(request):
    os.chdir(BASE_DIR)
    folder = request.path.replace("/", "_")
    # uploaded_filename = request.FILES['file'].name
    uploaded_filename = request.FILES['your_image']
    uploaded_filename = str(uploaded_filename).replace(" ", "_")
    # print(uploaded_filename)
    dname = str(request.user)+"_"+str(request.user.id)
    u_dir = abcdpath+os.path.sep+dname+os.path.sep+"images"
    if os.path.exists(u_dir):
        os.chdir(u_dir)
    else:
        os.mkdir(u_dir)
    # save the uploaded file inside that folder.
    full_filename = os.path.join(u_dir,  uploaded_filename)
    img = Image.open(request.FILES['your_image'])
    img.save(full_filename)
    # print(os.path.getsize(full_filename))
    # fout = open(full_filename, 'wb+')
    # file_content = ContentFile( request.FILES['your_image'].read() )
    #
    # # Iterate through the chunks.
    # for chunk in file_content.chunks():
    #     fout.write(chunk)
    # fout.close()
    print("File {} saved to disk.".format(full_filename))


def upload_video_to_disk(request):
    os.chdir(BASE_DIR)
    folder = request.path.replace("/", "_")
    # uploaded_filename = request.FILES['file'].name
    uploaded_filename = request.FILES['your_image']
    uploaded_filename = str(uploaded_filename).replace(" ", "_")
    # print(uploaded_filename)
    dname = str(request.user)+"_"+str(request.user.id)
    u_dir = abcdpath+os.path.sep+dname+os.path.sep+"videos"
    if os.path.exists(u_dir):
        os.chdir(u_dir)
    else:
        os.mkdir(u_dir)
    # save the uploaded file inside that folder.
    full_filename = os.path.join(u_dir,  uploaded_filename)
    fout = open(full_filename, 'wb+')
    file_content = ContentFile( request.FILES['your_image'].read() )

    # Iterate through the chunks.
    for chunk in file_content.chunks():
        fout.write(chunk)
    fout.close()
    print("File {} saved to disk.".format(full_filename))
