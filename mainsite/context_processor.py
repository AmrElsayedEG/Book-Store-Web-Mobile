from .models import website_layout as w
def website_layout(request):
    try:
        wl = w.objects.all().last()
    except:
        wl = {'logo_dark':None,'logo_light':None,'facebook':None,'twitter':None,
              'instagram':None}
    return {'website_layout':wl}
