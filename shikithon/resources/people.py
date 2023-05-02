"""Represents `/api/people` resource."""
from typing import Any, Dict, List, Optional, cast

from ..decorators import exceptions_handler, method_endpoint
from ..enums import PersonSearchKind
from ..exceptions import ShikimoriAPIResponseError
from ..models import PersonInfo, Person
from ..utils import Utils
from .base_resource import BaseResource


class People(BaseResource):
    """People resource class.

    Used to represent `/api/people` resource
    """

    @method_endpoint('/api/people/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def get(self, people_id: int):
        """Returns info about a person.

        :param people_id: ID of person to get info
        :type people_id: int

        :return: Info about a person
        :rtype: Optional[Person]
        """
        response = await self._client.request(
            self._client.endpoints.people(people_id))

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Person)

    @method_endpoint('/api/people/search')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def search(self,
                     search: Optional[str] = None,
                     people_kind: Optional[PersonSearchKind] = None):
        """Returns list of found persons.

        :param search: Search query for persons
        :type search: Optional[str]

        :param people_kind: Kind of person for searching
        :type people_kind: Optional[PersonSearchKind]

        :return: List of found persons
        :rtype: List[PersonInfo]
        """
        query_dict = Utils.create_query_dict(search=search, kind=people_kind)

        response = await self._client.request(
            self._client.endpoints.people_search, query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=PersonInfo)
