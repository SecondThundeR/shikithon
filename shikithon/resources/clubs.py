"""Represents /api/clubs resource."""
from typing import Any, Dict, List, Optional, Union

from ..decorators import method_endpoint, protected_method
from ..enums import (
    CommentPolicy,
    ImageUploadPolicy,
    JoinPolicy,
    PagePolicy,
    RequestType,
    TopicPolicy,
)
from ..models import Anime, Character, Club, ClubImage, Manga, Ranobe, User
from ..utils import Utils
from .base_resource import BaseResource


class Clubs(BaseResource):
    """Clubs resource class.

    Used to represent /api/clubs resource.
    """

    @method_endpoint('/api/clubs')
    async def get_all(self,
                      page: Optional[int] = None,
                      limit: Optional[int] = None,
                      search: Optional[str] = None) -> Optional[List[Club]]:
        """
        Returns clubs list.

        :param page: Number of page
        :type page: Optional[int]

        :param limit: Number of results limit
        :type limit: Optional[int]

        :param search: Search phrase to filter clubs by name
        :type search: Optional[str]

        :return: Clubs list
        :rtype: Optional[List[Club]]
        """
        validated_numbers = Utils.query_numbers_validator(
            page=[page, 100000],
            limit=[limit, 30],
        )

        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.clubs,
            query=Utils.generate_query_dict(page=validated_numbers['page'],
                                            limit=validated_numbers['limit'],
                                            search=search))
        return Utils.validate_return_data(response, data_model=Club)

    @method_endpoint('/api/clubs/:id')
    async def get(self, club_id: int) -> Optional[Club]:
        """
        Returns info about club.

        :param club_id: Club ID to get info
        :type club_id: int

        :return: Info about club
        :rtype: Optional[Club]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.club(club_id))
        return Utils.validate_return_data(response, data_model=Club)

    @method_endpoint('/api/clubs/:id')
    @protected_method('_client', 'clubs')
    async def update(
            self,
            club_id: int,
            name: Optional[str] = None,
            join_policy: Optional[str] = None,
            description: Optional[str] = None,
            display_images: Optional[bool] = None,
            comment_policy: Optional[str] = None,
            topic_policy: Optional[str] = None,
            page_policy: Optional[str] = None,
            image_upload_policy: Optional[str] = None,
            is_censored: Optional[bool] = None,
            anime_ids: Optional[List[int]] = None,
            manga_ids: Optional[List[int]] = None,
            ranobe_ids: Optional[List[int]] = None,
            character_ids: Optional[List[int]] = None,
            club_ids: Optional[List[int]] = None,
            admin_ids: Optional[List[int]] = None,
            collection_ids: Optional[List[int]] = None,
            banned_user_ids: Optional[List[int]] = None) -> Optional[Club]:
        """
        Update info/settings about/of club.

        :param club_id: Club ID to modify/update
        :type club_id: int

        :param name: New name of club
        :type name: Optional[str]

        :param description: New description of club
        :type description: Optional[str]

        :param display_images: New display images status of club
        :type display_images: Optional[bool]

        :param is_censored: New censored status of club
        :type is_censored: Optional[bool]

        :param join_policy: New join policy of club
        :type join_policy: Optional[str]

        :param comment_policy: New comment policy of club
        :type comment_policy: Optional[str]

        :param topic_policy: New topic policy of club
        :type topic_policy: Optional[str]

        :param page_policy: New page policy of club
        :type page_policy: Optional[str]

        :param image_upload_policy: New image upload policy of club
        :type image_upload_policy: Optional[str]

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
        if not Utils.validate_enum_params({
                JoinPolicy: join_policy,
                CommentPolicy: comment_policy,
                TopicPolicy: topic_policy,
                PagePolicy: page_policy,
                ImageUploadPolicy: image_upload_policy
        }):
            return None

        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.club(club_id),
            headers=self._client.authorization_header,
            data=Utils.generate_data_dict(
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
                banned_user_ids=banned_user_ids),
            request_type=RequestType.PATCH)
        return Utils.validate_return_data(response, data_model=Club)

    @method_endpoint('/api/clubs/:id/animes')
    async def animes(self, club_id: int) -> Optional[List[Anime]]:
        """
        Returns anime list of club.

        :param club_id: Club ID to get anime list
        :type club_id: int

        :return: Club anime list
        :rtype: Optional[List[Anime]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.club_animes(club_id))
        return Utils.validate_return_data(response, data_model=Anime)

    @method_endpoint('/api/clubs/:id/mangas')
    async def mangas(self, club_id: int) -> Optional[List[Manga]]:
        """
        Returns manga list of club.

        :param club_id: Club ID to get manga list
        :type club_id: int

        :return: Club manga list
        :rtype: Optional[List[Manga]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.club_mangas(club_id))
        return Utils.validate_return_data(response, data_model=Manga)

    @method_endpoint('/api/clubs/:id/ranobe')
    async def ranobe(self, club_id: int) -> Optional[List[Ranobe]]:
        """
        Returns ranobe list of club.

        :param club_id: Club ID to get ranobe list
        :type club_id: int

        :return: Club ranobe list
        :rtype: Optional[List[Ranobe]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.club_ranobe(club_id))
        return Utils.validate_return_data(response, data_model=Ranobe)

    @method_endpoint('/api/clubs/:id/characters')
    async def characters(self, club_id: int) -> Optional[List[Character]]:
        """
        Returns character list of club.

        :param club_id: Club ID to get character list
        :type club_id: int

        :return: Club character list
        :rtype: Optional[List[Character]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.club_characters(club_id))
        return Utils.validate_return_data(response, data_model=Character)

    @method_endpoint('/api/clubs/:id/members')
    async def members(self, club_id: int) -> Optional[List[User]]:
        """
        Returns member list of club.

        :param club_id: Club ID to get member list
        :type club_id: int

        :return: Club member list
        :rtype: Optional[List[User]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.club_members(club_id))
        return Utils.validate_return_data(response, data_model=User)

    @method_endpoint('/api/clubs/:id/images')
    async def images(self, club_id: int) -> Optional[List[ClubImage]]:
        """
        Returns images of club.

        :param club_id: Club ID to get images
        :type club_id: int

        :return: Club's images
        :rtype: Optional[List[ClubImage]]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.club_images(club_id))
        return Utils.validate_return_data(response, data_model=ClubImage)

    @method_endpoint('/api/clubs/:id/join')
    @protected_method('_client', 'clubs')
    async def join(self, club_id: int):
        """
        Joins club by ID.

        :param club_id: Club ID to join
        :type club_id: int

        :return: Status of join
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.club_join(club_id),
            headers=self._client.authorization_header,
            request_type=RequestType.POST)
        return Utils.validate_return_data(response)

    @method_endpoint('/api/clubs/:id/leave')
    @protected_method('_client', 'clubs')
    async def leave(self, club_id: int) -> bool:
        """
        Leaves club by ID.

        :param club_id: Club ID to leave
        :type club_id: int

        :return: Status of leave
        :rtype: bool
        """
        response: Union[Dict[str, Any], int] = await self._client.request(
            self._client.endpoints.club_leave(club_id),
            headers=self._client.authorization_header,
            request_type=RequestType.POST)
        return Utils.validate_return_data(response)
