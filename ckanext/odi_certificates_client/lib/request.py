from logging import getLogger
from urlparse import urljoin, urlsplit

import ckan.plugins.toolkit as t
from ckan import model
from ckan.common import config

log = getLogger(__name__)

_certs_config = dict({
    'server': config['ckanext.odi_certificates.server'],
    'username': config['ckanext.odi_certificates.username'],
    'token': config['ckanext.odi_certificates.token'],
    'jurisdiction': config['ckanext.odi_certificates.jurisdiction'],
    'locale': config.get('ckanext.odi_certificates.locale', 'en')
})

_ckan_site_url = config.get('ckan.site.alias_url', config['ckan.site_url'])


def get_auth():
    '''
    Returns Basic Authentication user and password for ODC API.
    '''
    return (_certs_config['username'], _certs_config['token'])


def get_request_path_for(path_function, params_function=None):
    """

    :param path_function:
    :param params_function:
    :return:
    """
    request_path = _certs_config['server'] + path_function()
    if params_function:
        request_path = t['h']._url_with_params(request_path, params_function())
    log.debug('Returning request path: %s', request_path)
    return request_path


def campaigns_feed_request_path():
    return location_request_path() + '.json'


def campaigns_feed_request_params():
    return {'datahub': _get_ckan_hostname(), 'jurisdiction': _certs_config['jurisdiction']}


def location_request_path():
    return '/' + _certs_config['locale'] + '/datasets'


def _get_ckan_hostname():
    split_url = urlsplit(_ckan_site_url)
    log.debug('split url is %r', split_url)
    return split_url[1]


def get_ckan_dataset_url(data_dict):
    '''
    Returns the full URL (HTML page) of the package.
    '''
    name = t.get_or_bust(data_dict, 'name')
    # start = 'http://host.docker.internal:5000'
    # log.debug('start is %s', start)
    # end = t.url_for(controller='package', action='read', id=name)
    # log.debug('end is %s', end)
    ckan_dataset_url = urljoin(_ckan_site_url, t.url_for(controller='package', action='read', id=name))
    log.debug('Returning ckan dataset url: %s', ckan_dataset_url)
    return ckan_dataset_url


def ckan_context():
    return {
        'model': model,
        'session': model.Session,
        'user': t.c.user,
        'auth_user_obj': t.c.userobj,
    }
