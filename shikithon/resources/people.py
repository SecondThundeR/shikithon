"""Represents /api/people resource."""
from typing import Any, Dict, List, Optional

from ..decorators import method_endpoint
from ..enums import PersonKind
from ..models import Person
from ..utils import Utils
from .base_resource import BaseResource


class People(BaseResource):
    """People resource class.

    Used to represent /api/people resource.
    """

    @method_endpoint('/api/people/:id')
    async def get(self, people_id: int) -> Optional[Person]:
        """
        Returns info about a person.

        :param people_id: ID of person to get info
        :type people_id: int

        :return: Info about a person
        :rtype: Optional[Person]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.people(people_id))
        return Utils.validate_response_data(response, data_model=Person)

    @method_endpoint('/api/people/search')
    async def search(self,
                     search: Optional[str] = None,
                     people_kind: Optional[str] = None) -> List[Person]:
        """
        Returns list of found persons.

        **Note:** This API method only allows 'seyu',
        'mangaka' or 'producer' as kind parameter

        :param search:  Search query for persons
        :type search: Optional[str]

        :param people_kind: Kind of person for searching
        :type people_kind: Optional[str]

        :return: List of found persons
        :rtype: List[Person]
        """
        if not Utils.validate_enum_params({PersonKind: people_kind}):
            return []

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.people_search,
            query=Utils.create_query_dict(search=search, kind=people_kind))
        return Utils.validate_response_data(response,
                                            data_model=Person,
                                            fallback=[])
