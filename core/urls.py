# core/urls.py
from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = 'core'

urlpatterns = [
    # ============================================================
    # HTML PAGES (clean URLs — no .html)
    # ============================================================
    path('',             views.home_view,        name='home'),
    path('about/',       views.about_view,       name='about'),
    path('contact/',     views.contact_view,     name='contact'),
    path('laboratory/',  views.laboratory_view,  name='laboratory'),
    path('engineering/', views.engineering_redirect, name='engineering'),
    path('privacy/',     views.privacy_view,     name='privacy'),
    path('terms/',       views.terms_view,       name='terms'),
    path('cookies/',     views.cookies_view,     name='cookies'),
    path('industries/', views.industries_view, name='industries'),

    # ============================================================
    # LEGACY .html REDIRECTS (301 permanent — keeps old links alive)
    # ============================================================
    path('index.html',       RedirectView.as_view(url='/',             permanent=True)),
    path('home.html',        RedirectView.as_view(url='/',             permanent=True)),
    path('about.html',       RedirectView.as_view(url='/about/',       permanent=True)),
    path('contact.html',     RedirectView.as_view(url='/contact/',     permanent=True)),
    path('laboratory.html',  RedirectView.as_view(url='/laboratory/',  permanent=True)),
    path('engineering.html', RedirectView.as_view(url='/engineering/', permanent=True)),
    path('privacy.html',     RedirectView.as_view(url='/privacy/',     permanent=True)),
    path('terms.html',       RedirectView.as_view(url='/terms/',       permanent=True)),
    path('cookies.html',     RedirectView.as_view(url='/cookies/',     permanent=True)),

    # ============================================================
    # API
    # ============================================================
    path('api/contact/',      views.ContactMessageCreateView.as_view(), name='api-contact'),
    path('api/testimonials/', views.TestimonialListView.as_view(),      name='api-testimonials'),
    path('api/highlights/',   views.HighlightListView.as_view(),        name='api-highlights'),
    path('api/hero-slides/',  views.HeroSlideListView.as_view(),        name='api-hero-slides'),

    # ============================================================
    # PWA
    # ============================================================
    path('manifest.json',    views.pwa_manifest, name='pwa-manifest'),
    path('serviceworker.js', views.pwa_sw,       name='pwa-sw'),
]