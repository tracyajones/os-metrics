
import urllib2
import json

release = 'mitaka'
company = 'VMware'

def get_data(url):
    attempts = 0
    data = None
    while attempts < 3:
        try:
            response = urllib2.urlopen(url, timeout = 5)
            content = response.read()
            data = json.loads(content)
            break
        except urllib2.URLError as e:
            attempts += 1
            print type(e)
    return data

def load_project_data(release, company, project_type):

    contributors_query = 'http://stackalytics.com/api/1.0/stats/engineers?' \
                                'release={0}&metric=commits&project_type={1}&company={2}'.format(release,
                                                                                                 project_type,
                                                                                                 company.lower())
    contributors = get_data(contributors_query)

    openstack_contribution_query = 'http://stackalytics.com/api/1.0/stats/companies?' \
                                   'release={0}&metric=commits&project_type={1}'.format(release, project_type)
    openstack_contribution = get_data(openstack_contribution_query)
    openstack_project = [ c for c in openstack_contribution['stats'] if c['name'].lower() == company.lower()]

    project_contribution_query = 'http://www.stackalytics.com//api/1.0/stats/companies?release={0}' \
                                       '&metric=commits&project_type={1}&module={2}'

    print "{0}'s Rank in Openstack is {1} with a total of {2} commits".\
        format(company, openstack_project[0]['index'], openstack_project[0]['metric'])

    engineer_query = 'http://www.stackalytics.com/api/1.0/stats/modules?' \
                     'release={0}&metric=commits&project_type={1}&user_id={2}'

    projects = [
                {'id': 'nova', 'gt_10_stats': '', 'lt_10_stats': '',
                 'rank': '', 'need_rank': True, 'has_core': 'No'},
                {'id': 'neutron', 'gt_10_stats': '', 'lt_10_stats': '',
                 'rank': '', 'need_rank': True, 'has_core': 'Yes'},
                #{'id': 'vmware-nsx', 'gt_10_stats': '', 'lt_10_stats': '', # 'rank': '', need_rank: True, has_core: False},
                {'id': 'glance', 'gt_10_stats': '', 'lt_10_stats': '',
                 'rank': '', 'need_rank': True, 'has_core': 'Yes'},
                #{'id': 'glance-store', 'gt_10_stats': '', 'lt_10_stats': '', 'rank': '', need_rank: True, has_core: False},
                {'id': 'cinder', 'gt_10_stats': '', 'lt_10_stats': '',
                 'rank': '', 'need_rank': True, 'has_core': 'No'},
                {'id': 'keystone', 'gt_10_stats': '', 'lt_10_stats': '',
                 'rank': '', 'need_rank': True, 'has_core': 'No'},
                #{'id': 'ceilometer', 'gt_10_stats': '', 'lt_10_stats': '', 'rank': '', 'need_rank': True, has_core: False},
                {'id': 'heat', 'gt_10_stats': '', 'lt_10_stats': '',
                 'rank': '', 'need_rank': True, 'has_core': 'No'},
                #{'id': 'horizon', 'gt_10_stats': '', 'lt_10_stats': '', 'rank': '', 'need_rank': True, has_core: False},
                ]

    for dev in contributors['stats']:
        print dev['name'], dev['metric']
        engineer_data = get_data(engineer_query.format(release, project_type, dev['id']))
        print engineer_data['stats']
        for project_data in projects:
            if project_data['need_rank']:
                project_rank_data = get_data(project_contribution_query.format(release, project_type,
                                                                               project_data['id']))
                project_rank = [ c for c in project_rank_data['stats'] if
                                         c['name'] == u'VMware']
                if len(project_rank) == 0:
                    project_data['rank'] += 'None'
                else:
                    project_data['rank'] += str(project_rank[0]['index'])
                project_data['need_rank'] = False

            eng_data = [p for p in engineer_data['stats'] if p['id'] == project_data['id']]

            if len(eng_data) == 1:
                data = '{0}: {1}<br>'.format(dev['id'], eng_data[0]['metric'])
                if eng_data[0]['metric'] >= 10:
                    project_data['gt_10_stats'] += data
                else:
                    project_data['lt_10_stats'] += data

    for p in projects:
        print p

    return openstack_project[0], projects