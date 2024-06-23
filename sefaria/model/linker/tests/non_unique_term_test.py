import pytest
from mekoros.model.schema import NonUniqueTerm
from mekoros.model.abstract import SluggedAbstractMongoRecord


@pytest.fixture(scope='module')
def duplicate_terms():
    initial_slug = "rashiBLAHBLAH"
    t = NonUniqueTerm({"slug": initial_slug, "titles": [{
        "text": "Rashi",
        "lang": "en",
        "primary": True
    }]})
    t.save()

    s = NonUniqueTerm({"slug": initial_slug, "titles": [{
        "text": "Rashi",
        "lang": "en",
        "primary": True
    }]})

    s.save()

    yield t, s, initial_slug

    t.delete()
    s.delete()


def test_duplicate_terms(duplicate_terms):
    t, s, initial_slug = duplicate_terms
    assert t.slug == SluggedAbstractMongoRecord.normalize_slug(initial_slug)
    assert s.slug == SluggedAbstractMongoRecord.normalize_slug(initial_slug) + "1"