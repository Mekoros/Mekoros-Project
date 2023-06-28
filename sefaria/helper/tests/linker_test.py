from sefaria.helper import linker
import json
import pytest
from unittest.mock import patch, Mock
from sefaria.google_storage_manager import GoogleStorageManager
from django.test import RequestFactory
import spacy
import tarfile
import io
from sefaria.model.text import Ref

@pytest.fixture
def mock_oref():
    return Ref("Job 17")


@pytest.fixture
def spacy_model():
    return spacy.blank('en')


class TestLoadSpacyModel:

    @staticmethod
    @pytest.fixture
    def tarfile_buffer():
        tar_buffer = io.BytesIO()
        with tarfile.open(fileobj=tar_buffer, mode='w:gz') as tar:
            tar.addfile(tarfile.TarInfo('test'))
        tar_buffer.seek(0)
        return tar_buffer

    @staticmethod
    @patch('spacy.load')
    def test_load_spacy_model_local(spacy_load_mock, spacy_model):
        spacy_load_mock.return_value = spacy_model
        assert linker.load_spacy_model('local/path') == spacy_model

    @staticmethod
    @patch('spacy.load')
    @patch.object(GoogleStorageManager, 'get_filename')
    def test_load_spacy_model_cloud(get_filename_mock, spacy_load_mock, spacy_model, tarfile_buffer):
        get_filename_mock.return_value = tarfile_buffer
        spacy_load_mock.return_value = spacy_model
        assert linker.load_spacy_model('gs://bucket_name/blob_name') == spacy_model

    @staticmethod
    @patch('spacy.load')
    @patch.object(GoogleStorageManager, 'get_filename')
    def test_load_spacy_model_cloud_invalid_path(get_filename_mock, spacy_load_mock, spacy_model, tarfile_buffer):
        get_filename_mock.return_value = tarfile_buffer
        spacy_load_mock.side_effect = OSError
        with pytest.raises(OSError):
            linker.load_spacy_model('invalid_path')


@pytest.fixture
def mock_request_post_data():
    return {
        'text': {'title': 'title', 'body': 'body'},
        'version_preferences_by_corpus': {},
        'metaDataForTracking': {'url': 'https://test.com', 'title': 'title', 'description': 'description'}
    }


@pytest.fixture
def mock_request_post_data_without_meta_data(mock_request_post_data):
    del mock_request_post_data['metaDataForTracking']
    return mock_request_post_data


def make_mock_request(post_data):
    factory = RequestFactory()
    request = factory.post('/api/find-refs', data=json.dumps(post_data), content_type='application/json')
    request.GET = {'with_text': '1', 'debug': '1', 'max_segments': '10'}
    return request


@pytest.fixture
def mock_request(mock_request_post_data):
    return make_mock_request(mock_request_post_data)


@pytest.fixture
def mock_find_refs_text(mock_request):
    post_body = json.loads(mock_request.body)
    return linker._create_find_refs_text(post_body)


@pytest.fixture
def mock_find_refs_options(mock_request):
    post_body = json.loads(mock_request.body)
    return linker._create_find_refs_options(mock_request.GET, post_body)


@pytest.fixture
def mock_request_without_meta_data(mock_request_post_data_without_meta_data):
    return make_mock_request(mock_request_post_data_without_meta_data)


@pytest.fixture
def mock_webpage():
    with patch('sefaria.helper.linker.WebPage') as MockWebPage:
        mock_webpage = MockWebPage.return_value
        loaded_webpage = Mock()
        mock_webpage.load.return_value = loaded_webpage
        loaded_webpage.url = "test url"
        MockWebPage.add_or_update_from_linker.return_value = (None, loaded_webpage)
        yield loaded_webpage


class TestFindRefsHelperClasses:

    @patch('sefaria.utils.hebrew.is_hebrew', return_value=False)
    def test_find_refs_text(self, mock_is_hebrew):
        find_refs_text = linker._FindRefsText('title', 'body')
        mock_is_hebrew.assert_called_once_with('body')
        assert find_refs_text.lang == 'en'

    def test_find_refs_text_options(self):
        find_refs_text_options = linker._FindRefsTextOptions(True, True, 10, {})
        assert find_refs_text_options.debug
        assert find_refs_text_options.with_text
        assert find_refs_text_options.max_segments == 10
        assert find_refs_text_options.version_preferences_by_corpus == {}

    def test_create_find_refs_text(self, mock_request):
        post_body = json.loads(mock_request.body)
        find_refs_text = linker._create_find_refs_text(post_body)
        assert find_refs_text.title == 'title'
        assert find_refs_text.body == 'body'

    def test_create_find_refs_options(self, mock_request):
        post_body = json.loads(mock_request.body)
        find_refs_options = linker._create_find_refs_options(mock_request.GET, post_body)
        assert find_refs_options.with_text
        assert find_refs_options.debug
        assert find_refs_options.max_segments == 10
        assert find_refs_options.version_preferences_by_corpus == {}


