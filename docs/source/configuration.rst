Configuration
=============

This section deals with the internal configuration of the APIS tool. For instructions on how to set it up please refer
to :doc:`installation`.
Most of the configuration goes into a Django settings file. We suggest that you create your own configuration file and 
- in case you use the Docker image - import everything from the base settingsfile found in ``/apis/apis-devops/apis/settings/base.py``: ``from .base import *``


REST_FRAMEWORK
--------------

APIS uses the `Django Restframework`_ for API provisioning. Restframework specific settings like the default page size can be set here.

.. code-block:: python

    REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = (
        "rest_framework.permissions.DjangoObjectPermissions",
    )

Use the above default to allow setting permissions on object level. Meaning that every user gets his permissions depending on his/her user group and the collections this group has permissions for.
Set ``"rest_framework.permissions.DjangoModelPermissions"`` for allowing every user with permissions on a model to change all model instances.
Set ``"rest_framework.permissions.IsAuthenticated"`` if every logged in user should have all permissions.

.. code-block:: python

    REST_FRAMEWORK["PAGE_SIZE"] = 50

Sets the default page size the APIS RestAPI should deliver.


APIS_BASE_URI
-------------

.. code-block:: python

    APIS_BASE_URI = "https://your-url-goes-here.com"

Sets the base URI your instance should use. This is important as APIS uses mainly URIs instead of IDs. These URIs are also used for the serialization.


APIS_MIN_CHAR
-------------

.. code-block:: python

    APIS_MIN_CHAR = 0

Sets the minimal characters needed to trigger the autocompletes.


APIS_COMPONENTS
---------------

.. code-block:: python

    APIS_COMPONENTS = []

This activates certain experimental components. This is not of interest for production use yet.


APIS_TEI
--------

.. code-block:: python

    APIS_TEI_TEXTS = ["xml/tei transcription"]
    APIS_CETEICEAN_CSS = "https://teic.github.io/CETEIcean/css/CETEIcean.css"
    APIS_CETEICEAN_JS = "https://teic.github.io/CETEIcean/js/CETEI.js"

APIS includes a experimental feature to save and render TEI files. These settings are used to define the css and js files used to render TEIs.


APIS_NEXT_PREV
--------------

.. code-block:: python
    
    APIS_NEXT_PREV = True


APIS_ALTERNATE_NAMES
--------------------

.. code-block:: python

    APIS_ALTERNATE_NAMES = [
        "Taufname",
        "Ehename",
        "Name laut ÖBL XML",
        "alternative Namensform",
        "alternative name",
        "Künstlername",
        "Mädchenname",
        "Pseudonym",
        "weitere Namensform",
    ]

This setting contains a list of :class:`apis_vocabularies.models.LabelType` entries that should be deemed as alternative name. This is used to determine the label types that should be search in addition to the main name.


APIS_RELATIONS_FILTER_EXCLUDE
-----------------------------

.. code-block:: python
    
    APIS_RELATIONS_FILTER_EXCLUDE = [
        "*uri*",
        "*tempentityclass*",
        "user",
        "*__id",
        "*source*",
        "label",
        "*temp_entity*",
        "*collection*",
        "*published*",
        "*_set",
        "*_set__*",
        "_ptr",
        "baseclass",
        "*id",
        "*written*",
        "relation_type__*",
        "*__text*",
        "text*",
        "*annotation_set_relation*",
        "*start_start_date*",
        "*end_end_date*",
        "*start_end_date*",
        "*end_start_date*",
        "*label*",
        "*review*",
        "*__name",
        "*__status",
        "*__references",
        "*__notes",
    ]


APIS automatically adapts to changes in the datamodel. To automatically create the 
filters used in the GUI and the API we do some code inspection on the models in use. 
This setting is used to define the attributes that shouldn't be used for filtering. You shouldn't 
replace this list in your settings file but append to it: ``APIS_RELATIONS_FILTER_EXCLUDE.extend(['item A', 'item B'])``
The setting uses wildcards (*) and therefore allows to use subsets of attributes.


APIS_RELATIONS
--------------

.. code-block:: python

    APIS_RELATIONS = {
        "list_filters": [("relation_type",)],
        "search": ["relation_type__name"],
        "exclude": ["name"],
        "PersonPlace": {
            "labels": ["related_person", "related_place", "relation_type"],
            "search": [
                "relation_type__name",
                "related_person__name",
                "related_person__first_name",
                "related_place__name",
            ],
            "list_filters": [("relation_type",), ("related_person",), ("related_place",)],
        },} #This is only a subset of the settings in the base file


APIS_ENTITIES
-------------

