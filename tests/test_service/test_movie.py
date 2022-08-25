from unittest.mock import MagicMock

import pytest

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService


@pytest.fixture(autouse=True)
def movie_dao(db):
    movie_dao = MovieDAO(db.session)

    movie_list = []
    for i in range(5):
        item = Movie(
            id=i + 1,
            title=f'movie{i + 1}',
            description=f'description{i + 1}',
            trailer='http://123.com',
            year=1800 + i,
            genre_id=1,
            director_id=2
        )
        movie_list.append(item)

    m1, m2, m3, m4, m5 = movie_list

    movie_dao.get_one = MagicMock(return_value=m1)
    movie_dao.get_all = MagicMock(return_value=movie_list)
    movie_dao.create = MagicMock(return_value=Movie(id=6, title='movie6', description='xxx', trailer='xxx',
                                                    year=1806, genre_id=2, director_id=2))
    movie_dao.update = MagicMock(return_value='object updated')
    movie_dao.delete = MagicMock(return_value='object deleted')

    return movie_dao


class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_attributes(self):
        assert hasattr(self.movie_service, 'get_one')
        assert hasattr(self.movie_service, 'get_all')
        assert hasattr(self.movie_service, 'create')
        assert hasattr(self.movie_service, 'delete')
        assert hasattr(self.movie_service, 'update')
        assert hasattr(self.movie_service, 'partially_update')

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie is not None
        assert movie.id == 1
        assert movie.title == 'movie1'
        assert movie.genre_id == 1

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) == 5
        assert isinstance(movies[0], Movie)
        assert isinstance(movies[3], Movie)
        assert movies[4].id == 5

    def test_create(self):
        new_movie = {}
        movie = self.movie_service.create(new_movie)
        assert movie.id == 6
        assert movie.title == 'movie6'
        assert movie.trailer == 'xxx'

    def test_delete(self):
        movie_del = self.movie_service.delete(1)
        assert movie_del is None

    def test_update(self):
        movie_d = {}
        self.movie_service.update(movie_d)
        assert self.movie_service.get_one(2).title == 'movie1'
