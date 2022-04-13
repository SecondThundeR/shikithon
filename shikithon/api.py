import json
from typing import Union
from typing import Any
from typing import Dict
from typing import List

from requests import Session

from .enums.Anime import *
from .models.Achievement import Achievement
from .models.Anime import Anime
from .models.Creator import Creator
from .models.FranchiseTree import FranchiseTree
from .models.Link import Link
from .models.Relation import Relation
from .models.Screenshot import Screenshot
from .models.Topic import Topic
from .models.User import User


class API:
    def __init__(self, api_config: Dict[str, str]):
        self.endpoints: APIEndpoints = APIEndpoints()
        self.session: Session = Session()
        self.__init_api_vars(api_config)
        self.__api_vars_validation()

    def __get(self, url: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, data: Dict[str, str] = {}):
        response = self.session.get(url, headers=headers, params=query, data=data)
        if response.status_code == 401:
            self.__update_tokens(self.__get_tokens_from_api(refresh_tokens=True))
            return self.__get(url, headers, query, data)
        return response.json()

    def __post(self, url: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, data: Dict[str, str] = {}):
        response = self.session.post(url, headers=headers, params=query, data=data)
        if response.status_code == 401:
            self.__update_tokens(self.__get_tokens_from_api(refresh_tokens=True))
            return self.__post(url, headers, query, data)
        return response.json()

    def __put(self, url: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, data: Dict[str, str] = {}):
        response = self.session.put(url, headers=headers, params=query, data=data)
        if response.status_code == 401:
            self.__update_tokens(self.__get_tokens_from_api(refresh_tokens=True))
            return self.__put(url, headers, query, data)
        return response.json()

    def __patch(self, url: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, data: Dict[str, str] = {}):
        response = self.session.patch(url, headers=headers, params=query, data=data)
        if response.status_code == 401:
            self.__update_tokens(self.__get_tokens_from_api(refresh_tokens=True))
            return self.__patch(url, headers, query, data)
        return response.json()

    def __delete(self, url: str, headers: Dict[str, str] = {}, query: Dict[str, str] = {}, data: Dict[str, str] = {}):
        response = self.session.delete(url, headers=headers, params=query, data=data)
        if response.status_code == 401:
            self.__update_tokens(self.__get_tokens_from_api(refresh_tokens=True))
            return self.__delete(url, headers, query, data)
        return response.json()

    def get_api_config_dict(self) -> Dict[str, str]:
        """Return config dictionary with current values."""
        return {
            "app_name": self.app_name,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
            "scopes": self.scopes,
            "auth_code": self.auth_code,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token
        }

    def set_api_config_dict(self, api_config: Dict[str, str]):
        self.__init_api_vars(api_config)
        self.__api_vars_validation()

    def __export_api_config(self, file_name: str = "new_config.json"):
        current_config: Dict[str, str] = self.get_api_config_dict()
        with open(file_name, "w", encoding="utf-8") as config_file:
            json.dump(current_config, config_file, indent=4, separators=(", ", ": "))

    def __init_api_vars(self, api_config):
        try:
            self.app_name: str = api_config["app_name"]
            self.client_id: str = api_config["client_id"]
            self.client_secret: str = api_config["client_secret"]
            self.redirect_uri: str = api_config["redirect_uri"]
            self.scopes: str = api_config["scopes"]
            self.auth_code: str = api_config["auth_code"]
            self.access_token: str = api_config["access_token"]
            self.refresh_token: str = api_config["refresh_token"]
        except KeyError:
            self.__raise_config_mismatch(api_config)

    def __api_vars_validation(self):
        if not self.app_name:
            raise MissingConfigData("To use the Shikimori API correctly, you need to pass the application name")

        self.session.headers.update({"User-Agent": self.app_name})

        if not self.client_id or not self.client_secret:
            raise MissingConfigData("Missing Client ID and/or Client Secret")

        if not self.auth_code:
            oauth_url_data: Union[str, List[str]] = self.endpoints.get_filled_oauth_url(self.client_id, self.redirect_uri, self.scopes)
            exception_msg: str = self.__parse_oauth_url_data(oauth_url_data)
            raise MissingConfigData(exception_msg)

        if not self.access_token or not self.refresh_token:
            self.__update_tokens(self.__get_tokens_from_api())

        self.session.headers.update({"Authorization": f"Bearer {self.access_token}"})

    def __raise_config_mismatch(self, api_config):
        configs_keys: tuple[List[str], List[str]] = list(api_config.keys()), list(APIHelpers.get_blank_config().keys())
        missing_keys_str: str = ", ".join(APIHelpers.get_missing_keys_list(configs_keys))
        raise MissingConfigData(f"It is impossible to initialize an object without missing variables. Here is the list of missing: {missing_keys_str}")

    def __update_tokens(self, tokens_tuple: tuple[str, str]):
        self.access_token, self.refresh_token = tokens_tuple
        self.__export_api_config()

    def __get_tokens_from_api(self, refresh_tokens: bool = False) -> tuple[str, str]:
        token_url = self.endpoints.get_token_url()
        data = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        if refresh_tokens:
            data["grant_type"] = "refresh_token"
            data["refresh_token"] = self.refresh_token
        else:
            data["grant_type"] = "authorization_code"
            data["code"] = self.auth_code
            data["redirect_uri"] = self.redirect_uri

        oauth_json = self.__post(url=token_url, data=data)

        try:
            return oauth_json["access_token"], oauth_json["refresh_token"]
        except KeyError:
            error_info = json.dumps(oauth_json)
            raise MissingConfigData(f"An error occurred while receiving tokens, here is the information from the response: {error_info}")

    def __parse_oauth_url_data(self, oauth_url_data):
        if isinstance(oauth_url_data, list):
            missing_variables_str = ", ".join(oauth_url_data)
            return "The authorization code and some related information necessary to obtain it are missing: " \
                f'"{missing_variables_str}".' \
                f"\nGo to {self.endpoints.get_oauth_url()} for more information to get the authorization code"
        return "The authorization code is missing. " \
            f"It's okay, just paste this link \"{oauth_url_data}\" and then save the authorization code in your configuration"

    def get_achievements(self, user_id: int) -> List[Achievement]:
        query: Dict[str, str] = {
            "user_id": str(user_id)
        }
        res: List[Dict[str, Any]] = self.__get(url=self.endpoints.get_achievements_url(), query=query)

        return [Achievement(**data) for data in res]

    def get_list_of_animes(self, page: int = 1, limit: int = 1, order: Order = Order.NONE, kind: Kind = Kind.NONE, status: Status = Status.NONE, season: str = "", score: int = 1, duration: Duration = Duration.NONE, rating: Rating = Rating.NONE, genre: List[int] = [], studio: List[int] = [], franchise: List[int] = [], censored: Censorship = Censorship.CENSORED, my_list: MyList = MyList.NONE, ids: List[int] = [], exclude_ids: List[int] = [], search: str = "") -> List[Anime]:
        """
            Returns list of animes.

            If some data not provided, using fallback values

            Parameters:
                page (int): number of page
                limit (int): number of limit results
                order (Order): type of order in list
                kind (Status): type of anime topic
                status (Status): type of anime status
                season (str): name of anime season
                score (int): minimal anime score
                duration (Duration): duration size of anime
                rating (Rating): type of anime rating
                genre (List[int]): IDs of genres
                studio (List[int]): IDs of studios
                franchise (str): IDs of franchises
                censored (Censorship): type of anime censorship
                my_list (MyList): status of anime in current user list
                ids (List[int]): IDs of animes to include
                excluded_ids (List[int]): IDs of animes to exclude
                search (str): search phrase to filter animes by name.


            Returns:
                List[Anime]: list of animes
        """
        if page < 1 or page > 10000:
            page = 1

        if limit < 1 or limit > 50:
            limit = 1

        if score < 1 or score > 9:
            score = 1

        query: Dict[str, str] = {
            "page": str(page),
            "limit": str(limit),
            "order": order.value,
            "kind": kind.value,
            "status": status.value,
            "season": season,
            "score": str(score),
            "duration": duration.value,
            "rating": rating.value,
            "genre": ",".join([str(id) for id in genre]),
            "studio": ",".join([str(id) for id in studio]),
            "franchise": ",".join([str(id) for id in franchise]),
            "censored": censored.value,
            "mylist": my_list.value,
            "ids": ",".join([str(id) for id in ids]),
            "exclude_ids": ",".join([str(id) for id in exclude_ids]),
            "search": search
        }
        res: List[Dict[str, Any]] = self.__get(url=self.endpoints.get_animes_url(), query=query)
        return [Anime(**anime) for anime in res]

    def get_anime(self, anime_id: int) -> Anime:
        """
            Returns info about anime

            Parameters:
                anime_id (int): ID of anime

            Returns:
                Anime: info about anime
        """
        res: Dict[str, Any] = self.__get(url=self.endpoints.get_anime_url(anime_id))
        return Anime(**res)

    def get_anime_creators(self, anime_id: int) -> List[Creator]:
        """
            Returns list of anime creators

            Parameters:
                anime_id (int): ID of anime

            Returns:
                List[Creator]: list of anime creators
        """
        res: List[Dict[str, Any]] = self.__get(url=self.endpoints.get_anime_roles_url(anime_id))
        return [Creator(**creator) for creator in res]

    def get_list_of_similar_animes(self, anime_id: int) -> List[Anime]:
        """
            Returns list of similar animes

            Parameters:
                anime_id (int): ID of anime

            Returns:
                List[Anime]: list of similar animes
        """
        res: List[Dict[str, Any]] = self.__get(url=self.endpoints.get_similar_animes_url(anime_id))
        return [Anime(**anime) for anime in res]

    def get_anime_related_content(self, anime_id: int) -> List[Relation]:
        """
            Returns list of anime related content

            Parameters:
                anime_id (int): ID of anime

            Returns:
                List[Relation]: list of anime related content
        """
        res: List[Dict[str, Any]] = self.__get(url=self.endpoints.get_anime_related_content_url(anime_id))
        return [Relation(**relation) for relation in res]

    def get_anime_screenshots(self, anime_id: int) -> List[Screenshot]:
        """
            Returns list of anime screenshots links

            Parameters:
                anime_id (int): ID of anime

            Returns:
                List[Screenshot]: list of anime screenshots links
        """
        res: List[Dict[str, Any]] = self.__get(url=self.endpoints.get_anime_screenshots_url(anime_id))
        return [Screenshot(**screenshot) for screenshot in res]

    def get_anime_franchise_tree(self, anime_id: int) -> FranchiseTree:
        """
            Returns anime franchise tree

            Parameters:
                anime_id (int): ID of anime

            Returns:
                FranchiseTree: franchise tree of anime
        """
        res: Dict[str, Any] = self.__get(url=self.endpoints.get_anime_franchise_tree_url(anime_id))
        return FranchiseTree(**res)

    def get_anime_external_links(self, anime_id: int) -> List[Link]:
        """
            Returns list of anime external links

            Parameters:
                anime_id (int): ID of anime

            Returns:
                List[Link]: list of anime links
        """
        res: List[Dict[str, Any]] = self.__get(url=self.endpoints.get_anime_external_links_url(anime_id))
        return [Link(**link) for link in res]

    def get_anime_topics(self, anime_id: int, page: int = 1, limit: int = 1, kind: Status = Status.EPISODE, episode: Union[int, str] = "") -> List[Topic]:
        """
            Returns list of anime topics.

            If some data not provided, using fallback values

            Parameters:
                anime_id (int): ID of anime
                page (int): number of page
                limit (int): number of limit results
                kind (Status): type of topic
                episode (int): number of anime episode

            Returns:
                List[Topic]: list of anime topics
        """
        if page < 1 or page > 100000:
            page = 1

        if limit < 1 or limit > 30:
            limit = 1

        query: Dict[str, str] = {
            "page": str(page),
            "limit": str(limit),
            "kind": kind.value,
            "episode": str(episode)
        }
        res: List[Dict[str, Any]] = self.__get(url=self.endpoints.get_anime_topics_url(anime_id), query=query)
        return [Topic(**topic) for topic in res]

    def get_current_user(self) -> User:
        res: Dict[str, Any] = self.__get(url=self.endpoints.get_whoami_url())
        return User(**res)

