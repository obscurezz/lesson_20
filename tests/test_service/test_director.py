from unittest.mock import MagicMock

import pytest

from dao.director import DirectorDAO
from dao.model.director import Director
from service.director import DirectorService


@pytest.fixture(autouse=True)
def director_dao(db):
    director_dao = DirectorDAO(db.session)

    d1 = Director(id=1, name='d1')
    d2 = Director(id=2, name='d2')

    director_dao.get_one = MagicMock(return_value=d1)
    director_dao.get_all = MagicMock(return_value=[d1, d2])
    director_dao.create = MagicMock(return_value=Director(id=3, name='d3'))
    director_dao.update = MagicMock(return_value='object updated')
    director_dao.delete = MagicMock(return_value='object deleted')

    return director_dao


class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_attributes(self):
        assert hasattr(self.director_service, 'get_one')
        assert hasattr(self.director_service, 'get_all')
        assert hasattr(self.director_service, 'create')
        assert hasattr(self.director_service, 'delete')
        assert hasattr(self.director_service, 'update')
        assert hasattr(self.director_service, 'partially_update')

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director is not None
        assert director.id == 1
        assert director.name == 'd1'

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) == 2
        assert isinstance(directors[0], Director)

    def test_create(self):
        new_director = {
            "name": "d3"
        }
        director = self.director_service.create(new_director)
        assert director.id == 3
        assert director.name == 'd3'

    def test_delete(self):
        director_del = self.director_service.delete(1)
        assert director_del is None

    def test_update(self):
        director_d = {
            "id": 2,
            "name": "d1"
        }
        self.director_service.update(director_d)
        assert self.director_service.get_one(2).name == 'd1'
