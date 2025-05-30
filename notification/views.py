from django.shortcuts import render




def notification(request):
    return render(request, 'notification/notification.html')