class APIHelpers:
    @staticmethod
    def get_missing_keys_list(configs_tuple: tuple[List[str], List[str]]) -> List[str]:
        return [key for key in configs_tuple[1] if key not in configs_tuple[0]]

    @staticmethod
    def get_blank_config():
        return {
            "app_name": "",
            "client_id": "",
            "client_secret": "",
            "redirect_uri": "",
            "scopes": "",
            "auth_code": "",
            "access_token": "",
            "refresh_token": ""
        }


class APIEndpoints:
    def __init__(self):
        self.base_url: str = "https://shikimori.one/api"
        self.base_url_v2: str = self.base_url + "/v2"
        self.oauth_url: str = "https://shikimori.one/oauth"

    # Shikimori OAuth Endpoints
    def get_oauth_url(self) -> str:
        return self.oauth_url

    def get_filled_oauth_url(self, client_id: str, redirect_uri: str, scopes: str) -> Union[str, List[str]]:
        missing_variables = []

        if not redirect_uri:
            missing_variables.append("redirect_uri")
        if not scopes:
            missing_variables.append("scopes")

        if missing_variables:
            return missing_variables

        query = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scopes
        }

        query_str = "&".join(f"{key}={val}" for (key, val) in query.items())
        auth_link = f"{self.oauth_url}/authorize?{query_str}"

        return auth_link

    def get_token_url(self) -> str:
        return f"{self.oauth_url}/token"

    # Shikimori API v1.0 Endpoints
    # Achievements

    def get_achievements_url(self) -> str:
        return f"{self.base_url}/achievements"

    # Animes
    def get_animes_url(self) -> str:
        return f"{self.base_url}/animes"

    def get_anime_url(self, anime_id: int) -> str:
        return f"{self.base_url}/animes/{anime_id}"

    def get_anime_roles_url(self, anime_id: int) -> str:
        return f"{self.base_url}/animes/{anime_id}/roles"

    def get_similar_animes_url(self, anime_id: int) -> str:
        return f"{self.base_url}/animes/{anime_id}/similar"

    def get_anime_related_content_url(self, anime_id: int) -> str:
        return f"{self.base_url}/animes/{anime_id}/related"

    def get_anime_screenshots_url(self, anime_id: int) -> str:
        return f"{self.base_url}/animes/{anime_id}/screenshots"

    def get_anime_franchise_tree_url(self, anime_id: int) -> str:
        return f"{self.base_url}/animes/{anime_id}/franchise"

    def get_anime_external_links_url(self, anime_id: int) -> str:
        return f"{self.base_url}/animes/{anime_id}/external_links"

    def get_anime_topics_url(self, anime_id: int) -> str:
        return f"{self.base_url}/animes/{anime_id}/topics"

    # Users
    def get_whoami_url(self) -> str:
        return f"{self.base_url}/users/whoami"

    # Shikimori API v2.0 Endpoints
    # Topic ignore

    def get_topic_ignore_url(self, topic_id: int) -> str:
        return f"{self.base_url_v2}/topics/{topic_id}/ignore"

    # User ignore
    def get_user_ignore_url(self, user_id: int) -> str:
        return f"{self.base_url_v2}/users/{user_id}/ignore"

    # Abuse requests
    def get_offtopic_request_url(self) -> str:
        return f"{self.base_url_v2}/abuse_requests/offtopic"

    def get_review_request_url(self) -> str:
        return f"{self.base_url_v2}/abuse_requests/review"

    def get_abuse_request_url(self) -> str:
        return f"{self.base_url_v2}/abuse_requests/abuse"

    def get_spoiler_request_url(self) -> str:
        return f"{self.base_url_v2}/abuse_requests/spoiler"

    # Episode notifications
    def get_episode_notifications_url(self) -> str:
        return f"{self.base_url_v2}/episode_notifications"

    # User rates
    def get_user_rate_id_url(self, user_rate_id: int) -> str:
        return f"{self.base_url_v2}/user_rates/{user_rate_id}"

    def get_user_rate_list_url(self) -> str:
        return f"{self.base_url_v2}/user_rates"

    def get_user_rate_id_increment_url(self, user_rate_id: int) -> str:
        return f"{self.base_url_v2}/user_rates/{user_rate_id}/increment"


class ShikithonException(Exception):
    """Base class for Shikithon Exceptions."""
    pass


class MissingConfigData(ShikithonException):
    """Exception for missing data required to work with the API."""
    pass
