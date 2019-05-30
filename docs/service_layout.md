# Service layout

Service project layout template:

    config
        settings            # django settings for different situations like local testing or production deployment
        constants.py        # different service-needed hard coded constants, gathered all in this file
        urls.py             # service-wide URL patterns config
        wsgi.py             # django WSGI config
    
    app
        json                # folder with different .json files like testing data or model-needed data
        models              # ML or another model objects saved in '*.model' name pattern
        tests               # unit test files in format 'test_<module_name>.py'
        admin.py            # registered django admin models
        apps.py             # this django app config
        authentication.py   # REST framework authentication classes
        models.py           # django models
        serializers.py      # REST framework serializers
        urls.py             # url patterns config of this app
        views.py            # django views
        ...
    
    ... another apps ...
    
    manage.py               # django project managing file
    utils.py                # service onload needed functions like secrets loading
    ...