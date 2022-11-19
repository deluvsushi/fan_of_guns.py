import requests
from os import urandom
from hashlib import md5

class FanOfGuns:
	def __init__(
			self,
			sdk: str = "UnitySDK-2.48.180809",
			app_version: str = "1.1.02",
			app_sign: str = "20:15:CE:96:C8:CD:B8:59:5E:5D:4A:04:21:79:EC:48") -> None:
		self.api = "https://f080.playfabapi.com/Client"
		self.headers = {
			"user-agent": "UnityPlayer/2019.4.17f1 (UnityWebRequest/1.0, libcurl/7.52.0-DEV)",
			"x-playfabsdk": "UnitySDK-2.48.180809",
			"x-unity-version": "2019.4.17f1",
			"content-type": "application/json"
		}
		self.sdk = sdk
		self.user_id = None
		self.title_id = "F080"
		self.app_sign = app_sign
		self.session_ticket = None
		self.app_version = app_version

	def generate_device_id(self) -> str:
		return md5(urandom(15)).hexdigest()

	def register(self) -> dict:
		data = {
			"AndroidDeviceId": self.generate_device_id(),
			"CreateAccount": True,
			"TitleId": self.title_id,
			"CustomTags": {
				"app_version": self.app_version,
				"app_sign": self.app_sign
			}
		}
		return requests.post(
			f"{self.api}/LoginWithAndroidDeviceID?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def login_with_session_ticket(
			self,
			session_ticket: str) -> str:
		self.session_ticket = session_ticket
		self.headers["x-authorization"] = self.session_ticket
		return self.session_ticket
		
	def get_account_info(self, username: str) -> dict:
		data = {
			"TitleDisplayName": username
		}
		return requests.post(
			f"{self.api}/GetAccountInfo?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def get_player_trades(self, status_filter: str) -> dict:
		data = {
			"StatusFilter": status_filter
		}
		return requests.post(
			f"{self.api}/GetPlayerTrades?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def get_inventory(self) -> dict:
		return requests.post(
			f"{self.api}/GetUserInventory?sdk={self.sdk}",
			headers=self.headers).json()

	def update_username(self, username: str) -> dict:
		data = {
			"TitleDisplayName": username
		}
		return requests.post(
			f"{self.api}/UpdateUserTitleDisplayName?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def get_friend_list(
			self,
			include_facebook_friends: bool = False,
			include_steam_friends: bool = False,
			show_statistics: bool = True,
			show_locations: bool = False,
			show_created: bool = True,
			show_last_login: bool = True,
			show_avatar_url: bool = True,
			show_banned_until: bool = True) -> dict:
		data = {
			"IncludeFacebookFriends": include_facebook_friends,
			"IncludeSteamFriends": include_steam_friends,
			"ProfileConstraints": {
				"ShowStatistics": show_statistics,
				"ShowLocations": show_locations,
				"ShowCreated": show_created,
				"ShowLastLogin": show_last_login,
				"ShowAvatarUrl": show_avatar_url,
				"ShowBannedUntil": show_banned_until
			}
		}
		return requests.post(
			f"{self.api}/GetFriendsList?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def get_store_items(
			self,
			store_id: str = "Store1000",
			catalog_version: str = None) -> dict:
		data = {
			"CatalogVersion": catalog_version,
			"StoreId": store_id
		}
		return requests.post(
			f"{self.api}/GetStoreItems?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def get_catalog_items(self, catalog_version: str = "Items") -> dict:
		data = {
			"CatalogVersion": catalog_version
		}
		return requests.post(
			f"{self.api}/GetCatalogItems?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def get_player_statistics(
			self, 
			statistic_names: list = ["score"],
			statistic_name_versions: str = None) -> dict:
		data = {
			"StatisticNames": statistic_names,
			"StatisticNameVersions": statistic_name_versions
		}
		return requests.post(
			f"{self.api}/GetPlayerStatistics?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def get_title_news(self, count: int = 10) -> dict:
		data = {
			"Count": count
		}
		return requests.post(
			f"{self.api}/GetTitleNews?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def purchase_item(
			self,
			item_id: str,
			price: int,
			virtual_currency: str,
			catalog_version: str = None,
			character_id: str = None,
			store_id: str = None) -> dict:
		data = {
			"CatalogVersion": catalog_version,
			"CharacterId": character_id,
			"ItemId": item_id,
			"Price": price,
			"StoreId": store_id,
			"VirtualCurrency": virtual_currency
		}
		return requests.post(
			f"{self.api}/PurchaseItem?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def unlock_container_instance(
			self,
			item_instance_id: str,
			catalog_version: str = "Items",
			character_id: str = None,
			key_item_instance_id: str = None) -> dict:
		data = {
			"CatalogVersion": catalog_version,
			"CharacterId": character_id,
			"ContainerItemInstanceId": item_instance_id,
			"KeyItemInstanceId": key_item_instance_id
		}
		return requests.post(
			f"{self.api}/UnlockContainerInstance?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def update_user_data(
			self, 
			data: dict, 
			permission: str,
			keys_to_remove: str = None) -> dict:
		data = {
			"Data": data,
			"KeysToRemove": keys_to_remove,
			"Permission": permission
		}
		return requests.post(
			f"{self.api}/UpdateUserData?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def ch_money(
			self,
			kill: int,
			kill_knife: int,
			kill_head: int = 0,
			dead: int = 0,
			generate_play_stream_event: bool = False,
			revision_selection: str = "Live",
			specific_revision: int = 0) -> dict:
		data = {
			"FunctionName": "ch_money",
			"FunctionParameter": {
				"kill": kill,
				"kill_knife": kill_knife,
				"kill_head": kill_head,
				"dead": dead
			},
			"GeneratePlayStreamEvent": generate_play_stream_event,
			"RevisionSelection": revision_selection,
			"SpecificRevision": specific_revision
		}
		return requests.post(
			f"{self.api}/ExecuteCloudScript?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def add_friend(self, username: str) -> dict:
		data = {
			"FriendTitleDisplayName": username
		}
		return requests.post(
			f"{self.api}/AddFriend?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def remove_friend(
			self,
			user_id: str,
			generate_play_stream_event: bool = False,
			revision_selection: str = "Live",
			specific_revision: int = 0) -> dict:
		data = {
			"FunctionName": "friendRemowe1",
			"FunctionParameter": {
				"playerId": user_id
			},
			"GeneratePlayStreamEvent": generate_play_stream_event,
			"RevisionSelection": revision_selection,
			"SpecificRevision": specific_revision
		}
		return requests.post(
			f"{self.api}/ExecuteCloudScript?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()

	def update_profile_status(self, status: str) -> dict:
		data = {
			"Data": {
				"status": status
			}
		}
		return requests.post(
			f"{self.api}/UpdateUserData?sdk={self.sdk}",
			json=data,
			headers=self.headers).json()
