from unittest.mock import Mock, call, patch

from django.core.management import call_command
from django.forms import model_to_dict
from django.test import TestCase
from googlesync.exceptions import SyncProfileNotFound
from googlesync.management.commands._google_sync import GoogleSyncCommandAbstract
from googlesync.management.commands.sync_google_people import (
    Command as GooglePeopleSyncCommand,
)
from googlesync.models import GooglePersonSyncProfile, GoogleServiceAccountConfig
from googlesync.tests.factories import (
    GooglePersonSyncProfileFactory,
    GoogleServiceAccountConfigFactory,
)
from people.models import Person
from people.tests.factories import PersonFactory, PersonStatusFactory, PersonTypeFactory


class SyncGooglePeopleTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        GoogleServiceAccountConfigFactory(project_id=1, delegate="test@example.com")

    def setUp(self):
        self.google_config = GoogleServiceAccountConfig.objects.get(project_id=1)

        # Mock the _get_my_customer call used in GoogleSyncCommand __init__
        mock_customer_resource = Mock()
        patcher__get_my_customer = patch.object(
            GoogleSyncCommandAbstract, "_get_my_customer"
        )

        self.addCleanup(patcher__get_my_customer.stop)
        self.mock__get_my_customer = patcher__get_my_customer.start()
        self.mock__get_my_customer.return_value = mock_customer_resource

    def test_subclass(self):
        self.assertTrue(issubclass(GooglePeopleSyncCommand, GoogleSyncCommandAbstract))

    def test_help(self):
        self.assertEqual(
            GooglePeopleSyncCommand.help, "Syncs google users to inventory people."
        )

    def test__sync_google_people_profiles(self):
        self.skipTest("Need to test")

    def test__sync_google_people_profile(self):
        self.skipTest("Need to test")

    def test__initialize_person_sync(self):
        self.skipTest("Need to test")

    @patch.object(GooglePeopleSyncCommand, "sync_google_people")
    def test__get_person_sync_profile_invalid_names(self, mock_sync_google_people):
        with self.assertRaises(SyncProfileNotFound) as context:
            call_command("sync_google_people", "sync", "random_profile")
        self.assertEqual(str(context.exception), "'random_profile' profile not found")

        GooglePersonSyncProfileFactory(name="real_sync_profile")
        with self.assertRaises(SyncProfileNotFound) as context:
            call_command(
                "sync_google_people", "sync", "real_sync_profile", "fake_sync_profile"
            )
        self.assertEqual(
            str(context.exception), "'fake_sync_profile' profile not found"
        )
        mock_sync_google_people.assert_not_called()

    @patch.object(GooglePeopleSyncCommand, "sync_google_people")
    def test__get_person_sync_profile_valid_names(self, mock_sync_google_people):
        GooglePersonSyncProfileFactory(name="real_sync_profile")
        GooglePersonSyncProfileFactory(name="another_real_sync_profile")
        google_person_sync1 = GooglePersonSyncProfile.objects.get(
            name="real_sync_profile"
        )
        google_person_sync2 = GooglePersonSyncProfile.objects.get(
            name="another_real_sync_profile"
        )

        call_command("sync_google_people", "sync", "real_sync_profile")

        mock_sync_google_people.assert_called_with(google_person_sync1)
        mock_sync_google_people.asssert_not_called_with(google_person_sync2)

        mock_sync_google_people.reset_mock()
        call_command(
            "sync_google_people",
            "sync",
            "real_sync_profile",
            "another_real_sync_profile",
        )
        self.assertEqual(mock_sync_google_people.call_count, 2)

        mock_sync_google_people.assert_has_calls(
            [call(google_person_sync1), call(google_person_sync2)]
        )

    @patch.object(GooglePeopleSyncCommand, "_get_users_service")
    def test__get_google_records_with_domain(self, mock__get_users_service):
        response_get_sideffect = []
        mock_response = Mock(**{"get.side_effect": response_get_sideffect})
        mock_request = Mock(**{"execute.return_value": mock_response})
        user_list_next_sideffect = [None]
        mock_user_service = Mock(
            **{
                "list.return_value": mock_request,
                "list_next.side_effect": user_list_next_sideffect,
            }
        )
        mock__get_users_service.return_value = mock_user_service

        # Testing with three results
        GooglePersonSyncProfileFactory(
            name="staff", google_query="test_query", domain="testdomain.com"
        )
        sync_profile = GooglePersonSyncProfile.objects.get(name="staff")
        command = GooglePeopleSyncCommand()
        query = sync_profile.google_query
        domain = sync_profile.domain
        return_value = command._get_google_records(query=query, domain=domain)

        mock__get_users_service.assert_called_once()
        mock_user_service.list.assert_called_with(
            domain=domain,
            projection="full",
            query=query,
        )

    @patch.object(GooglePeopleSyncCommand, "_get_users_service")
    def test__get_google_records_without_domain(self, mock__get_users_service):
        response_get_sideffect = [None]
        mock_response = Mock(**{"get.side_effect": response_get_sideffect})
        mock_request = Mock(**{"execute.return_value": mock_response})
        user_list_next_sideffect = [None]
        mock_user_service = Mock(
            **{
                "list.return_value": mock_request,
                "list_next.side_effect": user_list_next_sideffect,
            }
        )
        mock__get_users_service.return_value = mock_user_service

        # Testing with three results
        GooglePersonSyncProfileFactory(
            name="staff", google_query="test_query", domain=""
        )
        sync_profile = GooglePersonSyncProfile.objects.get(name="staff")
        command = GooglePeopleSyncCommand()
        query = sync_profile.google_query
        domain = sync_profile.domain
        return_value = command._get_google_records(query=query, domain=domain)

        mock__get_users_service.assert_called_once()
        mock_user_service.list.assert_called_with(
            customer=command.customer.get("id"),
            projection="full",
            query=query,
        )

    @patch.object(GooglePeopleSyncCommand, "_get_users_service")
    def test__get_google_records_with_domain(self, mock__get_users_service):
        pass

    @patch.object(GooglePeopleSyncCommand, "_get_users_service")
    def test__get_google_records(self, mock__get_users_service):
        response_get_sideffect = [
            [{"a": "a", "b": "b", "c": "c"}],
            [{"a": "a", "b": "b", "c": "c"}],
            [{"a": "a", "b": "b", "c": "c"}],
        ]
        mock_response = Mock(**{"get.side_effect": response_get_sideffect})
        mock_request = Mock(**{"execute.return_value": mock_response})
        user_list_next_sideffect = [mock_request, mock_request, None]
        mock_user_service = Mock(
            **{
                "list.return_value": mock_request,
                "list_next.side_effect": user_list_next_sideffect,
            }
        )
        mock__get_users_service.return_value = mock_user_service

        # Testing with three results
        GooglePersonSyncProfileFactory(name="staff", google_query="test_query")
        sync_profile = GooglePersonSyncProfile.objects.get(name="staff")
        command = GooglePeopleSyncCommand()
        query = sync_profile.google_query
        domain = sync_profile.domain
        return_value = command._get_google_records(query=query, domain=domain)

        mock__get_users_service.assert_called_once()
        mock_user_service.list.assert_called_with(
            domain=domain,
            projection="full",
            query=query,
        )
        mock_request.execute.assert_called()
        mock_response.get.assert_called_with("users")
        mock_user_service.list_next.assert_called_with(mock_request, mock_response)
        self.assertEqual(return_value, sum(response_get_sideffect, []))

    @patch.object(GooglePeopleSyncCommand, "_get_users_service")
    def test__get_google_records_no_results(self, mock__get_users_service):

        mock_response = Mock(**{"get.return_value": []})
        mock_request = Mock(**{"execute.return_value": mock_response})
        mock_user_service = Mock(**{"list.return_value": mock_request})
        mock__get_users_service.return_value = mock_user_service

        # Testing with three results
        GooglePersonSyncProfileFactory(name="staff", google_query="test_query")
        sync_profile = GooglePersonSyncProfile.objects.get(name="staff")
        command = GooglePeopleSyncCommand()
        query = sync_profile.google_query
        domain = sync_profile.domain
        return_value = command._get_google_records(query=query, domain=domain)

        mock__get_users_service.assert_called_once()
        mock_user_service.list.assert_called_with(
            projection="full",
            query=query,
            domain=domain,
        )
        mock_request.execute.assert_called()
        mock_response.get.assert_called_with("users")
        mock_user_service.list_next.assert_not_called()
        self.assertEqual(return_value, None)

    @patch.object(GooglePeopleSyncCommand, "convert_google_user_to_person")
    def test_convert_google_users_to_person(self, mock_convert_google_user_to_person):
        person1 = Mock(Person)
        person2 = Mock(Person)
        person3 = Mock(Person)
        google_people = [person1, person2, person3]
        mock_convert_google_user_to_person.side_effect = google_people

        GooglePersonSyncProfileFactory(name="staff", google_query="test_query")
        sync_profile = GooglePersonSyncProfile.objects.get(name="staff")
        google_users = [{"user": "user1"}, {"user": "user2"}, {"user": "user3"}]
        command = GooglePeopleSyncCommand()
        return_value = command.convert_google_users_to_person(
            sync_profile=sync_profile, google_users=google_users
        )
        mock_convert_google_user_to_person.assert_has_calls(
            [
                call(sync_profile, {"user": "user1"}),
                call(sync_profile, {"user": "user2"}),
                call(sync_profile, {"user": "user3"}),
            ]
        )
        self.assertEqual(return_value, google_people)

    @patch.object(GooglePeopleSyncCommand, "_map_dictionary")
    def test_convert_google_user_to_person_valid_user(self, mock__map_dictionary):
        person_status = PersonStatusFactory(name="Active")
        person_dictionary = model_to_dict(PersonFactory.build(google_id="123456789"))
        person_dictionary["status"] = person_status.name
        mock__map_dictionary.return_value = person_dictionary
        person_type = PersonTypeFactory(name="Staff")
        sync_profile = GooglePersonSyncProfileFactory(
            name="staff", google_query="test_query", person_type=person_type
        )
        sync_profile = GooglePersonSyncProfile.objects.get(name="staff")

        command = GooglePeopleSyncCommand()
        # google_user doesn't matter since we are mocking the return of _map_dictionary
        return_value = command.convert_google_user_to_person(
            sync_profile=sync_profile, google_user={}
        )
        self.assertIsInstance(return_value, Person)
        person = Person(**person_dictionary)
        person.type = sync_profile.person_type
        person.status = person_status
        person._buildings = None
        person._rooms = None

        for field in [p.name for p in Person._meta.concrete_fields]:
            self.assertEqual(getattr(person, field), getattr(return_value, field))

    def test_sync_google_people(self):
        self.skipTest("Need to test")