.. code-block:: python


    APIS_ENTITIES = {
        "Place": {
            "merge": True,
            "search": ["name"],
            "form_order": ["name", "kind", "lat", "lng", "status", "collection"],
            "table_fields": ["name"],
            "additional_cols": ["id", "lat", "lng", "part_of"],
            "list_filters": {
                "name": {"method": "name_label_filter"},
                "collection": {"label": "Collection"},
                "kind": {"label": "Kind of Place"},
                "age": {}, # don't change the filter, but put it after `kind` in the final output
                "custom_filter": {
                    "filter": "CharFilter",
                    "lookup_expr": "contains",
                    "field_name": "name"
                },
            },
            "list_filters_exclude": ["lat", "lng", "status"],
            "detail_view_exclude": ["notes", "references"],
        },}

``APIS_ENTITIES`` is the setting to define the behavior of the entities list views. Every entity has its own setting.
The example above is the default setting of the Place entity. 
``merge`` is boolean and sets whether the list views will include the possibility to add a merge column. This column
allows to merge several entities in one target entity at once.
``search`` is an array and sets the fields that the search field searches.
``form_order`` defines the order of the fields in the metadata form of the respective entity.
``form`` allows you to set a custom form for the entity, instead of the default `apis_entities.forms.GenericEntityForm`
``table_fields`` sets the default columns to show in the list views.
``additional_cols`` allows to set the columns that user can add to the result view.
``relations_per_page`` allows to set the number of relations listed before pagination begins
``detail_view_exclude`` allows to set fields that are excluded from the default detail view

``list_filters``
^^^^^^^^^^^^^^^^

``list_filters`` is a dictionary of configured filters for the list view. The default filters are generated based on the fields of an entity.
But you can override a generated filter or add additional filters. Overriding a filter is done by adding an entry to the dict
with the key being the name of a generated filter (usually that's identical to the name of the field it refers to).
If the entry does **not** refer to the name of a generated filter, you are creating a new filter and you have
to define the filter type using the ``filter`` keyword being one of `the ones defined in the django-filters documentation <https://django-filter.readthedocs.io/en/stable/ref/filters.html#filters>`_.

The attributes of the ``list_filter`` dict items can be `attributes listed in the django-filters documentation <https://django-filter.readthedocs.io/en/stable/ref/filters.html>`_.
The :py:mod:`apis_core.utils.filtermethods` module contains some functions that can be used as ``method`` for the filters.

The view shows all the filters, first the ones changed or created in the ``list_filters`` dict, then the rest of the automatically generated ones.
Using the ``list_filters_exclude`` setting it is possible to list the names of the fields that should **not** be part of the list views filter form.
This does *not* override filters that are defined in the ``list_filters`` settings. If they should not be displayed, they should be removed from ``list_filters``.
Using the keyword ``__defaults__`` excludes all the filters that are not explicitly defined in the ``list_filters`` setting.


APIS_API_EXCLUDE_SETS
---------------------

.. code-block:: python

    APIS_API_EXCLUDE_SETS = True


Boolean setting for excluding related objects from the API. Normally its not needed to touch this.



APIS_API_ID_WRITABLE
---------------------

.. code-block:: python

    APIS_API_ID_WRITABLE = False


Boolean setting for defining if the `id` field of an entity is writable via the
API. Defaults to false. You can set it to `True` if you want to import entities
from another instance and want to keep the `id`.


APIS_LIST_VIEWS_ALLOWED
-----------------------

.. code-block:: python

    APIS_LIST_VIEWS_ALLOWED = False


Sets whether list views are accessible for anonymous (not logged in) users.


APIS_DETAIL_VIEWS_ALLOWED
-------------------------

.. code-block:: python
    
    APIS_DETAIL_VIEWS_ALLOWED - False


Sets whether detail views are accessible for anonymous (note logged in) users.

APIS_VIEW_PASSES_TEST
---------------------

Allows to define a function that receives the view as an argument - including
e.g. the `request` object - and can perform checks on any of the views
attributes. The function can, based on these checks, return a boolean which
decides if the request is successful or leads to a 403 permission denied.

APIS_LIST_VIEW_OBJECT_FILTER
----------------------------

Allows to define a function that receives the view - including e.g. the
`request` object - and a queryset and can do custom filtering on that queryset.
This can be used to set the listviews to public using the
`APIS_LIST_VIEWS_ALLOWED` setting, but still only list specific entities.


APIS_LIST_VIEW_TEMPLATE
-----------------------

.. code-block:: python
    
    APIS_LIST_VIEW_TEMPLATE = "generic_list.html"


Sets the path of the list view template. This is only needed if you want to customize the appearance of the list views.


APIS_DELETE_VIEW_TEMPLATE
-------------------------

.. code-block:: python
    
    APIS_DELETE_VIEW_TEMPLATE = "webpage/confirm_delete.html"


Sets the path of the delete view template. This is only needed if you want to customize the appearance of the template for 
confirming the deletion of an object.


.. _Django Restframework: https://www.django-rest-framework.org/
