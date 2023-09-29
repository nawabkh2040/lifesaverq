from django.shortcuts import render, HttpResponse ,redirect
import qrcode
from io import BytesIO
import base64
from django.http import FileResponse
from PIL import Image
import tempfile
import os

def create_qr_code(data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")

    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    return img_str

def profile(request):
    if request.method == 'POST':
        person_name = request.POST['person_name']
        p_mobile_number = request.POST['p_mobile_number']
        family_name1 = request.POST['family_name1']
        family_contact1 = request.POST['family_contact1']
        family_name2 = request.POST['family_name2']
        family_contact2 = request.POST['family_contact2']
        family_name3 = request.POST['family_name3']
        family_contact3 = request.POST['family_contact3']
        blood_group = request.POST['blood_group']
        medical_description = request.POST['medical_description']

        # Generate QR code data
        qr_data = f"Person Name: {person_name}\n"
        qr_data += f"Mobile Number: {p_mobile_number}\n"
        qr_data += f"Family Contact 1: {family_name1} - {family_contact1}\n"
        qr_data += f"Family Contact 2: {family_name2} - {family_contact2}\n"
        qr_data += f"Family Contact 3: {family_name3} - {family_contact3}\n"
        qr_data += f"Blood Group: {blood_group}\n"
        qr_data += f"Medical Description: {medical_description}"

        # Generate QR code
        qr_code = create_qr_code(qr_data)

        # Save the QR code as a file
        img = Image.open(BytesIO(base64.b64decode(qr_code)))
        temp_dir = tempfile.mkdtemp()
        qr_code_path = os.path.join(temp_dir, 'qrcode.png')
        img.save(qr_code_path, 'PNG')
        request.session['qr_code_data'] = qr_code
        # Provide a download link for the QR code
        response = FileResponse(open(qr_code_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="qrcode.png"'
     #    return response
        return redirect('display_qr_code')

    return render(request, 'emergencyapp/index.html')

def display_qr_code(request):
    # Retrieve the QR code data from the session (set it in the profile view)
    qr_code_data = request.session.get('qr_code_data')

    if not qr_code_data:
        return HttpResponse("QR code data not found.")

    # Generate the QR code image
    img = Image.open(BytesIO(base64.b64decode(qr_code_data)))
    
    # Save the QR code as a file (optional)
    temp_dir = tempfile.mkdtemp()
    qr_code_path = os.path.join(temp_dir, 'qrcode.png')
    img.save(qr_code_path, 'PNG')

    # Provide a download link for the QR code
    response = FileResponse(open(qr_code_path, 'rb'))
    response['Content-Disposition'] = f'attachment; filename="qrcode.png"'

    # Render the template with the QR code image
    return render(request, 'emergencyapp/display_qr_code.html', {'qr_code_data': qr_code_data, 'qr_code_path': qr_code_path, 'qr_code_response': response})
