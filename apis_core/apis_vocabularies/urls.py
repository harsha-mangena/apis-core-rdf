from django.urls import path, re_path

from apis_core.apis_entities.autocomplete3 import GenericVocabulariesAutocomplete
from apis_core.apis_vocabularies import views

app_name = "apis_vocabularies"

urlpatterns = [
    path("download/<model_name>/", views.dl_vocabs_as_csv, name="dl-vocabs"),
    # url(r'^autocomplete/(?P<vocab>[a-zA-Z0-9-]+)/(?P<direct>[a-zA-Z0-9-]+)/$',
    re_path(
        r"^autocomplete/(?P<xyz>[a-zA-Z0-9-]+)/$",
        # url(r'^autocomplete/$',
        GenericVocabulariesAutocomplete.as_view(),
        name="generic_vocabularies_autocomplete",
    ),
]
