import unittest
import json
import logging
from unittest.mock import patch
from httpreq.req import get_json
from docker.catalog import Catalog
from docker.repository import Repository
from docker.tag import Tag

class TestDockerRegistryManager(unittest.TestCase):

    @patch('httpreq.req.get_json')
    def test_catalog(self, patch):
        # mocking http request
        patch.return_value = {"repositories": ["repo1", "repo2", "repo3"]}
        test_list = [Repository('repo1'), Repository('repo2'), Repository('repo3')]

        cat = Catalog()
        ret = cat.get_catalog()
       
        self.assertEqual(len(test_list), len(ret))

        for index, repo in enumerate(ret):
            self.assertEqual(test_list[index].name, repo.name)
        
    @patch('httpreq.req.get_json')
    def test_repository(self, patch):
        # mocking http request
        patch.return_value = {"name": "repo1", "tags": ["tag1", "tag2", "tag3"]}
        test_list = [Tag('repo1', 'tag1'), Tag('repo1', 'tag2'), Tag('repo1', 'tag3')]

        rep = Repository('repo1')
        ret = rep.get_tags()

        self.assertEqual(len(test_list), len(ret))

        for index, tag in enumerate(ret):
            self.assertEqual(test_list[index].name, tag.name)
            self.assertEqual(test_list[index].tag, tag.tag)

    @patch('httpreq.req.get_image_ref')
    def test_tag(self, patch):
        # mocking http request
        sha = "sha:0145ds51005gg515e"
        patch.return_value = sha
        tag = Tag('repo1', 'tag1')
        tag.get_manifest()

        self.assertEqual('repo1', tag.name)
        self.assertEqual('tag1', tag.tag)
        self.assertEqual(sha, tag.sha)

if __name__ == '__main__':
    unittest.main()