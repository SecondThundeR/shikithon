"""Represents /api/ranobes resource."""
from typing import Any, Dict, List, Optional, Union

from ..decorators import method_endpoint
from ..enums import RanobeCensorship
from ..enums import RanobeList
from ..enums import RanobeOrder
from ..enums import RanobeStatus
from ..models import Creator
from ..models import FranchiseTree
from ..models import Link
from ..models import Ranobe
from ..models import Relation
from ..models import Topic
from ..utils import Utils
from .base_resource import BaseResource


class Ranobes(BaseResource):
    """Ranobes resource class.

    Used to represent /api/ranobes resource.
    """

    @method_endpoint('/api/ranobe')
    async def get_all(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      order: Optional[str] = None,
                      status: Optional[Union[str, List[str]]] = None,
                      season: Optional[Union[str, List[str]]] = None,
                      score: Optional[int] = None,
                      genre: Optional[Union[int, List[int]]] = None,
                      publisher: Optional[Union[int, List[int]]] = None,
                      franchise: Optional[Union[int, List[int]]] = None,
                      censored: Optional[str] = None,
                      my_list: Optional[Union[str, List[str]]] = None,
                      ids: Optional[Union[int, List[int]]] = None,
                      exclude_ids: Optional[Union[int, List[int]]] = None,
                      search: Optional[str] = None) -> Optional[List[Ranobe]]:
        """
        Returns ranobe list.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param order: Type of order in list
        :type order: Optional[str]

        :param status: Type(s) of ranobe status
        :type status: Optional[Union[str, List[str]]]

        :param season: Name(s) of ranobe seasons
        :type season: Optional[Union[str, List[str]]]

        :param score: Minimal ranobe score
        :type score: Optional[int]

        :param publisher: Publisher(s) ID
        :type publisher: Optional[Union[int, List[int]]

        :param genre: Genre(s) ID
        :type genre: Optional[Union[int, List[int]]

        :param franchise: Franchise(s) ID
        :type franchise: Optional[Union[int, List[int]]

        :param censored: Type of ranobe censorship
        :type censored: Optional[str]

        :param my_list: Status(-es) of ranobe in current user list
            **Note:** If app in restricted mode,
            this won't affect on response.
        :type my_list: Optional[Union[str, List[str]]]

        :param ids: Ranobe(s) ID to include
        :type ids: Optional[Union[int, List[int]]

        :param exclude_ids: Ranobe(s) ID to exclude
        :type exclude_ids: Optional[Union[int, List[int]]

        :param search: Search phrase to filter ranobe by name
        :type search: Optional[str]

        :return: List of Ranobe
        :rtype: Optional[List[Ranobe]]
        """
        if not Utils.validate_enum_params({
                RanobeOrder: order,
                RanobeStatus: status,
                RanobeList: my_list,
                RanobeCensorship: censored
        }):
            return None

        validated_numbers = Utils.query_numbers_validator(page=[page, 100000],
                                                          limit=[limit, 50],
                                                          score=[score, 9])

        headers: Dict[str, str] = self._client.user_agent

        if my_list:
            headers = self._client.semi_protected_method('/api/ranobe')

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.ranobes,
            headers=headers,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            order=order,
                                            status=status,
                                            season=season,
                                            score=validated_numbers['score'],
                                            genre=genre,
                                            publisher=publisher,
                                            franchise=franchise,
                                            censored=censored,
                                            mylist=my_list,
                                            ids=ids,
                                            exclude_ids=exclude_ids,
                                            search=search))
        return Utils.validate_return_data(response, data_model=Ranobe)

    @method_endpoint('/api/ranobe/:id')
    async def get(self, ranobe_id: int) -> Optional[Ranobe]:
        """
        Returns info about certain ranobe.

        :param ranobe_id: Ranobe ID to get info
        :type ranobe_id: int

        :return: Ranobe info
        :rtype: Optional[Ranobe]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.ranobe(ranobe_id))
        return Utils.validate_return_data(response, data_model=Ranobe)

    @method_endpoint('/api/ranobe/:id/roles')
    async def creators(self, ranobe_id: int) -> Optional[List[Creator]]:
        """
        Returns creators info of certain ranobe.

        :param ranobe_id: Ranobe ID to get creators
        :type ranobe_id: int

        :return: List of ranobe creators
        :rtype: Optional[List[Creator]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.ranobe_roles(ranobe_id))
        return Utils.validate_return_data(response, data_model=Creator)

    @method_endpoint('/api/ranobe/:id/similar')
    async def similar(self, ranobe_id: int) -> Optional[List[Ranobe]]:
        """
        Returns list of similar ranobes for certain ranobe.

        :param ranobe_id: Ranobe ID to get similar ranobes
        :type ranobe_id: int

        :return: List of similar ranobes
        :rtype: Optional[List[Ranobe]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.similar_ranobes(ranobe_id))
        return Utils.validate_return_data(response, data_model=Ranobe)

    @method_endpoint('/api/ranobe/:id/related')
    async def related_content(self, ranobe_id: int) -> Optional[List[Relation]]:
        """
        Returns list of related content of certain ranobe.

        :param ranobe_id: Ranobe ID to get related content
        :type ranobe_id: int

        :return: List of relations
        :rtype: Optional[List[Relation]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.ranobe_related_content(ranobe_id))
        return Utils.validate_return_data(response, data_model=Relation)

    @method_endpoint('/api/ranobe/:id/franchise')
    async def franchise_tree(self, ranobe_id: int) -> Optional[FranchiseTree]:
        """
        Returns franchise tree of certain ranobe.

        :param ranobe_id: Ranobe ID to get franchise tree
        :type ranobe_id: int

        :return: Franchise tree of certain ranobe
        :rtype: Optional[FranchiseTree]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.ranobe_franchise_tree(ranobe_id))
        return Utils.validate_return_data(response, data_model=FranchiseTree)

    @method_endpoint('/api/ranobe/:id/external_links')
    async def external_links(self, ranobe_id: int) -> Optional[List[Link]]:
        """
        Returns list of external links of certain ranobe.

        :param ranobe_id: Ranobe ID to get external links
        :type ranobe_id: int

        :return: List of external links
        :rtype: Optional[List[Link]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.ranobe_external_links(ranobe_id))
        return Utils.validate_return_data(response, data_model=Link)

    @method_endpoint('/api/ranobe/:id/topics')
    async def topics(self,
                     ranobe_id: int,
                     page: Optional[int] = None,
                     limit: Optional[int] = None) -> Optional[List[Topic]]:
        """
        Returns list of topics of certain ranobe.

        If some data are not provided, using default values.

        :param ranobe_id: Ranobe ID to get topics
        :type ranobe_id: int

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of topics
        :rtype: Optional[List[Topic]]
        """
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.ranobe_topics(ranobe_id),
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit']))
        return Utils.validate_return_data(response, data_model=Topic)
