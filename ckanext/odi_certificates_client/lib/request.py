from logging import getLogger
from urlparse import urljoin, urlparse

import ckan.plugins.toolkit as t
from ckan import model
from ckan.lib.dictization.model_dictize import package_dictize

log = getLogger(__name__)


def get_package_dict_from_id(id):
    pkg = model.Package.get(id)
    if not pkg:
        t.abort(404, "Unable to find package by id.")
    data_dict = package_dictize(pkg)
    return data_dict


def get_auth(context):
    '''
    Returns Basic Authentication user and password for ODC API.
    '''
    certs_config = _certs_config(context)
    return (certs_config['username'], certs_config['token'])


def get_request_path_for(context, path_function, params_function=None):
    """

    :param context:
    :param path_function:
    :param params_function:
    :return:
    """
    certs_config = _certs_config(context)
    request_path = certs_config['server'] + path_function(context)
    if params_function:
        request_path = t['h']._url_with_params(request_path, params_function(context))
    return request_path


def campaigns_feed_request_path(context):
    certs_config = _certs_config(context)
    return location_request_path(certs_config) + '.json'


def campaigns_feed_request_params(context):
    certs_config = _certs_config(context)
    raw_params = ({'datahub': _get_ckan_hostname(context), 'jurisdiction': certs_config('jurisdiction')})
    return raw_params


def location_request_path(certs_config):
    ##TODO: this should be locale, not jurisdiction
    return '/' + str(certs_config['data']['jurisdiction']) + '/datasets'


def _get_ckan_hostname(context):
    site_url = _site_url(context)
    split_url = urlparse.urlsplit(site_url)
    return t.get_or_bust(split_url, 'hostname')


def _certs_config(context):
    return t.get_or_bust(context, 'odi_certificates_config')


def _site_url(context):
    return context('ckan.site_url')


def get_ckan_dataset_url(context, data_dict):
    '''
    Returns the full URL (HTML page) of the package.
    '''
    name = t.get_or_bust(data_dict, 'name')
    return urljoin(_site_url(context), t.url_for(controller='package', action='read', id=name))
