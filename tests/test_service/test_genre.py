import pytest
from unittest.mock import MagicMock

from dao.genre import GenreDAO
from dao.model.genre import Genre
from service.genre import GenreService


@pytest.fixture(autouse=True)
def genre_dao(db):
    genre_dao = GenreDAO(db.session)

    g1 = Genre(id=1, name='g1')
    g2 = Genre(id=2, name='g2')

    genre_dao.get_one = MagicMock(return_value=g1)
    genre_dao.get_all = MagicMock(return_value=[g1, g2])
    genre_dao.create = MagicMock(return_value=Genre(id=3, name='g3'))
    genre_dao.update = MagicMock(return_value='object updated')
    genre_dao.delete = MagicMock(return_value='object deleted')

    return genre_dao


class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_attributes(self):
        assert hasattr(self.genre_service, 'get_one')
        assert hasattr(self.genre_service, 'get_all')
        assert hasattr(self.genre_service, 'create')
        assert hasattr(self.genre_service, 'delete')
        assert hasattr(self.genre_service, 'update')
        assert hasattr(self.genre_service, 'partially_update')

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre is not None
        assert genre.id == 1
        assert genre.name == 'g1'

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) == 2
        assert isinstance(genres[0], Genre)

    def test_create(self):
        new_genre = {
            "name": "g3"
        }
        genre = self.genre_service.create(new_genre)
        assert genre.id == 3
        assert genre.name == 'g3'

    def test_delete(self):
        genre_del = self.genre_service.delete(1)
        assert genre_del is None

    def test_update(self):
        genre_g = {
            "id": 2,
            "name": "g1"
        }
        self.genre_service.update(genre_g)
        assert self.genre_service.get_one(2).name == 'g1'
