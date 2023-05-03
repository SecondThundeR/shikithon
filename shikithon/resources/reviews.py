"""Represents `/api/reviews` resource."""
from typing import Any, Dict, Optional, cast

from loguru import logger

from ..decorators import exceptions_handler, method_endpoint
from ..enums import RequestType, ReviewOpinion
from ..exceptions import ShikimoriAPIResponseError
from ..models import Review
from ..utils import Utils
from .base_resource import BaseResource

DICT_NAME = 'review'


class Reviews(BaseResource):
    """Reviews resource class.

    Used to represent `/api/reviews` resource
    """

    @method_endpoint('/api/reviews')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def create_anime(self, anime_id: int, body: str,
                           opinion: ReviewOpinion):
        """Creates review for anime.

        :param anime_id: ID of anime to create review for
        :type anime_id: int

        :param body: Body of review
        :type body: str

        :param opinion: Opinion of the review
        :type opinion: ReviewOpinion

        :return: Created review info
        :rtype: Optional[Review]
        """
        data_dict = Utils.create_data_dict(dict_name=DICT_NAME,
                                           anime_id=anime_id,
                                           body=body,
                                           opinion=opinion)

        response = await self._client.request(self._client.endpoints.reviews,
                                              data=data_dict,
                                              request_type=RequestType.POST)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Review)

    # @method_endpoint('/api/reviews')
    # @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    # async def create_manga(self,
    #                        manga_id: int,
    #                        body: str,
    #                        opinion: ReviewOpinion
    # ):
    #     """Creates review for manga."""
    # ! Currently there is no way to use API for creating review for manga
    # ? Unfortunately, trying to send request with "manga_id"
    # ? and without "anime_id", returns error, that "anime_id" is missing
    # * So this method is comment out for later addition, when API will be
    # * capable of creating review for manga, tho source code has lines for that
    # * See reviews_controller.rb in Shikimori repository

    @method_endpoint('/api/reviews/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=None)
    async def update(self,
                     review_id: int,
                     body: Optional[str] = None,
                     opinion: Optional[ReviewOpinion] = None,
                     is_written_before_release: Optional[bool] = None):
        """Updates review.

        :param review_id: ID of review to update
        :type review_id: int

        :param body: New body of review
        :type body: Optional[str]

        :param opinion: New opinion of review
        :type opinion: Optional[ReviewOpinion]

        :param is_written_before_release:
        Status of review publish, before title release
        :type is_written_before_release: Optional[bool]

        :return: Updated review info
        or None if review cannot be updated
        :rtype: Optional[Review]
        """
        data_dict = Utils.create_data_dict(
            dict_name=DICT_NAME,
            body=body,
            opinion=opinion,
            is_written_before_release=is_written_before_release)

        response = await self._client.request(
            self._client.endpoints.review(review_id),
            data=data_dict,
            request_type=RequestType.PATCH)

        return Utils.validate_response_data(cast(Dict[str, Any], response),
                                            data_model=Review)

    @method_endpoint('/api/reviews/:id')
    @exceptions_handler(ShikimoriAPIResponseError, fallback=False)
    async def delete(self, review_id: int):
        """Deletes review.

        :param review_id: ID of review to delete
        :type review_id: int

        :return: Status of review deletion
        :rtype: bool
        """
        response = await self._client.request(
            self._client.endpoints.review(review_id),
            request_type=RequestType.DELETE)

        logger.info(response)

        return True
