"""Represents `/api/ranobes` resource."""
from typing import Any, Dict, List, Optional, Union, cast

from ..decorators import exceptions_handler, method_endpoint
from ..enums import RanobeCensorship, RanobeList, RanobeOrder, RanobeStatus
from ..exceptions import ShikimoriAPIResponseError
from ..models import FranchiseTree, Link, RanobeInfo, MangaInfo, Ranobe, Relation, Role, Topic
from ..utils import Utils
from .base_resource import BaseResource


class Ranobes(BaseResource):
    """Ranobes resource class.

    Used to represent `/api/ranobes` resource
    """

    @method_endpoint('/api/ranobe')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      order: Optional[RanobeOrder] = None,
                      status: Optional[Union[RanobeStatus,
                                             List[RanobeStatus]]] = None,
                      season: Optional[Union[str, List[str]]] = None,
                      score: Optional[int] = None,
                      genre: Optional[Union[int, List[int]]] = None,
                      publisher: Optional[Union[int, List[int]]] = None,
                      franchise: Optional[Union[int, List[int]]] = None,
                      censored: Optional[RanobeCensorship] = None,
                      mylist: Optional[Union[RanobeList,
                                             List[RanobeList]]] = None,
                      ids: Optional[Union[int, List[int]]] = None,
                      exclude_ids: Optional[Union[int, List[int]]] = None,
                      search: Optional[str] = None):
        """Returns ranobe list.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param order: Type of order in list
        :type order: Optional[RanobeOrder]

        :param status: Type(s) of ranobe status
        :type status: Optional[Union[RanobeStatus, List[RanobeStatus]]]

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
        :type censored: Optional[RanobeCensorship]

        :param mylist: Status(-es) of ranobe in current user list.
            If app is in restricted mode,
            this parameter won't affect on response.
        :type mylist: Optional[Union[RanobeList, List[RanobeList]]]

        :param ids: Ranobe(s) ID to include
        :type ids: Optional[Union[int, List[int]]

        :param exclude_ids: Ranobe(s) ID to exclude
        :type exclude_ids: Optional[Union[int, List[int]]

        :param search: Search phrase to filter ranobe by name
        :type search: Optional[str]

        :return: List of Ranobe
        :rtype: List[RanobeInfo]
        """
        query_dict = Utils.create_query_dict(page=page,
                                             limit=limit,
                                             order=order,
                                             status=status,
                                             season=season,
                                             score=score,
                                             genre=genre,
                                             publisher=publisher,
                                             franchise=franchise,
                                             censored=censored,
                                             mylist=mylist,
                                             ids=ids,
                                             exclude_ids=exclude_ids,
                                             search=search)

        response = await self._client.request(self._client.endpoints.ranobes,
                                              query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=RanobeInfo)

    @method_endpoint('/api/ranobe/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def get(self, ranobe_id: int):
        """Returns info about certain ranobe.

        :param ranobe_id: Ranobe ID to get info
        :type ranobe_id: int

        :return: Ranobe info
        :rtype: Optional[Ranobe]
        """
        response = await self._client.request(
            self._client.endpoints.ranobe(ranobe_id))

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Ranobe)

    @method_endpoint('/api/ranobe/:id/roles')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def roles(self, ranobe_id: int):
        """Returns roles info of certain ranobe.

        :param ranobe_id: Ranobe ID to get creators
        :type ranobe_id: int

        :return: List of ranobe roles
        :rtype: List[Role]
        """
        response = await self._client.request(
            self._client.endpoints.ranobe_roles(ranobe_id))

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Role)

    @method_endpoint('/api/ranobe/:id/similar')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def similar(self, ranobe_id: int):
        """Returns list of similar mangas or ranobe for certain ranobe.

        :param ranobe_id: Ranobe ID to get similar mangas/ranobe
        :type ranobe_id: int

        :return: List of similar mangas/ranobe
        :rtype: List[Union[MangaInfo, RanobeInfo]]
        """
        response = await self._client.request(
            self._client.endpoints.similar_ranobes(ranobe_id))

        return Utils.parse_mixed_response(response, List[Union[MangaInfo,
                                                               RanobeInfo]])

    @method_endpoint('/api/ranobe/:id/related')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def related(self, ranobe_id: int):
        """Returns list of related content of certain ranobe.

        :param ranobe_id: Ranobe ID to get related content
        :type ranobe_id: int

        :return: List of relations
        :rtype: List[Relation]
        """
        response = await self._client.request(
            self._client.endpoints.ranobe_related_content(ranobe_id))

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Relation)

    @method_endpoint('/api/ranobe/:id/franchise')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def franchise(self, ranobe_id: int):
        """Returns franchise tree of certain ranobe.

        :param ranobe_id: Ranobe ID to get franchise tree
        :type ranobe_id: int

        :return: Franchise tree of certain ranobe
        :rtype: Optional[FranchiseTree]
        """
        response = await self._client.request(
            self._client.endpoints.ranobe_franchise_tree(ranobe_id))

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=FranchiseTree)

    @method_endpoint('/api/ranobe/:id/external_links')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def external_links(self, ranobe_id: int):
        """Returns list of external links of certain ranobe.

        :param ranobe_id: Ranobe ID to get external links
        :type ranobe_id: int

        :return: List of external links
        :rtype: List[Link]
        """
        response = await self._client.request(
            self._client.endpoints.ranobe_external_links(ranobe_id))

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Link)

    @method_endpoint('/api/ranobe/:id/topics')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def topics(self,
                     ranobe_id: int,
                     page: Optional[int] = None,
                     limit: Optional[int] = None):
        """Returns list of topics of certain ranobe.

        :param ranobe_id: Ranobe ID to get topics
        :type ranobe_id: int

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of topics
        :rtype: List[Topic]
        """
        query_dict = Utils.create_query_dict(page=page, limit=limit)

        response = await self._client.request(
            self._client.endpoints.ranobe_topics(ranobe_id), query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Topic)
