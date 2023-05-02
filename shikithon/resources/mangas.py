"""Represents `/api/mangas` resource."""
from typing import Any, Dict, List, Optional, Union, cast

from ..decorators import exceptions_handler, method_endpoint
from ..enums import (MangaCensorship, MangaKind, MangaList, MangaOrder,
                     MangaStatus)
from ..exceptions import ShikimoriAPIResponseError
from ..models import FranchiseTree, Link, Manga, MangaInfo, RanobeInfo, Relation, Role, Topic
from ..utils import Utils
from .base_resource import BaseResource


class Mangas(BaseResource):
    """Mangas resource class.

    Used to represent `/api/mangas` resource
    """

    @method_endpoint('/api/mangas')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      order: Optional[MangaOrder] = None,
                      kind: Optional[Union[MangaKind, List[MangaKind]]] = None,
                      status: Optional[Union[MangaStatus,
                                             List[MangaStatus]]] = None,
                      season: Optional[Union[str, List[str]]] = None,
                      score: Optional[int] = None,
                      genre: Optional[Union[int, List[int]]] = None,
                      publisher: Optional[Union[int, List[int]]] = None,
                      franchise: Optional[Union[int, List[int]]] = None,
                      censored: Optional[MangaCensorship] = None,
                      mylist: Optional[Union[MangaList,
                                             List[MangaList]]] = None,
                      ids: Optional[Union[int, List[int]]] = None,
                      exclude_ids: Optional[Union[int, List[int]]] = None,
                      search: Optional[str] = None):
        """Returns mangas list.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param order: Type of order in list
        :type order: Optional[MangaOrder]

        :param kind: Type(s) of manga topic
        :type kind: Optional[Union[MangaKind, List[MangaKind]]

        :param status: Type(s) of manga status
        :type status: Optional[Union[MangaStatus, List[MangaStatus]]]

        :param season: Name(s) of manga seasons
        :type season: Optional[Union[str, List[str]]]

        :param score: Minimal manga score
        :type score: Optional[int]

        :param publisher: Publisher(s) ID
        :type publisher: Optional[Union[int, List[int]]

        :param genre: Genre(s) ID
        :type genre: Optional[Union[int, List[int]]

        :param franchise: Franchise(s) ID
        :type franchise: Optional[Union[int, List[int]]

        :param censored: Type of manga censorship
        :type censored: Optional[MangaCensorship]

        :param mylist: Status(-es) of manga in current user list.
            If app is in restricted mode,
            this parameter won't affect on response.
        :type mylist: Optional[Union[MangaList, List[MangaList]]]

        :param ids: Manga(s) ID to include
        :type ids: Optional[Union[int, List[int]]

        :param exclude_ids: Manga(s) ID to exclude
        :type exclude_ids: Optional[Union[int, List[int]]

        :param search: Search phrase to filter mangas by name
        :type search: Optional[str]

        :return: List of Mangas
        :rtype: List[MangaInfo]
        """
        query_dict = Utils.create_query_dict(page=page,
                                             limit=limit,
                                             order=order,
                                             kind=kind,
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

        response = await self._client.request(self._client.endpoints.mangas,
                                              query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=MangaInfo)

    @method_endpoint('/api/mangas/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def get(self, manga_id: int):
        """Returns info about certain manga.

        :param manga_id: Manga ID to get info
        :type manga_id: int

        :return: Manga info
        :rtype: Optional[Manga]
        """
        response = await self._client.request(
            self._client.endpoints.manga(manga_id))

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Manga)

    @method_endpoint('/api/mangas/:id/roles')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def roles(self, manga_id: int):
        """Returns roles info of certain manga.

        :param manga_id: Manga ID to get roles
        :type manga_id: int

        :return: List of manga roles
        :rtype: List[Role]
        """
        response = await self._client.request(
            self._client.endpoints.manga_roles(manga_id))

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Role)

    @method_endpoint('/api/mangas/:id/similar')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def similar(self, manga_id: int):
        """Returns list of similar mangas or ranobe for certain manga.

        :param manga_id: Manga ID to get similar mangas/ranobe
        :type manga_id: int

        :return: List of similar mangas/ranobe
        :rtype: List[Union[MangaInfo, RanobeInfo]]
        """
        response = await self._client.request(
            self._client.endpoints.similar_mangas(manga_id))

        return Utils.parse_mixed_response(response, List[Union[MangaInfo,
                                                               RanobeInfo]])

    @method_endpoint('/api/mangas/:id/related')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def related(self, manga_id: int):
        """Returns list of related content of certain manga.

        :param manga_id: Manga ID to get related content
        :type manga_id: int

        :return: List of relations
        :rtype: List[Relation]
        """
        response = await self._client.request(
            self._client.endpoints.manga_related_content(manga_id))

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Relation)

    @method_endpoint('/api/mangas/:id/franchise')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def franchise(self, manga_id: int):
        """Returns franchise tree of certain manga.

        :param manga_id: Manga ID to get franchise tree
        :type manga_id: int

        :return: Franchise tree of certain manga
        :rtype: Optional[FranchiseTree]
        """
        response = await self._client.request(
            self._client.endpoints.manga_franchise_tree(manga_id))

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=FranchiseTree)

    @method_endpoint('/api/mangas/:id/external_links')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def external_links(self, manga_id: int):
        """Returns list of external links of certain manga.

        :param manga_id: Manga ID to get external links
        :type manga_id: int

        :return: List of external links
        :rtype: List[Link]
        """
        response = await self._client.request(
            self._client.endpoints.manga_external_links(manga_id))

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Link)

    @method_endpoint('/api/mangas/:id/topics')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def topics(self,
                     manga_id: int,
                     page: Optional[int] = None,
                     limit: Optional[int] = None):
        """Returns list of topics of certain manga.

        :param manga_id: Manga ID to get topics
        :type manga_id: int

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of topics
        :rtype: List[Topic]
        """
        query_dict = Utils.create_query_dict(page=page, limit=limit)

        response = await self._client.request(
            self._client.endpoints.manga_topics(manga_id), query=query_dict)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=Topic)