class TestMakeFindRefsResponse:
    def test_make_find_refs_response_with_meta_data(self, mock_request, mock_webpage):
        response = linker.make_find_refs_response(mock_request)
        mock_webpage.add_hit.assert_called_once()
        mock_webpage.save.assert_called_once()

    def test_make_find_refs_response_without_meta_data(self, mock_request_without_meta_data, mock_webpage):
        response = linker.make_find_refs_response(mock_request_without_meta_data)
        mock_webpage.add_hit.assert_not_called()
        mock_webpage.save.assert_not_called()


class TestUnpackFindRefsRequest:
    def test_unpack_find_refs_request(self, mock_request):
        text, options, meta_data = linker._unpack_find_refs_request(mock_request)
        assert isinstance(text, linker._FindRefsText)
        assert isinstance(options, linker._FindRefsTextOptions)
        assert meta_data == {'url': 'https://test.com', 'description': 'description', 'title': 'title'}

    def test_unpack_find_refs_request_without_meta_data(self, mock_request_without_meta_data):
        text, options, meta_data = linker._unpack_find_refs_request(mock_request_without_meta_data)
        assert isinstance(text, linker._FindRefsText)
        assert isinstance(options, linker._FindRefsTextOptions)
        assert meta_data is None


class TestAddWebpageHitForUrl:
    def test_add_webpage_hit_for_url(self, mock_webpage):
        linker._add_webpage_hit_for_url('https://test.com')
        mock_webpage.add_hit.assert_called_once()
        mock_webpage.save.assert_called_once()

    def test_add_webpage_hit_for_url_no_url(self, mock_webpage):
        linker._add_webpage_hit_for_url(None)
        mock_webpage.add_hit.assert_not_called()
        mock_webpage.save.assert_not_called()


class TestFindRefsResponseLinkerV3:

    @pytest.fixture
    def mock_get_ref_resolver(self, spacy_model):
        from sefaria.model.text import library
        with patch.object(library, 'get_ref_resolver') as mock_get_ref_resolver:
            mock_ref_resolver = Mock()
            mock_ref_resolver._raw_ref_model_by_lang = {"en": spacy_model}
            mock_get_ref_resolver.return_value = mock_ref_resolver
            mock_ref_resolver.bulk_resolve_refs.return_value = [[]]
            yield mock_get_ref_resolver

    def test_make_find_refs_response_linker_v3(self, mock_get_ref_resolver, mock_find_refs_text, mock_find_refs_options):
        response = linker._make_find_refs_response_linker_v3(mock_find_refs_text, mock_find_refs_options)
        assert 'title' in response
        assert 'body' in response


class TestFindRefsResponseInner:
    @pytest.fixture
    def mock_resolved(self):
        return [[]]

    def test_make_find_refs_response_inner(self, mock_resolved, mock_find_refs_options):
        response = linker._make_find_refs_response_inner(mock_resolved, mock_find_refs_options)
        assert 'results' in response
        assert 'refData' in response


class TestRefResponseForLinker:

    def test_make_ref_response_for_linker(self, mock_oref, mock_find_refs_options):
        response = linker._make_ref_response_for_linker(mock_oref, mock_find_refs_options)
        assert 'heRef' in response
        assert 'url' in response
        assert 'primaryCategory' in response


class TestPreferredVtitle:
    @pytest.mark.parametrize(('oref', 'vprefs_by_corpus', 'expected_vpref'), [
        [Ref("Job 17"), None, None],
        [Ref("Job 17"), {"Tanakh": {"en": "vtitle1"}}, "vtitle1"],
        [Ref("Shabbat 2a"), {"Tanakh": {"en": "vtitle1"}}, None],
        [Ref("Shabbat 2a"), {"Bavli": {"en": "vtitle1"}}, "vtitle1"],
        [Ref("Shabbat 2a"), {"Bavli": {"he": "vtitle1"}}, None],
    ])
    def test_get_preferred_vtitle(self, oref, vprefs_by_corpus, expected_vpref):
        vpref = linker._get_preferred_vtitle(oref, 'en', vprefs_by_corpus)
        assert vpref == expected_vpref


class TestRefTextByLangForLinker:

    @pytest.mark.parametrize(('options', 'text_array', 'expected_text_array', 'expected_was_truncated'), [
        ({"max_segments": 4}, ['a'], ['a'], False),
        ({"max_segments": 2}, ['a', 'b'], ['a', 'b'], False),
        ({"max_segments": 2}, ['a', 'b', 'c'], ['a', 'b'], True),
    ])
    def test_get_ref_text_by_lang_for_linker(self, mock_oref, options, text_array, expected_text_array, expected_was_truncated):
        find_refs_options = linker._FindRefsTextOptions(**options)
        with patch('sefaria.model.text.TextChunk') as MockedTC:
            mocked_tc = MockedTC.return_value
            mocked_ja = Mock()
            mocked_ja.flatten_to_array.return_value = text_array
            mocked_tc.ja.return_value = mocked_ja
            mocked_tc.strip_itags.side_effect = lambda x: x

            # test
            actual_text_array, actual_was_truncated = linker._get_ref_text_by_lang_for_linker(mock_oref, 'en', find_refs_options)
            assert actual_text_array == expected_text_array
            assert actual_was_truncated == expected_was_truncated
