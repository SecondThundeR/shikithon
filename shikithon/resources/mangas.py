"""Represents /api/mangas resource."""
from typing import Any, Dict, List, Optional, Union

from ..decorators import method_endpoint
from ..enums import MangaCensorship
from ..enums import MangaKind
from ..enums import MangaList
from ..enums import MangaOrder
from ..enums import MangaStatus
from ..models import Creator
from ..models import FranchiseTree
from ..models import Link
from ..models import Manga
from ..models import Relation
from ..models import Topic
from ..utils import Utils
from .base_resource import BaseResource


class Mangas(BaseResource):
    """Mangas resource class.

    Used to represent /api/mangas resource.
    """

    @method_endpoint('/api/mangas')
    async def get_all(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      order: Optional[str] = None,
                      kind: Optional[Union[str, List[str]]] = None,
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
                      search: Optional[str] = None) -> List[Manga]:
        """
        Returns mangas list.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param order: Type of order in list
        :type order: Optional[str]

        :param kind: Type(s) of manga topic
        :type kind: Optional[Union[str, List[str]]

        :param status: Type(s) of manga status
        :type status: Optional[Union[str, List[str]]]

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
        :type censored: Optional[str]

        :param my_list: Status(-es) of manga in current user list.
            If app is in restricted mode,
            this parameter won't affect on response.
        :type my_list: Optional[Union[str, List[str]]]

        :param ids: Manga(s) ID to include
        :type ids: Optional[Union[int, List[int]]

        :param exclude_ids: Manga(s) ID to exclude
        :type exclude_ids: Optional[Union[int, List[int]]

        :param search: Search phrase to filter mangas by name
        :type search: Optional[str]

        :return: List of Mangas
        :rtype: List[Manga]
        """
        if not Utils.validate_enum_params({
                MangaOrder: order,
                MangaKind: kind,
                MangaStatus: status,
                MangaCensorship: censored,
                MangaList: my_list
        }):
            return []

        validated_numbers = Utils.query_numbers_validator(page=[page, 100000],
                                                          limit=[limit, 50],
                                                          score=[score, 9])

        headers: Dict[str, str] = self._client.user_agent

        if my_list:
            headers = self._client.protected_method_headers('/api/mangas')

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.mangas,
            headers=headers,
            query=Utils.create_query_dict(page=validated_numbers['page'],
                                          limit=validated_numbers['limit'],
                                          order=order,
                                          kind=kind,
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
        return Utils.validate_response_data(response,
                                            data_model=Manga,
                                            fallback=[])

    @method_endpoint('/api/mangas/:id')
    async def get(self, manga_id: int) -> Optional[Manga]:
        """
        Returns info about certain manga.

        :param manga_id: Manga ID to get info
        :type manga_id: int

        :return: Manga info
        :rtype: Optional[Manga]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.manga(manga_id))
        return Utils.validate_response_data(response, data_model=Manga)

    @method_endpoint('/api/mangas/:id/roles')
    async def creators(self, manga_id: int) -> List[Creator]:
        """
        Returns creators info of certain manga.

        :param manga_id: Manga ID to get creators
        :type manga_id: int

        :return: List of manga creators
        :rtype: List[Creator]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.manga_roles(manga_id))
        return Utils.validate_response_data(response,
                                            data_model=Creator,
                                            fallback=[])

    @method_endpoint('/api/mangas/:id/similar')
    async def similar(self, manga_id: int) -> List[Manga]:
        """
        Returns list of similar mangas for certain manga.

        :param manga_id: Manga ID to get similar mangas
        :type manga_id: int

        :return: List of similar mangas
        :rtype: List[Manga]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.similar_mangas(manga_id))
        return Utils.validate_response_data(response, data_model=Manga)

    @method_endpoint('/api/mangas/:id/related')
    async def related_content(self, manga_id: int) -> List[Relation]:
        """
        Returns list of related content of certain manga.

        :param manga_id: Manga ID to get related content
        :type manga_id: int

        :return: List of relations
        :rtype: List[Relation]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.manga_related_content(manga_id))
        return Utils.validate_response_data(response,
                                            data_model=Relation,
                                            fallback=[])

    @method_endpoint('/api/mangas/:id/franchise')
    async def franchise_tree(self, manga_id: int) -> Optional[FranchiseTree]:
        """
        Returns franchise tree of certain manga.

        :param manga_id: Manga ID to get franchise tree
        :type manga_id: int

        :return: Franchise tree of certain manga
        :rtype: Optional[FranchiseTree]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.manga_franchise_tree(manga_id))
        return Utils.validate_response_data(response, data_model=FranchiseTree)

    @method_endpoint('/api/mangas/:id/external_links')
    async def external_links(self, manga_id: int) -> List[Link]:
        """
        Returns list of external links of certain manga.

        :param manga_id: Manga ID to get external links
        :type manga_id: int

        :return: List of external links
        :rtype: List[Link]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.manga_external_links(manga_id))
        return Utils.validate_response_data(response,
                                            data_model=Link,
                                            fallback=[])

    @method_endpoint('/api/mangas/:id/topics')
    async def topics(self,
                     manga_id: int,
                     page: Optional[int] = None,
                     limit: Optional[int] = None) -> List[Topic]:
        """
        Returns list of topics of certain manga.

        :param manga_id: Manga ID to get topics
        :type manga_id: int

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :return: List of topics
        :rtype: List[Topic]
        """
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.manga_topics(manga_id),
            query=Utils.create_query_dict(page=validated_numbers['page'],
                                          limit=validated_numbers['limit']))
        return Utils.validate_response_data(response,
                                            data_model=Topic,
                                            fallback=[])
