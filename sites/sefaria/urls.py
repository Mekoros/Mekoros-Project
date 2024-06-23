# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.http import HttpResponseRedirect
import reader.views as reader_views
from mekoros.settings import STATIC_URL


static_pages = [
    "terms",
    "privacy-policy",
    "adin-even-israel-steinsaltz",
    "william-davidson-talmud",
    "ios",
    "mobile",
    "app",
    "sheets",
    "powered-by",
    "cloudflare_site_is_down_en",
    "cloudflare_site_is_down_he",
    "ways-to-give"
]

static_pages_by_lang = [
]


# Static and Semi Static Content
site_urlpatterns = [
    url(r'^enable_new_editor/?$', reader_views.enable_new_editor),
    url(r'^disable_new_editor/?$', reader_views.disable_new_editor),
    url(r'^metrics/?$', reader_views.metrics),
    url(r'^digitized-by-mekoros/?$', reader_views.digitized_by_mekoros),
    url(r'^apple-app-site-association/?$', reader_views.apple_app_site_association),
    url(r'^\.well-known/apple-app-site-association/?$', reader_views.apple_app_site_association),
    url(r'^\.well-known/assetlinks.json/?$', reader_views.android_asset_links_json),
    url(r'^(%s)/?$' % "|".join(static_pages), reader_views.serve_static),
    url(r'^(%s)/?$' % "|".join(static_pages_by_lang), reader_views.serve_static_by_lang),
    url(r'^healthz/?$', reader_views.application_health_api),  # this oddly is returning 'alive' when it's not.  is k8s jumping in the way?
    url(r'^health-check/?$', reader_views.application_health_api),
    url(r'^healthz-rollout/?$', reader_views.rollout_health_api),
]