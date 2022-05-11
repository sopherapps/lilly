"""Module for testing the CRUDRouteSet"""
from lilly.actions import CreateOneAction, CreateManyAction, ReadOneAction, ReadManyAction, UpdateOneAction, \
    UpdateManyAction, DeleteOneAction, DeleteManyAction
from lilly.routing import routeset, CRUDRouteSet, CRUDRouteSetSettings
from test.assets.mock_internals import NameTestDTO, NameTestCreationDTO


@routeset
class MockCRUDRouteSet(CRUDRouteSet):
    """
    Mock class Based Route set that handles CRUD functionality out of the box
    """

    @classmethod
    def get_settings(cls) -> CRUDRouteSetSettings:
        # When an action is not defined, the dependant routes will not be shown
        return CRUDRouteSetSettings(
            base_path="/names",
            base_path_for_multiple_items="/admin/names",
            response_model=NameTestDTO,
            creation_request_model=NameTestCreationDTO,
            create_one_action=CreateOneAction,
            create_many_action=CreateManyAction,
            read_one_action=ReadOneAction,
            read_many_action=ReadManyAction,
            update_one_action=UpdateOneAction,
            update_many_action=UpdateManyAction,
            delete_one_action=DeleteOneAction,
            delete_many_action=DeleteManyAction,
            string_searchable_fields=["title"],
        )
