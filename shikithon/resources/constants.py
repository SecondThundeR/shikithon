"""Represents `/api/constants` resource."""
from typing import Any, Dict, List, cast

from ..decorators import exceptions_handler, method_endpoint
from ..exceptions import ShikimoriAPIResponseError
from ..models import (AnimeConstants, ClubConstants, MangaConstants,
                      SmileyConstant, UserRateConstants)
from ..utils import Utils
from .base_resource import BaseResource


class Constants(BaseResource):
    """Constants resource class.

    Used to represent `/api/constants` resource
    """

    @method_endpoint('/api/constants/anime')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def anime(self):
        """Returns anime constants values.

        :return: Anime constants values
        :rtype: Optional[AnimeConstants]
        """
        response = await self._client.request(
            self._client.endpoints.anime_constants)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=AnimeConstants)

    @method_endpoint('/api/constants/manga')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def manga(self):
        """Returns manga constants values.

        :return: Manga constants values
        :rtype: Optional[MangaConstants]
        """
        response = await self._client.request(
            self._client.endpoints.manga_constants)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=MangaConstants)

    @method_endpoint('/api/constants/user_rate')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def user_rate(self):
        """Returns user rate constants values.

        :return: User rate constants values
        :rtype: Optional[UserRateConstants]
        """
        response = await self._client.request(
            self._client.endpoints.user_rate_constants)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=UserRateConstants)

    @method_endpoint('/api/constants/club')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def club(self):
        """Returns club constants values.

        :return: Club constants values
        :rtype: Optional[ClubConstants]
        """
        response = await self._client.request(
            self._client.endpoints.club_constants)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=ClubConstants)

    @method_endpoint('/api/constants/smileys')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=[])
    async def smileys(self):
        """Returns list of smiley constant values.

        :return: List of smiley constant values
        :rtype: List[SmileyConstant]
        """
        response = await self._client.request(
            self._client.endpoints.smileys_constants)

        return Utils.validate_response_data(cast(List[Dict[str, Any]],
                                                 response),
                                            data_model=SmileyConstant)
