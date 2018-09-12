from logging import getLogger

import ckan.plugins.toolkit as t

from ckanext.odi_certificates_client.logic.action.get import odi_certificate_location_head, odi_certificate_get, odi_certificates_get_all
from ckanext.odi_certificates_client.lib.request import get_package_dict_from_id

log = getLogger(__name__)


class OdiCertificatesClientController(t.BaseController):

    def odi_certificate_get_from_id(self, id):
        log.info("entered controller get from id...")
        data_dict = get_package_dict_from_id(id)
        location_url = self.odi_certificate_location_get(data_dict)
        data = self.odi_certificate_get_from_url(data_dict, location_url)
        ##TODO: inspect response headers for application/json and response status for 200
        return data

    def odi_certificate_location_get_from_id(self, id):
        log.info("entered controller get location from id...")
        data_dict = get_package_dict_from_id(id)
        return self.odi_certificate_location_get(data_dict)

    def odi_certificate_location_get(self, data_dict):
        log.info("entered controller get location...")
        response = odi_certificate_location_head(t.c, data_dict)
        if not response.headers or not response.headers.location:
            t.abort(404, "No odi certificate location was found.")
        ##TODO: inspect response headers for application/json and response status for 200
        location_url = response.headers.location
        return location_url

    def odi_certificates_get_all(self):
        log.info("entered controller get all...")
        response = odi_certificates_get_all(t.c)
        if not response.text:
            t.abort(404, "No odi certificates were found.")
        return response

    def _odi_certificate_get_from_url(self, data_dict, location_url):
        log.info("entered controller get from url...")
        response = odi_certificate_get(t.c, data_dict, location_url)

        if not response.text:
            t.abort(404, "No odi certificate was found.")
        ##TODO: inspect response headers for application/json and response status for 200
        return response
