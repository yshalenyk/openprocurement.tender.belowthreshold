# -*- coding: utf-8 -*-
import unittest

from openprocurement.tender.belowthreshold.tests.base import (
    TenderContentWebTest, test_features_tender_data, test_organization
)


class TenderBidResourceTest(TenderContentWebTest):
    initial_status = 'active.tendering'

    def test_create_tender_bid_invalid(self):
        response = self.app.post_json('/tenders/some_id/bids', {
                                      'data': {'tenderers': [test_organization], "value": {"amount": 500}}}, status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

        request_path = '/tenders/{}/bids'.format(self.tender_id)
        response = self.app.post(request_path, 'data', status=415)
        self.assertEqual(response.status, '415 Unsupported Media Type')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description':
                u"Content-Type header should be one of ['application/json']", u'location': u'header', u'name': u'Content-Type'}
        ])

        response = self.app.post(
            request_path, 'data', content_type='application/json', status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'No JSON object could be decoded',
                u'location': u'body', u'name': u'data'}
        ])

        response = self.app.post_json(request_path, 'data', status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Data not available',
                u'location': u'body', u'name': u'data'}
        ])

        response = self.app.post_json(
            request_path, {'not_data': {}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Data not available',
                u'location': u'body', u'name': u'data'}
        ])

        response = self.app.post_json(request_path, {'data': {
                                      'invalid_field': 'invalid_value'}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Rogue field', u'location':
                u'body', u'name': u'invalid_field'}
        ])

        response = self.app.post_json(request_path, {
                                      'data': {'tenderers': [{'identifier': 'invalid_value'}]}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': {u'identifier': [
                u'Please use a mapping for this field or Identifier instance instead of unicode.']}, u'location': u'body', u'name': u'tenderers'}
        ])

        response = self.app.post_json(request_path, {
                                      'data': {'tenderers': [{'identifier': {}}]}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [{u'contactPoint': [u'This field is required.'], u'identifier': {u'scheme': [u'This field is required.'], u'id': [u'This field is required.']}, u'name': [u'This field is required.'], u'address': [u'This field is required.']}], u'location': u'body', u'name': u'tenderers'}
        ])

        response = self.app.post_json(request_path, {'data': {'tenderers': [{
            'name': 'name', 'identifier': {'uri': 'invalid_value'}}]}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [{u'contactPoint': [u'This field is required.'], u'identifier': {u'scheme': [u'This field is required.'], u'id': [u'This field is required.'], u'uri': [u'Not a well formed URL.']}, u'address': [u'This field is required.']}], u'location': u'body', u'name': u'tenderers'}
        ])

        response = self.app.post_json(request_path, {'data': {'tenderers': [test_organization]}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [u'This field is required.'], u'location': u'body', u'name': u'value'}
        ])

        response = self.app.post_json(request_path, {'data': {'tenderers': [test_organization], "value": {"amount": 500, 'valueAddedTaxIncluded': False}}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [u'valueAddedTaxIncluded of bid should be identical to valueAddedTaxIncluded of value of tender'], u'location': u'body', u'name': u'value'}
        ])

        response = self.app.post_json(request_path, {'data': {'tenderers': [test_organization], "value": {"amount": 500, 'currency': "USD"}}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [u'currency of bid should be identical to currency of value of tender'], u'location': u'body', u'name': u'value'},
        ])

        response = self.app.post_json(request_path, {'data': {'tenderers': test_organization, "value": {"amount": 500}}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u"invalid literal for int() with base 10: 'contactPoint'", u'location': u'body', u'name': u'data'},
        ])

    def test_create_tender_bid(self):
        dateModified = self.db.get(self.tender_id).get('dateModified')

        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bid = response.json['data']
        self.assertEqual(bid['tenderers'][0]['name'], test_organization['name'])
        self.assertIn('id', bid)
        self.assertIn(bid['id'], response.headers['Location'])

        self.assertEqual(self.db.get(self.tender_id).get('dateModified'), dateModified)

        self.set_status('complete')

        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't add bid in current (complete) tender status")

    def test_patch_tender_bid(self):
        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': {'tenderers': [test_organization], "status": "draft", "value": {"amount": 500}}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bid = response.json['data']
        token = response.json['access']['token']

        response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], token), {"data": {"value": {"amount": 600}}}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [u'value of bid should be less than value of tender'], u'location': u'body', u'name': u'value'}
        ])

        response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], token), {"data": {'tenderers': [{"name": u"Державне управління управлінням справами"}]}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['date'], bid['date'])
        self.assertNotEqual(response.json['data']['tenderers'][0]['name'], bid['tenderers'][0]['name'])

        response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], token), {"data": {"value": {"amount": 500}, 'tenderers': [test_organization]}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']['date'], bid['date'])
        self.assertEqual(response.json['data']['tenderers'][0]['name'], bid['tenderers'][0]['name'])

        response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], token), {"data": {"value": {"amount": 400}}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["value"]["amount"], 400)
        self.assertNotEqual(response.json['data']['date'], bid['date'])

        response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], token), {"data": {"status": "active"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["status"], "active")
        self.assertNotEqual(response.json['data']['date'], bid['date'])

        response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], token), {"data": {"status": "draft"}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can\'t update bid to (draft) status")

        response = self.app.patch_json('/tenders/{}/bids/some_id'.format(self.tender_id), {"data": {"value": {"amount": 400}}}, status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'bid_id'}
        ])

        response = self.app.patch_json('/tenders/some_id/bids/some_id', {"data": {"value": {"amount": 400}}}, status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

        self.set_status('complete')

        response = self.app.get('/tenders/{}/bids/{}'.format(self.tender_id, bid['id']))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data']["value"]["amount"], 400)

        response = self.app.patch_json('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], token), {"data": {"value": {"amount": 400}}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't update bid in current (complete) tender status")

    def test_get_tender_bid(self):
        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bid = response.json['data']
        bid_token = response.json['access']['token']

        response = self.app.get('/tenders/{}/bids/{}'.format(self.tender_id, bid['id']), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't view bid in current (active.tendering) tender status")

        response = self.app.get('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data'], bid)

        self.set_status('active.qualification')

        response = self.app.get('/tenders/{}/bids/{}'.format(self.tender_id, bid['id']))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        bid_data = response.json['data']
        #self.assertIn(u'participationUrl', bid_data)
        #bid_data.pop(u'participationUrl')
        self.assertEqual(bid_data, bid)

        response = self.app.get('/tenders/{}/bids/some_id'.format(self.tender_id), status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'bid_id'}
        ])

        response = self.app.get('/tenders/some_id/bids/some_id', status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

        response = self.app.delete('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't delete bid in current (active.qualification) tender status")

    def test_delete_tender_bid(self):
        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bid = response.json['data']
        bid_token = response.json['access']['token']

        response = self.app.delete('/tenders/{}/bids/{}?acc_token={}'.format(self.tender_id, bid['id'], bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data'], bid)

        revisions = self.db.get(self.tender_id).get('revisions')
        self.assertTrue(any([i for i in revisions[-2][u'changes'] if i['op'] == u'remove' and i['path'] == u'/bids']))
        self.assertTrue(any([i for i in revisions[-1][u'changes'] if i['op'] == u'add' and i['path'] == u'/bids']))

        response = self.app.delete('/tenders/{}/bids/some_id'.format(self.tender_id), status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'bid_id'}
        ])

        response = self.app.delete('/tenders/some_id/bids/some_id', status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

    def test_get_tender_tenderers(self):
        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bid = response.json['data']

        response = self.app.get('/tenders/{}/bids'.format(self.tender_id), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't view bids in current (active.tendering) tender status")

        self.set_status('active.qualification')

        response = self.app.get('/tenders/{}/bids'.format(self.tender_id))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['data'][0], bid)

        response = self.app.get('/tenders/some_id/bids', status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

    def test_bid_Administrator_change(self):
        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bid = response.json['data']

        self.app.authorization = ('Basic', ('administrator', ''))
        response = self.app.patch_json('/tenders/{}/bids/{}'.format(self.tender_id, bid['id']), {"data": {
            'tenderers': [{"identifier": {"id": "00000000"}}],
            "value": {"amount": 400}
        }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertNotEqual(response.json['data']["value"]["amount"], 400)
        self.assertEqual(response.json['data']["tenderers"][0]["identifier"]["id"], "00000000")


class TenderBidFeaturesResourceTest(TenderContentWebTest):
    initial_data = test_features_tender_data
    initial_status = 'active.tendering'

    def test_features_bid(self):
        test_features_bids = [
            {
                "parameters": [
                    {
                        "code": i["code"],
                        "value": 0.1,
                    }
                    for i in self.initial_data['features']
                ],
                "status": "active",
                "tenderers": [
                    test_organization
                ],
                "value": {
                    "amount": 469,
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            },
            {
                "parameters": [
                    {
                        "code": i["code"],
                        "value": 0.15,
                    }
                    for i in self.initial_data['features']
                ],
                "tenderers": [
                    test_organization
                ],
                "status": "draft",
                "value": {
                    "amount": 479,
                    "currency": "UAH",
                    "valueAddedTaxIncluded": True
                }
            }
        ]
        for i in test_features_bids:
            response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': i})
            self.assertEqual(response.status, '201 Created')
            self.assertEqual(response.content_type, 'application/json')
            bid = response.json['data']
            bid.pop(u'date')
            bid.pop(u'id')
            self.assertEqual(bid, i)

    def test_features_bid_invalid(self):
        data = {
            "tenderers": [
                test_organization
            ],
            "value": {
                "amount": 469,
                "currency": "UAH",
                "valueAddedTaxIncluded": True
            }
        }
        response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': data}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [u'This field is required.'], u'location': u'body', u'name': u'parameters'}
        ])
        data["parameters"] = [
            {
                "code": "OCDS-123454-AIR-INTAKE",
                "value": 0.1,
            }
        ]
        response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': data}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [u'All features parameters is required.'], u'location': u'body', u'name': u'parameters'}
        ])
        data["parameters"].append({
            "code": "OCDS-123454-AIR-INTAKE",
            "value": 0.1,
        })
        response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': data}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [u'Parameter code should be uniq for all parameters'], u'location': u'body', u'name': u'parameters'}
        ])
        data["parameters"][1]["code"] = "OCDS-123454-YEARS"
        data["parameters"][1]["value"] = 0.2
        response = self.app.post_json('/tenders/{}/bids'.format(self.tender_id), {'data': data}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [{u'value': [u'value should be one of feature value.']}], u'location': u'body', u'name': u'parameters'}
        ])


