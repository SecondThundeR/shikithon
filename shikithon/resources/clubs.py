"""Represents /api/clubs resource."""
from typing import Any, Dict, List, Optional

from ..decorators import exceptions_handler
from ..decorators import method_endpoint
from ..enums import CommentPolicy
from ..enums import ImageUploadPolicy
from ..enums import JoinPolicy
from ..enums import PagePolicy
from ..enums import RequestType
from ..enums import ResponseCode
from ..enums import TopicPolicy
from ..exceptions import ShikimoriAPIResponseError
from ..models import Anime
from ..models import Character
from ..models import Club
from ..models import ClubImage
from ..models import Manga
from ..models import Ranobe
from ..models import User
from ..utils import ExperimentalUtils
from .base_resource import BaseResource


class Clubs(BaseResource):
    """Clubs resource class.

    Used to represent /api/clubs resource.
    """

    @method_endpoint('/api/clubs')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def get_all(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      search: Optional[str] = None):
        """Returns clubs list.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param search: Search phrase to filter clubs by name
        :type search: Optional[str]

        :return: Clubs list
        :rtype: List[Club]
        """
        query_dict = ExperimentalUtils.create_query_dict(page=page,
                                                         limit=limit,
                                                         search=search)

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.clubs, query=query_dict)

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Club)

    @method_endpoint('/api/clubs/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def get(self, club_id: int):
        """Returns info about club.

        :param club_id: Club ID to get info
        :type club_id: int

        :return: Info about club
        :rtype: Optional[Club]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.club(club_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Club)

    @method_endpoint('/api/clubs/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def update(self,
                     club_id: int,
                     name: Optional[str] = None,
                     description: Optional[str] = None,
                     join_policy: Optional[JoinPolicy] = None,
                     display_images: Optional[bool] = None,
                     comment_policy: Optional[CommentPolicy] = None,
                     topic_policy: Optional[TopicPolicy] = None,
                     page_policy: Optional[PagePolicy] = None,
                     image_upload_policy: Optional[ImageUploadPolicy] = None,
                     is_censored: Optional[bool] = None,
                     anime_ids: Optional[List[int]] = None,
                     manga_ids: Optional[List[int]] = None,
                     ranobe_ids: Optional[List[int]] = None,
                     character_ids: Optional[List[int]] = None,
                     club_ids: Optional[List[int]] = None,
                     admin_ids: Optional[List[int]] = None,
                     collection_ids: Optional[List[int]] = None,
                     banned_user_ids: Optional[List[int]] = None):
        """Update info/settings about/of club.

        :param club_id: Club ID to modify/update
        :type club_id: int

        :param name: New name of club
        :type name: Optional[str]

        :param description: New description of club
        :type description: Optional[str]

        :param join_policy: New join policy of club
        :type join_policy: Optional[JoinPolicy]

        :param display_images: New display images status of club
        :type display_images: Optional[bool]

        :param comment_policy: New comment policy of club
        :type comment_policy: Optional[CommentPolicy]

        :param topic_policy: New topic policy of club
        :type topic_policy: Optional[TopicPolicy]

        :param page_policy: New page policy of club
        :type page_policy: Optional[PagePolicy]

        :param image_upload_policy: New image upload policy of club
        :type image_upload_policy: Optional[ImageUploadPolicy]

        :param is_censored: New censored status of club
        :type is_censored: Optional[bool]

        :param anime_ids: New anime ids of club
        :type anime_ids: Optional[List[int]]

        :param manga_ids: New manga ids of club
        :type manga_ids: Optional[List[int]]

        :param ranobe_ids: New ranobe ids of club
        :type ranobe_ids: Optional[List[int]]

        :param character_ids: New character ids of club
        :type character_ids: Optional[List[int]]

        :param club_ids: New club ids of club
        :type club_ids: Optional[List[int]]

        :param admin_ids: New admin ids of club
        :type admin_ids: Optional[List[int]]

        :param collection_ids: New collection ids of club
        :type collection_ids: Optional[List[int]]

        :param banned_user_ids: New banned user ids of club
        :type banned_user_ids: Optional[List[int]]

        :return: Updated club info
        :rtype: Optional[Club]
        """

        data_dict = ExperimentalUtils.create_data_dict(
            dict_name='club',
            name=name,
            join_policy=join_policy,
            description=description,
            display_images=display_images,
            comment_policy=comment_policy,
            topic_policy=topic_policy,
            page_policy=page_policy,
            image_upload_policy=image_upload_policy,
            is_censored=is_censored,
            anime_ids=anime_ids,
            manga_ids=manga_ids,
            ranobe_ids=ranobe_ids,
            character_ids=character_ids,
            club_ids=club_ids,
            admin_ids=admin_ids,
            collection_ids=collection_ids,
            banned_user_ids=banned_user_ids)

        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.club(club_id),
            data=data_dict,
            request_type=RequestType.PATCH)

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Club)

    @method_endpoint('/api/clubs/:id/animes')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def animes(self, club_id: int):
        """Returns anime list of club.

        :param club_id: Club ID to get anime list
        :type club_id: int

        :return: Club's anime list
        :rtype: List[Anime]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.club_animes(club_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Anime)

    @method_endpoint('/api/clubs/:id/mangas')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def mangas(self, club_id: int):
        """Returns manga list of club.

        :param club_id: Club ID to get manga list
        :type club_id: int

        :return: Club's manga list
        :rtype: List[Manga]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.club_mangas(club_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Manga)

    @method_endpoint('/api/clubs/:id/ranobe')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def ranobe(self, club_id: int):
        """Returns ranobe list of club.

        :param club_id: Club ID to get ranobe list
        :type club_id: int

        :return: Club's ranobe list
        :rtype: List[Ranobe]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.club_ranobe(club_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Ranobe)

    @method_endpoint('/api/clubs/:id/characters')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def characters(self, club_id: int):
        """Returns character list of club.

        :param club_id: Club ID to get character list
        :type club_id: int

        :return: Club's character list
        :rtype: List[Character]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.club_characters(club_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=Character)

    @method_endpoint('/api/clubs/:id/members')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def members(self, club_id: int):
        """Returns member list of club.

        :param club_id: Club ID to get member list
        :type club_id: int

        :return: Club's member list
        :rtype: List[User]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.club_members(club_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=User)

    @method_endpoint('/api/clubs/:id/images')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def images(self, club_id: int):
        """Returns images of club.

        :param club_id: Club ID to get images
        :type club_id: int

        :return: Club's image list
        :rtype: List[ClubImage]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.club_images(club_id))

        return ExperimentalUtils.validate_response_data(response,
                                                        data_model=ClubImage)

    @method_endpoint('/api/clubs/:id/join')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def join(self, club_id: int):
        """Joins club by ID.

        :param club_id: Club ID to join
        :type club_id: int

        :return: Status of join
        :rtype: bool
        """
        response: int = await self._client.request(
            self._client.endpoints.club_join(club_id),
            request_type=RequestType.POST)

        return ExperimentalUtils.validate_response_code(
            response, check_code=ResponseCode.SUCCESS)

    @method_endpoint('/api/clubs/:id/leave')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def leave(self, club_id: int):
        """Leaves club by ID.

        :param club_id: Club ID to leave
        :type club_id: int

        :return: Status of leave
        :rtype: bool
        """
        response: int = await self._client.request(
            self._client.endpoints.club_leave(club_id),
            request_type=RequestType.POST)

        return ExperimentalUtils.validate_response_code(
            response, check_code=ResponseCode.SUCCESS)
