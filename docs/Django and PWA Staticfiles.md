# Django and PWA Staticfiles

How to serve PWA's `sw.js` and `worker-[hash].js` files?

## Problem

With the way I setup Django, I cannot serve any staticfiles on `base_url`. That means I can't serve `/worker-[hash].js` without having to manually add TemplateView(s).

## Solution?

From [5517950](https://stackoverflow.com/questions/5517950/django-media-url-and-media-root)

```py
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # ... the rest of your URLconf goes here ...
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
