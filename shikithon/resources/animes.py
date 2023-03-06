"""Represents /api/animes and /api/animes/:anime_id/videos resource."""
from typing import List, Optional, Union

from ..decorators import exceptions_handler
from ..decorators import method_endpoint
from ..enums import AnimeCensorship
from ..enums import AnimeDuration
from ..enums import AnimeKind
from ..enums import AnimeList
from ..enums import AnimeOrder
from ..enums import AnimeRating
from ..enums import AnimeStatus
from ..enums import AnimeTopicKind
from ..enums import RequestType
from ..enums import VideoKind
from ..enums.response import ResponseCode
from ..exceptions import ShikimoriAPIResponseError
from ..models import Anime
from ..models import Creator
from ..models import FranchiseTree
from ..models import Link
from ..models import Relation
from ..models import Screenshot
from ..models import Topic
from ..models import Video
from ..utils import ExperimentalUtils
from .base_resource import BaseResource


class Animes(BaseResource):
    """Anime resource class.

    Used to represent /api/animes and
    /api/animes/:anime_id/videos resource.
    """

    @method_endpoint('/api/animes')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      order: Optional[AnimeOrder] = None,
                      kind: Optional[Union[AnimeKind, List[AnimeKind]]] = None,
                      status: Optional[Union[AnimeStatus,
                                             List[AnimeStatus]]] = None,
                      season: Optional[Union[str, List[str]]] = None,
                      score: Optional[int] = None,
                      duration: Optional[Union[AnimeDuration,
                                               List[AnimeDuration]]] = None,
                      rating: Optional[Union[AnimeRating,
                                             List[AnimeRating]]] = None,
                      genre: Optional[Union[int, List[int]]] = None,
                      studio: Optional[Union[int, List[int]]] = None,
                      franchise: Optional[Union[int, List[int]]] = None,
                      censored: Optional[AnimeCensorship] = None,
                      my_list: Optional[Union[AnimeList,
                                              List[AnimeList]]] = None,
                      ids: Optional[Union[int, List[int]]] = None,
                      exclude_ids: Optional[Union[int, List[int]]] = None,
                      search: Optional[str] = None) -> List[Anime]:
        """Returns list of anime.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param order: Type of order in list
        :type order: Optional[AnimeOrder]

        :param kind: Type(s) of anime topics
        :type kind: Optional[Union[AnimeKind, List[AnimeKind]]]

        :param status: Type(s) of anime status
        :type status: Optional[Union[AnimeStatus, List[AnimeStatus]]]

        :param season: Name(s) of anime seasons
        :type season: Optional[Union[str, List[str]]]

        :param score: Minimal anime score
        :type score: Optional[int]

        :param duration: Duration size(s) of anime
        :type duration: Optional[Union[AnimeDuration, List[AnimeDuration]]]

        :param rating: Type of anime rating(s)
        :type rating: Optional[Union[AnimeRating, List[AnimeRating]]]

        :param genre: Genre(s) ID
        :type genre: Optional[Union[int, List[int]]]

        :param studio: Studio(s) ID
        :type studio: Optional[Union[int, List[int]]]

        :param franchise: Franchise(s) ID
        :type franchise: Optional[Union[int, List[int]]]

        :param censored: Type of anime censorship
        :type censored: Optional[AnimeCensorship]

        :param my_list: Status(-es) of anime in current user list.
            If app is in restricted mode,
            this parameter won't affect on response.
        :type my_list: Optional[Union[AnimeList, List[AnimeList]]]

        :param ids: Anime(s) ID to include
        :type ids: Optional[Union[int, List[int]]]

        :param exclude_ids: Anime(s) ID to exclude
        :type exclude_ids: Optional[Union[int, List[int]]]

        :param search: Search phrase to filter animes by name
        :type search: Optional[str]

        :return: List of anime
        :rtype: List[Anime]
        """
        if not ExperimentalUtils.is_enum_passed(
                order,
                kind,
                status,
                duration,
                rating,
                censored,
                my_list,
        ):
            return []

        validated_numbers = ExperimentalUtils.validate_query_numbers(
            page=(page, 100000), limit=(limit, 50), score=(score, 9))

        response = await self._client.request(
            self._client.endpoints.animes,
            query=ExperimentalUtils.create_query_dict(
                page=validated_numbers['page'],
                limit=validated_numbers['limit'],
                order=order,
                kind=kind,
                status=status,
                season=season,
                score=validated_numbers['score'],
                duration=duration,
                rating=rating,
                genre=genre,
                studio=studio,
                franchise=franchise,
                censored=censored,
                mylist=my_list,
                ids=ids,
                exclude_ids=exclude_ids,
                search=search))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Anime)

    @method_endpoint('/api/animes/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def get(self, anime_id: int) -> Optional[Anime]:
        """Returns info about certain anime.

        :param anime_id: Anime ID to get info
        :type anime_id: int

        :return: Anime info
        :rtype: Optional[Anime]
        """
        response = await self._client.request(
            self._client.endpoints.anime(anime_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Anime)

    @method_endpoint('/api/animes/:id/roles')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def creators(self, anime_id: int) -> List[Creator]:
        """Returns creators info of certain anime.

        :param anime_id: Anime ID to get creators
        :type anime_id: int

        :return: List of anime creators
        :rtype: List[Creator]
        """
        response = await self._client.request(
            self._client.endpoints.anime_roles(anime_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Creator)

    @method_endpoint('/api/animes/:id/similar')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def similar(self, anime_id: int) -> List[Anime]:
        """Returns list of similar animes for certain anime.

        :param anime_id: Anime ID to get similar animes
        :type anime_id: int

        :return: List of similar animes
        :rtype: List[Anime]
        """
        response = await self._client.request(
            self._client.endpoints.similar_animes(anime_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Anime)

    @method_endpoint('/api/animes/:id/related')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def related_content(self, anime_id: int) -> List[Relation]:
        """Returns list of related content of certain anime.

        :param anime_id: Anime ID to get related content
        :type anime_id: int

        :return: List of relations
        :rtype: List[Relation]
        """
        response = await self._client.request(
            self._client.endpoints.anime_related_content(anime_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Relation)

    @method_endpoint('/api/animes/:id/screenshots')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def screenshots(self, anime_id: int) -> List[Screenshot]:
        """Returns list of screenshot links of certain anime.

        :param anime_id: Anime ID to get screenshot links
        :type anime_id: int

        :return: List of screenshot links
        :rtype: List[Screenshot]
        """
        response = await self._client.request(
            self._client.endpoints.anime_screenshots(anime_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Screenshot)

    @method_endpoint('/api/animes/:id/franchise')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def franchise_tree(self, anime_id: int) -> Optional[FranchiseTree]:
        """Returns franchise tree of certain anime.

        :param anime_id: Anime ID to get franchise tree
        :type anime_id: int

        :return: Franchise tree of certain anime
        :rtype: Optional[FranchiseTree]
        """
        response = await self._client.request(
            self._client.endpoints.anime_franchise_tree(anime_id))

        return ExperimentalUtils.validate_response_data(
            response, data_model=FranchiseTree)

    @method_endpoint('/api/animes/:id/external_links')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def external_links(self, anime_id: int) -> List[Link]:
        """Returns list of external links of certain anime.

        :param anime_id: Anime ID to get external links
        :type anime_id: int

        :return: List of external links
        :rtype: List[Link]
        """
        response = await self._client.request(
            self._client.endpoints.anime_external_links(anime_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Link)

    @method_endpoint('/api/animes/:id/topics')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def topics(self,
                     anime_id: int,
                     page: Optional[int] = None,
                     limit: Optional[int] = None,
                     kind: Optional[AnimeTopicKind] = None,
                     episode: Optional[int] = None) -> List[Topic]:
        """Returns list of topics of certain anime.

        :param anime_id: Anime ID to get topics
        :type anime_id: int

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param kind: Kind of anime
        :type kind: Optional[AnimeTopicKind]

        :param episode: Number of anime episode
        :type episode: Optional[int]

        :return: List of topics
        :rtype: List[Topic]
        """
        if not ExperimentalUtils.is_enum_passed(kind):
            return []

        validated_numbers = ExperimentalUtils.validate_query_numbers(
            page=(page, 100000), limit=(limit, 30))

        response = await self._client.request(
            self._client.endpoints.anime_topics(anime_id),
            query=ExperimentalUtils.create_query_dict(
                page=validated_numbers['page'],
                limit=validated_numbers['limit'],
                kind=kind,
                episode=episode))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Topic)

    @method_endpoint('/api/animes/:anime_id/videos')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def videos(self, anime_id: int) -> List[Video]:
        """Returns list of anime videos.

        :param anime_id: Anime ID to get videos
        :type anime_id: int

        :return: Anime videos list
        :rtype: List[Video]
        """
        response = await self._client.request(
            self._client.endpoints.anime_videos(anime_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Video)

    @method_endpoint('/api/animes/:anime_id/videos')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def create_video(self, anime_id: int, kind: VideoKind, name: str,
                           url: str) -> Optional[Video]:
        """Creates anime video.

        :param anime_id: Anime ID to create video
        :type anime_id: int

        :param kind: Kind of video
        :type kind: VideoKind

        :param name: Name of video
        :type name: str

        :param url: URL of video
        :type url: str

        :return: Created video info
        :rtype: Optional[Video]
        """
        if not ExperimentalUtils.is_enum_passed(kind):
            return None

        response = await self._client.request(
            self._client.endpoints.anime_videos(anime_id),
            data=ExperimentalUtils.create_data_dict(dict_name='video',
                                                    kind=kind,
                                                    name=name,
                                                    url=url),
            request_type=RequestType.POST)

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Video)

    @method_endpoint('/api/animes/:anime_id/videos/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def delete_video(self, anime_id: int, video_id: int) -> bool:
        """Deletes anime video.

        :param anime_id: Anime ID to delete video
        :type anime_id: int

        :param video_id: Video ID to delete
        :type video_id: str

        :return: Status of video deletion
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.anime_video(anime_id, video_id),
            request_type=RequestType.DELETE)

        return ExperimentalUtils.validate_response_code(response,
                                                        ResponseCode.SUCCESS)
