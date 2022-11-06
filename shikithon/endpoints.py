"""Shikimori API Endpoints.

This module contains Endpoints class, which
contains all endpoints for API and can form
customized endpoints via input parameters.
"""
from typing import Union

from .utils import Utils


class Endpoints:
    """
    Contains endpoints for Shikimori API.

    This class allows to form customized endpoint depending
    on input parameters.
    """

    def __init__(self, base_url: str, base_url_v2: str, oauth_url: str):
        """
        Initializing URLs for Shikimori's API/OAuth.

        This constructor also has base_url_v2, which is
        modified base_url that routes to new API methods

        :param base_url: URL for Shikimori API
        :type base_url: str

        :param base_url_v2: URL for Shikimori API (v.2)
        :type base_url_v2: str

        :param oauth_url: URL for Shikimori OAuth
        :type oauth_url: str
        """
        self._base_url = base_url
        self._base_url_v2 = base_url_v2
        self._oauth_url = oauth_url

    @property
    def base_url(self) -> str:
        """
        Getter for base_url

        :return: Link for Shikimori API
        :rtype: str
        """
        return self._base_url

    @base_url.setter
    def base_url(self, base_url: str):
        """
        Setter for base_url

        :param base_url: Link for Shikimori API
        :type base_url: str
        """
        self._base_url = base_url

    @property
    def base_url_v2(self) -> str:
        """
        Getter for base_url_v2

        :return: Link for Shikimori API (v.2)
        :rtype: str
        """
        return self._base_url_v2

    @base_url_v2.setter
    def base_url_v2(self, base_url_v2: str):
        """
        Setter for base_url_v2

        :param base_url_v2: Link for Shikimori API (v.2)
        :type base_url_v2: str
        """
        self._base_url_v2 = base_url_v2

    @property
    def oauth_url(self) -> str:
        """
        Getter for oauth_url

        :return: Link for Shikimori OAuth
        :rtype: str
        """
        return self._oauth_url

    @oauth_url.setter
    def oauth_url(self, oauth_url: str):
        """
        Setter for oauth_url

        :param oauth_url: Link for Shikimori OAuth
        :type oauth_url: str
        """
        self._oauth_url = oauth_url

    @property
    def oauth_token(self) -> str:
        """
        Returns endpoint for OAuth token

        :return: Link for Shikimori OAuth token endpoint
        :rtype: str
        """
        return f'{self.oauth_url}/token'

    @property
    def oauth_authorize(self) -> str:
        """
        Returns endpoint for OAuth authorization

        :return: Link for Shikimori OAuth authorization endpoint
        :rtype: str
        """
        return f'{self.oauth_url}/authorize'

    def authorization_link(self, client_id: str, redirect_uri: str,
                           scopes: str) -> str:
        """
        Returns link for getting authorization code.

        **Note:** Since you need to pass a captcha to log in to Shikimori,
        there is no automatic authorization method.
        So, the user needs to pass the authorization code manually

        :param client_id: Client ID of an OAuth App
        :type client_id: str

        :param redirect_uri: Redirect URI of an OAuth App
        :type redirect_uri: str

        :param scopes: Scopes of an OAuth App
        :type scopes: str

        :return: Link for getting authorization code
        :rtype: str
        """
        query_str = Utils.convert_to_query_string({
            'client_id': client_id,
            'redirect_uri': redirect_uri,
            'response_type': 'code',
            'scope': scopes
        })
        return f'{self.oauth_authorize}{query_str}'

    @property
    def abuse_requests(self) -> str:
        """
        Returns endpoint for abuse requests methods.

        :return: Abuse request main endpoint link
        :rtype: str
        """
        return f'{self.base_url_v2}/abuse_requests'

    @property
    def abuse_offtopic(self) -> str:
        """
        Returns endpoint for marking comment as offtopic.

        :return: Abuse offtopic endpoint link
        :rtype: str
        """
        return f'{self.abuse_requests}/offtopic'

    @property
    def abuse_review(self) -> str:
        """
        Returns endpoint for convering comment to review.

        :return: Abuse review endpoint link
        :rtype: str
        """
        return f'{self.abuse_requests}/review'

    @property
    def abuse_violation(self) -> str:
        """
        Returns endpoint for creating request about violation of site rules.

        **Note:** In Shikimori API docs, this endpoint also named as
        '/api/v2/abuse_requests/**abuse**'

        :return: Abuse violation endpoint link
        :rtype: str
        """
        return f'{self.abuse_requests}/abuse'

    @property
    def abuse_spoiler(self) -> str:
        """
        Returns endpoint for creating request about spoiler in content.

        :return: Abuse spoiler endpoint link
        :rtype: str
        """
        return f'{self.abuse_requests}/spoiler'

    @property
    def achievements(self) -> str:
        """
        Returns endpoint of user achievements.

        :return: Achievements endpoint link
        :rtype: str
        """
        return f'{self.base_url}/achievements'

    @property
    def animes(self) -> str:
        """
        Returns endpoint of the animes list.

        :return: Animes list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/animes'

    def anime(self, anime_id: int) -> str:
        """
        Returns endpoint of a specific anime.

        :param anime_id: Anime ID for endpoint
        :type anime_id: int

        :return: Anime endpoint link
        :rtype: str
        """
        return f'{self.animes}/{anime_id}'

    def anime_roles(self, anime_id: int) -> str:
        """
        Returns endpoint of a list of roles of a specific anime.

        :param anime_id: Anime ID for endpoint
        :type anime_id: int

        :return: Anime roles endpoint link
        :rtype: str
        """
        return f'{self.anime(anime_id)}/roles'

    def similar_animes(self, anime_id: int) -> str:
        """
        Returns endpoint of a list of similar anime of a certain anime.

        :param anime_id: Anime ID for endpoint
        :type anime_id: int

        :return: Similar animes endpoint link
        :rtype: str
        """
        return f'{self.anime(anime_id)}/similar'

    def anime_related_content(self, anime_id: int) -> str:
        """
        Returns endpoint of a list of similar anime of a certain anime.

        :param anime_id: Anime ID for endpoint
        :type anime_id: int

        :return: Anime related content endpoint link
        :rtype: str
        """
        return f'{self.anime(anime_id)}/related'

    def anime_screenshots(self, anime_id: int) -> str:
        """
        Returns endpoint of screenshots of a specific anime.

        :param anime_id: Anime ID for endpoint
        :type anime_id: int

        :return: Anime screenshots endpoint link
        :rtype: str
        """
        return f'{self.anime(anime_id)}/screenshots'

    def anime_franchise_tree(self, anime_id: int) -> str:
        """
        Returns endpoint of franchise tree of a certain anime.

        :param anime_id: Anime ID for endpoint
        :type anime_id: int

        :return: Anime franchise tree endpoint link
        :rtype: str
        """
        return f'{self.anime(anime_id)}/franchise'

    def anime_external_links(self, anime_id: int) -> str:
        """
        Returns endpoint of a list of external links of a certain anime.

        :param anime_id: Anime ID for endpoint
        :type anime_id: int

        :return: Anime external links endpoint link
        :rtype: str
        """
        return f'{self.anime(anime_id)}/external_links'

    def anime_topics(self, anime_id: int) -> str:
        """
        Returns endpoint of a list of topics of a certain anime.

        :param anime_id: Anime ID for endpoint
        :type anime_id: int

        :return: Anime topics endpoint link
        :rtype: str
        """
        return f'{self.anime(anime_id)}/topics'

    def anime_videos(self, anime_id: int) -> str:
        """
        Returns endpoint of the anime's videos list.

        This endpoint also used for creating videos
        for anime entity.

        :param anime_id: Anime ID for endpoint
        :type anime_id: int

        :return: Anime's videos list endpoint link
        :rtype: str
        """
        return f'{self.anime(anime_id)}/videos'

    def anime_video(self, anime_id: int, video_id: int) -> str:
        """
        Returns endpoint for destroying anime's video.

        :param anime_id: Anime ID for endpoint
        :type anime_id: int

        :param video_id: Video ID for endpoint
        :type video_id: int

        :return: Anime's video destroy endpoint link
        :rtype: str
        """
        return f'{self.anime_videos(anime_id)}/{video_id}'

    @property
    def appears(self) -> str:
        """
        Returns endpoint for marking comments/topics as read.

        :return: Appears endpoint link
        :rtype: str
        """
        return f'{self.base_url}/appears'

    @property
    def bans_list(self) -> str:
        """
        Returns endpoint of the bans list.

        :return: Bans list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/bans'

    @property
    def calendar(self) -> str:
        """
        Returns endpoint for events calendar.

        :return: Calendar endpoint link
        :rtype: str
        """
        return f'{self.base_url}/calendar'

    def character(self, character_id: int) -> str:
        """
        Returns endpoint for a certain character.

        :param character_id: Character ID for endpoint
        :type character_id: int

        :return: Character endpoint link
        :rtype: str
        """
        return f'{self.base_url}/characters/{character_id}'

    @property
    def character_search(self) -> str:
        """
        Returns endpoint for characters search.

        :return: Characters search endpoint link
        :rtype: str
        """
        return f'{self.base_url}/characters/search'

    @property
    def clubs(self) -> str:
        """
        Returns endpoint of the clubs list.

        :return: Clubs list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/clubs'

    def club(self, club_id: int) -> str:
        """
        Returns endpoint of a certain club.

        :param club_id: Club ID for endpoint
        :type club_id: int

        :return: Club endpoint link
        :rtype: str
        """
        return f'{self.clubs}/{club_id}'

    def club_animes(self, club_id: int) -> str:
        """
        Returns endpoint of a list of animes of a certain club.

        :param club_id: Club ID for endpoint
        :type club_id: int

        :return: Club animes endpoint link
        :rtype: str
        """
        return f'{self.club(club_id)}/animes'

    def club_mangas(self, club_id: int) -> str:
        """
        Returns endpoint of a list of mangas of a certain club.

        :param club_id: Club ID for endpoint
        :type club_id: int

        :return: Club mangas endpoint link
        :rtype: str
        """
        return f'{self.club(club_id)}/mangas'

    def club_ranobe(self, club_id: int) -> str:
        """
        Returns endpoint of a list of ranobe of a certain club.

        :param club_id: Club ID for endpoint
        :type club_id: int

        :return: Club ranobe endpoint link
        :rtype: str
        """
        return f'{self.club(club_id)}/ranobe'

    def club_characters(self, club_id: int) -> str:
        """
        Returns endpoint of a list of characters of a certain club.

        :param club_id: Club ID for endpoint
        :type club_id: int

        :return: Club characters endpoint link
        :rtype: str
        """
        return f'{self.club(club_id)}/characters'

    def club_members(self, club_id: int) -> str:
        """
        Returns endpoint of a list of members of a certain club.

        :param club_id: Club ID for endpoint
        :type club_id: int

        :return: Club members endpoint link
        :rtype: str
        """
        return f'{self.club(club_id)}/members'

    def club_images(self, club_id: int) -> str:
        """
        Returns endpoint of a list of images of a certain club.

        :param club_id: Club ID for endpoint
        :type club_id: int

        :return: Club images endpoint link
        :rtype: str
        """
        return f'{self.club(club_id)}/images'

    def club_join(self, club_id: int) -> str:
        """
        Returns endpoint for joining the certain club.

        :param club_id: Club ID for endpoint
        :type club_id: int

        :return: Club join endpoint link
        :rtype: str
        """
        return f'{self.club(club_id)}/join'

    def club_leave(self, club_id: int) -> str:
        """
        Returns endpoint for leaving the certain club.

        :param club_id: Club ID for endpoint
        :type club_id: int

        :return: Club leave endpoint link
        :rtype: str
        """
        return f'{self.club(club_id)}/leave'

    @property
    def comments(self) -> str:
        """
        Returns endpoint of the comments list.

        :return: Comments list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/comments'

    def comment(self, comment_id: int) -> str:
        """
        Returns endpoint of a certain comment.

        :param comment_id: Comment ID for endpoint
        :type comment_id: int

        :return: Comment endpoint link
        :rtype: str
        """
        return f'{self.comments}/{comment_id}'

    @property
    def constants(self) -> str:
        """
        Returns endpoint of the certain API constants.

        :return: API constants endpoint link
        :rtype: str
        """
        return f'{self.base_url}/constants'

    @property
    def anime_constants(self) -> str:
        """
        Returns endpoint of the anime constants.

        :return: Anime constants endpoint link
        :rtype: str
        """
        return f'{self.constants}/anime'

    @property
    def manga_constants(self) -> str:
        """
        Returns endpoint of the manga constants.

        :return: Manga constants endpoint link
        :rtype: str
        """
        return f'{self.constants}/manga'

    @property
    def user_rate_constants(self) -> str:
        """
        Returns endpoint of the user rate constants.

        :return: User rate constants endpoint link
        :rtype: str
        """
        return f'{self.constants}/user_rate'

    @property
    def club_constants(self) -> str:
        """
        Returns endpoint of the club constants.

        :return: Club constants endpoint link
        :rtype: str
        """
        return f'{self.constants}/club'

    @property
    def smileys_constants(self) -> str:
        """
        Returns endpoint of the smileys constants.

        :return: Smileys constants endpoint link
        :rtype: str
        """
        return f'{self.constants}/smileys'

    @property
    def dialogs(self) -> str:
        """
        Returns endpoint of the dialogs list.

        :return: Dialogs list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/dialogs'

    def dialog(self, dialog_id: Union[int, str]) -> str:
        """
        Returns endpoint of a certain dialog with user.

        :param dialog_id: User ID/Nickname for endpoint
        :type dialog_id: Union[int, str]

        :return: Dialog endpoint link
        :rtype: str
        """
        return f'{self.dialogs}/{dialog_id}'

    @property
    def episode_notifications(self) -> str:
        """
        Returns endpoint for notifying Shikimori about anime episode release.

        **Note:** To use this endpoint, you need special private token,
        required to access this API

        :return: Episode notifications endpoint link
        :rtype: str
        """
        return f'{self.base_url_v2}/episode_notifications'

    def favorites_create(self, linked_type: str, linked_id: int,
                         kind: str) -> str:
        """
        Returns endpoint for creating some type
        of object as favorite

        :param linked_type: Type of object
        :type linked_type: str

        :param linked_id: ID of linked object
        :type linked_id: int

        :param kind: Kind of linked object
            (Required when linked_type is 'Person')
        :type kind: str

        :return: Favorite create endpoint link
        :rtype: str
        """
        return f'{self.base_url}/favorites/' \
               f'{linked_type}/{linked_id}/{kind}'

    def favorites_destroy(self, linked_type: str, linked_id: int) -> str:
        """
        Returns endpoint for destroying some type
        of object from favorites

        :param linked_type: Type of object
        :type linked_type: str

        :param linked_id: ID of linked object
        :type linked_id: int

        :return: Favorite destroy endpoint link
        :rtype: str
        """
        return f'{self.base_url}/favorites/' \
               f'{linked_type}/{linked_id}'

    def favorites_reorder(self, favorite_id: int) -> str:
        """
        Returns endpoint for assigning new position of a favorite.

        :param favorite_id: Favorite ID for endpoint
        :type favorite_id: int

        :return: Favorite reorder endpoint link
        :rtype: str
        """
        return f'{self.base_url}/favorites/{favorite_id}/reorder'

    @property
    def forums(self) -> str:
        """
        Returns endpoint of the forums list.

        :return: Forums list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/forums'

    def friend(self, friend_id: int) -> str:
        """
        Returns endpoint for adding/deleting friend

        :param friend_id: Friend ID for endpoint
        :type friend_id: int

        :return: Friend addition/deletion endpoint link
        :rtype: str
        """
        return f'{self.base_url}/friends/{friend_id}'

    @property
    def genres(self) -> str:
        """
        Returns endpoint of the genres list.

        :return: Genres list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/genres'

    @property
    def mangas(self) -> str:
        """
        Returns endpoint of the mangas list.

        :return: Mangas list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/mangas'

    def manga(self, manga_id: int) -> str:
        """
        Returns endpoint of a specific manga.

        :param manga_id: Manga ID for endpoint
        :type manga_id: int

        :return: Manga endpoint link
        :rtype: str
        """
        return f'{self.mangas}/{manga_id}'

    def manga_roles(self, manga_id: int) -> str:
        """
        Returns endpoint of a list of roles of a specific manga.

        :param manga_id: Manga ID for endpoint
        :type manga_id: int

        :return: Manga roles endpoint link
        :rtype: str
        """
        return f'{self.manga(manga_id)}/roles'

    def similar_mangas(self, manga_id: int) -> str:
        """
        Returns endpoint of a list of similar manga of a certain manga.

        :param manga_id: Manga ID for endpoint
        :type manga_id: int

        :return: Similar mangas endpoint link
        :rtype: str
        """
        return f'{self.manga(manga_id)}/similar'

    def manga_related_content(self, manga_id: int) -> str:
        """
        Returns endpoint of a list of similar manga of a certain manga.

        :param manga_id: Manga ID for endpoint
        :type manga_id: int

        :return: Manga related content endpoint link
        :rtype: str
        """
        return f'{self.manga(manga_id)}/related'

    def manga_screenshots(self, manga_id: int) -> str:
        """
        Returns endpoint of screenshots of a specific manga.

        :param manga_id: Manga ID for endpoint
        :type manga_id: int

        :return: Manga screenshots endpoint link
        :rtype: str
        """
        return f'{self.manga(manga_id)}/screenshots'

    def manga_franchise_tree(self, manga_id: int) -> str:
        """
        Returns endpoint of franchise tree of a certain manga.

        :param manga_id: Manga ID for endpoint
        :type manga_id: int

        :return: Manga franchise tree endpoint link
        :rtype: str
        """
        return f'{self.manga(manga_id)}/franchise'

    def manga_external_links(self, manga_id: int) -> str:
        """
        Returns endpoint of a list of external links of a certain manga.

        :param manga_id: Manga ID for endpoint
        :type manga_id: int

        :return: Manga external links endpoint link
        :rtype: str
        """
        return f'{self.manga(manga_id)}/external_links'

    def manga_topics(self, manga_id: int) -> str:
        """
        Returns endpoint of a list of topics of a certain manga.

        :param manga_id: Manga ID for endpoint
        :type manga_id: int

        :return: Manga topics endpoint link
        :rtype: str
        """
        return f'{self.manga(manga_id)}/topics'

    @property
    def messages(self) -> str:
        """
        Returns endpoint of the messages list.

        :return: Messages list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/messages'

    def message(self, message_id: int) -> str:
        """
        Returns endpoint of a specific message.

        :param message_id: Message ID for endpoint
        :type message_id: int

        :return: Message endpoint link
        :rtype: str
        """
        return f'{self.messages}/{message_id}'

    @property
    def messages_mark_read(self) -> str:
        """
        Returns endpoint for marking messages as read/unread.

        :return: Marking messages endpoint link
        :rtype: str
        """
        return f'{self.messages}/mark_read'

    @property
    def messages_read_all(self) -> str:
        """
        Returns endpoint for marking all messages as read.

        :return: Reading messages endpoint link
        :rtype: str
        """
        return f'{self.messages}/read_all'

    @property
    def messages_delete_all(self) -> str:
        """
        Returns endpoint for deleting all messages.

        :return: Deleting messages endpoint link
        :rtype: str
        """
        return f'{self.messages}/delete_all'

    def people(self, person_id: int) -> str:
        """
        Returns endpoint for a certain person.

        :param person_id: Person ID for endpoint
        :type person_id: int

        :return: Person endpoint link
        :rtype: str
        """
        return f'{self.base_url}/people/{person_id}'

    @property
    def people_search(self) -> str:
        """
        Returns endpoint for people search.

        :return: People search endpoint link
        :rtype: str
        """
        return f'{self.base_url}/people/search'

    @property
    def publishers(self) -> str:
        """
        Returns endpoint of the publishers list.

        :return: Publishers list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/publishers'

    @property
    def ranobes(self) -> str:
        """
        Returns endpoint of the ranobes list.

        :return: Ranobes list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/ranobe'

    def ranobe(self, ranobe_id: int) -> str:
        """
        Returns endpoint of a specific ranobe.

        :param ranobe_id: Ranobe ID for endpoint
        :type ranobe_id: int

        :return: Ranobe endpoint link
        :rtype: str
        """
        return f'{self.ranobes}/{ranobe_id}'

    def ranobe_roles(self, ranobe_id: int) -> str:
        """
        Returns endpoint of a list of roles of a specific ranobe.

        :param ranobe_id: Ranobe ID for endpoint
        :type ranobe_id: int

        :return: Ranobe roles endpoint link
        :rtype: str
        """
        return f'{self.ranobe(ranobe_id)}/roles'

    def similar_ranobes(self, ranobe_id: int) -> str:
        """
        Returns endpoint of a list of similar ranobe of a certain ranobe.

        :param ranobe_id: Ranobe ID for endpoint
        :type ranobe_id: int

        :return: Similar ranobes endpoint link
        :rtype: str
        """
        return f'{self.ranobe(ranobe_id)}/similar'

    def ranobe_related_content(self, ranobe_id: int) -> str:
        """
        Returns endpoint of a list of similar ranobe of a certain ranobe.

        :param ranobe_id: Ranobe ID for endpoint
        :type ranobe_id: int

        :return: Ranobe related content endpoint link
        :rtype: str
        """
        return f'{self.ranobe(ranobe_id)}/related'

    def ranobe_franchise_tree(self, ranobe_id: int) -> str:
        """
        Returns endpoint of franchise tree of a certain ranobe.

        :param ranobe_id: Ranobe ID for endpoint
        :type ranobe_id: int

        :return: Ranobe franchise tree endpoint link
        :rtype: str
        """
        return f'{self.ranobe(ranobe_id)}/franchise'

    def ranobe_external_links(self, ranobe_id: int) -> str:
        """
        Returns endpoint of a list of external links of a certain ranobe.

        :param ranobe_id: Ranobe ID for endpoint
        :type ranobe_id: int

        :return: Ranobe external links endpoint link
        :rtype: str
        """
        return f'{self.ranobe(ranobe_id)}/external_links'

    def ranobe_topics(self, ranobe_id: int) -> str:
        """
        Returns endpoint of a list of topics of a certain ranobe.

        :param ranobe_id: Ranobe ID for endpoint
        :type ranobe_id: int

        :return: Ranobe topics endpoint link
        :rtype: str
        """
        return f'{self.ranobe(ranobe_id)}/topics'

    @property
    def active_users(self) -> str:
        """
        Returns endpoints of a list of users,
        having at least 1 completed animes and active during last month.

        :return: Active users list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/stats/active_users'

    @property
    def studios(self) -> str:
        """
        Returns endpoint of the studios list.

        :return: Studios list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/studios'

    @property
    def styles(self) -> str:
        """
        Returns endpoint for creating/previewing style.

        :return: Style create/preview endpoint link
        :rtype: str
        """
        return f'{self.base_url}/styles'

    @property
    def style_preview(self) -> str:
        return f'{self.styles}/preview'

    def style(self, style_id: int) -> str:
        """
        Returns endpoint of the style.

        :param style_id: Style ID for endpoint
        :type style_id: int
        :return: Style endpoint link
        :rtype: str
        """
        return f'{self.styles}/{style_id}'

    @property
    def topics(self) -> str:
        """
        Returns endpoint of the topics list.

        :return: Topics list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/topics'

    def topic(self, topic_id: int) -> str:
        """
        Returns endpoint of the topic.

        :param topic_id: Topic ID for endpoint
        :type topic_id: int

        :return: Topic endpoint link
        :rtype: str
        """
        return f'{self.topics}/{topic_id}'

    @property
    def updates_topics(self) -> str:
        """
        Returns endpoint of the topics updates list.

        :return: Topics updates list endpoint link
        :rtype: str
        """
        return f'{self.topics}/updates'

    @property
    def hot_topics(self) -> str:
        """
        Returns endpoint of the hot topics list.

        :return: Hot topics list endpoint link
        :rtype: str
        """
        return f'{self.topics}/hot'

    def topic_ignore(self, topic_id: int) -> str:
        """
        Returns endpoint for ignoring/unignoring topic.

        :param topic_id: Topic ID for endpoint
        :type topic_id: int

        :return: Ignore/unignore topic endpoint link
        :rtype: str
        """
        return f'{self.base_url_v2}/topics/{topic_id}/ignore'

    @property
    def user_images(self) -> str:
        """
        Returns endpoint for creating an user image.

        :return: User image create endpoint link
        :rtype: str
        """
        return f'{self.base_url}/user_images'

    @property
    def users(self) -> str:
        """
        Returns endpoint of the users list.

        :return: Users list endpoint link
        :rtype: str
        """
        return f'{self.base_url}/users'

    @property
    def whoami(self) -> str:
        """
        Returns endpoint of the current user's brief info.

        :return: Current user's brief info endpoint link
        :rtype: str
        """
        return f'{self.users}/whoami'

    @property
    def sign_out(self) -> str:
        """
        Returns endpoint of a user's sign out.

        :return: User's sign out endpoint link
        :rtype: str
        """
        return f'{self.users}/sign_out'

    def user(self, user_id: Union[int, str]) -> str:
        """
        Returns endpoint of the user.

        :param user_id: User ID/Nickname for endpoint
        :type user_id: Union[int, str]

        :return: User endpoint link
        :rtype: str
        """
        return f'{self.users}/{user_id}'

    def user_info(self, user_id: Union[int, str]) -> str:
        """
        Returns endpoint of the user's brief info.

        :param user_id: User ID/Nickname for endpoint
        :type user_id: Union[int, str]

        :return: User's brief info endpoint link
        :rtype: str
        """
        return f'{self.user(user_id)}/info'

    def user_friends(self, user_id: Union[int, str]) -> str:
        """
        Returns endpoint of the user's friends list.

        :param user_id: User ID/Nickname for endpoint
        :type user_id: Union[int, str]

        :return: User's friends list endpoint link
        :rtype: str
        """
        return f'{self.user(user_id)}/friends'

    def user_clubs(self, user_id: Union[int, str]) -> str:
        """
        Returns endpoint of the user's clubs list.

        :param user_id: User ID/Nickname for endpoint
        :type user_id: Union[int, str]

        :return: User's clubs list endpoint link
        :rtype: str
        """
        return f'{self.user(user_id)}/clubs'

    def user_anime_rates(self, user_id: Union[int, str]) -> str:
        """
        Returns endpoint of the user's anime rates list.

        :param user_id: User ID/Nickname for endpoint
        :type user_id: Union[int, str]

        :return: User's anime rates list endpoint link
        :rtype: str
        """
        return f'{self.user(user_id)}/anime_rates'

    def user_manga_rates(self, user_id: Union[int, str]) -> str:
        """
        Returns endpoint of the user's manga rates list.

        :param user_id: User ID/Nickname for endpoint
        :type user_id: Union[int, str]

        :return: User's manga rates list endpoint link
        :rtype: str
        """
        return f'{self.user(user_id)}/manga_rates'

    def user_favourites(self, user_id: Union[int, str]) -> str:
        """
        Returns endpoint of the user's favourites list.

        :param user_id: User ID/Nickname for endpoint
        :type user_id: Union[int, str]

        :return: User's favorites list endpoint link
        :rtype: str
        """
        return f'{self.user(user_id)}/favourites'

    def user_messages(self, user_id: Union[int, str]) -> str:
        """
        Returns endpoint of the user's messages list.

        :param user_id: User ID/Nickname for endpoint
        :type user_id: Union[int, str]

        :return: User's messages list endpoint link
        :rtype: str
        """
        return f'{self.user(user_id)}/messages'

    def user_unread_messages(self, user_id: Union[int, str]) -> str:
        """
        Returns endpoint of the user's unread messages counts.

        :param user_id: User ID/Nickname for endpoint
        :type user_id: Union[int, str]

        :return: User's unread messages counts endpoint link
        :rtype: str
        """
        return f'{self.user(user_id)}/unread_messages'

    def user_history(self, user_id: Union[int, str]) -> str:
        """
        Returns endpoint of the user's history list.

        :param user_id: User ID/Nickname for endpoint
        :type user_id: Union[int, str]

        :return: User's history list endpoint link
        :rtype: str
        """
        return f'{self.user(user_id)}/history'

    def user_bans(self, user_id: Union[int, str]) -> str:
        """
        Returns endpoint of the user's bans list.

        :param user_id: User ID/Nickname for endpoint
        :type user_id: Union[int, str]

        :return: User's bans list endpoint link
        :rtype: str
        """
        return f'{self.user(user_id)}/bans'

    def user_ignore(self, user_id: Union[int, str]) -> str:
        """
        Returns endpoint for ignoring/unignoring user.

        :param user_id: User ID/Nickname for endpoint
        :type user_id: Union[int, str]

        :return: Ignore/unignore user endpoint link
        :rtype: str
        """
        return f'{self.base_url_v2}/users/{user_id}/ignore'

    @property
    def user_rates(self) -> str:
        """
        Returns endpoint of the user rates list.

        :return: User rates list endpoint link
        :rtype: str
        """
        return f'{self.base_url_v2}/user_rates'

    def user_rate(self, user_rate_id: int) -> str:
        """
        Returns endpoint of the user rate.

        :param user_rate_id: User rate ID for endpoint
        :type user_rate_id: int

        :return: User rate endpoint link
        :rtype: str
        """
        return f'{self.user_rates}/{user_rate_id}'

    def user_rate_increment(self, user_rate_id: int) -> str:
        """
        Returns endpoint for incrementing episodes/chapters by 1

        :param user_rate_id: User rate ID for increment endpoint
        :type user_rate_id: int

        :return: User rate increment endpoint link
        :rtype: str
        """
        return f'{self.user_rate(user_rate_id)}/increment'

    def user_rates_cleanup(self, user_rate_type: str) -> str:
        """
        Returns endpoint for cleanup user rates by type.

        **Note:** This endpoint is using API v.1

        :param user_rate_type: Type of an user rate
        :type user_rate_type: str

        :return: User rates cleanup endpoint link
        :rtype: str
        """
        return f'{self.base_url}/user_rates/{user_rate_type}/cleanup'

    def user_rates_reset(self, user_rate_type: str) -> str:
        """
        Returns endpoint for resetting user rates by type.

        **Note:** This endpoint is using API v.1

        :param user_rate_type: Type of an user rate
        :type user_rate_type: str

        :return: User rates reset endpoint link
        :rtype: str
        """
        return f'{self.base_url}/user_rates/{user_rate_type}/reset'
