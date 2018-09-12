from logging import getLogger

import ckan.plugins.toolkit as t

from ckanext.odi_certificates_client.lib.request import ckan_context
from ckanext.odi_certificates_client.logic.action.get import odi_certificate_location_head, odi_certificate_get, \
    odi_certificates_get_all

log = getLogger(__name__)


class OdiCertificatesClientController(t.BaseController):

    def odi_certificate_get_from_id(self, id):
        log.info("entered controller get from id...")
        log.info('self is %r', self)
        data_dict = t.get_action('package_show')(ckan_context(), {'id': id})
        location_json_url = self.odi_certificate_location_get_json(data_dict)
        data = self.odi_certificate_get_from_url(data_dict, location_json_url)
        ##TODO: inspect response headers for application/json and response status for 200
        return data

    def odi_certificate_location_get_from_id(self, id):
        log.info("entered controller get location from id...")
        data_dict = t.get_action('package_show')(ckan_context(), {'id': id})
        return self.odi_certificate_location_get_json(data_dict)

    def odi_certificate_location_get_json(self, data_dict):
        log.info("entered controller get location...")
        response = odi_certificate_location_head(ckan_context(), data_dict)
        if not response.headers or not response.headers.get('Location', ''):
            t.abort(404, t._("No odi certificate location was found."))
        location_json = response.headers['Location'] + '.json'
        log.debug('returning location json: %s', location_json)
        return location_json

    def odi_certificates_get_all(self):
        log.info("entered controller get all...")
        response = odi_certificates_get_all(ckan_context(), {})
        if not response.text:
            t.abort(404, "No odi certificates were found.")
        content_type = 'application/json;charset=utf-8'
        response.headers['Content-Type'] = content_type
        log.debug('returning response headers %r', response.headers)
        return response

    def odi_certificate_get_from_url(self, data_dict, location_url):
        log.info("entered controller get from url...")
        context = ckan_context()
        context['odi_certificates'] = {
            'location_url': location_url
        }
        response = odi_certificate_get(context, data_dict)

        if not response.text:
            t.abort(404, "No odi certificate was found.")
        ##TODO: inspect response headers for application/json and response status for 200
        return response
