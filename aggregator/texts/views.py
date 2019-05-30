from django.views import generic
from django.urls import reverse
from config import constants
from .arclient import ARClient
from .models import Text
from .helpers import form_services_data, get_status_repr


class TextsView(generic.ListView):
    """ Retrieve all Texts """

    model = Text
    context_object_name = 'texts'
    ordering = '-created'
    template_name = 'texts.html'
    paginate_by = constants.texts_count


class TextView(generic.DetailView):
    """ Text object detail view """

    model = Text
    context_object_name = 'text'
    template_name = 'text.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # perform get requests and truth checking via post requests if necessary

        if self.kwargs['new']:
            # new object, send post requests

            ar_client = ARClient()
            post_data = self.object.get_post_request_data()
            post_data = {service: post_data for service in constants.services}
            responses = ar_client.run_loop(post_data, gather_results=False)
            context['services_data'] = form_services_data(responses, necessary_code=201)

        else:
            # existed object, send get and if this objects does not exist - send post requests

            ar_client = ARClient()
            responses = ar_client.run_loop(self.object.message_id)
            context['services_data'] = form_services_data(responses, necessary_code=200)

            services_post = {key: constants.services[key] for key in responses if responses[key][1] == 404}

            if len(services_post):
                ar_client = ARClient(services=services_post)
                post_data = self.object.get_post_request_data()
                post_data = {service: post_data for service in services_post}
                responses_post = ar_client.run_loop(post_data, gather_results=False)
                context['services_data'].update(form_services_data(responses_post, necessary_code=201))

        context['status'] = get_status_repr(list(context['services_data'].values()))
        return context


class StartCheck(generic.CreateView):
    """ Create Text and initiate truth checking """

    model = Text
    fields = 'headline', 'raw_text'
    template_name = 'form.html'

    def get_success_url(self):
        return reverse('detail_view', args=(self.object.id,))