class TenderBidDocumentResourceTest(TenderContentWebTest):
    initial_status = 'active.tendering'

    def setUp(self):
        super(TenderBidDocumentResourceTest, self).setUp()
        # Create bid
        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
        bid = response.json['data']
        self.bid_id = bid['id']
        self.bid_token = response.json['access']['token']

    def test_not_found(self):
        response = self.app.post('/tenders/some_id/bids/some_id/documents', status=404, upload_files=[
                                 ('file', 'name.doc', 'content')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

        response = self.app.post('/tenders/{}/bids/some_id/documents'.format(self.tender_id), status=404, upload_files=[('file', 'name.doc', 'content')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'bid_id'}
        ])

        response = self.app.post('/tenders/{}/bids/{}/documents?acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token), status=404, upload_files=[
                                 ('invalid_value', 'name.doc', 'content')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'body', u'name': u'file'}
        ])

        response = self.app.get('/tenders/some_id/bids/some_id/documents', status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

        response = self.app.get('/tenders/{}/bids/some_id/documents'.format(self.tender_id), status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'bid_id'}
        ])

        response = self.app.get('/tenders/some_id/bids/some_id/documents/some_id', status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

        response = self.app.get('/tenders/{}/bids/some_id/documents/some_id'.format(self.tender_id), status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'bid_id'}
        ])

        response = self.app.get('/tenders/{}/bids/{}/documents/some_id'.format(self.tender_id, self.bid_id), status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'document_id'}
        ])

        response = self.app.put('/tenders/some_id/bids/some_id/documents/some_id', status=404,
                                upload_files=[('file', 'name.doc', 'content2')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'tender_id'}
        ])

        response = self.app.put('/tenders/{}/bids/some_id/documents/some_id'.format(self.tender_id), status=404, upload_files=[
                                ('file', 'name.doc', 'content2')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'url', u'name': u'bid_id'}
        ])

        response = self.app.put('/tenders/{}/bids/{}/documents/some_id'.format(
            self.tender_id, self.bid_id), status=404, upload_files=[('file', 'name.doc', 'content2')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location': u'url', u'name': u'document_id'}
        ])

        self.app.authorization = ('Basic', ('invalid', ''))
        response = self.app.put('/tenders/{}/bids/{}/documents/some_id'.format(
            self.tender_id, self.bid_id), status=404, upload_files=[('file', 'name.doc', 'content2')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location': u'url', u'name': u'document_id'}
        ])

    def test_create_tender_bid_document(self):
        response = self.app.post('/tenders/{}/bids/{}/documents?acc_token={}'.format(
            self.tender_id, self.bid_id, self.bid_token), upload_files=[('file', 'name.doc', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('name.doc', response.json["data"]["title"])
        key = response.json["data"]["url"].split('?')[-1].split('=')[-1]

        response = self.app.get('/tenders/{}/bids/{}/documents'.format(self.tender_id, self.bid_id), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't view bid documents in current (active.tendering) tender status")

        response = self.app.get('/tenders/{}/bids/{}/documents?acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"][0]["id"])
        self.assertEqual('name.doc', response.json["data"][0]["title"])

        response = self.app.get('/tenders/{}/bids/{}/documents?all=true&acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"][0]["id"])
        self.assertEqual('name.doc', response.json["data"][0]["title"])

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?download=some_id&acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, self.bid_token), status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location': u'url', u'name': u'download'}
        ])

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?download={}'.format(
            self.tender_id, self.bid_id, doc_id, key), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't view bid document in current (active.tendering) tender status")

        if self.docservice:
            response = self.app.get('/tenders/{}/bids/{}/documents/{}?download={}&acc_token={}'.format(
                self.tender_id, self.bid_id, doc_id, key, self.bid_token))
            self.assertEqual(response.status, '302 Moved Temporarily')
            self.assertIn('http://localhost/get/', response.location)
            self.assertIn('Signature=', response.location)
            self.assertIn('KeyID=', response.location)
            self.assertIn('Expires=', response.location)
        else:
            response = self.app.get('/tenders/{}/bids/{}/documents/{}?download={}&acc_token={}'.format(
                self.tender_id, self.bid_id, doc_id, key, self.bid_token))
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/msword')
            self.assertEqual(response.content_length, 7)
            self.assertEqual(response.body, 'content')

        response = self.app.get('/tenders/{}/bids/{}/documents/{}'.format(
            self.tender_id, self.bid_id, doc_id), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't view bid document in current (active.tendering) tender status")

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertEqual('name.doc', response.json["data"]["title"])

        self.set_status('active.awarded')

        response = self.app.post('/tenders/{}/bids/{}/documents?acc_token={}'.format(
            self.tender_id, self.bid_id, self.bid_token), upload_files=[('file', 'name.doc', 'content')], status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't add document in current (active.awarded) tender status")

        response = self.app.get('/tenders/{}/bids/{}/documents/{}'.format(self.tender_id, self.bid_id, doc_id))
        self.assertEqual(response.status, '200 OK')
        if self.docservice:
            self.assertIn('http://localhost/get/', response.json['data']['url'])
            self.assertIn('Signature=', response.json['data']['url'])
            self.assertIn('KeyID=', response.json['data']['url'])
            self.assertNotIn('Expires=', response.json['data']['url'])
        else:
            self.assertIn('download=', response.json['data']['url'])

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?download={}&acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, key, self.bid_token))
        if self.docservice:
            self.assertIn('http://localhost/get/', response.location)
            self.assertIn('Signature=', response.location)
            self.assertIn('KeyID=', response.location)
            self.assertIn('Expires=', response.location)
        else:
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/msword')
            self.assertEqual(response.content_length, 7)
            self.assertEqual(response.body, 'content')

    def test_put_tender_bid_document(self):
        response = self.app.post('/tenders/{}/bids/{}/documents?acc_token={}'.format(
            self.tender_id, self.bid_id, self.bid_token), upload_files=[('file', 'name.doc', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])

        response = self.app.put('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(self.tender_id, self.bid_id, doc_id, self.bid_token),
                                status=404,
                                upload_files=[('invalid_name', 'name.doc', 'content')])
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location':
                u'body', u'name': u'file'}
        ])

        response = self.app.put('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, self.bid_token), upload_files=[('file', 'name.doc', 'content2')])
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?{}&acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, key, self.bid_token))
        if self.docservice:
            self.assertEqual(response.status, '302 Moved Temporarily')
            self.assertIn('http://localhost/get/', response.location)
            self.assertIn('Signature=', response.location)
            self.assertIn('KeyID=', response.location)
            self.assertIn('Expires=', response.location)
        else:
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/msword')
            self.assertEqual(response.content_length, 8)
            self.assertEqual(response.body, 'content2')

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertEqual('name.doc', response.json["data"]["title"])

        response = self.app.put('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, self.bid_token), 'content3', content_type='application/msword')
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?{}&acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, key, self.bid_token))
        if self.docservice:
            self.assertEqual(response.status, '302 Moved Temporarily')
            self.assertIn('http://localhost/get/', response.location)
            self.assertIn('Signature=', response.location)
            self.assertIn('KeyID=', response.location)
            self.assertIn('Expires=', response.location)
        else:
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/msword')
            self.assertEqual(response.content_length, 8)
            self.assertEqual(response.body, 'content3')

        self.set_status('active.awarded')

        response = self.app.put('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, self.bid_token), upload_files=[('file', 'name.doc', 'content3')], status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't update document in current (active.awarded) tender status")

    def test_patch_tender_bid_document(self):
        response = self.app.post('/tenders/{}/bids/{}/documents?acc_token={}'.format(
            self.tender_id, self.bid_id, self.bid_token), upload_files=[('file', 'name.doc', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])

        response = self.app.patch_json('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(self.tender_id, self.bid_id, doc_id, self.bid_token), {"data": {
            "documentOf": "lot"
        }}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [u'This field is required.'], u'location': u'body', u'name': u'relatedItem'},
        ])

        response = self.app.patch_json('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(self.tender_id, self.bid_id, doc_id, self.bid_token), {"data": {
            "documentOf": "lot",
            "relatedItem": '0' * 32
        }}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': [u'relatedItem should be one of lots'], u'location': u'body', u'name': u'relatedItem'}
        ])

        response = self.app.patch_json('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(self.tender_id, self.bid_id, doc_id, self.bid_token), {"data": {"description": "document description"}})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertEqual('document description', response.json["data"]["description"])

        self.set_status('active.awarded')

        response = self.app.patch_json('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(self.tender_id, self.bid_id, doc_id, self.bid_token), {"data": {"description": "document description"}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't update document in current (active.awarded) tender status")

    def test_create_tender_bid_document_nopending(self):
        response = self.app.post_json('/tenders/{}/bids'.format(
            self.tender_id), {'data': {'tenderers': [test_organization], "value": {"amount": 500}}})
        bid = response.json['data']
        token = response.json['access']['token']
        bid_id = bid['id']

        response = self.app.post('/tenders/{}/bids/{}/documents?acc_token={}'.format(
            self.tender_id, bid_id, token), upload_files=[('file', 'name.doc', 'content')])
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])

        self.set_status('active.qualification')

        response = self.app.patch_json('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(
            self.tender_id, bid_id, doc_id, token), {"data": {"description": "document description"}}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't update document because award of bid is not in pending state")

        response = self.app.put('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(
            self.tender_id, bid_id, doc_id, token), 'content3', content_type='application/msword', status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't update document because award of bid is not in pending state")

        response = self.app.post('/tenders/{}/bids/{}/documents?acc_token={}'.format(
            self.tender_id, bid_id, token), upload_files=[('file', 'name.doc', 'content')], status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't add document because award of bid is not in pending state")


class TenderBidDocumentWithDSResourceTest(TenderBidDocumentResourceTest):
    docservice = True

    def test_create_tender_bid_document_json(self):
        response = self.app.post_json('/tenders/{}/bids/{}/documents?acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token),
            {'data': {
                'title': 'name.doc',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/msword',
            }})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])
        self.assertEqual('name.doc', response.json["data"]["title"])
        key = response.json["data"]["url"].split('?')[-1].split('=')[-1]

        response = self.app.get('/tenders/{}/bids/{}/documents'.format(self.tender_id, self.bid_id), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't view bid documents in current (active.tendering) tender status")

        response = self.app.get('/tenders/{}/bids/{}/documents?acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"][0]["id"])
        self.assertEqual('name.doc', response.json["data"][0]["title"])

        response = self.app.get('/tenders/{}/bids/{}/documents?all=true&acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"][0]["id"])
        self.assertEqual('name.doc', response.json["data"][0]["title"])

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?download=some_id&acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, self.bid_token), status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location': u'url', u'name': u'download'}
        ])

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?download={}'.format(
            self.tender_id, self.bid_id, doc_id, key), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't view bid document in current (active.tendering) tender status")

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?download={}&acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, key, self.bid_token))
        self.assertEqual(response.status, '302 Moved Temporarily')
        self.assertIn('http://localhost/get/', response.location)
        self.assertIn('Signature=', response.location)
        self.assertIn('KeyID=', response.location)
        self.assertIn('Expires=', response.location)

        response = self.app.get('/tenders/{}/bids/{}/documents/{}'.format(
            self.tender_id, self.bid_id, doc_id), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't view bid document in current (active.tendering) tender status")

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertEqual('name.doc', response.json["data"]["title"])

        response = self.app.post_json('/tenders/{}/bids/{}/documents?acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token),
            {'data': {
                'title': 'name.doc',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/msword',
            }})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        self.assertIn(response.json["data"]['id'], response.headers['Location'])
        self.assertEqual('name.doc', response.json["data"]["title"])

        self.set_status('active.awarded')

        response = self.app.post_json('/tenders/{}/bids/{}/documents?acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token),
            {'data': {
                'title': 'name.doc',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/msword',
            }}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't add document in current (active.awarded) tender status")

        response = self.app.get('/tenders/{}/bids/{}/documents/{}'.format(self.tender_id, self.bid_id, doc_id))
        self.assertEqual(response.status, '200 OK')
        self.assertIn('http://localhost/get/', response.json['data']['url'])
        self.assertIn('Signature=', response.json['data']['url'])
        self.assertIn('KeyID=', response.json['data']['url'])
        self.assertNotIn('Expires=', response.json['data']['url'])

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?download={}&acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, key, self.bid_token))
        self.assertIn('http://localhost/get/', response.location)
        self.assertIn('Signature=', response.location)
        self.assertIn('KeyID=', response.location)
        self.assertIn('Expires=', response.location)

    def test_put_tender_bid_document_json(self):
        response = self.app.post_json('/tenders/{}/bids/{}/documents?acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token),
            {'data': {
                'title': 'name.doc',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/msword',
            }})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        doc_id = response.json["data"]['id']
        self.assertIn(doc_id, response.headers['Location'])

        response = self.app.put_json('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(self.tender_id, self.bid_id, doc_id, self.bid_token),
            {'data': {
                'title': 'name.doc',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/msword',
                'description': 'test description',
            }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual('test description', response.json["data"]["description"])
        self.assertEqual(doc_id, response.json["data"]["id"])
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?{}&acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, key, self.bid_token))
        self.assertEqual(response.status, '302 Moved Temporarily')
        self.assertIn('http://localhost/get/', response.location)
        self.assertIn('Signature=', response.location)
        self.assertIn('KeyID=', response.location)
        self.assertIn('Expires=', response.location)

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(doc_id, response.json["data"]["id"])
        self.assertEqual('name.doc', response.json["data"]["title"])

        response = self.app.put_json('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(self.tender_id, self.bid_id, doc_id, self.bid_token),
            {'data': {
                'title': 'name.doc',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/msword',
            }})
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual('test description', response.json["data"]["description"])
        self.assertEqual(doc_id, response.json["data"]["id"])
        key = response.json["data"]["url"].split('?')[-1]

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?{}&acc_token={}'.format(
            self.tender_id, self.bid_id, doc_id, key, self.bid_token))
        self.assertEqual(response.status, '302 Moved Temporarily')
        self.assertIn('http://localhost/get/', response.location)
        self.assertIn('Signature=', response.location)
        self.assertIn('KeyID=', response.location)
        self.assertIn('Expires=', response.location)

        self.set_status('active.awarded')

        response = self.app.put_json('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(self.tender_id, self.bid_id, doc_id, self.bid_token),
            {'data': {
                'title': 'name.doc',
                'url': self.generate_docservice_url(),
                'hash': 'md5:' + '0' * 32,
                'format': 'application/msword',
            }}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't update document in current (active.awarded) tender status")


class TenderBidBatchDocumentWithDSResourceTest(TenderContentWebTest):
    docservice = True
    initial_status = 'active.tendering'

    def test_create_tender_bid_with_document_invalid(self):
        response = self.app.post_json('/tenders/{}/bids'.format( self.tender_id),
            {'data': {
                 'tenderers': [test_organization],
                 "value": {"amount": 500},
                 'documents': [{
                        'title': 'name.doc',
                        'url': 'http://invalid.docservice.url/get/uuid',
                        'hash': 'md5:' + '0' * 32,
                        'format': 'application/msword'
                    }]
            }}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can add document only from document service.")

        response = self.app.post_json('/tenders/{}/bids'.format( self.tender_id),
            {'data': {
                 'tenderers': [test_organization],
                 "value": {"amount": 500},
                 'documents': [{
                        'title': 'name.doc',
                        'url': '/'.join(self.generate_docservice_url().split('/')[:4]),
                        'hash': 'md5:' + '0' * 32,
                        'format': 'application/msword'
                    }]
            }}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can add document only from document service.")

        response = self.app.post_json('/tenders/{}/bids'.format( self.tender_id),
            {'data': {
                 'tenderers': [test_organization],
                 "value": {"amount": 500},
                 'documents': [{
                        'title': 'name.doc',
                        'url': self.generate_docservice_url().split('?')[0],
                        'hash': 'md5:' + '0' * 32,
                        'format': 'application/msword'
                    }]
            }}, status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can add document only from document service.")

        response = self.app.post_json('/tenders/{}/bids'.format( self.tender_id),
            {'data': {
                 'tenderers': [test_organization],
                 "value": {"amount": 500},
                 'documents': [{
                        'title': 'name.doc',
                        'url': self.generate_docservice_url(),
                        'format': 'application/msword'
                    }]
            }}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["location"], "documents")
        self.assertEqual(response.json['errors'][0]["name"], "hash")
        self.assertEqual(response.json['errors'][0]["description"], "This field is required.")

        response = self.app.post_json('/tenders/{}/bids'.format( self.tender_id),
            {'data': {
                 'tenderers': [test_organization],
                 "value": {"amount": 500},
                 'documents': [{
                        'title': 'name.doc',
                        'url': self.generate_docservice_url().replace(self.app.app.registry.keyring.keys()[-1], '0' * 8),
                        'hash': 'md5:' + '0' * 32,
                        'format': 'application/msword'
                    }]
            }}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Document url expired.")

        response = self.app.post_json('/tenders/{}/bids'.format( self.tender_id),
            {'data': {
                 'tenderers': [test_organization],
                 "value": {"amount": 500},
                 'documents': [{
                        'title': 'name.doc',
                        'url': self.generate_docservice_url().replace("Signature=", "Signature=ABC"),
                        'hash': 'md5:' + '0' * 32,
                        'format': 'application/msword'
                    }]
            }}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Document url signature invalid.")

        response = self.app.post_json('/tenders/{}/bids'.format( self.tender_id),
            {'data': {
                 'tenderers': [test_organization],
                 "value": {"amount": 500},
                 'documents': [{
                        'title': 'name.doc',
                        'url': self.generate_docservice_url().replace("Signature=", "Signature=bw%3D%3D"),
                        'hash': 'md5:' + '0' * 32,
                        'format': 'application/msword'
                    }]
            }}, status=422)
        self.assertEqual(response.status, '422 Unprocessable Entity')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Document url invalid.")


    def test_create_tender_bid_with_document(self):
        response = self.app.post_json('/tenders/{}/bids'.format( self.tender_id),
            {'data': {
                 'tenderers': [test_organization],
                 "value": {"amount": 500},
                 'documents': [{
                        'title': 'name.doc',
                        'url': self.generate_docservice_url(),
                        'hash': 'md5:' + '0' * 32,
                        'format': 'application/msword'
                    }]
            }})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bid = response.json['data']
        self.assertEqual(bid['tenderers'][0]['name'], test_organization['name'])
        self.assertIn('id', bid)
        self.bid_id = bid['id']
        self.bid_token = response.json['access']['token']
        self.assertIn(bid['id'], response.headers['Location'])
        document = bid['documents'][0]
        self.assertEqual('name.doc', document["title"])
        key = document["url"].split('?')[-1].split('=')[-1]

        response = self.app.get('/tenders/{}/bids/{}/documents'.format(self.tender_id, self.bid_id), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't view bid documents in current (active.tendering) tender status")

        response = self.app.get('/tenders/{}/bids/{}/documents?acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(document['id'], response.json["data"][0]["id"])
        self.assertEqual('name.doc', response.json["data"][0]["title"])

        response = self.app.get('/tenders/{}/bids/{}/documents?all=true&acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(document['id'], response.json["data"][0]["id"])
        self.assertEqual('name.doc', response.json["data"][0]["title"])

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?download=some_id&acc_token={}'.format(
            self.tender_id, self.bid_id, document['id'], self.bid_token), status=404)
        self.assertEqual(response.status, '404 Not Found')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['status'], 'error')
        self.assertEqual(response.json['errors'], [
            {u'description': u'Not Found', u'location': u'url', u'name': u'download'}
        ])

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?download={}'.format(
            self.tender_id, self.bid_id, document['id'], key), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't view bid document in current (active.tendering) tender status")

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?download={}&acc_token={}'.format(
            self.tender_id, self.bid_id, document['id'], key, self.bid_token))
        self.assertEqual(response.status, '302 Moved Temporarily')
        self.assertIn('http://localhost/get/', response.location)
        self.assertIn('Signature=', response.location)
        self.assertIn('KeyID=', response.location)
        self.assertIn('Expires=', response.location)

        response = self.app.get('/tenders/{}/bids/{}/documents/{}'.format(
            self.tender_id, self.bid_id, document['id']), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't view bid document in current (active.tendering) tender status")

        response = self.app.get('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(
            self.tender_id, self.bid_id, document['id'], self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(document['id'], response.json["data"]["id"])
        self.assertEqual('name.doc', response.json["data"]["title"])


    def test_create_tender_bid_with_documents(self):
        dateModified = self.db.get(self.tender_id).get('dateModified')

        response = self.app.post_json('/tenders/{}/bids'.format( self.tender_id),
            {'data': {
                 'tenderers': [test_organization],
                 "value": {"amount": 500},
                 'documents': [{
                        'title': 'first.doc',
                        'url': self.generate_docservice_url(),
                        'hash': 'md5:' + '0' * 32,
                        'format': 'application/msword'
                    },
                    {
                        'title': 'second.doc',
                        'url': self.generate_docservice_url(),
                        'hash': 'md5:' + '0' * 32,
                        'format': 'application/msword'
                    },
                    {
                        'title': 'third.doc',
                        'url': self.generate_docservice_url(),
                        'hash': 'md5:' + '0' * 32,
                        'format': 'application/msword'
                    }]
            }})
        self.assertEqual(response.status, '201 Created')
        self.assertEqual(response.content_type, 'application/json')
        bid = response.json['data']
        self.assertEqual(bid['tenderers'][0]['name'], test_organization['name'])
        self.assertIn('id', bid)
        self.bid_id = bid['id']
        self.bid_token = response.json['access']['token']
        self.assertIn(bid['id'], response.headers['Location'])
        documents = bid['documents']
        ids = [doc['id'] for doc in documents]
        self.assertEqual(['first.doc', 'second.doc', 'third.doc'], [document["title"] for document in documents])

        response = self.app.get('/tenders/{}/bids/{}/documents'.format(self.tender_id, self.bid_id), status=403)
        self.assertEqual(response.status, '403 Forbidden')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(response.json['errors'][0]["description"], "Can't view bid documents in current (active.tendering) tender status")

        response = self.app.get('/tenders/{}/bids/{}/documents?acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(len(response.json["data"]), 3)
        self.assertEqual(ids, [doc['id'] for doc in response.json["data"]])

        response = self.app.get('/tenders/{}/bids/{}/documents?all=true&acc_token={}'.format(self.tender_id, self.bid_id, self.bid_token))
        self.assertEqual(response.status, '200 OK')
        self.assertEqual(response.content_type, 'application/json')
        self.assertEqual(len(response.json["data"]), 3)
        self.assertEqual(ids, [doc['id'] for doc in response.json["data"]])

        for index, document in enumerate(documents):
            key = document["url"].split('?')[-1].split('=')[-1]

            response = self.app.get('/tenders/{}/bids/{}/documents/{}?download=some_id&acc_token={}'.format(
                self.tender_id, self.bid_id, document['id'], self.bid_token), status=404)
            self.assertEqual(response.status, '404 Not Found')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.json['status'], 'error')
            self.assertEqual(response.json['errors'], [
                {u'description': u'Not Found', u'location': u'url', u'name': u'download'}
            ])

            response = self.app.get('/tenders/{}/bids/{}/documents/{}?download={}'.format(
                self.tender_id, self.bid_id, document['id'], key), status=403)
            self.assertEqual(response.status, '403 Forbidden')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.json['errors'][0]["description"], "Can't view bid document in current (active.tendering) tender status")

            response = self.app.get('/tenders/{}/bids/{}/documents/{}?download={}&acc_token={}'.format(
                self.tender_id, self.bid_id, document['id'], key, self.bid_token))
            self.assertEqual(response.status, '302 Moved Temporarily')
            self.assertIn('http://localhost/get/', response.location)
            self.assertIn('Signature=', response.location)
            self.assertIn('KeyID=', response.location)
            self.assertIn('Expires=', response.location)

            response = self.app.get('/tenders/{}/bids/{}/documents/{}'.format(
                self.tender_id, self.bid_id, document['id']), status=403)
            self.assertEqual(response.status, '403 Forbidden')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(response.json['errors'][0]["description"], "Can't view bid document in current (active.tendering) tender status")

            response = self.app.get('/tenders/{}/bids/{}/documents/{}?acc_token={}'.format(
                self.tender_id, self.bid_id, document['id'], self.bid_token))
            self.assertEqual(response.status, '200 OK')
            self.assertEqual(response.content_type, 'application/json')
            self.assertEqual(document['id'], response.json["data"]["id"])


def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TenderBidDocumentResourceTest))
    suite.addTest(unittest.makeSuite(TenderBidDocumentWithDSResourceTest))
    suite.addTest(unittest.makeSuite(TenderBidFeaturesResourceTest))
    suite.addTest(unittest.makeSuite(TenderBidResourceTest))
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
