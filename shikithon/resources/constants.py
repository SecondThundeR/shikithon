"""Represents /api/constants resource."""
from typing import Any, Dict, List, Optional

from ..decorators import method_endpoint
from ..models.constants import AnimeConstants
from ..models.constants import ClubConstants
from ..models.constants import MangaConstants
from ..models.constants import SmileyConstants
from ..models.constants import UserRateConstants
from ..utils import Utils
from .base_resource import BaseResource


class Constants(BaseResource):
    """Constants resource class.

    Used to represent /api/constants resource.
    """

    @method_endpoint('/api/constants/anime')
    async def anime(self) -> Optional[AnimeConstants]:
        """
        Returns anime constants values.

        :return: Anime constants values
        :rtype: Optional[AnimeConstants]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.anime_constants)
        return Utils.validate_response_data(response, data_model=AnimeConstants)

    @method_endpoint('/api/constants/manga')
    async def manga(self) -> Optional[MangaConstants]:
        """
        Returns manga constants values.

        :return: Manga constants values
        :rtype: Optional[MangaConstants]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.manga_constants)
        return Utils.validate_response_data(response, data_model=MangaConstants)

    @method_endpoint('/api/constants/user_rate')
    async def user_rate(self) -> Optional[UserRateConstants]:
        """
        Returns user rate constants values.

        :return: User rate constants values
        :rtype: Optional[UserRateConstants]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.user_rate_constants)
        return Utils.validate_response_data(response,
                                            data_model=UserRateConstants)

    @method_endpoint('/api/constants/club')
    async def club(self) -> Optional[ClubConstants]:
        """
        Returns club constants values.

        :return: Club constants values
        :rtype: Optional[ClubConstants]
        """
        response: Dict[str, Any] = await self._client.request(
            self._client.endpoints.club_constants)
        return Utils.validate_response_data(response, data_model=ClubConstants)

    @method_endpoint('/api/constants/smileys')
    async def smileys(self) -> List[SmileyConstants]:
        """
        Returns list of smileys constants values.

        :return: List of smileys constants values
        :rtype: List[SmileyConstants]
        """
        response: List[Dict[str, Any]] = await self._client.request(
            self._client.endpoints.smileys_constants)
        return Utils.validate_response_data(response,
                                            data_model=SmileyConstants)
