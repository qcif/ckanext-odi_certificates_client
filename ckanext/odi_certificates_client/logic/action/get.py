from logging import getLogger

import ckan.plugins.toolkit as t
import requests

from ckanext.odi_certificates_client.lib.request import get_ckan_dataset_url, get_auth, \
    get_request_path_for, location_request_path, campaigns_feed_request_path, campaigns_feed_request_params

log = getLogger(__name__)


@t.side_effect_free
def odi_certificate_location_head(context=None, data_dict=None):
    """

    :param context:
    :param data_dict:
    :return:
    """
    log.info("entered api get location head...")
    t.check_access('odi_certificates_client_get', context, data_dict)

    request_path = get_request_path_for(context, location_request_path)
    dataset_url = get_ckan_dataset_url(context, data_dict)

    response = requests.head(
        request_path,
        params=dict({'datasetUrl': dataset_url}),
        auth=get_auth(context)
    )
    log.debug('response headers from get is: %s' % response.headers)
    return response


@t.side_effect_free
def odi_certificate_get(context=None, data_dict=None, request_path=None):
    """

    :param context:
    :param data_dict:
    :param request_path:
    :return:
    """
    log.info("entered api get...")
    t.check_access('odi_certificates_client_get', context, data_dict)

    certs_config = context['odi_certificates_config']
    response = requests.get(
        request_path,
        auth=get_auth(certs_config)
    )
    log.debug('response from get is: %s' % response.text)
    return response

@t.side_effect_free
def odi_certificate_get_from_id(context=None, data_dict=None, request_path=None):
    """

    :param context:
    :param data_dict:
    :param request_path:
    :return:
    """
    log.info("entered api get...")
    t.check_access('odi_certificates_client_get', context, data_dict)

    certs_config = context['odi_certificates_config']
    response = requests.get(
        request_path,
        auth=get_auth(certs_config)
    )
    log.debug('response from get is: %s' % response.text)
    return response

@t.side_effect_free
def odi_certificates_get_all(context=None):
    """

    :param context:
    :param data_dict:
    :param request_path:
    :return:
    """
    log.info("entered controller get all...")
    t.check_access('odi_certificates_client_get_all', context)

    request_path = get_request_path_for(context, campaigns_feed_request_path)
    response = requests.get(
        request_path,
        params=dict(campaigns_feed_request_params),
        auth=get_auth(context)
    )
    log.debug('response from get is: %s' % response.text)

    return response