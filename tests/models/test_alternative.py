# -*- coding: utf-8 -*-
from datetime import datetime

import pytest
from sqlalchemy_utils import (
    assert_max_length,
    assert_non_nullable,
    assert_nullable
)

from ..factories import AlternativeFactory, HearingFactory, ImageFactory


class TestAlternative(object):
    @pytest.fixture
    def alternative(self):
        return AlternativeFactory.build()

    def test_repr(self, alternative):
        expected = '<Alternative title=\'{title}\'>'.format(
            title=alternative.title
        )
        assert repr(alternative) == expected

    def test_commentable_id(self, alternative):
        expected = 'alternative-{id}'.format(id=alternative.id)
        assert alternative.commentable_id == expected

    def test_commentable_name(self, alternative):
        expected = 'Vaihtoehto {letter}'.format(letter=alternative.letter)
        assert alternative.commentable_name == expected

    def test_commentable_option(self, alternative):
        expected = '{id}:{name}'.format(
            id=alternative.commentable_id,
            name=alternative.commentable_name
        )
        assert alternative.commentable_option == expected


@pytest.mark.usefixtures('database')
class TestAlternativeWithDatabase(object):
    @pytest.fixture
    def alternative(self):
        return AlternativeFactory()

    @pytest.mark.parametrize(
        'column_name',
        [
            'created_at',
            'title',
            'lead',
            'body',
        ]
    )
    def test_non_nullable_columns(self, column_name, alternative):
        assert_non_nullable(alternative, column_name)

    def test_created_at_defaults_to_datetime(self):
        assert isinstance(
            AlternativeFactory(created_at=None).created_at,
            datetime
        )

    def test_updated_at_is_nullable(self, alternative):
        assert_nullable(alternative, 'updated_at')

    def test_updated_at_defaults_to_datetime(self):
        assert isinstance(
            AlternativeFactory(updated_at=None).created_at,
            datetime
        )

    def test_title_max_length_is_255(self, alternative):
        assert_max_length(alternative, 'title', 255)

    def test_title_defaults_to_empty_string(self):
        assert AlternativeFactory(title=None).title == ''

    def test_lead_defaults_to_empty_string(self):
        assert AlternativeFactory(lead=None).lead == ''

    def test_body_defaults_to_empty_string(self):
        assert AlternativeFactory(body=None).body == ''

    def test_hearing_id_is_nullable(self, alternative):
        assert_nullable(alternative, 'hearing_id')


@pytest.mark.usefixtures('database')
class TestImagePositionAndLetter(object):
    @pytest.fixture
    def hearing(self):
        return HearingFactory()

    @pytest.fixture
    def alternative(self):
        return AlternativeFactory.build()

    def test_position_should_be_automatically_set(self, hearing):
        hearing.alternatives.append(AlternativeFactory.build())
        hearing.alternatives.append(AlternativeFactory.build())
        assert hearing.alternatives[1].position == 1

    def test_position_should_update_automatically(sefl, hearing, alternative):
        hearing.alternatives.append(alternative)
        assert alternative.position == 0
        hearing.alternatives.insert(
            0, AlternativeFactory.build()
        )
        assert alternative.position == 1

    def test_first_alternative_letter_should_be_A(self, hearing, alternative):
        hearing.alternatives.append(alternative)
        assert alternative.letter == 'A'

    def test_letter_should_be_A_if_position_is_None(self, alternative):
        assert alternative.letter == 'A'


@pytest.mark.usefixtures('database')
class TestGetCommentableSectionsString(object):
    @pytest.fixture
    def image(self):
        return ImageFactory()

    @pytest.fixture
    def images(self):
        return [
            ImageFactory(),
            ImageFactory()
        ]

    @pytest.fixture
    def alternative(self):
        return AlternativeFactory()

    def test_contains_own_data(self, alternative):
        assert (
            alternative.commentable_id in
            alternative.get_commentable_sections_string()
        )

    def test_contains_main_image_data(self, alternative, image):
        alternative.main_image = image
        assert (
            image.commentable_id in
            alternative.get_commentable_sections_string()
        )

    def test_contains_data_of_all_the_images(self, alternative, images):
        alternative.images = images
        assert (
            images[0].commentable_id in
            alternative.get_commentable_sections_string()
        )
        assert (
            images[1].commentable_id in
            alternative.get_commentable_sections_string()
        )