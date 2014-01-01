from django.shortcuts import render
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import requests
from mailer.models import Email
import json

api_endpoint = "https://patients.apiary.io/"
MAIL_PER_PAGE = 10

def patients(request):
    """
    Renders the patient details page.
    Requests the Practo Ray API, gets details and passes
    data to the template to beautify it.
    """
    # Request the API
    req = requests.get(api_endpoint + "patients")
    all_patients = req.json()["items"]
    
    # Store detail of each patient.
    patient_names = [one_patient[u'name'] for one_patient in all_patients]
    patient_emails = [one_patient[u'email'] for one_patient in all_patients]
    patient_dobs = [one_patient[u'dob'] for one_patient in all_patients]
    patient_mobiles = [one_patient[u'mobile'] for one_patient in all_patients]
   
    # Defining dictionary to render template.
    context = {'total_patients': range(len(all_patients)),
               'patient_names': patient_names,
               'patient_emails': patient_emails,
               'patient_dobs': patient_dobs,
               'patient_mobiles': patient_mobiles
    }
    return render(request, 'patients.html', context)

def mail(request):
    """
    Renders the email sending page.
    
    On a GET request:
        
        Shows only name of patients who have an email ID.

    On a POST request:
        Gets data from the submitted form and sends email.
        If attachment is found, it is sent along, else not.
    """
    if request.method == 'GET':

        # Request the API.
        req = requests.get(api_endpoint + "patients")

        # Store detail of each patient if email is present.
        email_patients = [one_patient for one_patient in req.json()["items"] if \
                            one_patient['email']]
        patient_names = [one_patient[u'name'] for one_patient in email_patients]
        patient_emails = [one_patient[u'email'] for one_patient in email_patients]
        
        # Defining dictionary to render template.
        context = {'total_patients_having_email': range(len(email_patients)),
               'patient_names': patient_names,
               'patient_emails': patient_emails
        }
        return render(request, 'mail.html', context)

    if request.method == 'POST':

        # Get data from POST request.
        subject = request.POST['subject']
        message = request.POST['message']
        email = request.POST['email']
        patient_email = request.POST.getlist('patientcheck')
        
        # Object for sending email meassages.
        email_object = EmailMessage(
            subject,
            message, 
            email,
            patient_email,
        )


        if request.FILES:

            # If attachment is found, attach file to object.
            file_name = request.FILES['attachment'].name
            file_data = request.FILES['attachment'].read()
            email_object.attach(file_name,file_data)
            email_data = Email(mail_content=message,
                mail_users=json.dumps(patient_email),
                mail_subject=subject,
                mail_attachment=request.FILES['attachment'],
            )
        else:
            # Else, send the text only.
            email_data = Email(mail_content=message,
                mail_users=json.dumps(patient_email),
                mail_subject=subject,
            )
        # Send the email.
        email_object.send()
        # Save the email data.
        email_data.save()
        # Redirect to home page.
        return HttpResponseRedirect('/?q=Mail Sent.')

def sentmail(request):
    """
    Renders the page to show all sent mails.
    """
    # Get all email objects in order of creaion.
    mail_list = Email.objects.all().order_by("-mail_date")

    # Creating paginator object for Pagination.
    paginator = Paginator(mail_list, MAIL_PER_PAGE)
    page = request.GET.get('page')
    try:
        # Go to the page as requested.
        mails = paginator.page(page)
    except PageNotAnInteger:
        # Wrong page. Go to 1st page.
        mails = paginator.page(1)
    except EmptyPage:
        # Too large value, go to last page.
        mails = paginator.page(paginator.num_pages)

    return render(request, 'sentmail.html', {'emails': mails})

def homepage(request):
    """
    Used for rendering the home page.
    """
    context = {}
    if 'q' in request.GET:
        # If redirected from /email/, show mail sent.
        context = {'mail_sent': request.GET['q']}
    return render(request, 'home.html', context)
